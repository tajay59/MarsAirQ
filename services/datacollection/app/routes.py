from app import app, Logger, Header, Cookie, Query, HTTPException, Request, DB, Config, mongo, Item
from typing import Annotated
from enum import Enum 
from time import sleep, time, perf_counter
import asyncio

# Create MongoDB instance
# mongo = DB(Config,Logger)

from argon2 import PasswordHasher,Type
ph  = PasswordHasher(time_cost=3, memory_cost=4096, parallelism=2, hash_len=64, salt_len=16, encoding='utf-8', type= Type(2))

async def brewCoffee():
    print("Started to make coffee")
    await asyncio.sleep(3)
    print("coffee maded")
    return "coffee ready"

async def toastBagel():
    print("Started to toast Bagel")
    await asyncio.sleep(2)
    print("Bagel toasted")
    return "Bagel toasted"


@app.middleware("http") # A "middleware" is a function that works with every request before it is processed by any specific path operation. And also with every response before returning it.
async def add_process_time_header(request: Request, call_next):
    start_time = perf_counter()
    response = await call_next(request)
    process_time = perf_counter() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


@app.post("/items/")
async def create_item(item: Item):
    return item




@app.get("/books/{item_id}")
async def read_item(item_id: str):
    items = {"foo": "The Foo Wrestlers"}
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"item": items[item_id]}

@app.post("/items/all")
async def create_item(item: Item):
    item_dict = item.model_dump()
    if item.tax is not None:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    return item_dict

@app.get("/get/items/")
async def read_items( q: Annotated[str | None, Query(min_length=3, max_length=50)] = None, ):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results

@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item): # Request body + path parameters. FastAPI will recognize that the function parameters that match path parameters should be taken from the path, and that function parameters that are declared to be Pydantic models should be taken from the request body.
    return {"item_id": item_id, **item.model_dump()}

@app.put("/items/id/{item_id}") # Request body + path + query parameters. You can also declare body, path and query parameters, all at the same time. FastAPI will recognize each of them and take the data from the correct place.
async def update_item(item_id: int, item: Item, q: str | None = None):
    result = {"item_id_1": item_id, **item.model_dump()}
    if q:
        result.update({"q": q})
    return result


@app.get("/data")
async def data():
    res = await mongo.findAllEntitiesForSignup()
    return {"message": res}


@app.get("/run")
async def run():
    result_coffee = ""
    result_bagel  = ""
    start_time = time()
    # Non Async
    # result_coffee = brewCoffee()
    # result_bagel = toastBagel()

    ## Batch Async
    # batch = asyncio.gather(brewCoffee(), toastBagel())
    # result_coffee,result_bagel = await batch

    ## Task Async
    # coffee_task = asyncio.create_task(brewCoffee())
    # bagel_task  = asyncio.create_task(toastBagel())

    # result_coffee = await coffee_task 
    # result_bagel = await bagel_task

    ## Task Group Async
    async with asyncio.TaskGroup() as tg:
        result_coffee = tg.create_task(brewCoffee())
        result_bagel  = tg.create_task(toastBagel())
        start_time = time() 
    
    ent_time = time()
    elaspsed_time = ent_time - start_time
    print(f"Result of Brew Coffee", result_coffee)
    print(f"Result of Toast Bagel ", result_bagel)
    print(f"Total execution time: {elaspsed_time:.2f}")

    return {"message": f"Time: {elaspsed_time:.2f} seconds"}