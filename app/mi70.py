
# https://realpython.com/queue-in-python/#using-thread-safe-queues
# https://www.troyfawkes.com/learn-python-multithreading-queues-basics/

import serial
import asyncio
import serial_asyncio
from time import sleep
from .mqtt import MQTT  
from .functions import DB  
# from app import MQTT  
from json import dumps, loads
from queue import Empty, Queue

 
from os import name, system, getcwd
from os.path import join, exists  
from datetime import datetime
from threading import Thread

# PATH = getcwd()
# print("MY PATH ", PATH)
# import sys
# sys.path.insert(0, '/home/ubuntu/app/piAWS')
# # from config import Config


# PATH = join(getcwd(),"app")
# PATH =  getcwd() 
# print("MY PATH ", PATH)
# import sys
# sys.path.insert(0, PATH) 
# from mqtt import MQTT  

pressure_loop       = asyncio.new_event_loop()
temperature_loop    = asyncio.new_event_loop()
esp32_loop          = asyncio.new_event_loop()

'''
ser = serial.Serial()
ser.baudrate    = 19200
ser.bytesize    = 8
ser.parity      = 'N'
ser.stopbits    = 1
ser.port        = 'COM12'
ser.xonxoff     = False


ser.open()
print("open : ",ser.is_open)
for x in range(20):
    print(x)
    ser.write(b'\r\n')
    #s = ser.readline()
    #print("initializing ", str(s.decode("utf-8")))
    sleep(1)

print("sent ")    
while True:
    ser.write(b'SEND\r\n')
    s = ser.readline()
    print("output ", str(s.decode("utf-8")))
    #if "SEND" not in str(s):
    #    print("output ", str(s.decode("utf-8")))
    sleep(2)
    

ser.close()

'''

def processAllHMP75(msg, mongo: DB, Mqtt: MQTT, collectData: bool):
    
    msg = msg.split("\r\n")
    
    insertList = []
    for line in msg:
        if "\t" in line:
            data = line.split("\t")
            data = list(filter(None, data)) # Remove empty strings
            if len(data) == 3:
                try:                                
                    date, humidity, temperature = data
                    temperature = float(temperature)
                    humidity    = float(humidity)
                    print("Temperature ",date, humidity, temperature)
                    date_format = "%y-%m-%d %H:%M:%S"
                    dt = datetime.strptime(date, date_format)
                except Exception as e:
                    print(f"HMP75_TRH error: {e}")
                else:
                    timestamp = int(dt.timestamp())  
                    insertList.append({"type":"reference","model":"HMP75","param":"TRH","date": dt,"timestamp": timestamp, "humidity": humidity, "temperature": temperature})

    if collectData and len(insertList) > 0:
        try:
            mongo.addBatchData(insertList)
        except Exception as e:
            print(f"HMP75 Mongo Insert Error: {str(e)}")
        else:
            print("HMP75 Database Updated")

              
    if Mqtt:
        if Mqtt.client.is_connected  and collectData:
            for message in insertList:
                print(f"Publishing: {message}")
                message.pop("date")
                message.pop("_id")
                Mqtt.publish("/references", dumps(message))  

def processAllPTB330(msg, mongo: DB, Mqtt: MQTT, collectData: bool):    
    msg = msg.split("\r\n")
    
    insertList = []        
    for line in msg:           
        data = line.split("\t")
        data = list(filter(None, data)) # Remove empty strings
    
        if len(data) == 3:  
            if "\t" in line:                                          
                try:
                    date, QFE, QNH = data
                    print("Pressure ",date,QFE, QNH )
                    QFE = float(QFE)
                    QNH = float(QNH)
                    date_format = "%y-%m-%d %H:%M:%S"
                    dt = datetime.strptime(date, date_format)
                except Exception as e:
                    print(f"PTB330 error: {e}")
                else:
                    timestamp       = int(dt.timestamp()) 
                    insertList.append({"type":"reference","model":"PTB330","param":"P","date": dt,"timestamp": timestamp, "pressure": QFE, "qnh": QNH})

    if collectData and len(insertList) > 0:
        try:
            mongo.addBatchData(insertList)
        except Exception as e:
            print(f"PTB330: Mongo Insert Error: {str(e)}")
        else:
            print("PTB330: Database Update")

              
    if Mqtt:
        if Mqtt.client.is_connected  and collectData:
            for message in insertList:
                print(f"PTB330 Publishing: {message}")
                message.pop("date")
                message.pop("_id")
                Mqtt.publish("/references", dumps(message))  

# This example will read chunks from the serial port every 1000ms:

