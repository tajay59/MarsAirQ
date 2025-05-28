"""
Flask Documentation:     https://flask.palletsprojects.com/
Jinja2 Documentation:    https://jinja.palletsprojects.com/
Werkzeug Documentation:  https://werkzeug.palletsprojects.com/
This file creates your application.
"""

# from crypt import methods
import site
import bcrypt
from app import app, jwt, DB, Config,Logger, mail, db , JWTtoDict, CheckForm,  Message, create_invoice,create_quotation,create_comm_inv, create_fileNotFound #, csrf , HTML,
from app.models import Tokenlist
from flask import render_template, request, jsonify, send_file, redirect, make_response, session, url_for, abort, send_from_directory 
from markupsafe import escape
from json import dumps, loads
from secrets import token_hex
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
# from flask_mail import Message
from flask_wtf.csrf import generate_csrf 
from flask_jwt_extended import (decode_token,get_csrf_token ,jwt_required, get_jwt, get_jwt_identity, create_access_token, create_refresh_token, set_access_cookies, set_refresh_cookies, unset_jwt_cookies,unset_access_cookies, current_user)
from datetime import datetime,timedelta, timezone
from os import getcwd, name, remove as fileRemove, listdir
from os.path import join , abspath, exists
from time import time, ctime
from math import floor
from PIL import Image, ImageOps
from PIL.ExifTags import TAGS
from timeit import default_timer as timer 
from rembg import new_session, remove 
from io import BytesIO
from functools import wraps

from argon2 import PasswordHasher,Type
ph  = PasswordHasher(time_cost=3, memory_cost=4096, parallelism=2, hash_len=64, salt_len=16, encoding='utf-8', type= Type(2))
import pytz


tect = 5  # Token Expiration Check Time... 
adminRoles = ["staff","admin"]
staffRoles = ["staff","admin"]

# Create MongoDB instance
mongo = DB(Config,Logger)

# Create CheckForm instance decorator class
checkform = CheckForm(Logger)

# TIME OFFSET TO CORRECT ALL TIME TO BARBADOS (-4) TIME
timeOffset = -4

PRODUCT_DELIMITER = "_"

caribbean_countries = [
     {
        "name": "Anguilla",
        "icon": "emojione-v1:flag-for-anguilla",
        "code": "AI",
        "center": {
            "latitude": 18.2206,
            "longitude": -63.0686
        }
    },
    {
        "name": "Antigua and Barbuda",
        "icon": "emojione-v1:flag-for-antigua-and-barbuda",
        "code": "AG",
        "center": {
            "latitude": 17.0608,
            "longitude": -61.7964
        }
    },
    {
        "name": "Bahamas",
        "icon": "emojione-v1:flag-for-bahamas",
        "code": "BS",
        "center": {
            "latitude": 25.0239,
            "longitude": -77.3963
        }
    },
    {
        "name": "Barbados",
        "icon": "emojione-v1:flag-for-barbados",
        "code": "BB",
        "center": {
            "latitude": 13.1939,
            "longitude": -59.5431
        }
    },
    {
        "name": "Belize",
        "icon": "emojione-v1:flag-for-belize",
        "code": "BZ",
        "center": {
            "latitude": 17.2510,
            "longitude": -88.7719
        }
    },
     {
        "name": "British Virgin Islands",
        "icon": "twemoji:flag-british-virgin-islands",
        "code": "VG",
        "center": {
            "latitude": 18.4207,
            "longitude": -64.6400
        }
    },
    {
        "name": "Cayman Islands",
        "icon": "emojione-v1:flag-for-cayman-islands",
        "code": "KY",
        "center": {
            "latitude": 19.3133,
            "longitude": -81.2546
        }
    },
    {
        "name": "Cuba",
        "icon": "emojione-v1:flag-for-cuba",
        "code": "CU",
        "center": {
            "latitude": 21.5217,
            "longitude": -77.7812
        }
    },
    {
        "name": "Dominica",
        "icon": "emojione-v1:flag-for-dominica",
        "code": "DM",
        "center": {
            "latitude": 15.4150,
            "longitude": -61.3710
        }
    },
    {
        "name": "Dominican Republic",
        "icon": "emojione-v1:flag-for-dominican-republic",
        "code": "DO",
        "center": {
            "latitude": 19.1940,
            "longitude": -70.6667
        }
    },
    {
        "name": "Grenada",
        "icon": "emojione-v1:flag-for-grenada",
        "code": "GD",
        "center": {
            "latitude": 12.1165,
            "longitude": -61.6790
        }
    },
    {
        "name": "Guyana",
        "icon": "emojione-v1:flag-for-guyana",
        "code": "GY",
        "center": {
            "latitude": 4.9387,
            "longitude": -58.9310
        }
    },
    {
        "name": "Haiti",
        "icon": "emojione-v1:flag-for-haiti",
        "code": "HT",
        "center": {
            "latitude": 18.9712,
            "longitude": -72.2852
        }
    },
    {
        "name": "Jamaica",
        "icon": "emojione-v1:flag-for-jamaica",
        "code": "JM",
        "center": {
            "latitude": 18.1096,
            "longitude": -77.2975
        }
    },
    {
        "name": "Montserrat",
        "icon": "emojione-v1:flag-for-montserrat",
        "code": "MS",
        "center": {
            "latitude": 16.7425,
            "longitude": -62.1874
        }
    },
    {
        "name": "Saint Kitts and Nevis",
        "icon": "emojione-v1:flag-for-st-kitts-and-nevis",
        "code": "KN",
        "center": {
            "latitude": 17.3571,
            "longitude": -62.7829
        }
    },
    {
        "name": "Saint Lucia",
        "icon": "emojione-v1:flag-for-st-lucia",
        "code": "LC",
        "center": {
            "latitude": 13.9094,
            "longitude": -60.9789
        }
    },
    {
        "name": "Sint Maarten",
        "icon": "twemoji:flag-sint-maarten",
        "code": "SX",
        "center": {
            "latitude": 18.0425,
            "longitude": -63.0548
        }
    },
    {
        "name": "Saint Vincent and the Grenadines",
        "icon": "emojione-v1:flag-for-st-vincent-and-grenadines",
        "code": "VC",
        "center": {
            "latitude": 13.2541,
            "longitude": -61.2072
        }
    },
    {
        "name": "Suriname",
        "icon": "emojione-v1:flag-for-suriname",
        "code": "SR",
        "center": {
            "latitude": 3.9190,
            "longitude": -56.0278
        }
    },
    {
        "name": "Trinidad and Tobago",
        "icon": "emojione-v1:flag-for-trinidad-and-tobago",
        "code": "TT",
        "center": {
            "latitude": 10.6918,
            "longitude": -61.2225
        }
    },
    {
        "name": "Turks and Caicos Islands",
        "icon": "twemoji:flag-turks-and-caicos-islands",
        "code": "TC",
        "center": {
            "latitude": 21.6940,
            "longitude": -71.7979
        }
    }
]


# ENSURE THAT ALL ROUTES OR FUNCTIONS THAT USES THIS DECORATOR RUNS IN A TRY CATCH BLOCK TO PREVENT CODE CRASHES
def tryCatch(name=""):
    def innerDecorator(f):            
        @wraps(f)
        def wrapper(*args,**kwargs):                  
            try:                    
                output = f(*args,**kwargs)                  
            except Exception as e:
                # print(f" {name} error: ",str(e))
                Logger.warning(f" {name}() error: {str(e)}")
                return jsonify({"status":"Are you a bot"})
            else:
                return output
                
        return wrapper
    return innerDecorator


 ########################
 #  JWT TOKEN CONFIGS   #
 ########################


@jwt.token_verification_loader
@tryCatch(name="token_verification_callback")
def token_verification_callback(header: dict, payload: dict) -> bool:
    # print(f"HEADER  : {header} ")
 
    token   = payload # data.getToken()  

    # print(f"ABOUT TO VERIFY TOKEN {token}")

    now     = floor(datetime.now(timezone(timedelta(hours= timeOffset))).timestamp())

    if token["type"] == "access": 
        access   = db.session.query(Tokenlist).filter_by(jti= token["jti"],iat=token['iat'],user_id= token["sub"]).order_by(Tokenlist.iat.desc()).first() 

        if access is None:
            # print("Access token not found in the database")
            return False
        
        target_timestamp    = datetime.fromtimestamp(now) + timedelta(minutes= 1)

        if target_timestamp > datetime.fromtimestamp(access.exp): 
            # print("Access token will expire in < 1 minutes")
            access.valid = False
            access.fresh = False
            db.session.commit()
            return False
        
        # print("Access token is valid")
        return True
 

    elif token["type"] == "refresh": 
        refresh   = db.session.query(Tokenlist).filter_by(jti= token["jti"],iat=token['iat'],user_id= token["sub"]).order_by(Tokenlist.iat.desc()).first() 
    
        if refresh is None:
            # Refresh token not found in the database
            return False  

        target_timestamp     = datetime.fromtimestamp(now) + timedelta(minutes=1)

        if target_timestamp > datetime.fromtimestamp(refresh.exp): 
            #print(f"Refresh token will expire in < {tect} minutes")
            refresh.valid = False
            refresh.fresh = False
            db.session.commit()
            return False

        # print("Refresh token is valid")
        return True


@jwt.token_verification_failed_loader
@tryCatch(name="token_verification_failed_callback")
def token_verification_failed_callback(header, payload): 
 
    token   = payload # data.getToken()  

    # print(f"token_verification_failed_callback: {token}")
     
    now     = floor(datetime.now(timezone(timedelta(hours= timeOffset))).timestamp()) 

    access   = db.session.query(Tokenlist).filter_by(type="access",iat=token['iat'],user_id= token["sub"] ).order_by(Tokenlist.iat.desc()).first() 
    refresh  = db.session.query(Tokenlist).filter_by(type="refresh",created_at=access.created_at,user_id= token["sub"] ).order_by(Tokenlist.iat.desc()).first() 

    if refresh: 
        if refresh.exp > now:
            if access :
                target_timestamp    = datetime.fromtimestamp(now) + timedelta(minutes= 1)
                
                if target_timestamp > datetime.fromtimestamp(access.exp): 
                    # Token expired, so refresh/send a new token
                    # print("Token expired, so refresh/send a new token")
                    user_id     = token["sub"] # get_jwt_identity() 
                    accessToken = refreshToken(user_id,token["iat"],access.created_at)
                    # resp        = make_response(redirect( request.url.replace("http://","https://")))   # Redirect to original request received from frontend  
                    resp        = make_response() 
                    resp.headers['X-Tokenized'] = "Tokenized"                  
                    set_access_cookies(resp, accessToken)                                       
                    return resp
                else:
                    # Token not yet expired 
                    # print("Token not yet expired ")
                    resp = make_response(redirect( request.url.replace("http://","https://")))   # Redirect to original request received from frontend  
                    return resp
     
    # This will logout user  forcing them to re-login
    # print("This will logout user  forcing them to re-login")
    logoutUser(token)
    resp = make_response({"status":"Unauthorized","user":"","role":"user","id": ""})
    unset_jwt_cookies(resp)
    return resp, 401 
    

# Callback function to check if a JWT exists in the database blocklist
@jwt.token_in_blocklist_loader
@tryCatch(name="check_if_token_revoked")
def check_if_token_revoked(header, payload: dict) -> bool:
    
    
    token   = payload # data.getToken()  

    now     = floor(datetime.now(timezone(timedelta(hours= timeOffset))).timestamp())
   
    # Its possible that the token could be an Access token or Refresh token
    if token["type"] == "access": 
        access   = db.session.query(Tokenlist).filter_by(jti=token["jti"],iat=token['iat'],user_id=token["sub"]).order_by(Tokenlist.iat.desc()).first() 

        if access is None:
            # Refresh token not found in the database
            return False  

        if (access.exp <= now)  :   
            # print(f"ACCESS BLACKLISTED: ==> {True}") 
            return True                                          
       
        # print(f"ACCESS BLACKLISTED: ==> {False}") 
        return False
    

    elif token["type"] == "refresh": 
        refresh   = db.session.query(Tokenlist).filter_by(jti= token["jti"],iat=token['iat'],user_id= token["sub"] ).order_by(Tokenlist.iat.desc()).first() 
    
        if refresh is None:
            # print("Access token not found in the database")
            return False
     
        if (refresh.exp <= now)  :  
            # print(f"REFRESH BLACKLISTED: ==> {True}") 
            return True   
         
        # print(f"REFRESH BLACKLISTED: ==> {False}") 
        return False


@jwt_required()
@jwt.revoked_token_loader 
@tryCatch(name="revoked_token_callback")
def revoked_token_callback(header, payload):
   
    # print(f"REVOKED TOKEN CALLBACK -> {payload}")
    resp = jsonify({"status":"Unauthorized","user":"","role":"user","id": ""})
    unset_jwt_cookies(resp)
    return resp, 401


@jwt.unauthorized_loader
@tryCatch(name="unauthorized_callback")
def unauthorized_callback(reason):
    # No auth header, @jwt.unauthorized_loader is called when the user has no access tokens in their request 
    print("UNAUTHORIZED CALLBACK: ", reason)

    resp = jsonify({"status":"Unauthorized","message":"signup"})
    return resp, 401


