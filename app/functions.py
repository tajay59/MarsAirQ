 #!/usr/bin/python3


#################################################################################################################################################
#                                                    CLASSES CONTAINING ALL THE APP FUNCTIONS                                                                                                    #
#################################################################################################################################################


class JWTtoDict: 

    def __init__(self,payload: dict):

        # Imports
        from json import loads, dumps

        self.dumps          = dumps
        self.loads          = loads


        # Variables
        if type(payload["sub"]) == str :
            self.token           = payload 
            self.token["sub"]    = loads(payload["sub"])            
        else :
            self.token           = payload 
             

    def getToken(self) -> dict:
        return self.token
    
    def getSubStr(self) -> str:
        return self.dumps(self.token["sub"])
    
    def __del__(self):
         # Delete class instance to free resources
         pass


from functools import wraps


class DB:

    def __init__(self,Config, Logger):

        from functools import wraps
        from time import sleep, time, localtime, ctime, mktime 
        from math import floor, ceil
        from os import getcwd, makedirs, listdir, remove
        from os.path import join, exists
        from io import BytesIO
        from requests import get
        from json import loads, dumps, dump
        from datetime import timedelta, datetime, timezone
        import pytz
        from flask import  jsonify
        from pymongo import MongoClient , errors, ReturnDocument
        from urllib import parse
        from urllib.request import  urlopen 
        from random import randint 
        from pandas import DataFrame,  to_datetime, concat, Grouper, to_numeric
        from numpy import nan, max, min, sum , mean, int64, array_split, log 
        from secrets import token_hex
        import sqlite3 as sql
        from itertools import islice
        from bson.objectid import ObjectId
        from bson.codec_options import CodecOptions
        import cv2 
        from pyzbar.pyzbar import decode
        import pyqrcode
        import png
        from collections import defaultdict
        from reportlab.lib.pagesizes import letter
        from reportlab.pdfgen import canvas
        from PIL import Image
        from glob import glob
        import csv
        

        self.glob                           = glob
        self.csv                            = csv
        self.letter                         = letter
        self.canvas                         = canvas
        self.Image                          = Image
        self.defaultdict                    = defaultdict
        self.Config                         = Config
        self.randint                    	= randint 
        self.sql                            = sql
        self.token_hex                      = token_hex
        self.getcwd                         = getcwd
        self.makedirs                       = makedirs
        self.listdir                        = listdir
        self.remove                         = remove
        self.get                            = get
        self.join                           = join 
        self.sleep                      	= sleep
        self.time                       	= time
        self.DataFrame                  	= DataFrame 
        self.localtime                  	= localtime
        self.ctime                      	= ctime
        self.mktime                     	= mktime
        self.floor                      	= floor 
        self.ceil                           = ceil
        self.to_datetime                	= to_datetime
        self.to_numeric                     = to_numeric
        self.Grouper                        = Grouper
        self.concat                         = concat
        self.bardecoder                     = decode
        self.cv                             = cv2
        self.nan                        	= nan
        self.max                        	= max
        self.min                        	= min
        self.sum                       	    = sum
        self.int64                      	= int64
        self.mean                       	= mean
        self.log                        	= log
        self.loads                      	= loads
        self.dumps                      	= dumps
        self.dump                       	= dump
        self.jsonify                        = jsonify
        self.islice                         = islice
        self.ObjectId                       = ObjectId
        self.CodecOptions                   = CodecOptions( tz_aware=True, tzinfo= pytz.timezone('America/Barbados'))
        self.request                    	= urlopen
        self.array_split                	= array_split
        self.pyqrcode                       = pyqrcode
        self.png                            = png
        self.BytesIO                        = BytesIO
        self.wraps                          = wraps
        self.exists                         = exists
        self.timedelta                  	= timedelta
        self.datetime                       = datetime
        self.timezone                       = timezone
        self.pytz                           = pytz
        self.logger                         = Logger
        self.server			                = Config.DB_SERVER
        self.port			                = Config.DB_PORT
        self.username                   	= parse.quote_plus(Config.DB_USERNAME)
        self.password                   	= parse.quote_plus(Config.DB_PASSWORD)
        self.remoteMongo                	= MongoClient
        self.ReturnDocument                 = ReturnDocument
        self.PyMongoError               	= errors.PyMongoError
        self.BulkWriteError             	= errors.BulkWriteError 
        self.DESCENDING                 	= 1
        self.ASCENDING                  	= -1  
        self.tls                            = False # MUST SET TO TRUE IN PRODUCTION


    def __del__(self):
            # Delete class instance to free resources
            pass
    
    def Print(self, message):
        print(message)

    def testConnection(self):
        # TEST CONNECTION TO MONGODB DATABASE
        self.Print("TESTING CONNECTION TO REMOTE DATABASE ")
        print(self.username, self.password,self.server,self.port)
        result 	= False
        try:
            #The ismaster command is cheap and does not require auth.
            remotedb 	= self.remoteMongo('mongodb://%s:%s@%s:%s' % (self.username, self.password,self.server,self.port), tls=self.tls ) 
            result      = remotedb.server_info()
            # print(result)

        except  self.PyMongoError as e:
            message 	= "UNABLE TO CONNECT TO REMOTE DATABASE ,ERROR CODE : {error} \n EXITING \n".format( error = str(e))
        else:
            self.Print("CONNECTED TO REMOTE SERVER \n")
            #self.Print(str(result))
            result 		= True
        finally:
            pass

        return result
    
    def downloadSampleImages(self):
        # Create a directory to save the downloaded images
        if not self.exists('productImages'):
            self.makedirs('productImages')

        # Number of images to download
        num_images = 50000

        for i in range(num_images):
            response = self.get(f'https://picsum.photos/800/600?random={i}', stream=True)
            if response.status_code == 200:
                image_path = f'productImages/image_{i}.jpg'
                with open(image_path, 'wb') as file:
                    for chunk in response.iter_content(chunk_size=1024):
                        file.write(chunk)
                print(f"Downloaded {image_path}")
            else:
                print(f"Error downloading image {i}: Status code {response.status_code}")


    def chunk(self,it, size):
        it = iter(it)
        return iter(lambda: tuple(self.islice(it, size)), ())
    

    def getCode(self, data):
        url = self.pyqrcode.create(data.split(".")[0])

        path = self.join(self.getcwd(),self.Config.QRCODE_FOLDER,data) 
        url.png(path, scale=15)
        # in-memory stream is also supported
        # buffer = self.BytesIO()
        # url.svg(buffer, title = "one.png")
        # do whatever you want with buffer.getvalue()
        # print(list(buffer.getvalue()))
        return path
    
    def getBatchCodePDF(self, product, codes):
        path    = self.join(self.getcwd(),self.Config.QRCODE_TEMP_FOLDER) 
        files   = self.listdir(path)

        # Delete existing files
        for file in files:
            self.remove(self.join(self.getcwd(),self.Config.QRCODE_TEMP_FOLDER,file))

        # Define constants
        num_rows        = 5
        num_cols        = 4
        image_width     = 150
        image_height    = 150
        spacing         = 1 
        
        # Create a new PDF file
        c = self.canvas.Canvas(self.join(self.getcwd(),self.Config.QRCODE_TEMP_FOLDER,"output.pdf") , pagesize= self.letter)
        
        # Calculate grid dimensions
        total_width = (num_cols * image_width) + ((num_cols - 1) * spacing)
        total_height = (num_rows * image_height) + ((num_rows - 1) * spacing)
        
        # Calculate starting positions
        start_x = (self.letter[0] - total_width) / 2
        start_y = (self.letter[1] - total_height) / 2
         
        for code in codes:
            name    = f"{product}_{code}"
            url     = self.pyqrcode.create(name)
            path    = self.join(self.getcwd(),self.Config.QRCODE_TEMP_FOLDER,f"{name}.png") 
            url.png(path, scale=5, module_color=[0, 0, 0, 128])

         
        # Get list of images
        path     = self.join(self.getcwd(),self.Config.QRCODE_TEMP_FOLDER) 
        images   = self.listdir(path)
         
        # Draw images on the canvas
        for i, file in enumerate(images):
            row = i // num_cols
            col = i % num_cols
            x = start_x + col * (image_width + spacing)
            y = start_y + row * (image_height + spacing)
            
            # Draw the image
            image_path    = self.join(self.getcwd(),self.Config.QRCODE_TEMP_FOLDER,file) 
            image = self.Image.open(image_path)
            c.drawImage(image_path, x, y, width=image_width, height=image_height)

         
        # Save the PDF
        c.save()

        #path = self.join(self.getcwd(),self.Config.QRCODE_FOLDER,"output.pdf")

        # in-memory stream is also supported
        # buffer = self.BytesIO()
        # url.svg(buffer, title = "one.png")
        # do whatever you want with buffer.getvalue()
        # print(list(buffer.getvalue()))
        return "output.pdf"


    def getBatchCodeCSV(self, product, codes):
        path    = self.join(self.getcwd(),self.Config.QRCODE_TEMP_FOLDER) 
        files   = self.listdir(path)

        # Delete existing files
        for file in files:
            self.remove(self.join(self.getcwd(),self.Config.QRCODE_TEMP_FOLDER,file))

        path = self.join(self.getcwd(),self.Config.QRCODE_TEMP_FOLDER,'labels.csv') 

        with open(path, 'w', newline='') as csvfile:
            spamwriter = self.csv.writer(csvfile, delimiter=',',quotechar='|', quoting= self.csv.QUOTE_MINIMAL)
            spamwriter.writerow(['Product','Serial'])
            for code in codes:
                spamwriter.writerow([f"{product}_{code}",f"{code.upper()}"]) 

        csvfile.close()     

        return "labels.csv"



    def generateQRcode(self,codeInfo):

        try:
            path = self.join(self.getcwd(),self.Config.QRCODE_FOLDER,f"{codeInfo['code']}.png")
            #path = self.join(self.getcwd(),"qrcodes\\",f"{codeInfo['code']}.png")   # PATH USED WHEN TESTING
            qr_code = self.pyqrcode.create(codeInfo['code'])
            qr_code.png(path,scale = 15)

            # READ SAVED IMAGE
            image = self.cv.imread(path)
            font = self.cv.FONT_HERSHEY_SIMPLEX
            #               image , text                   ,x,y   , font, fontize,colors 
            self.cv.putText(image,codeInfo['site'].upper(),(60,20), font, 0.5,(0,0,0),1,self.cv.LINE_AA)
            self.cv.putText(image,codeInfo['location'].upper(),(60,37), font, 0.5,(0,0,0),1,self.cv.LINE_AA)
            if codeInfo['param'] == "shelf":
                self.cv.putText(image,f"SHELF {codeInfo['shelf']}",(520,20), font, 0.5,(0,0,0),1,self.cv.LINE_AA)
            self.cv.putText(image,codeInfo['code'],(60,55), font, 0.5,(0,0,0),1,self.cv.LINE_AA)
            

            #self.cv.imshow("Display window", image)
            #k = self.cv.waitKey(0)
            self.cv.imwrite(path, image)

        except Exception as e:
            msg = str(e)
            print("generateQRcode error ",msg)
            return None
        else: 
            return self.exists(path)
 


    def BarcodeReader(self,image):
        # READ BARCODDE FROM IMAGE FILE AND RETURN THE DECODED DATA
        print("IMAGE NAME IS ",image)
        path = self.join(self.getcwd(),self.Config.UPLOAD_FOLDER , image)
        # read the image in numpy array using cv2
        img = self.cv.imread(path)
        data = ""
        # Decode the barcode image
        detectedBarcodes = self.bardecoder(img)
        
        # If not detected then print the message
        if not detectedBarcodes:
            print("Barcode Not Detected or your barcode is blank/corrupted!")
        else:
        
            # Traverse through all the detected barcodes in image
            for barcode in detectedBarcodes:
            
                # Locate the barcode position in image
                (x, y, w, h) = barcode.rect
                
                # Put the rectangle in image using
                # cv2 to heighlight the barcode
                self.cv.rectangle(img, (x-10, y-10),
                            (x + w+10, y + h+10),
                            (255, 120, 0), 2)
                
                if barcode.data!="":
                
                    # Print the barcode data
                    data = barcode.data.decode('utf-8')
                    print(barcode.data.decode('utf-8'))
                    print(barcode.type)
                    self.cv.imwrite(path, img)
                    
        #Display the image
        # cv2.imshow("Image", img)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        return {"decodedTo":data,"image":image}#{data:img}
    

    def defaultDecorator(db="",collection=""):
        def innerDecorator(f):            
            @wraps(f)
            def wrapper(*args,**kwargs):   
                cmd = list(kwargs.keys())

                col = collection
                if 'role' in cmd:
                    pass
                    # print(kwargs['role'], " <- ROLE")
                    # if kwargs['role'] == 'user':
                    #     col = "xuser"     

                self                = args[0]
                client 	            = self.remoteMongo('mongodb://%s:%s@%s:%s' % (self.username, self.password,self.server,self.port), tls=self.tls)
                remotedb            = client[db][col].with_options(codec_options= self.CodecOptions )                
                kwargs['remotedb']  = remotedb

                try:      
                    output = f(*args,**kwargs)

                    # CLOSE MONGODB CONNECTION
                    client.close()  
                    return output
                    
                except Exception as e:
                    print("defaultDecorator exception: ",str(e))
                    
            return wrapper
        return innerDecorator
    

    @defaultDecorator(db="marsairq",collection="storage")
    def test(self,query, remotedb = None):
        result = remotedb.find_one(query,{"_id":0})  
        return result


    ##############################
    # DATABASE OPERATION FUNCTIONS
    ##############################
    @defaultDecorator(db="marsairq",collection="sites")
    def searchPaginationPageCount(self,searchtext, entity='' ,role='', remotedb = None):
        # RETURNS A COUNT OF HOW MANY SITES MATCHES WITH THE QUERY PARAMETERS
        pageSize = 30
        try: 
            query = { "entity": entity, "type": "site", 'name': { '$regex': f'{searchtext}', '$options': 'i' } }    

            if role in ['staff','admin']:
                query = { "type": "site", 'name': { '$regex': f'{searchtext}', '$options': 'i' } }
             
            # SEARCH PAGINATION-FINAL COUNT 
            number  = remotedb.count_documents(query)    
            pages   = 0      
           
            if number > 0:
                if (number % pageSize) > 0:
                    pages      = self.ceil(number / pageSize)
                else:
                    pages = self.floor(number / pageSize)                
             
        except Exception as e:
            msg = str(e)
            print("searchPaginationPageCount error ",msg)
            return None
        else:            
            return pages
        

    @defaultDecorator(db="marsairq",collection="sites") # xuser
    def getSearchPagination(self,searchtext,page, entity='', role='', remotedb = None):
        # RETURN A SPECIFIC PAGE FOR A SPECIFIC PRODUCT TYPE
        try:
            pageSize = 30   
            query = { "entity": entity, "type": "site", 'name': { '$regex': f'{searchtext}', '$options': 'i' }    }   

            if role in ['staff','admin']:
                query = {"type": "site", f'name': { '$regex': f'{searchtext}', '$options': 'i' }   }    

            #  SEARCH PAGINATION-FINAL            
            result      = list(remotedb.aggregate([{ '$match': query }, { '$sort': { 'number': 1 } }, { '$skip':  pageSize * page }, { '$limit': pageSize }, { '$project': { '_id': 0 } } ])) 
        
        except Exception as e:
            msg = str(e)
            print("getSearchPagination error ",msg)
            return None
        else:             
            return result
 
    @defaultDecorator(db="marsairq",collection="sites") # xuser
    def paginationPage(self,page,entity='', role='', remotedb = None):
        # RETURN A SPECIFIC PAGE FOR A SPECIFIC PRODUCT TYPE
        try:
            pageSize = 5 #30      
            query = { "entity": entity, "type": "site" } 

            if role in ['staff','admin']:
                query = { "type": "site"  }    
            #  PAGINATION FINAL
            result      = list(remotedb.aggregate([ { '$match': query }, { '$skip': pageSize * page }, { '$limit': pageSize }, { '$project': { '_id': 0 } } ])) 
                  
        except Exception as e:
            msg = str(e)
            print("paginationPage error ",msg)
            return None
        else:             
            return result
        

    @defaultDecorator(db="marsairq", collection="sites")
    def paginationPageCount(self, entity='' ,role='', remotedb = None):
        # RETURNS A COUNT OF HOW MANY SITES MATCHES WITH THE QUERY PARAMETERS
        pageSize = 5  
        try: 
            query = { "type": "site","entity": entity}    

            if role in ['staff','admin']:
                query = { "type": "site"}
                       
            # SEARCH PAGINATION-FINAL COUNT 
            number  = remotedb.count_documents(query)      
            pages   = 0      
           
            if number > 0:
                if (number % pageSize) > 0:
                    pages      = self.ceil(number / pageSize)
                else:
                    pages = self.floor(number / pageSize)                
             
        except Exception as e:
            msg = str(e)
            print("paginationPageCount error ",msg)
            return None
        else:            
            return pages


    @defaultDecorator(db="marsairq",collection="entities")
    def searchPaginationPageCountEntity(self,searchtext, entity='' ,role='', remotedb = None):
        # RETURNS A COUNT OF HOW MANY ENTITIES MATCHES WITH THE QUERY PARAMETERS
        pageSize = 5
        try: 
            query = {"entity": entity,'name': { '$regex': f'{searchtext}', '$options': 'i' } }    

            if role in ['staff','admin']:
                query = {'name': { '$regex': f'{searchtext}', '$options': 'i' } }
             
            # SEARCH PAGINATION-FINAL COUNT 
            number  = remotedb.count_documents(query)    
            pages   = 0       

            if number > 0:
                if (number % pageSize) > 0:
                    pages      = self.ceil(number / pageSize)
                else:
                    pages = self.floor(number / pageSize)                
             
        except Exception as e:
            msg = str(e)
            print("searchPaginationPageCountEntity error ",msg)
            return None
        else:            
            return pages
        

    @defaultDecorator(db="marsairq",collection="entities") # xuser
    def getSearchPaginationEntity(self,searchtext,page, entity='', role='', remotedb = None):
        # RETURN A SPECIFIC PAGE FOR A SPECIFIC PRODUCT TYPE
        try:
            pageSize = 5   
            query = {"id": entity,'name': { '$regex': f'{searchtext}', '$options': 'i' }    }   

            if role in ['staff','admin']:
                query = {f'name': { '$regex': f'{searchtext}', '$options': 'i' }   }    

            #  SEARCH PAGINATION-FINAL            
            result      = list(remotedb.aggregate([{ '$match': query }, { '$sort': { 'number': 1 } }, { '$skip':  pageSize * page }, { '$limit': pageSize }, { '$lookup': { 'from': 'sites', 'localField': 'id', 'foreignField': 'entity', 'as': 'sites', 'pipeline': [ { '$project': { '_id': 0, 'id': 1, 'name': 1, 'lat': 1, 'lon': 1 } } ] } }, { '$project': { '_id': 0 } } ])) 
        
        except Exception as e:
            msg = str(e)
            print("getSearchPaginationEntity error ",msg)
            return None
        else:             
            return result
 

    @defaultDecorator(db="marsairq",collection="entities") # xuser
    def paginationPageEntity(self,page,entity='', role='', remotedb = None):
        # RETURN A SPECIFIC PAGE FOR A SPECIFIC PRODUCT TYPE
        try:
            pageSize = 5 #30      
            query = {"id": entity } 

            if role in ['staff','admin']:
                query = { }    
            #  PAGINATION FINAL
            result      = list(remotedb.aggregate([ { '$match': query }, { '$skip': pageSize * page }, { '$limit': pageSize }, { '$lookup': { 'from': 'sites', 'localField': 'id', 'foreignField': 'entity', 'as': 'sites', 'pipeline': [ { '$project': { '_id': 0, 'id': 1, 'name': 1, 'lat': 1, 'lon': 1 } } ] } }, { '$project': { '_id': 0 } } ])) 
                  
        except Exception as e:
            msg = str(e)
            print("paginationPageEntity error ",msg)
            return None
        else:             
            return result

    @defaultDecorator(db="marsairq",collection="entities")
    def paginationPageCountEntity(self, entity='' ,role='', remotedb = None):
        # RETURNS A COUNT OF HOW MANY SITES MATCHES WITH THE QUERY PARAMETERS
        pageSize = 5  #30
        try: 
            query = {"id": entity }    

            if role in ['staff','admin']:
                query = { }
           
            # SEARCH PAGINATION-FINAL COUNT 
            number  = remotedb.count_documents(query)     
            pages   = 0      
           
            if number > 0:
                if (number % pageSize) > 0:
                    pages      = self.ceil(number / pageSize)
                else:
                    pages = self.floor(number / pageSize)                
             
        except Exception as e:
            msg = str(e)
            print("paginationPageCountEntity error ",msg)
            return None
        else:            
            return pages
   
        
    @defaultDecorator(db="marsairq",collection="misc")
    def miscLocOrShel(self,ID, remotedb = None):
        # RETURN LOCATION OR SHELVE INFO BASED ON SPECIFIED ID
        try:
            result      = list(remotedb.aggregate([ { '$match': { 'id': 'location', '$or': [ { 'barcode': ID }, { 'shelves.barcode': ID } ] } }, { '$addFields': { 'shelve': { '$arrayElemAt': [ { '$filter': { 'input': '$shelves', 'as': 'item', 'cond': { '$eq': [ '$$item.barcode', ID ] } } }, 0 ] } } }, { '$project': { '_id': 0, 'barcode': 1, 'name': 1, 'shelve': '$shelve.number' } } ]))
        except Exception as e:
            msg = str(e)
            print(" miscLocOrShel error ",msg)
            return None
        else: 
            return result

    @defaultDecorator(db="marsairq",collection="misc")
    def miscFind(self,query, remotedb = None):
        # SEARCH MISC COLLECTION WITH QUERY
        try:
            result      = remotedb.find_one(query,{"_id":0})
        except Exception as e:
            msg = str(e)
            print("miscFind error ",msg)
            return None
        else: 
            return result


    @defaultDecorator(db="marsairq",collection="misc")
    def miscFindAll(self,query,projection, remotedb = None):
        # SEARCH MISC COLLECTION, RETURN ALL THAT MATCHES QUERY
        try:
            result      = list(remotedb.find(query,projection))
        except Exception as e:
            msg = str(e)
            print("miscFindAll error ",msg)
            return None
        else: 
            return result

    @defaultDecorator(db="marsairq",collection="misc")
    def miscUpdate(self,query,update, remotedb = None):
        # ADD NEW ENTRY TO MISC COLLECTION
        try:
            result      = remotedb.find_one_and_update(query,update,{"_id":0},return_document= self.ReturnDocument.AFTER,upsert=True)
        except Exception as e:
            msg = str(e)
            print("miscUpdate error ",msg)
            return None
        else: 
            return result


    @defaultDecorator(db="marsairq",collection="misc")
    def miscUpsert(self,id,name,site,location,object, remotedb = None):
        # INSERT 'object' INTO THE MISC COLLECT
        try:
            result      = remotedb.find_one_and_update({"id":id,"name":name,"site":site,"barcode":location},object,{"_id":0},return_document= self.ReturnDocument.AFTER,upsert=True)
        except Exception as e:
            msg = str(e)
            print("miscUpsert error ",msg)
            return None
        else: 
            return result


    #########################
    #         ROUTES        #
    #########################
    @defaultDecorator(db="marsairq",collection="data")
    def addData(self,data, remotedb = None):
        '''ADD A NEW STORAGE LOCATION TO COLLECTION'''
        try: 
            result      = remotedb.insert_one(data) 
        except Exception as e:
            print("addData error ",str(e))
            return False 
        else:                  
            return True


    @defaultDecorator(db="marsairq",collection="data")
    def addBatchData(self,data, remotedb = None):
        '''ADD A NEW STORAGE LOCATION TO COLLECTION'''
        try: 
            result      = remotedb.insert_many(data, ordered=False) 
        except Exception as e:
            print("addBatchData error ",str(e))
            return False 
        else:                  
            return True
        
    @defaultDecorator(db="marsairq",collection="data")
    def getCollocationData(self,start,end, query, remotedb = None):
        ''' GET PRESSURE DATA FOR ALL SENSORS '''
        try: 
            result      = list(remotedb.aggregate([{'$match': { 'date': { '$gte': start, '$lte': end }, 'model': { '$in': query } } }, { '$project': { '_id': 0 } }, { '$group': { '_id': '$model', 'values': { '$push': '$$ROOT' } } }]))
        except Exception as e:
            print("getCollocationData error ",str(e))            
        else:                  
            return result
        
    @defaultDecorator(db="marsairq",collection="data")
    def getMapHistoryData(self,id,start,end, param, remotedb = None):
        ''' GET PRESSURE DATA FOR ALL SENSORS '''
        try:
           
            result      = list(remotedb.aggregate(  [ { '$match': { 'id': id, 'date': { '$gte': start, '$lte': end } } }, { '$project': { '_id': 0, 'name': 1, 'id': 1, param: f'$data.{param}', 'date': 1 } } ]))
            sq = self.DataFrame(result)
            
            # sq['date'] = self.to_datetime(sq['timestamp'],unit='s')
            sq   = sq.set_index("date")  
            groups = sq.groupby(self.Grouper(freq='h'))          
            hourly = groups.agg({"name": 'max',"id":"max", param: "mean"}) 
            hourly.reset_index(inplace=True)
            hourly.dropna(inplace=True)
            hourly['timestamp'] = self.to_numeric(hourly['date'].values) / 10 ** 6 
            # hourly.to_csv("data.csv")
            # hourly.reset_index(drop=True)
            result = hourly.to_dict(orient='records')
            
        except Exception as e:
            print("getMapHistoryData error ",str(e))            
        else:                  
            return result


    #########################
    #          TEMP         #
    #########################
    @defaultDecorator(db="marsairq",collection="temp")
    def createTempDoc(self,query, remotedb = None):
        # CREATE TEMPORARY DOCUMENT IN TEMP COLLECTION
        try:
            result      = remotedb.insert_one(query)
        except Exception as e:
            print("createTempDoc error ",str(e))
            return False
        else:                  
            return True

    @defaultDecorator(db="marsairq",collection="temp")
    def findTempDoc(self,query, remotedb = None):
        # SEARCH FOR A TEMPORARY DOCUMENT IN TEMP COLLECTION
        try:
            result      = remotedb.find_one(query,{"_id":0})
        except Exception as e:
            print("findTempDoc error ",str(e))
            return None
        else:                  
            return result

    @defaultDecorator(db="marsairq",collection="temp")
    def findAllTempDoc(self,query, remotedb = None):
        # SEARCH FOR A TEMPORARY DOCUMENT IN TEMP COLLECTION
        try:
            result      = list(remotedb.find(query,{"_id":0}))
        except Exception as e:
            print("findAllTempDoc error ",str(e))
            return None
        else:                  
            return result

    @defaultDecorator(db="marsairq",collection="temp")
    def deleteTempDoc(self,query, remotedb = None):
        # SEARCH FOR A TEMPORARY DOCUMENT IN TEMP COLLECTION
        try:
            result      = remotedb.delete_one(query)
        except Exception as e:
            print("deleteTempDoc error ",str(e))
            return 0
        else:                  
            return result.deleted_count

    @defaultDecorator(db="marsairq",collection="temp")
    def updateTempDoc(self,query,update, remotedb = None):
        # UPDATE EXISTING DOCUMENT IN TEMP COLLECTION
        try:            
            result      = remotedb.find_one_and_update(query,update,{"_id":0},return_document= self.ReturnDocument.AFTER, upsert = True) 
        except Exception as e:
            msg = str(e)
            print("updateTempDoc error ",msg)
            return None
        else: 
            return result

    ###############################################################
    #   USER FUNCTIONS, LOGIN/LOGOUT/VERIFICATION/REGISTRATION    #
    ###############################################################

    @defaultDecorator(db="marsairq",collection="storage")
    def userAssignedItems(self,id, remotedb = None):
        # CHECKS IF USER EXIST USING ID OR EMAIL ADDRESS PROVIDED
        try: 
            result = list(remotedb.aggregate([ { '$match': { 'shelf': id } }, { '$project': { '_id': 0 } }, { '$group': { '_id': '$product', 'count': { '$sum': 1 }, 'barcodes': { '$push': '$$ROOT.barcode' }, 'pro': { '$push': '$$ROOT' } } }, { '$lookup': { 'from': 'product', 'localField': 'pro.product', 'foreignField': 'id', 'pipeline': [ { '$project': { '_id': 0 } } ], 'as': 'item' } }, { '$project': { '_id': 0, 'count': 1, 'barcodes': 1, 'product': { '$arrayElemAt': [ '$item', 0 ] } } } ])) 
            
        except Exception as e:
            msg = str(e)
            print("userAssignedItems error ",msg)
            return None
        else: 
            if len(result) > 0:
                return result               
            return None


    @defaultDecorator(db="marsairq",collection="accounts")
    def whoHasWhat(self, remotedb = None):
        # RETURN ALL THAT IS ASSIGNED TO EACH STAFF MEMBER
        try: 
            result      = list(remotedb.aggregate([ { '$match': { '$or':[{'role': 'staff' },{'role': 'admin' }] } }, { '$lookup': { 'from': 'storage', 'localField': 'shelf', 'foreignField': 'shelf', 'pipeline': [ { '$project': { '_id': 0, 'product': 1, 'barcode': 1 } }, { '$lookup': { 'from': 'product', 'localField': 'product', 'foreignField': 'id', 'pipeline': [ { '$project': { '_id': 0 } } ], 'as': 'product' } }, { '$project': { 'barcode': 1, 'product': { '$arrayElemAt': [ '$product', 0 ] } } }, { '$group': { '_id': '$product.id', 'count': { '$sum': 1 }, 'barcodes': { '$push': '$barcode' }, 'product': { '$first': '$product' } } } ], 'as': 'assigned' } }, { '$project': { '_id': 0, 'username': 1, 'email': 1, 'role': 1, 'firstname': 1, 'lastname': 1, 'department': 1, 'assigned': 1 } } ] ))
        except Exception as e:
            msg = str(e)
            print("whoHasWhat error ",msg)
            return None
        else: 
            return result
        

    @defaultDecorator(db="marsairq",collection="accounts")
    def userExist(self, email="",id="",role="user", remotedb = None):
        # CHECKS IF USER EXIST USING ID OR EMAIL ADDRESS PROVIDED
        try: 
            result      = remotedb.count_documents({'$or':[{"email": email},{"id":id}] })
        except Exception as e:
            msg = str(e)
            print("userExist error ",msg)
            return (False,"error")
        else: 
            if result > 0:
                return (True,"success")                 
            return (False,"success")

    @defaultDecorator(db="marsairq",collection="accounts")
    def findUser(self,email="",id="", remotedb = None):
        # SEARCH FOR USER USING ID OR EMAIL ADDRESS PROVIDED
        try: 
            result      = remotedb.find_one({'$or':[{"email": email},{"id":id}]  },{"_id":0}) 
        except Exception as e:
            msg = str(e)
            print("findUser error ",msg)
            return None
        else: 
            return result
        
        
    @defaultDecorator(db="marsairq",collection="accounts")
    def findAllUser(self,text='', remotedb = None):
        # SEARCH FOR USER USING ID OR EMAIL ADDRESS PROVIDED
        try: 
            result      = list(remotedb.find({'$or':[{"email": { '$regex': f'{text}', '$options': 'i' }},{"id": { '$regex': f'{text}', '$options': 'i' }},{"firstname": { '$regex': f'{text}', '$options': 'i' }},{"lastname": { '$regex': f'{text}', '$options': 'i' }},{"organization": { '$regex': f'{text}', '$options': 'i' }}]  },{"_id":0})) 
        except Exception as e:
            msg = str(e)
            print("findAllUser error ",msg)
            return None
        else: 
            return result
        
    @defaultDecorator(db="marsairq",collection="accounts")
    def findAllStaff(self, remotedb = None):
        # RETURN LIST OF STAFF MEMBERS FOR /ADMIN ROUTE
        try: 
            result      = list(remotedb.find( {'$or':[{"role":"staff"},{"role":"admin"}]  } ,{"_id":0,"password":0 }))
        except Exception as e:
            msg = str(e)
            print("findAllStaff error ",msg)
            return None
        else: 
            return result
        
    @defaultDecorator(db="marsairq",collection="accounts")
    def findAllClient(self, remotedb = None):
        # RETURN LIST OF EXTERNAL MEMBERS FOR /ADMIN ROUTE
        try: 
            result      = list(remotedb.find({"role":"user"},{"_id":0,"password":0}))
        except Exception as e:
            msg = str(e)
            print("findAllStaff error ",msg)
            return None
        else: 
            return result


    @defaultDecorator(db="marsairq",collection="accounts")
    def updateUser(self,query,update, remotedb = None):
        # UPDATE PARAMS FOR SPECIFIED USER
        try: 
            result      = remotedb.find_one_and_update(query,update,{"_id":0},return_document= self.ReturnDocument.AFTER, upsert = True) 
        except Exception as e:
            msg = str(e)
            print("updateUser error ",msg)
            return None
        else: 
            return result

    @defaultDecorator(db="marsairq",collection="accounts")
    def addUser(self,newAccount, remotedb = None):
        # ADD NEW USER ACCOUNT TO DATABASE
        try: 
            result      = remotedb.insert_one(newAccount)
        except Exception as e:
            msg = str(e)
            print("addUser error ",msg)
            return False
        else:                  
            return True

    @defaultDecorator(db="marsairq",collection="accounts")
    def removeUser(self,email, remotedb = None):
        # REMOVE USER ACCOUNT FROM  DATABASE
        try: 
            result      = remotedb.delete_one({"email":email})
        except Exception as e:
            msg = str(e)
            print("removeUser error ",msg)
            return 0
        else:                  
            return result.deleted_count
        
        
    @defaultDecorator(db="marsairq",collection="mqtt_users")
    def addMqttUser(self,newAccount, remotedb = None):
        # ADD NEW MQTT USER ACCOUNT TO DATABASE
        try: 
            result      = remotedb.insert_one(newAccount)
        except Exception as e:
            msg = str(e)
            print("addMqttUser error ",msg)
            return False
        else:                  
            return True

    @defaultDecorator(db="marsairq",collection="mqtt_users")
    def mqttUserExist(self,id="", site="", remotedb = None):
        # CHECKS IF MQTT USER EXIST USING ID PROVIDED
        try: 
            result      = remotedb.count_documents({"$or":[{"id":id},{"site":site}]})
        except Exception as e:
            msg = str(e)
            print("mqttUserExist error ",msg)
            return (False,"error")
        else: 
            if result > 0:
                return (True,"success")                 
            return (False,"success")


    @defaultDecorator(db="marsairq",collection="mqtt_users")
    def removeMqttUser(self,id, remotedb = None):
        # REMOVE USER ACCOUNT FROM  DATABASE
        try: 
            result      = remotedb.delete_many({"owner": id})
        except Exception as e:
            msg = str(e)
            print("removeMqttUser error ",msg)
            return 0
        else:                  
            return result.deleted_count


    @defaultDecorator(db="marsairq",collection="mqtt_users")
    def updateMqttUser(self,query,update, remotedb = None):
        # UPDATE PARAMS FOR SPECIFIED USER
        try: 
            result      = remotedb.find_one_and_update(query,update,{"_id":0},return_document= self.ReturnDocument.AFTER, upsert = True) 
        except Exception as e:
            msg = str(e)
            print("updateMqttUser error ",msg)
            return None
        else: 
            return result



    @defaultDecorator(db="marsairq",collection="sites")
    def addSite(self,newSite, remotedb = None):
        # ADD NEW USER ACCOUNT TO DATABASE
        try: 
            result      = remotedb.insert_one(newSite)
        except Exception as e:
            msg = str(e)
            print("addSite error ",msg)
            return False
        else:                  
            return True
        
    @defaultDecorator(db="marsairq",collection="sites")
    def deleteSite(self,query, remotedb = None):
        # DELETE SITE FROM COLLECTION
        try:
            result      = remotedb.delete_one(query)
        except Exception as e:
            print("deleteSite error ",str(e))
            return 0
        else:                  
            return result.deleted_count

    @defaultDecorator(db="marsairq",collection="sites")
    def deleteAllSite(self,query, remotedb = None):
        # REMOVE USER ACCOUNT FROM  DATABASE
        try: 
            result      = remotedb.delete_many(query)
        except Exception as e:
            msg = str(e)
            print("deleteAllSite error ",msg)
            return 0
        else:                  
            return result.deleted_count
        

    @defaultDecorator(db="marsairq",collection="sites")
    def findAllSites(self,query, remotedb = None):
        # RETURN LIST OF SITES
        try: 
            result      = list(remotedb.find(query,{"_id":0}))
            # [ { '$match': { 'type': 'site', '$or': [ { 'owner': owner }, { 'secondaryowners': { '$in': [ owner ] } } ] } }, { '$lookup': { 'from': 'mqtt_users', 'localField': 'id', 'foreignField': 'site', 'as': 'credentials', 'pipeline': [ { '$project': { '_id': 0, 'username': 1 } } ] } }, { '$addFields': { 'list': '$$CURRENT.credentials.username' } }, { '$addFields': { 'username': { '$cond': { 'if': { '$gt': [ { '$size': '$list' }, 0 ] }, 'then': { '$arrayElemAt': [ '$list', 0 ] }, 'else': '' } } } }, { '$project': { '_id': 0, 'list': 0, 'credentials': 0 } } ]
            # result      = list(remotedb.aggregate([ { '$match': query }, { '$lookup': { 'from': 'mqtt_users', 'localField': 'id', 'foreignField': 'site', 'as': 'credentials', 'pipeline': [ { '$project': { '_id': 0, 'username': 1 } } ] } }, { '$addFields': { 'list': '$$CURRENT.credentials.username' } }, { '$addFields': { 'username': { '$cond': { 'if': { '$gt': [ { '$size': '$list' }, 0 ] }, 'then': { '$arrayElemAt': [ '$list', 0 ] }, 'else': '' } } } }, { '$project': { '_id': 0, 'list': 0, 'credentials': 0 } } ]))
        except Exception as e:
            msg = str(e)
            print("findAllSites error ",msg)
            return None
        else: 
            return result
    
    @defaultDecorator(db="marsairq",collection="sites")
    def findSite(self,id="",project={"_id":0}, remotedb = None):
        # SEARCH FOR USER USING ID OR EMAIL ADDRESS PROVIDED
        try: 
            result      = remotedb.find_one({"id":id},project) 
        except Exception as e:
            msg = str(e)
            print("findSite error ",msg)
            return None
        else: 
            return result

    @defaultDecorator(db="marsairq",collection="sites")
    def updateSite(self,query,update, remotedb = None):
        # UPDATE PARAMS FOR SPECIFIED USER
        try: 
            result      = remotedb.find_one_and_update(query,update,{"_id":0},return_document= self.ReturnDocument.AFTER, upsert = True) 
        except Exception as e:
            msg = str(e)
            print("updateSite error ",msg)
            return None
        else: 
            return result


    @defaultDecorator(db="marsairq",collection="sites")
    def getSiteWithOwner(self,site, remotedb = None):
        # UPDATE PARAMS FOR SPECIFIED USER
        try: 
            result      = list(remotedb.aggregate([ { '$match': { 'type': 'site', 'id': site } }, { '$lookup': { 'from': 'accounts', 'localField': 'owner', 'foreignField': 'id', 'pipeline': [ { '$project': { '_id': 0, 'firstname': 1, 'lastname': 1, 'organization': 1, 'email': 1, 'country': 1 } } ], 'as': 'acc_owner' } }, { '$project': { '_id': 0 } } ]) )
            if len(result) > 0:
                result = result[0]
        
        
        except Exception as e:
            msg = str(e)
            print("getSiteWithOwner error ",msg)
            return None
        else: 
            return result


    @defaultDecorator(db="marsairq",collection="sites")
    def getSitesForOwner(self,owner, remotedb = None):
        # GET ALL SITES THAT IS ASSIGNED TO A SPECIFIC USER. 
        try: 
            # GET ALL SITES FOR OWNER WITH MQTT
            result      = list(remotedb.aggregate([ { '$match': { 'type': 'site', '$or': [ { 'owner': owner }, { 'secondaryowners': { '$in': [ owner ] } } ] } }, { '$lookup': { 'from': 'mqtt_users', 'localField': 'id', 'foreignField': 'site', 'as': 'credentials', 'pipeline': [ { '$project': { '_id': 0, 'username': 1 } } ] } }, { '$addFields': { 'list': '$$CURRENT.credentials.username' } }, { '$addFields': { 'username': { '$cond': { 'if': { '$gt': [ { '$size': '$list' }, 0 ] }, 'then': { '$arrayElemAt': [ '$list', 0 ] }, 'else': '' } } } }, { '$project': { '_id': 0, 'list': 0, 'credentials': 0 } } ]))
             
        except Exception as e:
            msg = str(e)
            print("getSitesForOwner error ",msg)
            return None
        else: 
            return result


    ###############################################################
    #                           ENTITY                            #
    ###############################################################
    @defaultDecorator(db="marsairq",collection="entities")
    def addEntity(self,query, remotedb = None):
        # ADD NEW USER ACCOUNT TO DATABASE
        try: 
            result      = remotedb.insert_one(query)
        except Exception as e:
            msg = str(e)
            print("addEntity error ",msg)
            return False
        else:                  
            return True
        
    @defaultDecorator(db="marsairq",collection="entities")
    def findAllEntitiesCredentials(self,query,project={"_id":0}, remotedb = None):
        # RETURN LIST OF ENTITIES
        try: 
            result      = list(remotedb.find(query,project))            
        except Exception as e:
            msg = str(e)
            print("findAllEntitiesCredentials error ",msg)
            return None
        else: 
            return result
        
    @defaultDecorator(db="marsairq",collection="entities")
    def findAllEntities(self,query,project={"_id":0}, remotedb = None):
        # RETURN LIST OF ENTITIES
        try: 
            # result      = list(remotedb.find({},project))
            result      = list(remotedb.aggregate([ { '$match': query }, { '$lookup': { 'from': 'sites', 'localField': 'id', 'foreignField': 'entity', 'as': 'sites', 'pipeline': [ { '$project': { '_id': 0, 'id': 1, 'name': 1, 'lat': 1, 'lon': 1 } } ] } }, { '$project': project } ]))
            
        except Exception as e:
            msg = str(e)
            print("findAllEntities error ",msg)
            return None
        else: 
            return result

    @defaultDecorator(db="marsairq",collection="entities")
    def findAllEntitiesForSignup(self,project={"_id":0}, remotedb = None):
        # RETURN LIST OF ENTITIES
        try: 
            result      = list(remotedb.find({},project))
            # result      = list(remotedb.aggregate([ { '$match': {} }, { '$lookup': { 'from': 'sites', 'localField': 'id', 'foreignField': 'entity', 'as': 'sites', 'pipeline': [ { '$project': { '_id': 0, 'id': 1, 'name': 1, 'lat': 1, 'lon': 1 } } ] } }, { '$project': { '_id': 0, 'web': 0, 'device': 0 } } ]))
            
        except Exception as e:
            msg = str(e)
            print("findAllEntitiesForSignup error ",msg)
            return None
        else: 
            return result

    @defaultDecorator(db="marsairq",collection="entities")
    def findEntityCredentials(self,query,project={"_id":0}, remotedb = None):
        # FIND A SINGLE ENTITY
        try: 
            result      = remotedb.find_one(query,project) 
        except Exception as e:
            msg = str(e)
            print("findEntityCredentials error ",msg)
            return None
        else: 
            return result

    @defaultDecorator(db="marsairq",collection="entities")
    def findEntity(self,id="",project={"_id":0}, remotedb = None):
        # FIND A SINGLE ENTITY
        try: 
            result      = remotedb.find_one({"id":id},project) 
        except Exception as e:
            msg = str(e)
            print("findEntity error ",msg)
            return None
        else: 
            return result
        
    @defaultDecorator(db="marsairq",collection="entities")
    def deleteEntity(self,query, remotedb = None):
        # SEARCH FOR A TEMPORARY DOCUMENT IN TEMP COLLECTION
        try:
            result      = remotedb.delete_one(query)
        except Exception as e:
            print("deleteEntity error ",str(e))
            return 0
        else:                  
            return result.deleted_count
        
    @defaultDecorator(db="marsairq",collection="entities")
    def entityExist(self,id="", name="", organization="", remotedb = None):
        # CHECKS IF MQTT USER EXIST USING ID PROVIDED
        try: 
            result      = remotedb.count_documents({"$or":[{"id":id},{"name": name},{"organization": organization}]})
        except Exception as e:
            msg = str(e)
            print("entityExist error ",msg)
            return (False,"error")
        else: 
            if result > 0:
                return (True,"success")                 
            return (False,"success")


    @defaultDecorator(db="marsairq",collection="entities")
    def updateEntity(self,query,update, remotedb = None):
        # UPDATE A SINGLE ENTITY
        try: 
            result      = remotedb.find_one_and_update(query,update,{"_id":0},return_document= self.ReturnDocument.AFTER, upsert = True) 
        except Exception as e:
            msg = str(e)
            print("updateEntity error ",msg)
            return None
        else: 
            return result