class PTB330(asyncio.Protocol):
    connected   = False
    collectData = False
    Mqtt: MQTT  = None
    mongo: DB   = None
    timeCount   = 0   
     
    def connection_made(self, transport):
        self.transport = transport
        # self.transport.serial.timeout = 1
        print("Connected to Pressure Device")

    def data_received(self, data):
        print(f"PTB330 Received: {data}")
        try:
            msg = data.decode("utf-8")        
        except Exception as e:
            print(f"PTB330 error: {str(e)}")
        else:     
        
            if "opened" in msg and self.connected == False:
                print("NOW OPEN")
                self.connected = True            
            
            elif "0>" in msg and self.connected == False: 
                print("Already OPEN")
                self.connected = True   

            elif "\r\n1>\x1a" in msg and self.connected == False: 
                print("Already OPEN")
                self.connected = True          
                
            elif "close" in msg:
                print("PTB330 Device Disconnected")
                self.connected = False

            elif "ERR" in msg:
                print("Need to send 'SEND 0'")
                self.transport.write(b'SEND 0\r\n')

            else: 
                worker = Thread(target=processAllPTB330, args=(msg, self.mongo, self.Mqtt, self.collectData))
                worker.setDaemon(True)
                worker.start()

        # stop callbacks again immediately
        self.pause_reading()
            

    def pause_reading(self):
        # This will stop the callbacks to data_received
        self.transport.pause_reading()

    def resume_reading(self):
        # This will start the callbacks to data_received again with all data that has been received in the meantime.
        self.transport.resume_reading()
    
    def setPublishState(self, state: bool):
        self.collectData = state

class HMP75_TRH(asyncio.Protocol):
    connected   = False
    collectData = False
    Mqtt: MQTT  = None
    mongo: DB   = None
    timeCount = 0  
    def connection_made(self, transport):
        self.transport = transport
        # self.transport.serial.timeout = 1
        print("Connected to Temperature Device")

    def data_received(self, data):
        print(f"HMP75 Received: {data}")
        
        try:
            msg = data.decode("utf-8")        
        except Exception as e:
            print(f"HMP75 error: {str(e)}")
        else:
            if "opened" in msg and self.connected == False:
                print("NOW OPEN")
                self.connected = True            
            
            elif "0>" in msg and self.connected == False:
                print("Already OPEN")
                self.connected = True     
                
            elif "close" in msg:
                print("HMP75 Device Disconnected")
                self.connected = False

            elif "ERR" in msg:
                print("Need to send 'SEND 0'")
                self.transport.write(b'SEND 0\r\n')

            else:                
                worker = Thread(target=processAllHMP75, args=(msg, self.mongo, self.Mqtt, self.collectData))
                worker.setDaemon(True)
                worker.start()

        # stop callbacks again immediately
        self.pause_reading()
            
        print("T>>>> End")

    def pause_reading(self):
        # This will stop the callbacks to data_received
        self.transport.pause_reading()

    def resume_reading(self):
        # This will start the callbacks to data_received again with all data that has been received in the meantime.
        self.transport.resume_reading()
    
    def setPublishState(self, state: bool):
        self.collectData = state

class ESP32_DEV(asyncio.Protocol):
    connected = False
    collectData = False
    Mqtt: MQTT = None
    mongo: DB = None
    timeCount = 0 
    dataTemp = {}
    dataHum = {}
    dataPres = {}
    def connection_made(self, transport):
        self.transport = transport
        print("Connected to ESP32 Device")
        self.connected = True
        self.resume_reading()

    def data_received(self, data):
        try:
            msg = data.decode("utf-8")
        except Exception as e:
            print(f"Read error: {e}")
        else:
            data = [x for x in msg.split("\n") if "sensorSource" in x ] 
            if len(data) > 0:           
                try:
                    collectedData = loads(data[0])
                except Exception as e:
                    print(e)
                else:
                    # print(f'ESP32 data received: {collectedData}')  
                    dt = datetime.fromtimestamp(collectedData["timestamp"])
                    collectedData["date"] = dt

                    if self.collectData:                        
                        try:
                            self.mongo.addData(collectedData)
                        except Exception as e:
                            print(f"Mongo Insert Error: {str(e)}")

                    if self.Mqtt:                    
                        if self.Mqtt.client.is_connected  and self.collectData:
                            # self.Mqtt.publish("/devices", data)  
                            pass
                    
                    if "open" in msg:
                        print("Device Connected")
                        self.connected = True
                        
                    if "close" in msg:
                        print("Device Disconnected")
                        self.connected = False       

                    # stop callbacks again immediately
                    self.pause_reading()
        

    def pause_reading(self):
        # This will stop the callbacks to data_received
        self.transport.pause_reading()

    def resume_reading(self):
        # This will start the callbacks to data_received again with all data that has been received in the meantime.
        self.transport.resume_reading()
    
    def setPublishState(self, state: bool):
        self.collectData = state