@jwt.invalid_token_loader
@tryCatch(name="invalid_token_callback")
def invalid_token_callback(callback):
    # Invalid Fresh/Non-Fresh Access token in auth header. @jwt.invalid_token_loader is called when the user has an invalid access token in their request. This happens when someone tries to access an endpoint using forged tokens.
    
    # print("INVALID TOKEN CALLBACK")
    resp = jsonify({"status":"Unauthorized","message":"invalidToken"})
    unset_jwt_cookies(resp)
    return resp, 401

 
@jwt.expired_token_loader
@tryCatch(name="expired_token_callback")
def expired_token_callback(header,payload):
    # Expired auth header. @jwt.expired_token_loader is called when the user 
    # has an expired but otherwise valid access token in their request.

    token   = payload # data.getToken()  

    # print(f"EXPIRED TOKEN CALLBACK: {token}")
    now     = floor(datetime.now(timezone(timedelta(hours= timeOffset))).timestamp()) 

    access   = db.session.query(Tokenlist).filter_by(type="access",iat=token['iat'],user_id= token["sub"] ).order_by(Tokenlist.iat.desc()).first() 
    if access:
        refresh  = db.session.query(Tokenlist).filter_by(type="refresh",created_at=access.created_at,user_id= token["sub"] ).order_by(Tokenlist.iat.desc()).first() 

        if refresh: 
            if refresh.exp > now:
                if access :
                    
                    if access.exp < now:
                        #print(f"REFRESH ACCESS ONE  {request.url}")
                        # Token expired, so refresh/send a new token
                        user_id         = token["sub"] # get_jwt_identity()
                        # resp = make_response(redirect(url_for('refresh',_external=True)))
                        # resp.location = resp.location.replace("http://","https://")
                        # unset_access_cookies(resp)
                        # print("REDIRECTING TO ", f'{request.url.replace("http://","https://")}')
                        accessToken = refreshToken(user_id,token["iat"],access.created_at)
                        # print(accessToken)
                        # resp        = make_response(redirect( request.url.replace("http://","https://"))) # Redirect to original request received from frontend   
                        resp        = make_response()   
                        resp.headers['X-Tokenized'] = "Tokenized"              
                        set_access_cookies(resp, accessToken) 
                        return resp
                    else:
                        # print("REFRESH ACCESS TWO")
                        # Token not yet expired
                        resp = make_response(redirect( request.url.replace("http://","https://")))   # Redirect to original request received from frontend  
                        return resp
     
    # print("LOGGIN OUT USER")
    # This will logout user  forcing them to re-login
    logoutUser(token)
    resp = make_response({"status":"Unauthorized","user":"","role":"user","id": ""})
    unset_jwt_cookies(resp)
    return resp, 401 
      
@tryCatch(name="assign_access_refresh_tokens")    
def assign_access_refresh_tokens(user_id, message,Bool):
    
    
    access_token    = create_access_token(identity=user_id ,fresh=Bool)   
    refresh_token   = create_refresh_token(identity=user_id )
    
    access          = decode_token(access_token)
    refresh         = decode_token(refresh_token)
    # print(f"TOKEN CREATED :  {access}")
   
    # UPDATE DATABASE
    now             = datetime.now(timezone(timedelta(hours= timeOffset)))
 
    db.session.add(Tokenlist(fresh=access["fresh"],iat=access["iat"],jti=access["jti"], type=access["type"],user_id= access["sub"],sub= access["sub"],nbf= access["nbf"],csrf= access["csrf"], created_at= now,exp= access["exp"],valid=True))
    db.session.add(Tokenlist(fresh=refresh["fresh"],iat=refresh["iat"],jti=refresh["jti"], type=refresh["type"],user_id= refresh["sub"],sub= refresh["sub"],nbf=refresh["nbf"],csrf=refresh["csrf"], created_at=now,exp=refresh["exp"],valid=True))
    db.session.commit()
    
    response        = make_response(message)
    response.set_cookie('csrf_token', generate_csrf(),httponly = False, secure = True)
    set_access_cookies(response, access_token)
    set_refresh_cookies(response, refresh_token) 

    return response, 200

@tryCatch(name="assign_access_refresh_tokens_mobile")
def assign_access_refresh_tokens_mobile(user_id, message,Bool):
    
    access_token    = create_access_token(identity=user_id ,fresh=Bool)
    refresh_token   = create_refresh_token(identity=user_id )

    access          = decode_token(access_token)
    refresh         = decode_token(refresh_token)
 
    # print(f"TOKEN CREATED : {type(tokenSub)} {access}") 

    # UPDATE DATABASE
    now             = datetime.now(timezone(timedelta(hours= timeOffset)))

    db.session.add(Tokenlist(fresh=access["fresh"],iat=access["iat"],jti=access["jti"], type=access["type"],user_id= access["sub"],sub= access["sub"],nbf= access["nbf"],csrf= access["csrf"], created_at= now,exp= access["exp"],valid=True))
    db.session.add(Tokenlist(fresh=refresh["fresh"],iat=refresh["iat"],jti=refresh["jti"], type=refresh["type"],user_id= refresh["sub"],sub= refresh["sub"],nbf=refresh["nbf"],csrf=refresh["csrf"], created_at=now,exp=refresh["exp"],valid=True))
    db.session.commit()
    
    response        = make_response(message)
    response.set_cookie('csrf_token_custom', generate_csrf(),httponly = False, secure = True)
    set_access_cookies(response, access_token)
    set_refresh_cookies(response, refresh_token) 
    
    return response, 200
    
 
@jwt.user_identity_loader
@tryCatch(name="user_identity_lookup")
def user_identity_lookup(user):
    # Register a callback function that takes whatever object is passed in 
    # as the identity when creating JWTs and converts it to a JSON serializable format.   

    # print(f"user_identity_lookup == {type(user)} {user}" )
    
    return user
 

@jwt.user_lookup_loader
@tryCatch(name="user_lookup_callback")
def user_lookup_callback(header, payload):
    # Register a callback function that loads a user from your database whenever
    # a protected route is accessed. This should return any python object on a
    # successful lookup, or None if the lookup failed for any reason (for example
    # if the user has been deleted from the database).

    
    token   = payload 
    
    account = mongo.findUser(id= token['sub'])
    
    if account:
        # account.pop("password")  
        account.pop("timestamp") 
        account.pop("registered") 
        account.pop("emailconfirmed")   
        # print(f"user_lookup_callback ACCOUNT =>  {token['sub']['id']}  {account}")
        return account
    return None


# Refresh expired JWT tokens if refresh token exist for user
@app.route('/api/token/refresh', methods=['GET'])
@jwt_required(refresh=True)
@tryCatch(name="refresh")
def refresh(): 

    """ This function checks whether the user has a valid refresh token first 
    using @jwt_refresh_token_required, if they do, it'll extract the identity 
    given to the token during it's creation using get_jwt_identity() and use it 
    to create another access token. We then assign and return it just like before! """

    # print(f"REFRESHING  {request} ")

    user_id         = get_jwt_identity() # get_jwt() get_jwt_identity() 

    # print(f"IDENTITY -> {user_id}") 
    # print(f"CUR USER -> {current_user}")
    # oldToken        = get_jwt() # decode_token(user_id)
    
    access_token    = create_access_token(identity=user_id, fresh=False)  
    # print(f"OLD Token  => {oldToken}")
     
    # UPDATE DATABASE   
    
    token           = db.session.query(Tokenlist).filter_by(user_id= user_id,type="access" ).order_by(Tokenlist.iat.desc()).first()  
    token.valid     = False
    token.fresh     = False

    # print(f"OLD IAT {token.iat}")

    newToken = decode_token(access_token)

    # print(f"NEW access_token => {newToken}")
   
    now     = datetime.now(timezone(timedelta(hours= timeOffset))) 
    
    # print(f"NEW IAT {newToken['iat']}")

    db.session.add(Tokenlist(fresh= newToken["fresh"],iat= newToken["iat"],jti= newToken["jti"], type= newToken["type"],sub= dumps(newToken["sub"]),user_id= newToken["sub"],nbf= newToken["nbf"],csrf= newToken["csrf"], created_at= now, exp= newToken["exp"],valid= True) )
    db.session.commit()
    # print("COMMITED")
    
    resp            = jsonify({"status":"Authorized","user":current_user['lastname'],"role":current_user['role'],"id":current_user['id']})
    set_access_cookies(resp, access_token)
    response = make_response(resp)
    response.set_cookie('csrf_token', generate_csrf(),httponly = False, secure = True)
    response.headers['X-Tokenized'] = "Tokenized"
    return resp, 200

@tryCatch(name="refreshToken")
def refreshToken(user_id,iat,created_at):
    print(f"REFRESHING TOKEN  {user_id} ") 
    
    access_token    = create_access_token(identity=user_id, fresh=False)   
     
    # UPDATE DATABASE       
    token           = db.session.query(Tokenlist).filter_by(user_id= user_id,iat=iat,type="access" ).order_by(Tokenlist.iat.desc()).first()  
    token.valid     = False
    token.fresh     = False

    # print(f"OLD IAT {iat}")

    newToken = decode_token(access_token)

    # print(f"NEW access_token => {newToken}")
   
    now     = created_at #datetime.now(timezone(timedelta(hours= timeOffset))) 
    
    # print(f"NEW IAT {newToken['iat']}")

    db.session.add(Tokenlist(fresh= newToken["fresh"],iat= newToken["iat"],jti= newToken["jti"], type= newToken["type"],sub= dumps(newToken["sub"]),user_id= newToken["sub"],nbf= newToken["nbf"],csrf= newToken["csrf"], created_at= now, exp= newToken["exp"],valid= True) )
    db.session.commit()
    #print("COMMITED")

    return access_token

 
#####################################
#   Routing for your application    #
#####################################
 
@app.route('/api/home')
@tryCatch(name="index")
def index():
    # ABORT SINCE THIS ROUTE WILL NOT BE USED
    # abort(401)
    data = "are you a bot"
    return jsonify({"status":"suspicious","message":data}), 404


#####################
#   LOGIN / LOGOUT  #
#####################

@app.route('/api/login', methods=['POST'])
# @tryCatch(name="login")
def login():
    # LOGIN A USER
     
    form =  request.form
    if request.method == "POST":       
            # FORM SUCCESSFULLY VALIDATED
            email       = escape(form.get("Email"))
            password    = escape(form.get("Password"))  
            user        = request.headers.get('x-user')     
            
            # CHECK IF USER ALREADY EXIST    
            account = mongo.findUser(email=email)    
            
            if not account:
                # LET VUE KNOW THE ACCOUNT DOES NOT EXIST
                message = {"status":"accountDoesNotExist"}
                return jsonify(message)
 

            # VALIDATE PASSWORD PROVIDED BY USER
            try:
                unhash   = ph.verify(account['password'],password) #check_password_hash(account['password'],password )
                entity   = mongo.findEntityCredentials({"id":account['entity']},{"_id":0,"web":1})
                 
                # entities = mongo.findAllEntitiesCredentials({"$or":[{"id": {"$in": account["entities"] }}, {"id":account['entity']}]},{"_id":0,"id":1,"web":1})
                if entity == None:
                    entity = ""
                else:
                    entity= entity["web"]

            except Exception as e:
                print(str(e))
            else:
                if  unhash and account:
                    message = {"status":"loggedIn","message":"loggedIn","username":account['lastname'],"email":account['email'],"id":account['id'],"role":account['role'],"entity": account["entity"],"entities": account["entities"],"web": entity,"suball": account["suball"],"image":account["image"]} #,"web": account["web"]
                    account.pop("email") 
                    account.pop("password")  
                    account.pop("timestamp") 
                    account.pop("registered") 
                    account.pop("emailconfirmed")  
                    return assign_access_refresh_tokens(account["id"],message,True)    
            
            return jsonify({"status":"Invalid credentials"}) 
    return jsonify({"status":"failed"}) 


@app.route('/api/token/auth', methods=['POST']) 
@tryCatch(name="mobile_login")
def mobile_login(): 
    print("MOBILE X-USER ",request.headers.get('x-user') )
    if request.method == "POST": 
     
        data           = request.get_json() 
        if data:
            email      = escape(data['email'])
            password   = escape(data['password'])

            if "cimh.edu.bb" in email:
                # RETRIEVE ACCOUNT SINCE IT EXIST
                account = mongo.findUser(email=email)

                if not account:
                    # LET VUE KNOW THE ACCOUNT DOES NOT EXIST
                    message = {"status":"accountDoesNotExist","message":"accountDoesNotExist","username":"","role":"user","id": ""}
                    return jsonify(message)       

                # VALIDATE PASSWORD PROVIDED BY USER
                unhash   = ph.verify(account['password'],password) # check_password_hash(account['password'],password )

                if  unhash and account:
                    message = {"status":"loggedIn","message":"loggedIn","username":account['lastname'],"email":account['email'],"id":account['id'],"role":account['role'],"image":account["image"]}
                    account.pop("email") 
                    account.pop("password")  
                    account.pop("timestamp") 
                    account.pop("registered") 
                    account.pop("emailconfirmed")        
                    return assign_access_refresh_tokens_mobile(account["id"], message, True)    
    
    return jsonify({"status":"failed","message":"Invalid Credentials","username":"","role":"user","id": ""}) 

    

