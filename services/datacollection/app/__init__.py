from fastapi import FastAPI, Header,Cookie, Query, HTTPException, Request

import logging
from os import getcwd,name
from os.path import join , abspath, dirname

from .config import Config
from .mqtt import MQTT  
from .functions import DB 
from .models import Item



# LOGGING SETTINGS
# https://realpython.com/python-logging/
# https://docs.python.org/3/library/logging.html#logrecord-attributes
# logging.basicConfig(level=logging.DEBUG,filename="app/log/sia_logs.csv",encoding="utf-8",filemode="a",format="{asctime},{process},{levelname},{name},{message},{exc_info}", style="{", datefmt="%Y-%m-%d %H:%M")
Logger             = logging.getLogger(__name__)
console_handler    = logging.StreamHandler()
file_handler       = logging.FileHandler(filename="app/log/app.log",encoding="utf-8",mode="a")
formatter          = logging.Formatter( "{asctime},{process},{levelname},{name},{message},{exc_info}", style="{",datefmt="%Y-%m-%d %H:%M" )

console_handler.setFormatter(formatter)        
file_handler.setFormatter(formatter)
console_handler.setLevel("DEBUG")
file_handler.setLevel("WARNING")
Logger.addHandler(console_handler)
Logger.addHandler(file_handler)
        

# Libraries
mongo = DB(Config, Logger)
Mqtt  = MQTT(mongo)

# CREATE APP
app = FastAPI()

# START MQTT CLIENT 
Mqtt.client.loop_start()


from app import routes