def main():
    from config import Config
    from time import time, ctime, sleep
    from math import floor
    from datetime import datetime, timedelta
    import logging

    Logger             = logging.getLogger(__name__)

    # SETTINGS
    # https://realpython.com/python-logging/
    # https://docs.python.org/3/library/logging.html#logrecord-attributes
    # logging.basicConfig(level=logging.DEBUG,filename="app/log/sia_logs.csv",encoding="utf-8",filemode="a",format="{asctime},{process},{levelname},{name},{message},{exc_info}", style="{", datefmt="%Y-%m-%d %H:%M")

    console_handler    = logging.StreamHandler()
    file_handler       = logging.FileHandler(filename="log/sia_logs.log",encoding="utf-8",mode="a")
    formatter          = logging.Formatter( "{asctime},{process},{levelname},{name},{message},{exc_info}", style="{",datefmt="%Y-%m-%d %H:%M" )


    console_handler.setFormatter(formatter)        
    file_handler.setFormatter(formatter)
    console_handler.setLevel("DEBUG")
    file_handler.setLevel("WARNING")
    Logger.addHandler(console_handler)
    Logger.addHandler(file_handler)

    one = DB(Config, Logger)
    timestamp = floor(time())
    registered = ctime(timestamp)
    user = {"username":"Legendary","email":"tajay59@gmail.com","password":"blackops","role":"admin","timestamp":timestamp,"registered":registered,"emailconfirmed":True}
    #one.addUser(user)
    # sleep(5)
    # res = one.userExist("tajay59@gmail.com")
    
    # res = one.removeUser("tajay59@gmail.com")
    # account = one.findUser("tajay59@gmail.com")
    # print(res)
    # print(account)
   
    # {$regex : "developer"}
    # one.addProducts()
    account = one.findUser(id="ACC355b9357e0365576c7e2fe5afd80bf98") 
    # account = one.findUser(id="ACC1eaa0653f9b470176d0c4cb5d0e5ac24") 
    # res = one.updateUserCart("ACC355b9357e0365576c7e2fe5afd80bf98",cart=[{"1":"one","2":"Gingerbeer"}])
    # res = one.updateUserCart("ACC355b9357e0365576c7e2fe5afd80bf98",cart=[])
 
    # print(res)
    # print("misc search ",one.miscFind({"id":"site","name":"cimh"}))
    # first =  one.generateQRcode("try")
    

    # product = {"id":"product","site":"SITEbb490ce66a95393ec7edf2f81080e816","location":"LOC9c0df535436f8f5ce6dd5fca4c2885f4","shelf": "SHELb468d7929bd58614a3dca409ee46074a","product":"PRO663638e2fce01a7b4ca27c1228dcd1fd","quantity":10}
    # print(one.insertProduct("cimh",product))


    # espireAt = datetime.utcnow() + timedelta(minutes=1000)
    # query = {"expireAt":espireAt, "username":"Legendary","email":"tajay59@gmail.com","logmessage":"well done!"}
    # res = one.createTempDoc(query)
    # codeInfo = {"site":"cimh","location":"alpha","shelf":"1","code":"LOC21e797b6f2fb7061be4439641095c07b","param":"shelf"}
    # res = one.generateQRcode(codeInfo)
    # res = one.findAllProductsPaginationPage("63a4a888036a25804d55166f","63adf576afcb897b65c590d1",True,False )
    # res = one.paginationList(True)
    # res = len(one.findSome("ryan",staff=True))
    # res = one.getSearchPagination("ryan")

    # res = one.pagination()
    # print(res)
    

    # req = {"search":"ryan","data":{'MET': [{'end': '64cfb2759142423d95daa0a2', 'page': 1, 'start': '64cfb26e9142423d95da526d'}, {'end': '64cfb2859142423d95daf837', 'page': 2, 'start': '64cfb2759142423d95daa0a2'}, {'end': '64cfb28a9142423d95db31ea', 'page': 3, 'start': '64cfb2859142423d95daf837'}, {'end': '64cfb2919142423d95db82d2', 'page': 4, 'start': '64cfb28a9142423d95db31ea'}, {'end': '64cfb2aa9142423d95dbe13f', 'page': 5, 'start': '64cfb2919142423d95db82d2'}], 'RAD': [{'end': '64cfb2779142423d95dabd58', 'page': 1, 'start': '64cfb26f9142423d95da5987'}, {'end': '64cfb2879142423d95db0c64', 'page': 2, 'start': '64cfb2779142423d95dabd58'}, {'end': '64cfb28f9142423d95db72ef', 'page': 3, 'start': '64cfb2879142423d95db0c64'}, {'end': '64cfb2a79142423d95dbc2c8', 'page': 4, 'start': '64cfb28f9142423d95db72ef'}, {'end': '64cfb2ae9142423d95dc0c8d', 'page': 5, 'start': '64cfb2a79142423d95dbc2c8'}], 'PRO': [{'end': '64cfb2759142423d95daa9fc', 'page': 1, 'start': '64cfb26e9142423d95da4ff8'}, {'end': '64cfb2899142423d95db1dd4', 'page': 2, 'start': '64cfb2759142423d95daa9fc'}, {'end': '64cfb2909142423d95db76c5', 'page': 3, 'start': '64cfb2899142423d95db1dd4'}, {'end': '64cfb2a69142423d95dbb59f', 'page': 4, 'start': '64cfb2909142423d95db76c5'}, {'end': '64cfb2ae9142423d95dc087e', 'page': 5, 'start': '64cfb2a69142423d95dbb59f'}], 'MISC': [{'end': '64cfb2759142423d95daa0e0', 'page': 1, 'start': '64cfb26e9142423d95da4fd3'}, {'end': '64cfb27a9142423d95dae8ff', 'page': 2, 'start': '64cfb2759142423d95daa0e0'}, {'end': '64cfb28e9142423d95db5ca4', 'page': 3, 'start': '64cfb27a9142423d95dae8ff'}, {'end': '64cfb2a69142423d95dbb700', 'page': 4, 'start': '64cfb28e9142423d95db5ca4'}, {'end': '64cfb2ae9142423d95dc04ba', 'page': 5, 'start': '64cfb2a69142423d95dbb700'}]}}
    # req = {'user': 'ACC93a132c00b4b8b9a384d483876f8ce7a', 'search': 'joseph', 'data': {'MET': [{'end': '64eac135e7197be908bf5b56', 'page': 1, 'start': '64eac12de7197be908bf24f3'}, {'end': '64eac13ee7197be908bf928f', 'page': 2, 'start': '64eac135e7197be908bf5b56'}, {'end': '64eac145e7197be908bfc189', 'page': 3, 'start': '64eac13ee7197be908bf928f'}, {'end': '64eac14de7197be908bff31c', 'page': 4, 'start': '64eac145e7197be908bfc189'}, {'end': '64eac156e7197be908c02f42', 'page': 5, 'start': '64eac14de7197be908bff31c'}], 'RAD': [{'end': '64eac135e7197be908bf57b1', 'page': 1, 'start': '64eac12de7197be908bf2505'}, {'end': '64eac13ce7197be908bf8895', 'page': 2, 'start': '64eac135e7197be908bf57b1'}, {'end': '64eac143e7197be908bfb542', 'page': 3, 'start': '64eac13ce7197be908bf8895'}, {'end': '64eac149e7197be908bfdb0b', 'page': 4, 'start': '64eac143e7197be908bfb542'}, {'end': '64eac14fe7197be908c0022b', 'page': 5, 'start': '64eac149e7197be908bfdb0b'}], 'PRO': [{'end': '64eac136e7197be908bf5e3d', 'page': 1, 'start': '64eac12de7197be908bf24df'}, {'end': '64eac13de7197be908bf8d11', 'page': 2, 'start': '64eac136e7197be908bf5e3d'}, {'end': '64eac145e7197be908bfbd71', 'page': 3, 'start': '64eac13de7197be908bf8d11'}, {'end': '64eac14ce7197be908bfef39', 'page': 4, 'start': '64eac145e7197be908bfbd71'}, {'end': '64eac152e7197be908c01528', 'page': 5, 'start': '64eac14ce7197be908bfef39'}], 'MISC': [{'end': '64eac136e7197be908bf5f79', 'page': 1, 'start': '64eac12de7197be908bf2749'}, {'end': '64eac13ce7197be908bf856f', 'page': 2, 'start': '64eac136e7197be908bf5f79'}, {'end': '64eac143e7197be908bfb5b9', 'page': 3, 'start': '64eac13ce7197be908bf856f'}, {'end': '64eac14de7197be908bff2d4', 'page': 4, 'start': '64eac143e7197be908bfb5b9'}, {'end': '64eac155e7197be908c02afe', 'page': 5, 'start': '64eac14de7197be908bff2d4'}]}}
    # one.getPages(req)
    # one.downloadSampleImages()
    # one.getSearchPaginationOld()
    # one.createLocationName("SITEe1dde58de4b62d3d070942303ce9bfdd") 
    # one.createLocationName("SITEa88644aea4fbbf20780d92b6a72671f5")
    # print(one.createLocationName("SITEaed6d69188a54b45d2e8f544b58244ef"))
    # one.getShelfCount("SITEe1dde58de4b62d3d070942303ce9bfdd","LOC3bbf09b92d3c144ebc5b0d64ae4f6acb")
    # print(one.scanshelf('SHEL377209aaeeba83ff23a1ab91d205216e'))
    print(one.paginationPageCount(entity='ENT5d753426c8d80c07bb6209ddb629e005'))
    # print(one.pagination("MET",0))
    # one.testConnection()
    # print(one.findOrder(id="ORD630fbd2af85880a1ee71f5a6d018360c"))
    print()
    # start = time()
    # print(one.findStorage({"barcode":"MISCc4c819dc57990680e8550547e8298f15*50980abcab4affbbb232f83c7b6d933f","picked": True}) )
    # print(one.getOrderWithTotal(order="ORD943d4971e1623017936d7bd3c8f0034b"))
    # if account:
    #     print(account)
    # else:
    #     print("Not found")
    # end = time()


    # print(f"completed in: {end - start} seconds")
     




if __name__ == '__main__':
    main()
  


    