# Endpoint for revoking the current users access token. Saved the unique
# identifier (jti) for the JWT into our database.
@app.route('/api/logout', methods=["GET"])
@jwt_required()
@tryCatch(name="logout")
def logout():

    token   = get_jwt() 
    user    = token["sub"]
     
    # Multiple row update
    Tokenlist.query.filter(Tokenlist.user_id.in_([user]),Tokenlist.iat.in_([token["iat"]])).update({Tokenlist.valid: False, Tokenlist.fresh: False}, synchronize_session=False)    
    db.session.commit() 
 
    resp = make_response({"status":"ok","message":"loggedOut"}) 
    unset_jwt_cookies(resp) 
    return resp, 401

@tryCatch(name="logoutUser")
def logoutUser(token):    
    user    = token["sub"] 
     
    # Multiple row update
    Tokenlist.query.filter(Tokenlist.user_id.in_([user]),Tokenlist.iat.in_([token["iat"]])).update({Tokenlist.valid: False, Tokenlist.fresh: False}, synchronize_session=False)    
    db.session.commit() 
 

#############################
#   ACCOUNT REGISTRATION    #
#############################

@app.route('/api/verification',methods=['POST'])
@tryCatch(name="send_email")
def send_email():

    if request.method == 'POST':
       
        form                = request.form                  
        firstname           = escape(form.get('Firstname'))
        lastname            = escape(form.get('Lastname'))
        email               = escape(form.get('Email'))
        password            = escape(form.get('Password'))
        passwordConfirm     = escape(form.get('PasswordConfirm'))
        code                = f"{token_hex(4)}"  
        entity              = escape(form.get("Entity"))  
        organization        = escape(form.get("Organization"))  
        country             = escape(form.get("Country"))  
        entities            = []

      
        
        if not (passwordConfirm == password):
                message = {"status":"ok","message":"Mismatched Passwords"}
                return jsonify(message)

        # CHECK IF USER ALREADY EXIST  
        exist, notice       = mongo.userExist(email = email)

        if exist and notice == "success":
            # LET VUE KNOW THE ACCOUNT ALREADY EXIST
            message = {"status":"ok","message":"Account Already Exist"}
            return jsonify(message)

        # CHECK TEMP COLLECTION DOCUMENT IF THAT USER ALREADY EXIST
        searchFor   = {"email":email, "type":"registration"}
        doc         = mongo.findTempDoc(searchFor)

        if doc:
            # VERIFICATION IS ALREADY IN PROGRESS, SEND A NEW ONE
            # SEND TIME LEFT UNTIL NEW VERIFICATION CODE EXPIRES
            espireAt    = datetime.now(timezone(timedelta(hours= timeOffset))) + timedelta(minutes=5)
            updateDoc   = mongo.updateTempDoc(query=searchFor,update= {"$set":{"expireAt": espireAt,"code":code}})
            if updateDoc: 
                # SEND EMAIL TO USER WITH VERIFICATION CODE 
                msg = Message("Verification code",sender="KS.donotreply@cimh.edu.bb" , recipients=[email])                        
                msg.html    = '<!DOCTYPE html> <html lang="en"> <head> <meta charset="UTF-8"> <meta http-equiv="X-UA-Compatible" content="IE=edge"> <meta name="viewport" content="width=device-width, initial-scale=1.0"> <title>Document</title> <style> body{ max-width: 700px; } .box{ box-sizing: border-box; width: 810px; /* height: 400px;  */ background-image: linear-gradient(180deg, #e2e8f0 , #e2e8f00c ); border-radius: 7px; display: grid; grid-template-columns: 1fr; grid-template-rows: 250px 120px 80px 70px 50px 50px; place-items: center; padding-bottom: 50px; margin: 0 26px; } .image{ grid-column: 1 / 2; grid-row: 1 / 2; background-color: #1e3a8a; border-radius: 7px; box-shadow: 0 4px 6px hsla(0,0%, 0%, .2); place-items: center; } .image > img{ height: 150px; margin: 25px 161px; } .info{ grid-column: 1 / 2; grid-row: 3 / 4; margin: 32px; } .title{ text-align: center; } </style> </head> <body> <div class="box"> <div class="image"> <img src="http://ww3.cimh.edu.bb/wp-content/uploads/2016/08/cimh-logo-web-white.png" alt=""> </div> <div class="title" > <h4>Verification Code:</h4> <h1 >'+ f"{code}"+ '</h1> </div> <div class="info"> <p class="message">Your verification code is right here. Please enter this code to confirm your identity and finish the registration process. <strong></strong></p> </div> <img src="" alt=""> </div> </body> </html>'
                ONE = mail.send(msg)                        
                return jsonify({"status":"emailSent","message":"emailSent"})
            return jsonify({"status":"failed","message":"failed"})

        else:
            # STORE TEMPORARILY IN DATABASE
            espireAt    = datetime.now(timezone(timedelta(hours= timeOffset))) + timedelta(minutes=5)
            query       = { "expireAt":espireAt,"type":"registration","firstname":firstname,"lastname":lastname,"email":email,"organization": organization,"entity":entity,"entities": entities,"country": country,"code":code,"password":password,"image":"default.png" }
            inserted    = mongo.createTempDoc(query)

            if inserted:
                # SEND EMAIL TO USER WITH VERIFICATION CODE 
                msg = Message("Verification code",sender="KS.donotreply@cimh.edu.bb" , recipients=[email])
                
                msg.html    = '<!DOCTYPE html> <html lang="en"> <head> <meta charset="UTF-8"> <meta http-equiv="X-UA-Compatible" content="IE=edge"> <meta name="viewport" content="width=device-width, initial-scale=1.0"> <title>Document</title> <style> body{ max-width: 700px; } .box{ box-sizing: border-box; width: 810px; /* height: 400px;  */ background-image: linear-gradient(180deg, #e2e8f0 , #e2e8f00c ); border-radius: 7px; display: grid; grid-template-columns: 1fr; grid-template-rows: 250px 120px 80px 70px 50px 50px; place-items: center; padding-bottom: 50px; margin: 0 26px; } .image{ grid-column: 1 / 2; grid-row: 1 / 2; background-color: #1e3a8a; border-radius: 7px; box-shadow: 0 4px 6px hsla(0,0%, 0%, .2); place-items: center; } .image > img{ height: 150px; margin: 25px 161px; } .info{ grid-column: 1 / 2; grid-row: 3 / 4; margin: 32px; } .title{ text-align: center; } </style> </head> <body> <div class="box"> <div class="image"> <img src="http://ww3.cimh.edu.bb/wp-content/uploads/2016/08/cimh-logo-web-white.png" alt=""> </div> <div class="title" > <h4>Verification Code:</h4> <h1 >'+ f"{code}"+ '</h1> </div> <div class="info"> <p class="message">Your verification code is right here. Please enter this code to confirm your identity and finish the registration process. <strong></strong></p> </div> <img src="" alt=""> </div> </body> </html>'
                mail.send(msg)  
                return jsonify({"status":"emailSent","message":"emailSent"})

    return jsonify({"status":"failed"})


@app.route('/api/register', methods=['POST'])
@tryCatch(name="register")
def register():
    # REGISTER A USER 
    form =  request.form
    if request.method == "POST":  
           
        firstname           = escape(form.get("Firstname") ).lower()
        lastname            = escape(form.get("Lastname") ).lower()
        email               = escape(form.get("Email") )
        password            = escape(form.get("Password") )
        passwordConfirm     = escape(form.get("PasswordConfirm") )
        code                = escape(form.get("Code"))  
        organization        = escape(form.get("Organization"))  
        entity              = escape(form.get("Entity"))  
        country             = escape(form.get("Country"))  
        entities            = []

      
        if not (passwordConfirm == password):
            message = {"status":"ok","message":"Mismatched passwords"}
            return jsonify(message)

        # VERIFY USER
        searchFor   = {"email":email}
        doc         = mongo.findTempDoc(searchFor)
        
    
        if doc: 
            if doc['code'] != code:
                return jsonify({"status":"failed","message":"Verification failed"}) 

            if doc['code'] == code and doc['email'] == email:
                # EMAIL ADDRESS VERIFIED

                # CREATE USER
                timestamp       = floor(time())
                registered      = ctime(timestamp)

                # Create Password hash  generate_password_hash(password, method='pbkdf2:sha256')
                pwdHash =  ph.hash(password)

                if "@cimh.edu.bb" in email:
                    # REGISTRATION FROM A CIMH STAFF
                    user = {"id":f"ACC{token_hex(16)}","firstname":firstname,"lastname":lastname,"email":email,"organization": organization,"entity":entity,"entities": entities,"country": country,"password": pwdHash,"role":"staff","timestamp":timestamp,"registered":registered,"emailconfirmed":True,"activated": True,"suball": False,"image":"default.png" }
                    
                else:
                    # REGISTRATION FROM EXTERNAL USER
                    user = {"id":f"ACC{token_hex(16)}","firstname":firstname,"lastname":lastname,"email":email,"organization": organization,"entity":entity,"entities": entities,"country": country,"password": pwdHash,"role":"user","timestamp":timestamp,"registered":registered,"emailconfirmed":True,"activated": False,"suball": False,"image":"default.png"}
                
            
                # UPDATE DATABASE
                # mongo.addUser(user.copy()) 
                location = [loc for loc in caribbean_countries if loc["name"] == country]

                if len(location) > 0:
                    user["icon"]    = location[0]["icon"]
                    user["center"]  = location[0]["center"]

                # STORE TEMPORARILY IN DATABASE FOR TWO WEEKS
                espireAt    = datetime.now(timezone(timedelta(hours= timeOffset))) + timedelta(weeks=2)
                query       = { "expireAt":espireAt,"type":"newregistration","email":email,"id":user["id"],"user": user }
                inserted    = mongo.createTempDoc(query)

                # CHECK IF USER WAS SUCCESSFULLY ADDED TO DATABASE
                searchFor   = {"type":"newregistration","email":email}
                doc         = mongo.findTempDoc(searchFor)            

                if doc:
                    emails = mongo.miscFind({"id":"emails"}) 
                    emailList = emails['registration']

                    if len(emailList) > 0:
                        # SEND EMAIL TO USER WITH VERIFICATION CODE 
                        msg = Message("KS -  New Account Alert",sender="KS.donotreply@cimh.edu.bb" , recipients=[x['email'] for x in  emailList])                      
                        msg.html    = f'New account request for {firstname.capitalize()} {lastname.capitalize()} with email: {email}. Login and visit the Admin section to Approve or Deny this request'
                        mail.send(msg) 

                    # SEND EMAIL TO USER ACKNOWLEDGING RECEIPT OF NEW ACCOUNT REQUEST 
                    msg = Message(f"kaleidoscope Account Request",sender="KS.donotreply@cimh.edu.bb" , recipients=[email])                        
                    msg.html    = f'''<!DOCTYPE html> <html> <head> <title>kaleidoscope</title> </head> <body>
                        <div><p>  Dear Customer, </p></div>
                        <div><p>  Thank you for your interest in a kaleidoscope account at the Caribbean Institute of Meteorology and Hydrology. Your information will be processed and a follow up email sent there after.</p></div>
                        
                        <div> <p> If you have any questions or need further assistance, please don\'t hesitate to contact us. </p></div>
                        <div><p>Sincerely,  </p> </div>
                        <div>
                            <address>THE CARIBBEAN INSTITUTE FOR METEOROLOGY AND HYDROLOGY  <br/>   
                                Husbands   <br/>   
                                St James   <br/>   
                                Barbados BB23006   <br/>     
                            </address>
                        </div>
                            </body> </html>'''
                    mail.send(msg) 

                    message = {"status":"ok","message":"Registered"}
                    return jsonify(message)

    return jsonify({"status":"failed","message":""}) 
       
@app.route('/api/verification/verifycode', methods=['POST']) 
# @jwt_required(optional=True)
@tryCatch(name="verify_reset_code")
def verify_reset_code():
    # VERIFY RESET CODE
    form =  request.form
    if request.method == "POST":       
        email               = escape(form.get("Email") ) 
        code                = escape(form.get("Code"))
        userType            = request.headers.get('x-user')   
 
        # VERIFY USER
        searchFor   = {"email":email, "type":"resetpassword","code": code}
        doc         = mongo.findTempDoc(searchFor)
        
        if doc:   
            message = {"status":"ok","message":"verified"}
            return jsonify(message)

    return jsonify({"status":"failed","message":"failed"}) 

