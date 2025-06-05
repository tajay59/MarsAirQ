from flask import Flask, make_response, redirect, jsonify
from .config import Config
from os import getcwd,name
from os.path import join , abspath, dirname
from flask_jwt_extended import JWTManager
from flask_mail import Mail, Message
from werkzeug.middleware.proxy_fix import ProxyFix
from queue import Empty, Queue

#import asyncio
#from .mi70 import  init_pressure, init_temperature, init_collocation_device
from .mqtt import MQTT  

from .functions import DB, JWTtoDict
#from .utils import create_invoice,create_quotation,create_comm_inv, create_fileNotFound, maintainFedExAuthToken
# from .decoratorsClasses import CheckForm
# from flask_wtf.csrf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy
import logging

from flask_migrate import Migrate
#from weasyprint import HTML
 
Logger             = logging.getLogger(__name__)


# SETTINGS
# https://realpython.com/python-logging/
# https://docs.python.org/3/library/logging.html#logrecord-attributes
# logging.basicConfig(level=logging.DEBUG,filename="app/log/sia_logs.csv",encoding="utf-8",filemode="a",format="{asctime},{process},{levelname},{name},{message},{exc_info}", style="{", datefmt="%Y-%m-%d %H:%M")

console_handler    = logging.StreamHandler()
file_handler       = logging.FileHandler(filename="app/log/sia_logs.log",encoding="utf-8",mode="a")
formatter          = logging.Formatter( "{asctime},{process},{levelname},{name},{message},{exc_info}", style="{",datefmt="%Y-%m-%d %H:%M" )


console_handler.setFormatter(formatter)        
file_handler.setFormatter(formatter)
console_handler.setLevel("DEBUG")
file_handler.setLevel("WARNING")
Logger.addHandler(console_handler)
Logger.addHandler(file_handler)
        



# create the extension
mongo = DB(Config, Logger)
Mqtt  = MQTT(mongo)
db = SQLAlchemy()

 
if name == "posix":
    app = Flask(__name__,static_folder='static')
else:
    app = Flask(__name__)

app.config.from_object(Config) 

# Flask mail
mail = Mail(app)

# Init and setup JWT Manager
jwt = JWTManager(app)  

# csrf = CSRFProtect(app) 

# initialize the app with the extension
db.init_app(app)

# Instantiate Flask-Migrate library here
migrate = Migrate(app,db)

# Tell Flask it is Behind a Proxy
app.wsgi_app = ProxyFix( app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1 )

# Thread Queues
HMP75_queue     = Queue(maxsize=100)
PTB330_queue    = Queue(maxsize=100)
ESP32_queue     = Queue(maxsize=100)


from app import views

# START MQTT CLIENT 
Mqtt.client.loop_start()