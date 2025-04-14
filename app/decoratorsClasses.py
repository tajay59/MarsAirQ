
class CheckForm:

    # IMPORT
    # INFO ON DECORATORS
    # Python Decorators Tutorial,  https://www.datacamp.com/tutorial/decorators-python?utm_source=google&utm_medium=paid_search&utm_campaignid=19589720824&utm_adgroupid=143216588537&utm_device=c&utm_keyword=&utm_matchtype=&utm_network=g&utm_adpostion=&utm_creative=675429089965&utm_targetid=dsa-1947282172981&utm_loc_interest_ms=&utm_loc_physical_ms=9070109&utm_content=dsa~page~community-tuto&utm_campaign=230119_1-sea~dsa~tofu-tutorials_2-b2c_3-row-p2_4-prc_5-na_6-na_7-le_8-pdsh-go_9-na_10-na_11-na-oct23odp&gclid=EAIaIQobChMIuqHlyojagQMVMwR9Ch2YPA6sEAAYASAAEgK0ZvD_BwE
    # Primer on Python Decorators, https://realpython.com/primer-on-python-decorators/
    # View Decorators, https://flask.palletsprojects.com/en/3.0.x/patterns/viewdecorators/

    def __init__(self, Logger):
        
        from json import loads, dumps
        from time import time, sleep, localtime, ctime 
        from os import system, getcwd, path, listdir 
        from os.path import join 
        import urllib.request as request 
        from collections import defaultdict
        from math import floor
        from datetime import datetime
        from functools import wraps
        from re import   match
        import logging
        from flask import render_template, request, jsonify
        from markupsafe import escape

        self.datetime           = datetime
        self.request            = request 
        self.time 			    = time
        self.localtime          = localtime
        self.ctime 			    = ctime
        self.sleep 			    = sleep 
        self.system             = system
        self.getcwd             = getcwd
        self.path 			    = path 
        self.listdir 		    = listdir  
        self.floor              = floor        
        self.loads              = loads
        self.dumps 		        = dumps
        self.join               = join
        self.defaultdict        = defaultdict
        self.wraps              = wraps
        self.match              = match
        self.escape             = escape
        self.jsonify            = jsonify
        self.logger             = Logger

        '''
        self.logging            = logging
        self.logger             = logging.getLogger(__name__)


        # SETTINGS
        # https://realpython.com/python-logging/
        # https://docs.python.org/3/library/logging.html#logrecord-attributes
        # self.logging.basicConfig(level=self.logging.DEBUG,filename="app/log/sia_logs.csv",encoding="utf-8",filemode="a",format="{asctime},{process},{levelname},{name},{message},{exc_info}", style="{", datefmt="%Y-%m-%d %H:%M")
        
        self.console_handler    = logging.StreamHandler()
        self.file_handler       = logging.FileHandler(filename="app/log/sia_logs.csv",encoding="utf-8",mode="a")
        self.formatter          = self.logging.Formatter( "{asctime},{process},{levelname},{name},{message},{exc_info}", style="{",datefmt="%Y-%m-%d %H:%M" )

        
        self.console_handler.setFormatter(self.formatter)        
        self.file_handler.setFormatter(self.formatter)
        self.console_handler.setLevel("DEBUG")
        self.file_handler.setLevel("WARNING")
        self.logger.addHandler(self.console_handler)
        self.logger.addHandler(self.file_handler)
        '''
        

        

    def tryCatch(self,name=""):
        def innerDecorator(f):            
            @self.wraps(f)
            def wrapper(*args,**kwargs):                  
                try:                    
                    output = f(*args,**kwargs)                  
                except Exception as e:
                    # print(f" {name} error: ",str(e))
                    self.logger.warning(f" {name}() error: {str(e)}")
                    return self.jsonify({"status":"Are you a bot"})
                else:
                    return output
                    
            return wrapper
        return innerDecorator
    


    # DECORATORS....DECORATORS ARE APPLIED BOTTOM UP
    def addproduct(self,f):
        @self.wraps(f)
        def wrapper(*args,**kwargs):        
            try:                
                form = self.request.form
                params = list(form) 
                # print(params)
              
                if params == ['Type','Project', 'Department','Name', 'Make', 'ModelName', 'ModelNumber', 'Sn', 'Sn1', 'Description', 'Detail', 'UnitQuantity', 'Cost', 'Threshold','Weight','Account','Barcode']:  # ENSURES ALL THE REQUIRED FIELD NAMES EXIST IN FORM                
                    name                = bool( self.match( R'^[A-Za-z0-9\s-]+$', self.escape(form.get("Name")) ))  
                    make                = bool( self.match( R'^[A-Za-z0-9\s-]+$', self.escape(form.get("Make")) ))  
                    modelname           = bool( self.match( R'^[A-Za-z0-9\s-]+$', self.escape(form.get("ModelName")) ))  
                    modelnumber         = bool( self.match( R'^[A-Za-z0-9\s-]+$', self.escape(form.get("ModelNumber")) ))  
                    Sn                  = bool( self.match( R'^[A-Za-z0-9,-.\s]+$', self.escape(form.get("Sn")) ))  
                    Sn1                 = bool( self.match( R'^[A-Za-z0-9,-.\s]*$', self.escape(form.get("Sn1")) ))  # * means field can also be empty
                    description         = bool( self.match( R'^[A-Za-z0-9,.\s]+$', self.escape(form.get("Description")) ))  
                    detail              = bool( self.match( R'^[A-Za-z0-9\s]*$', self.escape(form.get("Detail")) ))  
                    type                = bool( self.match( R'^[A-Za-z]+$', self.escape(form.get("Type") ) ))      
                    unit                = bool( self.match( R'^[0-9]+$', self.escape(form.get("UnitQuantity") ) ))  
                    cost                = bool( self.match( R'^[+]?([0-9]*[.])?[0-9]+$', self.escape(form.get("Cost") ) ))  
                    threshold           = bool( self.match( R'^[0-9]+$', self.escape(form.get("Threshold") ) ))  
                    weight              = bool( self.match( R'^[+]?([0-9]*[.])?[0-9]+$', self.escape(form.get("Weight") ) ))  
                    project             = bool( self.match( R'^[A-Za-z0-9,.\s]*$', self.escape(form.get("Project")) )) 
                    department          = bool( self.match( R'^[A-Za-z0-9]+$', self.escape(form.get("Department")) ))  
                    account             = bool( self.match( R'^[A-Za-z0-9\s]+$', self.escape(form.get("Account")) ))    
                    barcode             = bool( self.match( R'^[A-Za-z0-9\s_]*$', self.escape(form.get("Barcode")) ))  
                    
                   
                   
                    result =  [name,Sn,description,detail,unit,cost,threshold,weight,department,type]
                    # print("PROJECT: ",result)

                    if not (False in result):
                        return f(*args,**kwargs)
            
                return self.jsonify({"status":"formErrors"})
            except Exception as e:
                print("addproduct decorator exception: ",str(e))
                return self.jsonify({"status":"Are you a bot"})
        return wrapper
    
    
    def createsite(self,f):
        @self.wraps(f)
        def wrapper(*args,**kwargs):        
            try:                
                form = self.request.form
                params = list(form)
                print(params)
                if params == ['Name', 'Address', 'Country']:  # ENSURES ALL THE REQUIRED FIELD NAMES EXIST IN FORM      ,'Site'           
                    name                = bool( self.match( R'^[A-Za-z]+$', self.escape(form.get("Name")) ))  
                    address             = bool( self.match( R'^[A-Za-z0-9,.\s]*$', self.escape(form.get("Address")) )) 
                    country             = bool( self.match( R'^[A-Za-z\s]+$', self.escape(form.get("Country")) )) 
                    # site                = bool( self.match( R'^[A-Za-z0-9\s]+$', self.escape(form.get("Site") ) )) 
 
                    result =  [name,address,country] # ,site

                    if not (False in result):
                        return f(*args,**kwargs)
            
                return self.jsonify({"status":"formErrors"})
            except Exception as e:
                print("createsite decorator exception: ",str(e))
                return self.jsonify({"status":"Are you a bot"})
        return wrapper

      
    def newlocation(self,f):
        @self.wraps(f)
        def wrapper(*args,**kwargs):        
            try:              
                form = self.request.form
                params = list(form)
                if params == ['Site']:  # ENSURES ALL THE REQUIRED FIELD NAMES EXIST IN FORM          
                    site                = bool( self.match( R'^[A-Za-z0-9]+$', self.escape(form.get("Site") ) )) 
 
                    result =  [site]

                    if not (False in result):
                        return f(*args,**kwargs)
            
                return self.jsonify({"status":"formErrors"})
            except Exception as e:
                print("newlocation decorator exception: ",str(e))
                return "Are you a bot"
        return wrapper
    
    def newshelf(self,f):
        @self.wraps(f)
        def wrapper(*args,**kwargs):        
            try:            
               
                form = self.request.form
                params = list(form)
                if params == ['Site','Location']:  # ENSURES ALL THE REQUIRED FIELD NAMES EXIST IN FORM          
                    site                = bool( self.match( R'^[A-Za-z0-9]+$', self.escape(form.get("Site") ) )) 
                    location            = bool( self.match( R'^[A-Za-z0-9]+$', self.escape(form.get("Location") ) )) 
 
                    result =  [site,location]

                    if not (False in result):
                        return f(*args,**kwargs)
            
                return self.jsonify({"status":"formErrors"})
            except Exception as e:
                print("newshelf decorator exception: ",str(e))
                return self.jsonify({"status":"Are you a bot"})
        return wrapper 

    
    def shelfstocks(self,f):
        @self.wraps(f)
        def wrapper(*args,**kwargs):        
            try:            
               
                form = self.request.form
                params = list(form)
                if params == ['Shelf']:  # ENSURES ALL THE REQUIRED FIELD NAMES EXIST IN FORM          
                    shelf                = bool( self.match( R'^[A-Za-z0-9]+$', self.escape(form.get("Shelf") ) ))                    
 
                    result =  [shelf]

                    if not (False in result):
                        return f(*args,**kwargs)
            
                return self.jsonify({"status":"formErrors"})
            except Exception as e:
                print("shelfstocks decorator exception: ",str(e))
                return self.jsonify({"status":"Are you a bot"})
        return wrapper  
    

    def pickProduct(self,f):
        @self.wraps(f)
        def wrapper(*args,**kwargs):        
            try:                
                form = self.request.form
                params = list(form)
                # print(params)
                if params == ['User', 'ProductBarcode', 'Order', 'Reason']:  # ENSURES ALL THE REQUIRED FIELD NAMES EXIST IN FORM      ,'Site'           
                    user                = bool( self.match( R'^[A-Za-z0-9]+$', self.escape(form.get("User")) ))  
                    barcode             = bool( self.match( R'^[A-Za-z0-9_]+$', self.escape(form.get("ProductBarcode")) )) 
                    order               = bool( self.match( R'^[A-Za-z0-9]*$', self.escape(form.get("Order")) ))  
                    reason              = bool( self.match( R'^[A-Za-z0-9.,\s]+$', self.escape(form.get("Reason")) ))  
 
                    result =  [user,barcode,order, reason] # ,site
                    # print(result)
                    if not (False in result): 
                        return f(*args,**kwargs) 
                return self.jsonify({"status":"formErrors"})
            except Exception as e:
                print("pickProduct decorator exception: ",str(e))
                return self.jsonify({"status":"Are you a bot"})
        return wrapper

    def stowProduct(self,f):
        @self.wraps(f)
        def wrapper(*args,**kwargs):        
            try:                
                form = self.request.form
                params = list(form)
                print(params)
                if params == ['User', 'Shelf','ProductBarcode', 'Order']:  # ENSURES ALL THE REQUIRED FIELD NAMES EXIST IN FORM      ,'Site'           
                    user                = bool( self.match( R'^[A-Za-z0-9]+$', self.escape(form.get("User")) ))  
                    shelf               = bool( self.match( R'^[A-Za-z0-9]+$', self.escape(form.get("Shelf")) )) 
                    barcode             = bool( self.match( R'^[A-Za-z0-9_]+$', self.escape(form.get("ProductBarcode")) )) 
                    order               = bool( self.match( R'^[A-Za-z0-9]*$', self.escape(form.get("Order")) ))  
 
                    result =  [user,shelf,barcode,order] # ,site

                    if not (False in result):
                        return f(*args,**kwargs)
            
                return self.jsonify({"status":"formErrors"})
            except Exception as e:
                print("stowProduct decorator exception: ",str(e))
                return self.jsonify({"status":"Are you a bot"})
        return wrapper
    

    def orderPick(self,f):
        @self.wraps(f)
        def wrapper(*args,**kwargs):        
            try:                
                form = self.request.form
                params = list(form)
                print("Recieved ",params)
                if params == ['User', 'ProductBarcode', 'Order']:  # ENSURES ALL THE REQUIRED FIELD NAMES EXIST IN FORM      ,'Site'           
                    user                = bool( self.match( R'^[A-Za-z0-9]+$', self.escape(form.get("User")) ))  
                    barcode             = bool( self.match( R'^[A-Za-z0-9_]+$', self.escape(form.get("ProductBarcode")) )) 
                    order               = bool( self.match( R'^[A-Za-z0-9]*$', self.escape(form.get("Order")) ))  
                    
 
                    result =  [user,barcode,order] # ,site

                    if not (False in result):
                        return f(*args,**kwargs)
            
                return self.jsonify({"status":"formErrors"})
            except Exception as e:
                print("orderPick decorator exception: ",str(e))
                return self.jsonify({"status":"failed","user":"404 - bot vybz","date":"","data": {} })
        return wrapper
    
    def updateOrderShipping(self,f):
        @self.wraps(f)
        def wrapper(*args,**kwargs):        
   
            try:                
                form = self.request.form 
                params = list(form)
                # print("params",params)
                if params == ['User','Order','Date','Method','Tracking','SendEmailClient']:  # ENSURES ALL THE REQUIRED FIELD NAMES EXIST IN FORM            
                    user                = bool( self.match( R'^[A-Za-z0-9]+$', self.escape(form.get("User")) ))   
                    order               = bool( self.match( R'^[A-Za-z0-9]+$', self.escape(form.get("Order")) ))  
                    date                = bool( self.match( R'^[0-9]+$', self.escape(form.get("Date")) ))  
                    method              = bool( self.match( R'^[A-Za-z0-9\s]+$', self.escape(form.get("Method")) ))  
                    tracking            = bool( self.match( R'^[A-Za-z0-9]+$', self.escape(form.get("Tracking")) ))  
 
                    result =  [user,order,date,method,tracking] # ,site
                    # print(result)
                    if not (False in result):
                        return f(*args,**kwargs)
            
                return self.jsonify({"status":"formErrors","data":{}})
            except Exception as e:
                print("updateOrderShipping decorator exception: ",str(e))
                return self.jsonify({"status":"failed", "data": {}})
        return wrapper
    
    def updateOrderInvoice(self,f):
        @self.wraps(f)
        def wrapper(*args,**kwargs):        
   
            try:                
                form = self.request.form 
                params = list(form)
                # print("params",params)
                if params == ['User','Order','Invoice','Invoice1','Cost','Cost1','SendEmailClient','SendEmailStaff']:  # ENSURES ALL THE REQUIRED FIELD NAMES EXIST IN FORM            
                    user                = bool( self.match( R'^[A-Za-z0-9]+$', self.escape(form.get("User")) ))   
                    order               = bool( self.match( R'^[A-Za-z0-9]+$', self.escape(form.get("Order")) ))  
                    cost                = bool( self.match( R'^[+]?([0-9]*[.])?[0-9]+$', self.escape(form.get("Cost")) ))  
                    cost1               = bool( self.match( R'^[+]?([0-9]*[.])?[0-9]+$', self.escape(form.get("Cost1")) )) 
                    invoice             = bool( self.match( R'^[A-Za-z0-9\s]*$', self.escape(form.get("Invoice")) ))   
                    invoice1            = bool( self.match( R'^[A-Za-z0-9\s]*$', self.escape(form.get("Invoice1")) ))  
 
                    result =  [user,order,cost,cost1,invoice, invoice1] # ,site
                    # print(result)
                    if not (False in result):
                        return f(*args,**kwargs)
            
                return self.jsonify({"status":"formErrors","data":{}})
            except Exception as e:
                print("updateOrderInvoice decorator exception: ",str(e))
                return self.jsonify({"status":"failed", "data": {}})
        return wrapper
    
    def updateOrderCommercialInvoice(self,f):
        @self.wraps(f)
        def wrapper(*args,**kwargs):        
   
            try:                
                form = self.request.form 
                params = list(form)
                # print("params",params)
                if params == ['User','Order','Invoice3','Invoice4','SendEmailClient','SendEmailStaff']:  # ENSURES ALL THE REQUIRED FIELD NAMES EXIST IN FORM            
                    user                = bool( self.match( R'^[A-Za-z0-9]+$', self.escape(form.get("User")) ))   
                    order               = bool( self.match( R'^[A-Za-z0-9]+$', self.escape(form.get("Order")) ))   
                    invoice             = bool( self.match( R'^[A-Za-z0-9\s]*$', self.escape(form.get("Invoice3")) ))   
                    invoice1            = bool( self.match( R'^[A-Za-z0-9\s]*$', self.escape(form.get("Invoice4")) ))  
 
                    result =  [user,order, invoice, invoice1] # ,site
                    # print(result)
                    if not (False in result):
                        return f(*args,**kwargs)
            
                return self.jsonify({"status":"formErrors","data":{}})
            except Exception as e:
                print("updateOrderCommercialInvoice decorator exception: ",str(e))
                return self.jsonify({"status":"failed", "data": {}})
        return wrapper
    

    def addproject(self,f):
        @self.wraps(f)
        def wrapper(*args,**kwargs):        
            try:                
                form = self.request.form
                params = list(form) 
                # print(params)
                if params == [ 'Name',  'Description', 'User', 'Barcode']:  # ENSURES ALL THE REQUIRED FIELD NAMES EXIST IN FORM                
                    name                = bool( self.match( R'^[A-Za-z0-9\s-]+$', self.escape(form.get("Name")) ))   
                    description         = bool( self.match( R'^[A-Za-z0-9,.\s\(\)]+$', self.escape(form.get("Description")) )) 
                    account             = bool( self.match( R'^[A-Za-z0-9\s-]+$', self.escape(form.get("User")) ))        
                    barcode             = bool( self.match( R'^[A-Za-z0-9\s-]*$', self.escape(form.get("Barcode")) ))             
                   
 
                    result =  [name, description, account, barcode]
                    # print("NON PROJECT: ",result)

                    if not (False in result):
                        return f(*args,**kwargs)
                    
                return self.jsonify({"status":"formErrors"})
            except Exception as e:
                print("addproject decorator exception: ",str(e))
                return self.jsonify({"status":"Are you a bot"})
        return wrapper
    
    def assignItem(self,f):
        @self.wraps(f)
        def wrapper(*args,**kwargs):        
            try:                
                form = self.request.form
                params = list(form)
                print(params)
                if params == ['User', 'ProductBarcode']:  # ENSURES ALL THE REQUIRED FIELD NAMES EXIST IN FORM      ,'Site'           
                    user                = bool( self.match( R'^[A-Za-z0-9]+$', self.escape(form.get("User")) ))                     
                    barcode             = bool( self.match( R'^[A-Za-z0-9_]+$', self.escape(form.get("ProductBarcode")) ))                     
 
                    result =  [user,barcode]  

                    if not (False in result):
                        return f(*args,**kwargs)
            
                return self.jsonify({"status":"formErrors"})
            except Exception as e:
                print("assignItem decorator exception: ",str(e))
                return self.jsonify({"status":"Are you a bot"})
        return wrapper
    