@app.route('/api/verification/sendemail',methods=['POST'])
@tryCatch(name="send_email_password_reset")
def send_email_password_reset():

    if request.method == 'POST':
    
        form                = request.form              
        email               = escape(form.get('Email')) 
        code                = f"{token_hex(4)}"
        user                = request.headers.get('x-user')  

        # CHECK IF USER ALREADY EXIST 
        exist, notice       = mongo.userExist(email = email)

        if exist and notice == "success":
            # THE ACCOUNT ALREADY EXIST
            # CHECK TEMP COLLECTION DOCUMENT IF THAT USER ALREADY EXIST
            searchFor   = { "email": email, "type": "resetpassword" }
            doc         = mongo.findTempDoc(searchFor)

            if doc:
                # VERIFICATION IS ALREADY IN PROGRESS, SEND A NEW ONE
                # SEND TIME LEFT UNTIL NEW VERIFICATION CODE EXPIRES
                espireAt    = datetime.now(timezone(timedelta(hours= timeOffset))) + timedelta(minutes=5)
                updateDoc   = mongo.updateTempDoc(query=searchFor,update= {"$set":{"expireAt": espireAt,"code":code}})
                if updateDoc: 
                    # SEND EMAIL TO USER WITH VERIFICATION CODE 
                    msg = Message("Verification code",sender="KS.donotreply@cimh.edu.bb" , recipients=[email])                        
                    msg.html    = '<!DOCTYPE html> <html lang="en"> <head> <meta charset="UTF-8"> <meta http-equiv="X-UA-Compatible" content="IE=edge"> <meta name="viewport" content="width=device-width, initial-scale=1.0"> <title>Document</title> <style> body{ max-width: 700px; } .box{ box-sizing: border-box; width: 810px; /* height: 400px;  */ background-image: linear-gradient(180deg, #e2e8f0 , #e2e8f00c ); border-radius: 7px; display: grid; grid-template-columns: 1fr; grid-template-rows: 250px 120px 80px 70px 50px 50px; place-items: center; padding-bottom: 50px; margin: 0 26px; } .image{ grid-column: 1 / 2; grid-row: 1 / 2; background-color: #1e3a8a; border-radius: 7px; box-shadow: 0 4px 6px hsla(0,0%, 0%, .2); place-items: center; } .image > img{ height: 150px; margin: 25px 161px; } .info{ grid-column: 1 / 2; grid-row: 3 / 4; margin: 32px; } .title{ text-align: center; } </style> </head> <body> <div class="box"> <div class="image"> <img src="http://ww3.cimh.edu.bb/wp-content/uploads/2016/08/cimh-logo-web-white.png" alt=""> </div> <div class="title" > <h4>Verification Code:</h4> <h1 >'+ f"{code}"+ '</h1> </div> <div class="info"> <p class="message">Your verification code is right here. Please enter this code to confirm your identity and finish the registration process. <strong></strong></p> </div> <img src="" alt=""> </div> </body> </html>'
                    ONE = mail.send(msg)                        
                    return jsonify({"status":"emailSent","message":"emailSent"})
                return jsonify({"status":"failed","message":"failed"})

            else:
                # CREATE A NEW DOC AND SAVE TO TEMP COLLECTION 
                # STORE TEMPORARILY IN DATABASE 
                espireAt    = datetime.now(timezone(timedelta(hours= timeOffset))) + timedelta(minutes=5)
                query       = { "expireAt": espireAt,"email": email,"code":code, "type":"resetpassword" }
                inserted    = mongo.createTempDoc(query)

                if inserted:
                    # SEND EMAIL TO USER WITH VERIFICATION CODE 
                    msg = Message("Verification code",sender="KS.donotreply@cimh.edu.bb" , recipients=[email])                        
                    msg.html    = '<!DOCTYPE html> <html lang="en"> <head> <meta charset="UTF-8"> <meta http-equiv="X-UA-Compatible" content="IE=edge"> <meta name="viewport" content="width=device-width, initial-scale=1.0"> <title>Document</title> <style> body{ max-width: 700px; } .box{ box-sizing: border-box; width: 810px; /* height: 400px;  */ background-image: linear-gradient(180deg, #e2e8f0 , #e2e8f00c ); border-radius: 7px; display: grid; grid-template-columns: 1fr; grid-template-rows: 250px 120px 80px 70px 50px 50px; place-items: center; padding-bottom: 50px; margin: 0 26px; } .image{ grid-column: 1 / 2; grid-row: 1 / 2; background-color: #1e3a8a; border-radius: 7px; box-shadow: 0 4px 6px hsla(0,0%, 0%, .2); place-items: center; } .image > img{ height: 150px; margin: 25px 161px; } .info{ grid-column: 1 / 2; grid-row: 3 / 4; margin: 32px; } .title{ text-align: center; } </style> </head> <body> <div class="box"> <div class="image"> <img src="http://ww3.cimh.edu.bb/wp-content/uploads/2016/08/cimh-logo-web-white.png" alt=""> </div> <div class="title" > <h4>Verification Code:</h4> <h1 >'+ f"{code}"+ '</h1> </div> <div class="info"> <p class="message">Your verification code is right here. Please enter this code to confirm your identity and finish the registration process. <strong></strong></p> </div> <img src="" alt=""> </div> </body> </html>'
                    mail.send(msg) 
                    return jsonify({"status":"emailSent","message":"emailSent"})
        else:
            message = {"status":"failed","message":"Account Does Not Exist"}
            return jsonify(message)

    return jsonify({"status":"failed","message":"failed"})


@app.route('/api/verification/rp', methods=['POST'])
# @jwt_required(optional=True)
@tryCatch(name="reset_password")
def reset_password():
    # RESET PASSWORD
    form =  request.form
    if request.method == "POST":  
       
        email               = escape(form.get("Email") )
        password            = escape(form.get("Password") )
        passwordConfirm     = escape(form.get("PasswordConfirm") )
        code                = escape(form.get("Code"))
        user                = request.headers.get('x-user') 
                
        if not (passwordConfirm == password):
            message = {"status":"ok","message":"Mismatched passwords"}
            return jsonify(message)

        # CHECK IF USER ALREADY EXIST
        exist, notice       = mongo.userExist(email = email)
        
        if exist and notice == "success":
            # VERIFY USER
            searchFor   = { "email":email, "type":"resetpassword","code": code }
            doc         = mongo.findTempDoc(searchFor)
            
            if doc:   
                # Create Password hash  generate_password_hash(password, method='pbkdf2:sha256')
                pwdHash =  ph.hash(password)
                
                updatedUser = mongo.updateUser({"email": email} ,{"$set":{"password": pwdHash}})
                if updatedUser:
                    message = {"status":"ok","message":"updated"}
                    return jsonify(message)
                    
    return jsonify({"status":"failed","message":"failed"}) 


#####################
#     ADMIN APIs    #
#####################

@app.route('/api/auth', methods=['POST'])
@jwt_required()
@tryCatch(name="getAuthStatus")
def getAuthStatus():
    # username = get_jwt_identity()
    # very important account settings // 
    if request.method == "POST": 
            
        # GET USER ACCOUNT INFO
        user = request.get_json()
        account     = mongo.findUser(id=user['account'])
        # print(account, user['account'])
        if account:                    
            # IF STAFF
            if(account["role"] == "admin"):                     
                return jsonify({"status":"Auth"}) 
        return jsonify({"status":"NotAuth"})         
    return jsonify({"status":"failed"})

@app.route('/api/all/accounts', methods=['POST'])  
@jwt_required()
@tryCatch(name="getAllAccounts")
def getAllAccounts():   
    if request.method == "POST": 
        form = request.form 
        # GET USER ACCOUNT INFO
        user        = escape(form.get("account"))
        account     = mongo.findUser(id= user)

        if account["role"] in ["admin", "staff"]:
            newRegistrations = mongo.findAllTempDoc({"type":"newregistration"})
            users   = mongo.findAllClient()
            staffs  = mongo.findAllStaff()         
          
            return jsonify({"status":"ok","newRegistrations": newRegistrations,"users": users,"staffs": staffs})

    return jsonify({"status":"failed"})


@app.route('/api/get/account', methods=['POST'])  
@jwt_required()
@tryCatch(name="getAccount")
def getAccount():   
    if request.method == "POST": 
        form = request.form 
        # GET USER ACCOUNT INFO
        user        = escape(form.get("account"))
        account     = mongo.findUser(id= user)

        if account:
            account.pop("role") 
            account.pop("password")  
            # account.pop("timestamp") 
            account.pop("registered") 
            # account.pop("web") 
            account.pop("emailconfirmed")      
          
            return jsonify({"status":"ok","account": account})
    return jsonify({"status":"failed"})


@app.route('/api/get/suball', methods=['POST'])  
@jwt_required()
@tryCatch(name="getUserSuball")
def getUserSuball():   
    if request.method == "POST": 
        form = request.form 
        # GET USER ACCOUNT INFO
        user        = escape(form.get("account"))
        account     = mongo.findUser(id= user)

        if account:        
            return jsonify({"status":"ok","suball": account["suball"]})

    return jsonify({"status":"failed"})



@app.route('/api/all/sites', methods=['POST'])  
@jwt_required()
@tryCatch(name="getAllSites")
def getAllSites():   
    if request.method == "POST": 
        form = request.form 
        # GET USER ACCOUNT INFO
        user        = escape(form.get("account"))
        entity      = escape(form.get("entity"))
        account     = mongo.findUser(id= user)

        if account["role"] in ["admin", "staff"] or account["suball"] == True:
            sites = mongo.findAllSites({})
        else:
            sites = mongo.findAllSites({ 'type': 'site', '$or': [ { 'entity': account["entity"] }, { 'entities': { '$in': [account["entities"]] } } ] }) 

        if sites:          
            return jsonify({"status":"ok","sites": sites, "suball": account["suball"]})

    return jsonify({"status":"failed"})


@app.route('/api/get/site', methods=['POST'])  
@jwt_required()
@tryCatch(name="getSite")
def getSite():   
    if request.method == "POST": 
        form = request.form 
        # GET USER ACCOUNT INFO
        user        = escape(form.get("account"))
        siteID      = escape(form.get("id"))
        account     = mongo.findUser(id= user)

        if account:
            # site = mongo.findSite(id= siteID)
            site = mongo.getSiteWithOwner(site= siteID)
            if site:
                entity = mongo.findEntity(id= site["entity"],project={"_id":0,"name":1,"country":1,"code":1,"organization":1 })
                return jsonify({"status":"ok","site": site,"entity": entity})

    return jsonify({"status":"failed"})

@app.route('/api/get/requests', methods=['POST'])  
@jwt_required()
@tryCatch(name="getRequests")
def getRequests():   
    if request.method == "POST": 
        form = request.form 
        # GET USER ACCOUNT INFO
        user        = escape(form.get("account")) 
        account     = mongo.findUser(id= user)

        if account and account["role"] == "admin":
            req = mongo.findAllTempDoc({"type":"requests"})            
            return jsonify({"status":"ok","requests": req})

    return jsonify({"status":"failed"})

@app.route('/api/get/sites', methods=['POST'])  
@jwt_required()
@tryCatch(name="getSites")
def getSites():   
    if request.method == "POST": 
        form = request.form 
        # GET USER ACCOUNT INFO
        user        = escape(form.get("account"))
        account     = mongo.findUser(id= user)

        if account:
            # site = mongo.findSite(id= siteID)
            site = mongo.getSitesForOwner(owner= user)
            if site:
                return jsonify({"status":"ok","data": site})
    return jsonify({"status":"failed"})