async def pressure_reader(Mqtt: MQTT,port, PTB330_queue: Queue, mongo: DB):
    transport, protocol = await serial_asyncio.create_serial_connection(pressure_loop, PTB330, port, baudrate= 19200,bytesize=serial.EIGHTBITS,parity=serial.PARITY_NONE,stopbits=serial.STOPBITS_ONE,xonxoff=False) #, timeout=1 '/dev/ttyUSB0'
    protocol.Mqtt = Mqtt
    protocol.mongo = mongo

    while not protocol.connected:
        await asyncio.sleep(0.1)
        print("Initializing PTB330 Reader...")
        transport.write(b'\r\n')       
        protocol.resume_reading()         
    
    while True:
        await asyncio.sleep(1)
        while not PTB330_queue.empty():
            try:
                msg = PTB330_queue.get_nowait()
            except Empty:
                continue
            else:                
                ptb330_que_handler(msg, protocol) 
        
        transport.write(b'SEND\r\n') 
        protocol.resume_reading()   
        print("P>>>")
           

async def temperature_reader(Mqtt: MQTT,port, HMP75_queue: Queue, mongo: DB):
    transport, protocol = await serial_asyncio.create_serial_connection(temperature_loop, HMP75_TRH, port, baudrate= 19200,bytesize=serial.EIGHTBITS,parity=serial.PARITY_NONE,stopbits=serial.STOPBITS_ONE,xonxoff=False) #'/dev/ttyUSB0'
    protocol.Mqtt = Mqtt
    protocol.mongo = mongo

    while not protocol.connected:
        await asyncio.sleep(0.1)
        print("Initializing HMP75 Reader...")
        transport.write(b'\r\n')       
        protocol.resume_reading()  

    
    while True:
        await asyncio.sleep(5)
        while not HMP75_queue.empty():
            try:
                msg = HMP75_queue.get_nowait()
            except Empty:
                continue
            else:
                hmp75_que_handler(msg, protocol)

        
        transport.write(b'SEND\r\n') 
        protocol.resume_reading()
        
        print("T>>>")

async def esp32_reader(Mqtt: MQTT,port, ESP32_queue: Queue, mongo: DB):
    transport, protocol = await serial_asyncio.create_serial_connection(esp32_loop, ESP32_DEV, port, baudrate= 19200,bytesize=serial.EIGHTBITS,parity=serial.PARITY_NONE,stopbits=serial.STOPBITS_ONE,xonxoff=False, timeout=1) #'/dev/ttyUSB0'
    protocol.Mqtt = Mqtt
    protocol.mongo = mongo
    
    while True:
        while not ESP32_queue.empty():
            try:
                msg = ESP32_queue.get_nowait()
            except Empty:
                continue
            else:
                ESP32_que_handler(msg, protocol)

        await asyncio.sleep(1)
        # transport.write(b'SEND\r\n') 
        protocol.resume_reading()


def init_pressure(Mqtt: MQTT,port, PTB330_queue: Queue, mongo: DB):   #Mqtt: MQTT  
    asyncio.set_event_loop(pressure_loop)
    pressure_loop.run_until_complete(pressure_reader(Mqtt,port, PTB330_queue, mongo))
    pressure_loop.run_forever()
    pressure_loop.close()

def init_temperature(Mqtt: MQTT, port, HMP75_queue: Queue, mongo: DB): # Mqtt: MQTT   
    asyncio.set_event_loop(temperature_loop)
    temperature_loop.run_until_complete(temperature_reader(Mqtt,port, HMP75_queue, mongo))
    temperature_loop.run_forever()
    temperature_loop.close()

def init_collocation_device(Mqtt: MQTT, port, ESP32_queue: Queue, mongo: DB): # Mqtt: MQTT   
    asyncio.set_event_loop(esp32_loop)
    esp32_loop.run_until_complete(esp32_reader(Mqtt,port, ESP32_queue, mongo))
    esp32_loop.close()

def ptb330_que_handler(message, protocol):
    print("Found", message, " in PTB330_queue")
    params = list(message.keys())
    if "collectdata" in params:
        protocol.collectData = message["collectdata"]

def hmp75_que_handler(message, protocol):
    print("Found", message, " in HMP75_queue")
    params = list(message.keys())
    if "collectdata" in params:
        protocol.collectData = message["collectdata"]
    
def ESP32_que_handler(message, protocol):
    print("Found", message, " in ESP32_queue")
    params = list(message.keys())
    if "collectdata" in params:
        protocol.collectData = message["collectdata"]