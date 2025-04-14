#! /usr/bin/env python
from app import app, mongo, Config, Mqtt, init_pressure, init_temperature, init_collocation_device, HMP75_queue, PTB330_queue, ESP32_queue
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor 


if __name__ == "__main__":      
    app.run(debug=Config.FLASK_DEBUG, host=Config.FLASK_RUN_HOST, port=Config.FLASK_RUN_PORT)
'''
if __name__ == "__main__":    
    # RUN FLASK APP
    # app.run(debug=Config.FLASK_DEBUG, host=Config.FLASK_RUN_HOST, port=Config.FLASK_RUN_PORT)
    # Must connect to MI70over serial with putty first before running this app
    with ThreadPoolExecutor(max_workers=4) as executor: # RUN USING THREADING
    # with ProcessPoolExecutor(max_workers=3) as executor: # RUN USING MULTIPROCESSING
        
        future0  = executor.submit(init_pressure,Mqtt,Config.PRESSURE_PORT,PTB330_queue,mongo)
        future1  = executor.submit(init_temperature, Mqtt, Config.TEMPERATURE_PORT, HMP75_queue,mongo) 
        future2  = executor.submit(app.run, debug=Config.FLASK_DEBUG, host=Config.FLASK_RUN_HOST, port=Config.FLASK_RUN_PORT)  
        # future3  = executor.submit(init_collocation_device, Mqtt, Config.ESP32_PORT, ESP32_queue,mongo)  

        if future0.running():
            print(" Pressure Reader Task Running")

        if future1.running():
            print(" Temperature Reader Task Running")

        if future2.running():
            print(" Flask Task Running")
        
        # # if future3.running():
        # #     print(" ESP32 Task Running")
 
         
        while True: 
            if( future0.done() and future1.done() and future2.done() ):  # and future3.done() 
                print( future0.result())
                print( future1.result())
                print( future2.result())
                # print( future3.result())
                print("\n")
                break
''' 