@app.route('/api/aod/requests', methods=['POST'])  
@jwt_required()
@tryCatch(name="approveOrDenyRequests")
def approveOrDenyRequests():   
    if request.method == "POST": 
        form        = request.form 
        # GET USER ACCOUNT INFO  caribbean_countries
        user        = escape(form.get("account"))
        id          = escape(form.get("id"))
        decision    = escape(form.get("decision"))

        account     = mongo.findUser(id= user)
       
       
        if account["role"] == "admin":
            
            # Find new user account in Temp collection
            searchFor   = {"id": id}
            doc         = mongo.findTempDoc(searchFor)
            
            if doc:
                # Process request Approve or Deny
                
                # IF APPROVING
                if decision == "approve": 
                    status  = ""
                    message = ""

                    # UPDATE DATABASE
                    if doc["reqtype"] == "createentity":
                        status = createEntityFromRequest(doc["account"]["id"],doc["data"]["name"], doc["data"]["country"], doc["data"]["organization"])   
                    elif doc["reqtype"] == "updateentity":
                        status = updateEntityFromRequest(doc["data"]["id"],doc["data"]["name"], doc["data"]["country"], doc["data"]["organization"])
                    elif doc["reqtype"] == "deleteentity":
                        status = deleteEntityFromRequest(doc["data"]["id"] )   
                    
                    elif doc["reqtype"] == "createsite":
                        status =  addSite(doc["data"]["name"],float(doc["data"]["lat"]) ,float(doc["data"]["lon"]) ,doc["data"]["entity"] )   
                    elif doc["reqtype"] == "updatesite":
                        status =  updateSiteFromRequest(doc["data"]["id"], doc["data"]["name"], doc["data"]["lat"], doc["data"]["lon"])  
                    elif doc["reqtype"] == "deletesite":
                        status =  deleteSiteFromRequest(doc["data"]["id"])  
                        
                    elif doc["reqtype"] == "createdevice":
                        siteID = doc["data"].pop("siteid")
                        status =  createDeviceFromRequest(siteID,doc["data"])   
                    elif doc["reqtype"] == "updatedevice":
                        siteID  = doc["data"].pop("siteid")
                        deviceID = doc["data"].pop("deviceid")
                        status =  updateDeviceFromRequest(siteID,deviceID, doc["data"])  
                    elif doc["reqtype"] == "deletedevice":
                        siteID  = doc["data"].pop("siteid")
                        deviceID = doc["data"].pop("id")
                        status =  deleteDeviceFromRequest(siteID,deviceID)  


                    message = {"status": status}
                    if status in ["created","added","deleted","updated"]: 
                        # REMOVE REQUEST FROM TEMP COLLECTION
                        mongo.deleteTempDoc({"id":id})

                        reqMessage = ""
                        reqMessage2 = ""

                        if doc["reqtype"] == "createentity":
                            reqMessage = f"A new Entity ({doc["data"]["name"]}) request"
                            reqMessage2 = f"a new Entity ({doc["data"]["name"]})"
                        if doc["reqtype"] == "updateentity":
                            reqMessage = f"An Entity ({doc["data"]["name"]}) update request"
                            reqMessage2 = f"an update to Entity ({doc["data"]["name"]})"
                        if doc["reqtype"] == "deleteentity":
                            reqMessage = f"An Entity ({doc["data"]["name"]}) deletion request"
                            reqMessage2 = f"Entity ({doc["data"]["name"]}) to be deleted"

                        elif doc["reqtype"] == "createsite":
                            reqMessage = f"A new Site ({doc["data"]["name"]}) for {doc["entity"]["organization"]}"
                            reqMessage2 = f"a new Site ({doc["data"]["name"]}), linked to your {doc["entity"]["organization"]} entity"
                        elif doc["reqtype"] == "updatesite":
                            reqMessage = f"A Site ({doc["data"]["name"]}) for {doc["entity"]["organization"]} update request"
                            reqMessage2 = f"updating your Site ({doc["data"]["name"]}), linked to your {doc["entity"]["organization"]} entity"
                        elif doc["reqtype"] == "deletesite":
                            reqMessage = f"A Site ({doc["data"]["name"]}) for {doc["entity"]["organization"]} deletion request"
                            reqMessage2 = f"deleting your Site ({doc["data"]["name"]}), linked to your {doc["entity"]["organization"]} entity"

                        elif doc["reqtype"] == "createdevice":
                            reqMessage = f"A new Device ({doc["data"]["name"]}) for {doc["entity"]["organization"]}"
                            reqMessage2 = f"a new Device ({doc["data"]["name"]}), linked to your {doc["entity"]["organization"]} entity"
                        elif doc["reqtype"] == "updatedevice":
                            reqMessage = f"A Device ({doc["data"]["name"]}) for {doc["entity"]["organization"]} update request"
                            reqMessage2 = f"updating your Device ({doc["data"]["name"]}), linked to your {doc["entity"]["organization"]} entity"
                        elif doc["reqtype"] == "deletedevice":
                            reqMessage = f"A Device ({doc["data"]["name"]}) for {doc["entity"]["organization"]} deletion request"
                            reqMessage2 = f"deleting your Device ({doc["data"]["name"]}), linked to your {doc["entity"]["organization"]} entity"

                        #E-MAIL ALL RELEVANT PARTIES
                        emails = mongo.miscFind({"id":"emails"}) 
                        emailList = emails['requests']
                        # SEND EMAIL TO USER WITH VERIFICATION CODE 
                        msg = Message("KS -  Request(Approved) Alert",sender="KS.donotreply@cimh.edu.bb" , recipients=[x['email'] for x in  emailList])                      
                        msg.html    = f'{reqMessage} was approved for {doc["account"]['firstname'].capitalize()} {doc["account"]['lastname'].capitalize()} with email: {doc["account"]['email']} on our kaleidoscope platform. Login and visit the Admin section to see the account details.'
                        mail.send(msg) 

                        

                        # SEND EMAIL TO USER ACKNOWLEDGING RECEIPT OF NEW ACCOUNT REQUEST 
                        msg = Message(f"kaleidoscope Request",sender="KS.donotreply@cimh.edu.bb" , recipients=[doc["account"]['email']])                        
                        msg.html    = f'''<!DOCTYPE html> <html> <head> <title>kaleidoscope</title> </head> <body>
                            <div><p>  Dear Customer, </p></div>
                            <div><p>  We are pleased to inform you that your request for {reqMessage2}, on CIMH's kaleidoscope platform has been approved. Please visit our website and log in to begin using the platform.</p></div>
                            
                            <div> <p> If you have any questions or need further assistance, please don\'t hesitate to contact us. </p></div>
                            <div><p>Sincerely,  </p> </div>
                            <div>
                                <address>THE CARIBBEAN INSTITUTE FOR METEOROLOGY AND HYDROLOGY  <br/>   
                                    Husbands   <br/>   
                                    St James   <br/>   
                                    Barbados BB23006   <br/>     
                                </address>
                            </div>
                                </body> </html>'''
                        mail.send(msg) 

                        
                    return jsonify(message)


                #ELSE IF DENYING
                if decision == "deny":
                    
                    # REMOVE USER FROM TEMP COLLECTION 
                    count = mongo.deleteTempDoc({"id":id})

                    if count > 0:
                        reqMessage = ""
                        reqMessage2 = ""
                        if doc["reqtype"] == "createentity":
                            reqMessage = f"A new Entity ({doc["data"]["name"]}) request"
                            reqMessage2 = f"request for a new Entity ({doc["data"]["name"]})"
                        if doc["reqtype"] == "updateentity":
                            reqMessage = f"An Entity ({doc["data"]["name"]}) update request"
                            reqMessage2 = f"Entity ({doc["data"]["name"]}) update request"
                        if doc["reqtype"] == "deleteentity":
                            reqMessage = f"An Entity ({doc["data"]["name"]}) deletion request"
                            reqMessage2 = f"Entity ({doc["data"]["name"]}) deletion request"
                            
                        elif doc["reqtype"] == "createsite":
                            reqMessage = f"A new Site ({doc["data"]["name"]}) linked to the {doc["entity"]["organization"]} entity,"
                            reqMessage2 = f"request for a new Site ({doc["data"]["name"]}), linked to your {doc["entity"]["organization"]} entity,"
                        elif doc["reqtype"] == "updatesite":
                            reqMessage = f"A Site ({doc["data"]["name"]}) for {doc["entity"]["organization"]} update request"
                            reqMessage2 = f"request to update, Site ({doc["data"]["name"]}), linked to your {doc["entity"]["organization"]} entity"                    
                        elif doc["reqtype"] == "deletesite":
                            reqMessage = f"A Site ({doc["data"]["name"]}) for {doc["entity"]["organization"]} deletion request"
                            reqMessage2 = f"request to delete, Site ({doc["data"]["name"]}), linked to your {doc["entity"]["organization"]} entity"


                        elif doc["reqtype"] == "createdevice":
                            reqMessage = f"A new Device ({doc["data"]["name"]}) linked to the {doc["entity"]["organization"]} entity,"
                            reqMessage2 = f"request for a new Device ({doc["data"]["name"]}), linked to your {doc["entity"]["organization"]} entity,"
                        elif doc["reqtype"] == "updatedevice":
                            reqMessage = f"A Device ({doc["data"]["name"]}) for {doc["entity"]["organization"]} update request"
                            reqMessage2 = f"request to update, Device ({doc["data"]["name"]}), linked to your {doc["entity"]["organization"]} entity"                    
                        elif doc["reqtype"] == "deletedevice":
                            reqMessage = f"A Device ({doc["data"]["name"]}) for {doc["entity"]["organization"]} deletion request"
                            reqMessage2 = f"request to delete, Device ({doc["data"]["name"]}), linked to your {doc["entity"]["organization"]} entity"

                        #E-MAIL ALL RELEVANT PARTIES
                        emails = mongo.miscFind({"id":"emails"}) 
                        emailList = emails['requests']

                        # SEND EMAIL TO USER WITH VERIFICATION CODE 
                        msg = Message("KS -  Request(Denied) Alert",sender="KS.donotreply@cimh.edu.bb" , recipients=[x['email'] for x in  emailList])                      
                        msg.html    = f'FYI - {reqMessage} was denied for {doc["account"]['firstname'].capitalize()} {doc["account"]['lastname'].capitalize()} with email: {doc["account"]['email']}.'
                        mail.send(msg) 

                        # SEND EMAIL TO USER ACKNOWLEDGING RECEIPT OF NEW ACCOUNT REQUEST 
                        msg = Message(f"kaleidoscope Request",sender="KS.donotreply@cimh.edu.bb" , recipients=[doc["account"]['email']])                        
                        msg.html    = f'''<!DOCTYPE html> <html> <head> <title>kaleidoscope</title> </head> <body>
                            <div><p>  Dear Customer, </p></div>
                            <div><p>  We regret to inform you that your {reqMessage2} on CIMH's kaleidoscope platform, cannot be approved at this time.</p></div>
                            
                            <div> <p> If you have any questions or require further assistance, please feel free to contact our support team. </p></div>
                            <div><p>Sincerely,  </p> </div>
                            <div>
                                <address>THE CARIBBEAN INSTITUTE FOR METEOROLOGY AND HYDROLOGY  <br/>   
                                    Husbands   <br/>   
                                    St James   <br/>   
                                    Barbados BB23006   <br/>     
                                </address>
                            </div>
                                </body> </html>'''
                        mail.send(msg) 

                        message = {"status":"denied"}
                        return jsonify(message)             

    return jsonify({"status":"failed"})


@app.route('/api/aod', methods=['POST'])  
@jwt_required()
@tryCatch(name="approveOrDeny")
def approveOrDeny():   
    if request.method == "POST": 
        form        = request.form 
        # GET USER ACCOUNT INFO  caribbean_countries
        user        = escape(form.get("account"))
        id          = escape(form.get("id"))
        decision    = escape(form.get("decision"))

        account     = mongo.findUser(id= user)
       
       
        if account["role"] == "admin":
            
            # Find new user account in Temp collection
            searchFor   = {"id": id}
            doc         = mongo.findTempDoc(searchFor)
            
            if doc:
                # Process request Approve or Deny

                # IF APPROVING
                if decision == "approve":
                    newAccount              = doc["user"]
                    newAccount["activated"] = True 

                    # UPDATE COLLECTIONS 
                    mongo.addUser(newAccount.copy())  

                    # CHECK IF USER WAS SUCCESSFULLY ADDED TO DATABASE
                    exist,  notice       = mongo.userExist(email = newAccount['email']) 
                    
                   
                    if exist: # and exist1 
                        # REMOVE USER FROM TEMP COLLECTION
                        mongo.deleteTempDoc({"id":id})

                        #E-MAIL ALL RELEVANT PARTIES
                        emails = mongo.miscFind({"id":"emails"}) 
                        emailList = emails['registration']
                        # SEND EMAIL TO USER WITH VERIFICATION CODE 
                        msg = Message("KS -  Account(Approved) Alert",sender="KS.donotreply@cimh.edu.bb" , recipients=[x['email'] for x in  emailList])                      
                        msg.html    = f'A new kaleidoscope account was approved for {newAccount['firstname'].capitalize()} {newAccount['lastname'].capitalize()} with email: {newAccount['email']}. Login and visit the Admin section to see the account details.'
                        mail.send(msg) 

                        # SEND EMAIL TO USER ACKNOWLEDGING RECEIPT OF NEW ACCOUNT REQUEST 
                        msg = Message(f"kaleidoscope Account",sender="KS.donotreply@cimh.edu.bb" , recipients=[newAccount['email']])                        
                        msg.html    = f'''<!DOCTYPE html> <html> <head> <title>kaleidoscope</title> </head> <body>
                            <div><p>  Dear Customer, </p></div>
                            <div><p>  We are pleased to inform you that your request for a kaleidoscope account at the Caribbean Institute of Meteorology and Hydrology has been approved. Please visit our website and log in to begin using the platform.</p></div>
                            
                            <div> <p> If you have any questions or need further assistance, please don\'t hesitate to contact us. </p></div>
                            <div><p>Sincerely,  </p> </div>
                            <div>
                                <address>THE CARIBBEAN INSTITUTE FOR METEOROLOGY AND HYDROLOGY  <br/>   
                                    Husbands   <br/>   
                                    St James   <br/>   
                                    Barbados BB23006   <br/>     
                                </address>
                            </div>
                                </body> </html>'''
                        mail.send(msg) 

                        message = {"status":"approved"}
                        return jsonify(message)


                #ELSE IF DENYING
                if decision == "deny":
                    newAccount = doc["user"]
                    # REMOVE USER FROM TEMP COLLECTION 
                    count = mongo.deleteTempDoc({"id":id})

                    if count > 0:
                    
                        #E-MAIL ALL RELEVANT PARTIES
                        emails = mongo.miscFind({"id":"emails"}) 
                        emailList = emails['registration']
                        # SEND EMAIL TO USER WITH VERIFICATION CODE 
                        msg = Message("KS -  Account(Denied) Alert",sender="KS.donotreply@cimh.edu.bb" , recipients=[x['email'] for x in  emailList])                      
                        msg.html    = f'FYI - A new account request denied for {newAccount['firstname'].capitalize()} {newAccount['lastname'].capitalize()} with email: {newAccount['email']}.'
                        mail.send(msg) 

                        # SEND EMAIL TO USER ACKNOWLEDGING RECEIPT OF NEW ACCOUNT REQUEST 
                        msg = Message(f"kaleidoscope Account",sender="KS.donotreply@cimh.edu.bb" , recipients=[newAccount['email']])                        
                        msg.html    = f'''<!DOCTYPE html> <html> <head> <title>kaleidoscope</title> </head> <body>
                            <div><p>  Dear Customer, </p></div>
                            <div><p>  We regret to inform you that your request for a kaleidoscope account at the Caribbean Institute of Meteorology and Hydrology has not been approved.</p></div>
                            
                            <div> <p> If you have any questions or require further assistance, please feel free to contact our support team. </p></div>
                            <div><p>Sincerely,  </p> </div>
                            <div>
                                <address>THE CARIBBEAN INSTITUTE FOR METEOROLOGY AND HYDROLOGY  <br/>   
                                    Husbands   <br/>   
                                    St James   <br/>   
                                    Barbados BB23006   <br/>     
                                </address>
                            </div>
                                </body> </html>'''
                        mail.send(msg) 

                        message = {"status":"denied"}
                        return jsonify(message)             

    return jsonify({"status":"failed"})


