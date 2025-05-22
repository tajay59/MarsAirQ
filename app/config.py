
from os import getcwd, name, environ
from os.path import join , abspath, dirname
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()  # load environment variables from .env if it exists.
basedir = abspath(dirname(__file__))

class Config(object):
    """Base Config Object"""
    

    FLASK_DEBUG                             = eval(environ.get('DEBUG','False'))
    SECRET_KEY                              = environ.get('SECRET_KEY', 'Som3$ec5etK*y')
    UPLOAD_FOLDER                           = environ.get('UPLOAD_FOLDER') 
    TEMP_QUOTATIONS                         = environ.get('TEMP_QUOTATIONS') 
    IMAGE_FOLDER                            = environ.get('IMAGE_FOLDER')
    IMAGE_FOLDER_RAW                        = environ.get('IMAGE_FOLDER_RAW')
    INVOICE_FOLDER                          = environ.get('INVOICE_FOLDER') 
    QRCODE_FOLDER                           = environ.get('QRCODE_FOLDER') 
    QRCODE_TEMP_FOLDER                      = environ.get('QRCODE_TEMP_FOLDER') 

    PRESSURE_PORT                           = environ.get('PRESSURE_PORT') 
    TEMPERATURE_PORT                        = environ.get('TEMPERATURE_PORT') 
    ESP32_PORT                              = environ.get('ESP32_PORT') 


    ENV                                     = environ.get('FLASK_ENV') 
    FLASK_RUN_PORT                          = environ.get('FLASK_RUN_PORT') 
    FLASK_RUN_HOST                          = environ.get('FLASK_RUN_HOST') 

    # CONFIGURE JWT
    BASE_URL                                = f"http://127.0.0.1:{FLASK_RUN_PORT}"
    JWT_SECRET_KEY                          = environ.get('JWT_SECRET_KEY')                 
    JWT_COOKIE_CSRF_PROTECT                 = eval( environ.get('JWT_COOKIE_CSRF_PROTECT') )
    JWT_CSRF_CHECK_FORM                     = eval( environ.get('JWT_CSRF_CHECK_FORM') )
    JWT_ACCESS_COOKIE_PATH                  = '/'
    JWT_REFRESH_COOKIE_PATH                 = '/api/token/refresh' 
    JWT_TOKEN_LOCATION                      = ['cookies'] 
    JWT_COOKIE_SECURE                       = True
    JWT_ACCESS_TOKEN_EXPIRES                = timedelta(hours=3)  # minutes=60  CHANGE TO 60MIN IN PRODUCTION
    JWT_REFRESH_TOKEN_EXPIRES               = timedelta(days=3) # days=3

    WTF_CSRF_CHECK_DEFAULT                  = True # You can disable CSRF protection in all views by default, by setting WTF_CSRF_CHECK_DEFAULT to False, and selectively call protect() only when you need
    WTF_CSRF_TIME_LIMIT                     = None # Max age in seconds for CSRF tokens. Default is 3600. If set to None, the CSRF token is valid for the life of the session.

    # MONGODB VARIABLES
    DB_USERNAME                             = environ.get('DB_USERNAME') 
    DB_PASSWORD                             = environ.get('DB_PASSWORD')    
    DB_PORT                                 = environ.get('DB_PORT') 
    DB_SERVER                               = environ.get('DB_SERVER')  

    # FLASK MAIL
    MAIL_SERVER                             = environ.get('MAIL_SERVER') 
    MAIL_PORT                               = environ.get('MAIL_PORT') 
    MAIL_USE_TLS                            = eval(environ.get('MAIL_USE_TLS'))
    MAIL_USE_SSL                            = eval(environ.get('MAIL_USE_SSL'))
    MAIL_DEBUG                              = eval(environ.get('MAIL_DEBUG'))
    MAIL_USERNAME                           = environ.get('MAIL_USERNAME') 
    MAIL_PASSWORD                           = environ.get('MAIL_PASSWORD') 
    MAIL_DEFAULT_SENDER                     = environ.get('MAIL_DEFAULT_SENDER') 
    MAIL_MAX_EMAILS                         = environ.get('MAIL_MAX_EMAILS') 
    MAIL_SUPPRESS_SEND                      = environ.get('MAIL_SUPPRESS_SEND') 
    MAIL_ASCII_ATTACHMENTS                  = eval(environ.get('MAIL_ASCII_ATTACHMENTS'))
    PROPAGATE_EXCEPTIONS                    = False
    
     
    SQLALCHEMY_DATABASE_URI                 = 'sqlite:///' + join(basedir, 'database.db')
    SQLALCHEMY_TRACK_MODIFICATIONS          = False

    
    #SQLALCHEMY_DATABASE_URI = environ.get('DATABASE_URL', '').replace('postgres://', 'postgresql://')
    #SQLALCHEMY_TRACK_MODIFICATIONS = False # This is just here to suppress a warning from SQLAlchemy as it will soon be removed