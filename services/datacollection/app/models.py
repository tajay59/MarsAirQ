from pydantic import BaseModel


class Item(BaseModel):
    name: str
    description: str | None = None # variables with initial values are optional 
    price: float
    tax: float | None = None # variables with initial values are optional 