@app.route('/api/remove/account', methods=['POST'])  
@jwt_required()
@tryCatch(name="deleteAccounts")
def deleteAccounts():   
    if request.method == "POST": 
        form = request.form 
        # GET USER ACCOUNT INFO
        user        = escape(form.get("account"))
        id          = escape(form.get("id"))

        account     = mongo.findUser(id= user)

        if account["role"] == "admin":
            accountDel     = mongo.findUser(id= id) # Account to delete

            if accountDel:
                count = mongo.removeUser(email= accountDel["email"])
                count1 = mongo.removeMqttUser(accountDel["id"])

                if count > 0 and count1 > 0:          
                    return jsonify({"status":"deleted"})
                
    return jsonify({"status":"failed"})


@app.route('/api/get/entities', methods=['POST'])  
@jwt_required()
@tryCatch(name="getAllEntities")
def getAllEntities():   
    if request.method == "POST": 
        data        = request.get_json()
        # GET USER ACCOUNT INFO
        accountID   = escape(data["account"]) 
        account     = mongo.findUser(id= accountID)

        if account:
            query = {"$or":[{"id": {"$in": account["entities"] }}, {"id":account['entity']}]}
            if account["role"] == "admin":
                query = {}             
    
            entitiesData = mongo.findAllEntities(query,{ '_id': 0, 'web': 0, 'device': 0 })    
            return jsonify({"status":"ok","entity": account["entity"],"entities": account["entities"], "entitiesData": entitiesData})

    return jsonify({"status":"failed"})  



@app.route('/api/get/signup/entities', methods=['POST'])  
# @jwt_required()
@tryCatch(name="getAllEntitiesForSignup")
def getAllEntitiesForSignup():   
    if request.method == "POST": 
        data        = request.get_json()
        # GET USER ACCOUNT INFO
        accountID   = escape(data["account"]) # THIS WILL BE EMPTY
       
        entities = mongo.findAllEntitiesForSignup({"_id":0,"web":0,"device":0,"websubtopic":0,"devicesubtopic":0})    
        return jsonify({"status":"ok","entities": entities})

    return jsonify({"status":"failed"})

@app.route('/api/create/entity', methods=['POST'])  
@jwt_required()
@tryCatch(name="createEntity")
def createEntity():   
    if request.method == "POST": 
      
        data        = request.get_json()
        # GET USER ACCOUNT INFO
        accountID   = escape(data["account"])
        name        = escape(data["name"])
        organization = escape(data["organization"])
        code        = str(escape(data["code"])) 
        country     = ""
        account     = mongo.findUser(id= accountID)

        try:
            country     = [x["name"] for x in caribbean_countries if x["code"] == code ][0]
        except:
            pass

        if account["role"] == "admin":
            exist, notice  = mongo.entityExist(name= name)

            if exist:
                entities = mongo.findAllEntities({"_id":0})    
                return jsonify({"status":"exist","entities": entities})
            else:
                entity               = {"id": f"ENT{token_hex(16)}","name": name, "country": country, "code": code, "organization": organization} 
                entity["web"]        = {"username":token_hex(8),"password": token_hex(16)}
                entity["device"]     = {"username":token_hex(8),"password": token_hex(16)}
                entity["websubtopic"]       = f"/station/data/{name.replace(" ","").lower()}/#"
                entity["devicesubtopic"]    = f"/station/msg/{name.replace(" ","").lower()}/#"
                pwdWeb               = ph.hash(entity["web"]["password"])
                pwdDevice            = ph.hash(entity["device"]["password"])
            

                web                  = {} 
                web["id"]            = token_hex(16)
                web["username"]      = entity["web"]["username"]
                web["password"]      = pwdWeb
                web["type"]          = "web"
                web["superuser"]     = False
                web["owner"]         = entity["id"]
                web["acls"]          = [{"type":"main","topic": entity["websubtopic"],"acc":4},{"type":"other","topic": entity["websubtopic"],"acc":1}, {"type":"suball","topic":f"/station/data/#","acc":1},{"type":"other","topic":f"/station/data/#","acc":1}]
                
                device               = {}
                device["id"]         = token_hex(16)
                device["username"]   = entity["device"]["username"]
                device["password"]   = pwdDevice
                device["type"]       = "device"
                device["superuser"]  = False
                device["owner"]      = entity["id"]
                device["acls"]       = [{"type":"sub","topic": entity["devicesubtopic"],"acc":4},{"type":"other","topic": entity["devicesubtopic"],"acc":1},{"type":"pub","topic": entity["websubtopic"],"acc":2}]
                
                res = mongo.addEntity(entity)

                if res:
                    mongo.addMqttUser(web.copy())
                    mongo.addMqttUser(device.copy())
                    entities = mongo.findAllEntities({"_id":0})                
                    return jsonify({"status":"created","entities": entities})
                
    return jsonify({"status":"failed"})

@app.route('/api/delete/entity', methods=['POST'])  
@jwt_required()
@tryCatch(name="deleteEntity")
def deleteEntity():   
    if request.method == "POST": 
        form = request.form 
        # GET USER ACCOUNT INFO
        accountID   = escape(form.get("account")) 
        entityID    = escape(form.get("id"))
        account     = mongo.findUser(id= accountID)

        if account["role"] == "admin":    
            count = mongo.deleteEntity({"id": entityID})
            
            if count > 0: 
                count1 = mongo.removeMqttUser(entityID)
                count2 = mongo.deleteAllSite({"entity": entityID})                
                return jsonify({"status":"deleted" })

    return jsonify({"status":"failed"})

@app.route('/api/update/entity', methods=['POST'])  
@jwt_required()
@tryCatch(name="updateEntity")
def updateEntity():   
    if request.method == "POST": 
      
        data        = request.get_json()
        # GET USER ACCOUNT INFO
        id          = escape(data["id"])
        accountID   = escape(data["account"])
        name        = escape(data["name"])
        organization  = escape(data["organization"])
        code        = str(escape(data["code"]))
        country     = ""
        account     = mongo.findUser(id= accountID)

        try:
            country     = [x["name"] for x in caribbean_countries if x["code"] == code ][0]
        except:
            pass

        if account["role"] == "admin":
            # UPDATE SITE                
            updated = mongo.updateEntity({"id": id} ,{"$set": {"name": name,"country": country, "code": code, "organization": organization}})

            if updated:     
                return jsonify({"status":"updated"})
                
    return jsonify({"status":"failed"})


@app.route('/api/create/site', methods=['POST'])  
@jwt_required()
@tryCatch(name="createSite")
def createSite():   
    if request.method == "POST": 
        form = request.form 
        # GET USER ACCOUNT INFO
        user         = escape(form.get("account")) 
        name         = escape(form.get("name"))
        lat          = float(escape(form.get("lat")))
        lon          = float(escape(form.get("lon")))
        entity       = str(escape(form.get("entity")))

        account     = mongo.findUser(id= user)

        '''
        ACLs   meaning
            1 means read only, 
            2 means write only, 
            3 means readwrite and 
            4 means subscribe 
        '''
        
        if account["role"] == "admin":
            res = addSite(name,lat,lon, entity)

            if res == "added":                 
                return jsonify({"status":"added"})
                
    return jsonify({"status":"failed"})

@app.route('/api/delete/site', methods=['POST'])  
@jwt_required()
@tryCatch(name="deleteSite")
def deleteSite():   
    if request.method == "POST": 
        form = request.form 
        # GET USER ACCOUNT INFO
        accountID   = escape(form.get("account")) 
        siteID      = escape(form.get("site"))
        account     = mongo.findUser(id= accountID)

        if account["role"] == "admin":    
            count = mongo.deleteSite({"id": siteID})
            
            if count > 0: 
                return jsonify({"status":"deleted" })

    return jsonify({"status":"failed"})


@app.route('/api/create/device', methods=['POST'])  
@jwt_required()
@tryCatch(name="createDevice")
def createDevice():   
    if request.method == "POST": 
      
        data        = request.get_json()
        # GET USER ACCOUNT INFO
        accountID   = escape(data["account"])
        siteID      = escape(data["id"])
        account     = mongo.findUser(id= accountID)

        if account["role"] == "admin":

            siteToUpdate     = mongo.findSite(id= siteID) # Site to update

            if siteToUpdate:
                data.pop("id")
                data.pop("account")
                data["id"] = f"DEV{token_hex(16)}"
                data["lat"] = float(data["lat"])
                data["lon"] = float(data["lon"])
                data["dashboard"] = []

                # CREATE DEVICE              
                updated = mongo.updateSite({"id": siteID, "type": "site"} ,{"$push": { "devices": data}})

                if updated:      
                    site = mongo.getSiteWithOwner(site= siteID) 
                    return jsonify({"status":"added","data": site})
                
    return jsonify({"status":"failed"})

@app.route('/api/update/device', methods=['POST'])  
@jwt_required()
@tryCatch(name="updateDevice")
def updateDevice():   
    if request.method == "POST": 
      
        data        = request.get_json()
        # GET USER ACCOUNT INFO
        accountID   = escape(data["account"])
        siteID      = escape(data["siteid"])
        deviceID    = escape(data["deviceid"])
        account     = mongo.findUser(id= accountID)

        if account["role"] == "admin":

            siteToUpdate     = mongo.findSite(id= siteID) # Account to update

            if siteToUpdate:

                # UPDATE DEVICE                
                updated = mongo.updateSite({"id": siteID, "type": "site","devices.id": deviceID} ,{"$set": { "devices.$.name": data["name"],"devices.$.lat": float(data["lat"]),"devices.$.lon": float(data["lon"]),"devices.$.processor": data["processor"],"devices.$.params": data["params"]}})

                if updated:      
                    site = mongo.getSiteWithOwner(site= siteID) 
                    return jsonify({"status":"updated","data": site})
                
    return jsonify({"status":"failed"})


@app.route('/api/delete/device', methods=['POST'])  
@jwt_required()
@tryCatch(name="deleteDevice")
def deleteDevice():   
    if request.method == "POST": 
        form = request.form 
        # GET USER ACCOUNT INFO
        accountID   = escape(form.get("account")) 
        siteID      = escape(form.get("site"))
        deviceID    = escape(form.get("id"))
        account     = mongo.findUser(id= accountID)

        if account:    
            data = mongo.updateSite({"id": siteID,"devices.id": deviceID},{"$pull": {"devices" : { "id": deviceID }}})
            
            if deviceID not in [x["id"] for x in data["devices"]]:          
                site = mongo.getSiteWithOwner(site= siteID)
            
                if site:
                    return jsonify({"status":"deleted","data": site })

    return jsonify({"status":"failed"})

@app.route('/api/update/site', methods=['POST'])  
@jwt_required()
@tryCatch(name="updateSite")
def updateSite():   
    if request.method == "POST": 
      
        data        = request.get_json()
        # GET USER ACCOUNT INFO
        accountID   = escape(data["account"])
        siteID      = escape(data["id"])
        account     = mongo.findUser(id= accountID)

        if account["role"] == "admin":

            siteToUpdate     = mongo.findSite(id= siteID) # Account to update

            if siteToUpdate:

                # UPDATE SITE                
                updated = mongo.updateSite({"id": siteID, "type": "site"} ,{"$set": {"name": data["name"],"lat": float(data["lat"]),"lon": float(data["lon"]),"enabled": data["enabled"]  }})

                if updated:    
                    site = mongo.getSiteWithOwner(site= siteID)   
                    return jsonify({"status":"updated","data": site})
                
    return jsonify({"status":"failed"})


@app.route('/api/site/request', methods=['POST'])  
@jwt_required()
@tryCatch(name="userRequest")
def userRequest():   
    if request.method == "POST": 
      
        data        = request.get_json()

        # GET USER ACCOUNT INFO
        accountID   = escape(data["account"])
        params      = data["data"]
        reqType     = escape(data["type"])
        account     = mongo.findUser(id= accountID)

        if account["role"] == "user":            
            espireAt    = datetime.now(timezone(timedelta(hours= timeOffset))) + timedelta(weeks=2) 
            query       = { "expireAt":espireAt,"id": f"REQ{token_hex(16)}","account": account,"reqtype":reqType,"type":"requests","data": params }

            if reqType in ["createsite","updatesite","deletesite","updateentity"]:
                entity   = mongo.findEntity(account['entity'],{"_id":0,"web":0,"device":0,"websubtopic":0,"devicesubtopic":0}) 
                query    = { "expireAt":espireAt,"id": f"REQ{token_hex(16)}","entity": entity,"account": account,"reqtype":reqType,"type":"requests","data": params }
 
            if reqType in ["createdevice","updatedevice","deletedevice"]:
                entity   = mongo.findEntity(account['entity'],{"_id":0,"web":0,"device":0,"websubtopic":0,"devicesubtopic":0}) 
                site     = mongo.findSite(id= params["siteid"],project={"_id":0,"devices":0})
                query    = { "expireAt":espireAt,"id": f"REQ{token_hex(16)}","entity": entity,"site": site,"account": account,"reqtype":reqType,"type":"requests","data": params }
            data.pop("type")            
            inserted    = mongo.createTempDoc(query)

            if inserted:
                # REQUEST SUBMITTED               
                return jsonify({"status":"submitted"})
                
    return jsonify({"status":"failed"})



@app.route('/api/update/device/dashboard', methods=['POST'])  
@jwt_required()
@tryCatch(name="updateDeviceDashboard")
def updateDeviceDashboard():   
    if request.method == "POST": 
      
        data        = request.get_json()
        # GET USER ACCOUNT INFO
        accountID   = str(escape(data["account"]))
        siteID      = str(escape(data["site"]))
        deviceID    = str(escape(data["device"]))
        # deviceID    = escape(data["dashboad"])
        account     = mongo.findUser(id= accountID)

        if account:
            siteToUpdate     = mongo.findSite(id= siteID) # Account to update

            if siteToUpdate:
                # UPDATE DEVICE                
                updated = mongo.updateSite({"id": siteID, "type": "site","devices.id": deviceID} ,{"$set": {"devices.$.dashboard": data["dashboard"]}})

                if updated:      
                    site = mongo.getSiteWithOwner(site= siteID) 
                    return jsonify({"status":"updated","data": site})
                
    return jsonify({"status":"failed"})



@app.route('/api/update/account', methods=['POST'])  
@jwt_required()
@tryCatch(name="updateAccounts")
def updateAccounts():   
    if request.method == "POST": 
      
        data        = request.get_json()
        # GET USER ACCOUNT INFO
        id          = escape(data["account"])
        user        = escape(data["id"])

        account     = mongo.findUser(id= id)
      
        if account["role"] == "admin":
            accountToUpdate     = mongo.findUser(id= user) # Account to update

            if accountToUpdate:
                data.pop("id")
                data.pop("account")

                # UPDATE MQTT ACLS FIRST                
                mode = 1
                if data["suball"]:
                    mode = 4

                updatedAcls = mongo.updateMqttUser({"owner": user, "type": "web","acls.type": "suball"} ,{"$set": { "acls.$.acc": mode}})

                updated = mongo.updateUser({"id": user} ,{"$set":data})

                if updated:       
                    return jsonify({"status":"updated"})
                
    return jsonify({"status":"failed"})

@app.route('/api/get/pagecount', methods=['POST'])  
@jwt_required()
@tryCatch(name="getPageCount")
def getPageCount():   
    if request.method == "POST": 
        form = request.form 
        # GET USER ACCOUNT INFO
        user        = str(escape(form.get("account")))
        ops         = str(escape(form.get("ops")))
        search      = str(escape(form.get("search")))
        account     = mongo.findUser(id= user)
 
        if account:    
            if ops == "search":        
                count = mongo.searchPaginationPageCount(searchtext= search,entity= account["entity"], role= account["role"])    
            else: 
                count = mongo.paginationPageCount(entity=account["entity"], role=account["role"])  
                
        if count >= 0:          
            return jsonify({"status":"ok","count": count})

    return jsonify({"status":"failed"})


@app.route('/api/get/entity/pagecount', methods=['POST'])  
@jwt_required()
@tryCatch(name="getPageCountEntity")
def getPageCountEntity():   
    if request.method == "POST": 
        form = request.form 
        # GET USER ACCOUNT INFO
        user        = escape(form.get("account"))
        ops         = escape(form.get("ops"))
        search      = escape(form.get("search"))
        account     = mongo.findUser(id= user)

        if account:    
            if ops == "search":        
                count = mongo.searchPaginationPageCountEntity(searchtext= search,entity= account["entity"], role= account["role"])    
            else:
                count = mongo.paginationPageCountEntity(entity= account["entity"], role= account["role"])
        
        if count >= 0:          
            return jsonify({"status":"ok","count": count})

    return jsonify({"status":"failed"})


@app.route('/api/search/user', methods=['POST'])  
@jwt_required()
@tryCatch(name="searchUser")
def searchUser():   
    if request.method == "POST": 
        form = request.form 
        # GET USER ACCOUNT INFO
        user        = escape(form.get("account")) 
        search      = escape(form.get("search"))
        account     = mongo.findUser(id= user)

        if account:    
            data = mongo.findAllUser(text= search)
            
            if data:          
                return jsonify({"status":"ok","data": data})

    return jsonify({"status":"failed"})


@app.route('/api/assign/user', methods=['POST'])  
@jwt_required()
@tryCatch(name="assignUser")
def assignUser():   
    if request.method == "POST": 
        form = request.form 
        # GET USER ACCOUNT INFO
        accountID   = escape(form.get("account")) 
        siteID      = escape(form.get("site"))
        userID      = escape(form.get("id"))
        account     = mongo.findUser(id= accountID)
        userAcc     = mongo.findUser(id= userID)
        exist, notice    = mongo.mqttUserExist(site = siteID) 

        if account and userAcc :    
            # ASSIGN
            data = mongo.updateSite({"id": siteID},{"$set":{"owner": userID}})
            if exist:
                mongo.updateMqttUser({"site": siteID, "type": "device","acls.type": "sub"}   ,{"$set": { "acls.$.topic": f"/station/msg/{userAcc['web']['username']}/#"}})
                mongo.updateMqttUser({"site": siteID, "type": "device","acls.type": "other"} ,{"$set": { "acls.$.topic": f"/station/msg/{userAcc['web']['username']}/#"}})
                mongo.updateMqttUser({"site": siteID, "type": "device","acls.type": "pub"}   ,{"$set": { "acls.$.topic": f"/station/data/{userAcc['web']['username']}/#"}})
            
            if data:          
                site = mongo.getSiteWithOwner(site= siteID)
            
                if site:
                    return jsonify({"status":"assigned","data": site })
                
        if account and userID == "":    
            # DEASSIGN
            data = mongo.updateSite({"id": siteID},{"$set":{"owner": userID}})
            if exist:
                mongo.updateMqttUser({"site": siteID, "type": "device","acls.type": "sub"}   ,{"$set": { "acls.$.topic": f"/station/msg/username/#"}})
                mongo.updateMqttUser({"site": siteID, "type": "device","acls.type": "other"} ,{"$set": { "acls.$.topic": f"/station/msg/username/#"}})
                mongo.updateMqttUser({"site": siteID, "type": "device","acls.type": "pub"}   ,{"$set": { "acls.$.topic": f"/station/data/username/#"}})
            
            if data:          
                site = mongo.getSiteWithOwner(site= siteID)
            
                if site:
                    return jsonify({"status":"assigned","data": site })

    return jsonify({"status":"failed"})

@app.route('/api/assign/user/entity', methods=['POST'])  
@jwt_required()
@tryCatch(name="assignUserToEntity")
def assignUserToEntity():   
    if request.method == "POST": 
        form = request.form 
        # GET USER ACCOUNT INFO
        accountID   = escape(form.get("account")) 
        userID      = escape(form.get("user"))
        entityID    = escape(form.get("entity"))

        account     = mongo.findUser(id= accountID)
        userAcc     = mongo.findUser(id= userID)
        
        if account["role"] == "admin" : 
            if userAcc :    
                # ASSIGN
                res = mongo.updateUser({"id": userID},{"$set":{"entity": entityID}})
                if res:
                    return jsonify({"status":"assigned","data": res })
                    
            if  userID == "":    
                # DEASSIGN
                res = mongo.updateUser({"id": userID},{"$set":{"entity": ""}})
                if res:
                    return jsonify({"status":"deassigned","data": res })
                
    return jsonify({"status":"failed"})


@app.route('/api/get/page', methods=['POST'])  
@jwt_required()
@tryCatch(name="getPage")
def getPage():   
    if request.method == "POST": 
        form = request.form 
        # GET USER ACCOUNT INFO
        
        user        = escape(form.get("account"))
        ops         = escape(form.get("ops"))
        search      = escape(form.get("search"))
        page        = int(escape(form.get("page")))
        account     = mongo.findUser(id= user)

        if account:
            if ops == "search":   
                data = mongo.getSearchPagination(searchtext= search,page= page, entity= account["entity"], role= account["role"])   
            else:
                data = mongo.paginationPage(page= page, entity= account["entity"], role= account["role"])   

            if len(data) >= 0:          
                return jsonify({"status":"ok","page": page,"data": data})
            return jsonify({"status":"ok","page": page,"data": []})

    return jsonify({"status":"failed"})


@app.route('/api/get/entity/page', methods=['POST'])  
@jwt_required()
@tryCatch(name="getPageEntity")
def getPageEntity():   
    if request.method == "POST": 
        form        = request.form 

        # GET USER ACCOUNT INFO        
        user        = escape(form.get("account"))
        ops         = escape(form.get("ops"))
        search      = escape(form.get("search"))
        page        = int(escape(form.get("page")))
        account     = mongo.findUser(id= user)

        if account:
            if ops == "search":   
                data = mongo.getSearchPaginationEntity(searchtext= search,page= page, entity= account["entity"], role= account["role"])   
            else:
                data = mongo.paginationPageEntity(page= page, entity= account["entity"], role= account["role"])   

            if len(data) >= 0:          
                return jsonify({"status":"ok","page": page,"data": data})

    return jsonify({"status":"failed"})

@app.route('/api/misc/emaillist', methods=['GET'])
@jwt_required()
@tryCatch(name="getEmailList")
def getEmailList():
    if request.method == "GET": 

        emails = mongo.miscFind({"id":"emails"}) 
        if emails:
            return jsonify({"status":"found","data":emails}) 
        else:
            emails = mongo.miscUpdate(query={"id":"emails"},update={"$set":{"registration":[],"cancellation":[]}})  
            return jsonify({"status":"created","data":emails})    
    return jsonify({"status":"none found"})    

@app.route('/api/misc/emaillist/update', methods=['POST'])
@jwt_required()
@tryCatch(name="emailListUpdate")
def emailListUpdate():
    if request.method == "POST": 
 
        form            = request.form
        firstname       = form.get("Firstname")  
        lastname        = form.get("Lastname")  
        email           = form.get("Email")  
        acc             = form.get("Account")   
        user            = form.get("User")  
        emailType       = form.get("Type")  

        # GET USER ACCOUNT INFO
        account = mongo.findUser(id=user) 

        if account:
            if account["role"] == "admin": # ONLY ADMIN ACCOUNTS ARE ALLOW TO CARRY OT THIS OPERATION
                emails = mongo.miscFind({"id":"emails"}) 
                # print(emails)
                if not emails:
                    emails = mongo.miscUpdate(query={"id":"emails"},update={"$set":{"registration":[],"cancellation":[]}})  

                data = emails[emailType]
                currentList = [x['account'] for x in emails[emailType]]  

                if acc in currentList:
                    return jsonify({"status":"already","data":None}) 
                
                updateList = [x for x in data if x['account'] != acc]
                updateList.append({"firstname":firstname,"lastname":lastname,"account":acc,"email":email})

                emails = mongo.miscUpdate(query={"id":"emails"},update={"$set":{emailType: updateList}})    
                updatedData = [x['account'] for x in emails[emailType]]            

                if acc in updatedData:
                    return jsonify({"status":"added","data":emails})     
    return jsonify({"status":"failed"})   
 

@app.route('/api/misc/emaillist/delete', methods=['POST'])
@jwt_required()
@tryCatch(name="emailListDeleteUpdate")
def emailListDeleteUpdate():
    if request.method == "POST": 
 
        form            = request.form    
        acc             = form.get("Account")   
        user            = form.get("User")  
        emailType       = form.get("Type")  

        # GET USER ACCOUNT INFO
        account = mongo.findUser(id=user) 

        if account:
            if account["role"] == "admin": # ONLY ADMIN ACCOUNTS ARE ALLOW TO CARRY OT THIS OPERATION
                emails = mongo.miscFind({"id":"emails"}) 
                # print(emails)
                if emails:
                    data = emails[emailType]
                    currentList = [x['account'] for x in emails[emailType]]  

                    if acc in currentList:
                    
                        updateList = [x for x in data if x['account'] != acc]

                        emails = mongo.miscUpdate(query={"id":"emails"},update={"$set":{emailType: updateList}})    
                        updatedData = [x['account'] for x in emails[emailType]]            

                        if acc not in updatedData:
                            return jsonify({"status":"deleted","data":emails})   
                          
    return jsonify({"status":"failed"})   

@app.route('/api/staff/all/<userID>', methods=['GET'])  
@jwt_required()
@tryCatch(name="getAllStaff")
def getAllStaff(userID):   
    # GET ALL STAFF ACCOUNT 
    if request.method == 'GET':
               
        account = mongo.findUser(id= userID)      

        if account: 
            # GET USER ACCOUNT INFO
            if account['role'] == 'admin':
                items = mongo.findAllStaff()                

                if items:
                    return jsonify({"status":"found","data":items})

    return jsonify({"status":"not found","data":None})

#####################
#     APP APIs      #
#####################
@app.route('/api/map/data/history', methods=['POST'])  
@jwt_required()
@tryCatch(name="getMapHistoryData")
def getMapHistoryData():   
    if request.method == "POST": 
        form = request.form
        params = ['temperature','humidity','pressure','voc','vocindex']

        # GET USER ACCOUNT INFO
        user        = escape(form.get("account"))
        account     = mongo.findUser(id= user)
        if account:
            id      = form.get("id")
            start   = int(form.get("start"))
            end     = int(form.get("end"))
            param   = form.get("param")
            # print("START", form)
            if param in params:
                endDate     = datetime.fromtimestamp(start)
                startDate   = endDate - timedelta(days= 30)
                result      = mongo.getMapHistoryData(id,startDate,endDate,param)
                three       = endDate - timedelta(days= 3) 
                seven       = endDate - timedelta(days= 7)
                if result:
                    return jsonify({"status":"found","three": three,"seven": seven,"data": result})

    return jsonify({"status":"failed"})


#########################
# INVENTORY PAGE ROUTES #
#########################


#########################
#  MODELS PAGE ROUTES   #
#########################


######################################
#           INVENTORY ROUTES         #
######################################



######################################
#             ORDER ROUTES           #
######################################



######################################
#             MISC  ROUTES           #
######################################


######################################
#           UTIL FUNCTIONS           #
######################################

def createEntityFromRequest(accountID,name, code, organization):   
 
    country     = ""
    account     = mongo.findUser(id= accountID)  # USER'S ACCOUNT

    try:
        country     = [x["name"] for x in caribbean_countries if x["code"] == code ][0]
    except:
        pass

    if account:
        exist, notice  = mongo.entityExist(name=name,organization=organization)
        
        if exist:
            return "exist"
        else:
            # CREATE ENTITY SINCE IT DOESNT ALREADY EXIST
            entity               = {"id": f"ENT{token_hex(16)}","name": name, "country": country, "organization": organization, "code": code} 
            entity["web"]        = {"username":token_hex(8),"password": token_hex(16)}
            entity["device"]     = {"username":token_hex(8),"password": token_hex(16)}
            entity["websubtopic"]       = f"/station/data/{name.replace(" ","").lower()}/#"
            entity["devicesubtopic"]    = f"/station/msg/{name.replace(" ","").lower()}/#"
            pwdWeb               = ph.hash(entity["web"]["password"])
            pwdDevice            = ph.hash(entity["device"]["password"])
        

            web                  = {} 
            web["id"]            = token_hex(16)
            web["username"]      = entity["web"]["username"]
            web["password"]      = pwdWeb
            web["type"]          = "web"
            web["superuser"]     = False
            web["owner"]         = entity["id"]
            web["acls"]          = [{"type":"main","topic": entity["websubtopic"],"acc":4},{"type":"other","topic": entity["websubtopic"],"acc":1}, {"type":"suball","topic":f"/station/data/#","acc":1},{"type":"other","topic":f"/station/data/#","acc":1}]
            
            device               = {}
            device["id"]         = token_hex(16)
            device["username"]   = entity["device"]["username"]
            device["password"]   = pwdDevice
            device["type"]       = "device"
            device["superuser"]  = False
            device["owner"]      = entity["id"]
            device["acls"]       = [{"type":"sub","topic": entity["devicesubtopic"],"acc":4},{"type":"other","topic": entity["devicesubtopic"],"acc":1},{"type":"pub","topic": entity["websubtopic"],"acc":2}]
            
            res = mongo.addEntity(entity)

            if res:
                mongo.addMqttUser(web.copy())
                mongo.addMqttUser(device.copy())
                updated = mongo.updateUser({"id": accountID} ,{"$set": {"entity": entity["id"]}})
                entities = mongo.findAllEntities({"_id":0})                
                return "created"
            
    return "failed"

def deleteEntityFromRequest(entityID ):    
    count = mongo.deleteEntity({"id": entityID})
    
    if count > 0: 
        count1 = mongo.removeMqttUser(entityID)
        count2 = mongo.deleteAllSite({"entity": entityID})        
        return "deleted"

    return "failed"

def updateEntityFromRequest(entityID,name, code, organization):   
    try:
        country     = [x["name"] for x in caribbean_countries if x["code"] == code ][0]
    except:
        pass
    else:                    
        updated = mongo.updateEntity({"id": entityID} ,{"$set": {"name": name,"country": country, "code": code, "organization": organization}})

        if updated:     
            return "updated"
                
    return "failed"

def addSite(name,lat,lon,entity):
    '''
    ACLs   meaning
        1 means read only, 
        2 means write only, 
        3 means readwrite and 
        4 means subscribe 
    '''
    siteID  = f"SITE{token_hex(16)}" 
    site    = {"type":"site","id": siteID,"name": name, "lat": lat, "lon": lon,"entity": entity, "radius": 200,"enabled": True, "devices":[]}

    exist, notice    = mongo.entityExist(id = entity)
    if exist:        
        inserted = mongo.addSite(site)
        if inserted and exist:                 
            return  "added"    
            
    return "failed"

def deleteSiteFromRequest(siteID):    
    count = mongo.deleteSite({"id": siteID})
    
    if count > 0: 
        return "deleted"

    return "failed"

def updateSiteFromRequest(siteID, name,lat,lon): 
    siteToUpdate     = mongo.findSite(id= siteID) # Account to update

    if siteToUpdate:
        # UPDATE SITE                
        updated = mongo.updateSite({"id": siteID, "type": "site"} ,{"$set": {"name": name,"lat": lat,"lon": lon }})

        if updated:    
            return "updated"
                
    return "failed"


def createDeviceFromRequest(siteID, data):
    siteToUpdate     = mongo.findSite(id= siteID) # Site to update

    if siteToUpdate: 
        data["id"]          = f"DEV{token_hex(16)}" 
        data["dashboard"]   = []
        data["lat"]         = float(data["lat"])
        data["lon"]         = float(data["lon"])

        # CREATE DEVICE              
        updated = mongo.updateSite({"id": siteID, "type": "site"} ,{"$push": { "devices": data}})

        if updated:      
            return "added"
        
    return "failed"

def updateDeviceFromRequest(siteID,deviceID, data):
    siteToUpdate     = mongo.findSite(id= siteID) # Account to update

    if siteToUpdate:
        # UPDATE DEVICE                
        updated = mongo.updateSite({"id": siteID, "type": "site","devices.id": deviceID} ,{"$set": { "devices.$.name": data["name"],"devices.$.lat": float(data["lat"]),"devices.$.lon": float(data["lon"]),"devices.$.processor": data["processor"],"devices.$.params": data["params"]}})

        if updated:      
            return "updated"
                
    return "failed"

def deleteDeviceFromRequest(siteID,deviceID):   
    data = mongo.updateSite({"id": siteID,"devices.id": deviceID},{"$pull": {"devices" : { "id": deviceID }}})
    
    if deviceID not in [x["id"] for x in data["devices"]]:
        return  "deleted" 

    return  "failed" 


@app.route('/api/qrcode/<image_id>', methods=['GET'])  
@jwt_required()
@tryCatch(name="getCode")
def getCode(image_id):   
    if request.method == "GET": 
        path    = mongo.getCode(image_id)
        path    = join(getcwd(),Config.QRCODE_FOLDER)   
        return send_from_directory( path ,image_id)
 
    return jsonify({"status":"none found"})

@app.route('/api/qrcode/batch', methods=['POST'])  
#@jwt_required()
@tryCatch(name="getBatchCode")
def getBatchCode():   
    if request.method == "POST":
 
        data = request.get_json()
        format = data['type']
        product = data['product']
        names = data['codes']
        if format == "pdf":
            filename  = mongo.getBatchCodePDF(product,names)
        elif format == 'csv':
            filename  = mongo.getBatchCodeCSV(product,names)

        path      = join(getcwd(),Config.QRCODE_TEMP_FOLDER)   
        return send_from_directory( path ,filename)
    return jsonify({"status":"none found"})



@app.route('/api/account') 
@jwt_required(fresh=True)
@tryCatch(name="account")
def account():
    username = get_jwt_identity()
    # very important account settings //
    return jsonify({"Notice":"Account page","user":username})


@app.route('/api/service', methods=['GET']) 
@jwt_required()
@tryCatch(name="services")
def services():
    username = get_jwt_identity()
    # Not important stuff but still needs to be logged in //
    return jsonify({"Notice":"Service page","user":username})


@app.route('/api/images/<image_id>', methods=['GET']) 
@jwt_required(optional=True)
@tryCatch(name="get_images")
def get_images(image_id):   
    if request.method == "GET":
        path = join( getcwd(),Config.IMAGE_FOLDER) 
        return send_from_directory( path,image_id )


@app.route('/api/images/decode/<image_id>', methods=['GET']) 
@jwt_required()
@tryCatch(name="get_decoded_images")
def get_decoded_images(image_id):   
    if request.method == "GET":
        path = join( getcwd(),Config.UPLOAD_FOLDER)
        print(path,"/",image_id)
        return send_from_directory( path,image_id )


@app.route('/api/decode',methods=["POST"]) 
@tryCatch(name="decoder")
def decoder():
    form = request.form
    if request.method == "POST":  
        photo = form.get("photo")
        filename = f"{floor(time())}_{secure_filename(photo.filename)}"
        photo.save(join(Config.UPLOAD_FOLDER , filename))
        res = mongo.BarcodeReader(filename)
        # returnPath = join(getcwd(),Config.UPLOAD_FOLDER)
        return jsonify(res) 

        

@app.route('/api/upload',methods=["POST"]) 
@tryCatch(name="upload")
def upload():
    form = request.form

    if request.method == "POST": 
        photo = form.get("photo")
        description = form.get("description")
        filename = secure_filename(photo.filename)
        photo.save(join(getcwd(),Config.IMAGE_FOLDER , filename))
        return jsonify({"message":"File upload successful", "filename":f"{filename}", "description":f"{description}" })
    


@app.route('/api/upload/rmbkgrnd',methods=["POST"]) 
@tryCatch(name="upload_remove_background")
def upload_remove_background():
    '''REMOVE BACKGROUND AND THEN SAVE IMAGE'''
   
    if request.method == "POST": 
        file = request.files.getlist("Photo")[0]          
        photo = file.read()  
        # description = form.get("description")
        filename = secure_filename(file.filename)
 
        result = remove(photo) # Remove background  
        # out.save(join(getcwd(),Config.IMAGE_FOLDER, f"{id}{count}.webp") , format="webp")   
        result_image = Image.open(BytesIO(result)).convert("RGBA") # Convert result to image    
        # result_image.save(join(getcwd(),Config.UPLOAD_FOLDER , f"{filename.split('.')[0]}.png")) # Save result image
        result_image.save(join(getcwd(),Config.UPLOAD_FOLDER , f"{filename.split('.')[0]}.webp") , format="webp") # Save result image
        return jsonify({"message":"File upload successful", "filename": f"{filename}", "description":f"{'description'}" })
 

@app.route('/api/csrf-token', methods=['GET']) 
@tryCatch(name="get_csrf")
def get_csrf(): 
    response        = make_response({'message': "Tokenized"})
    response.set_cookie('csrf_token_custom', generate_csrf(),httponly = False, secure = True)
    return response




###
# The functions below should be applicable to all Flask apps.
###

# Here we define a function to collect form errors from Flask-WTF
# which we can later use
def form_errors(form):
    error_messages = []
    """Collects form errors"""
    for field, errors in form.errors.items():
        for error in errors:
            message = u"%s field is required" % (getattr(form, field).label.text)
            error_messages.append(message)

    return error_messages

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also tell the browser not to cache the rendered page. If we wanted
    to we could change max-age to 600 seconds which would be 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


# @app.before_request
# def include_headers(): 
#     # request.headers.set('X-User','internal' ) 
#     # request.headers['X-User'] = 'internal'
#     print(request.headers)
#     # return request



 


# @app.errorhandler(404)
# def page_not_found(error):
#     """Custom 404 page."""    
#     return render_template('404.html'), 404



@app.errorhandler(405)
def page_not_found(error):
    """Custom 404 page."""    
    return jsonify({"status":"404","data":"404"})   , 404


if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0",port="8080")
