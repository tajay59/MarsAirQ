########################################################################################################
#                                                                                                      #
#   MQTT Paho Documentation - https://eclipse.dev/paho/files/paho.mqtt.python/html/client.html         #
#                                                                                                      #
########################################################################################################
import paho.mqtt.client as mqtt
from random import randint
from json import dumps, loads
from time import sleep
from datetime import datetime

class MQTT:

    # ID = f"IOT_B_1000"
    ID = f"IOT_B_{randint(1,1000000)}"

    #  DEFINE ALL TOPICS TO SUBSCRIBE TO
    sub_topics = [("/station/data/#", 0)] #  A list of tuples of (topic, qos). Both topic and qos must be present in the tuple.


    def __init__(self,mongo):
       
        self.randint                = randint
        self.datetime               = datetime
        self.loads                  = loads
        self.dumps                  = dumps
        self.sleep                  = sleep
        self.mongo                  = mongo
        self.client                 = mqtt.Client(client_id= self.ID, clean_session=True, reconnect_on_failure = True,  transport="websockets")
        self.client.on_connect      = self.on_connect
        self.client.on_message      = self.on_message
        self.client.on_disconnect   = self.on_disconnect
        self.client.on_subscribe    = self.on_subscribe

        self.client.username_pw_set("f0395b8f63f8df00","133521bb064d14705ea66272ccffb5d1")


        # REGISTER CALLBACK FUNCTION FOR EACH TOPIC
        self.client.message_callback_add("/devices", self.update)
        self.client.message_callback_add("/station/data/#", self.addData)

        # UNCOMMENT WHEN USING TLS
        self.client.tls_set()

        # ADD MQTT SERVER AND PORT INFORMATION BELOW
        self.client.connect_async("mqtt.cimh.edu.bb", 443, 60)  #labs.yanacreations.com 172.16.0.202 65.48.133.172
        # self.client.connect_async("labs.yanacreations.com", 1883, 60)  #labs.yanacreations.com 172.16.0.202 65.48.133.172
        # self.client.connect_async("172.16.0.202", 8883, 60)  #labs.yanacreations.com 172.16.0.202 65.48.133.172
       


    def connack_string(self,rc):
        connection = {0: "Connection successful", 1: "Connection refused - incorrect protocol version", 2: "Connection refused - invalid client identifier", 3: "Connection refused - server unavailable", 4: "Connection refused - bad username or password", 5: "Connection refused - not authorised" }
        return connection[rc]

 
    def on_connect(self,client, userdata, flags, rc):
        # Called when the broker responds to our connection request.
        print("\n\nMQTT: "+ self.connack_string(rc)," ID: ",client._client_id.decode('utf-8'))
        # Subscribing in on_connect() means that if we lose the connection and
        # reconnect then subscriptions will be renewed.
        client.subscribe(self.sub_topics)     
 
    def on_subscribe(self, client, userdata, mid, granted_qos):   
        # Called when the broker responds to a subscribe request.   
        print("MQTT: Subscribed to", [topic[0] for topic in self.sub_topics])

    def publish(self,topic,payload):
        try :
            info = self.client.publish(topic, payload)
            info.wait_for_publish()
            return info.is_published()
        
        except Exception as e:
            print(f"MQTT: Publish failed {str(e)}")


    def on_message(self,client, userdata, msg):
        # The callback for when a PUBLISH message is received from the server.
        try:
            print(msg.topic+" "+str(msg.payload.decode("utf-8")))
        except Exception as e:
            print(f"MQTT: onMessage Error: {str(e)}")

    def on_disconnect(self, client, userdata, rc):
        if rc != 0:
            print("MQTT: Unexpected Disconnection.")
   

    # DEFINE CALLBACK FUNCTIONS FOR EACH TOPIC
    def update(self, client, userdata, msg):
        try:
            topic   = msg.topic
            payload = msg.payload.decode("utf-8")
            # print(payload) # UNCOMMENT WHEN DEBUGGING  
            
            update  = loads(payload) # CONVERT FROM JSON STRING TO JSON OBJECT  
            dt      = self.datetime.fromtimestamp(update["timestamp"])
            update["date"] = dt
            # self.mongo.addData(update) # INSERT INTO DATABASE 

        except Exception as e:
            print(f"MQTT: GDP Error: {str(e)}")

    def addData(self, client, userdata, msg):
        try:
            topic   = msg.topic
            payload = msg.payload.decode("utf-8")
            # print(payload) # UNCOMMENT WHEN DEBUGGING  
            
            update  = loads(payload) # CONVERT FROM JSON STRING TO JSON OBJECT  
            dt      = self.datetime.fromtimestamp(update["timestamp"])
            update["date"] = dt
            # self.mongo.addData(update) # INSERT INTO DATABASE 

        except Exception as e:
            print(f"MQTT: addData Error: {str(e)}")
            

    def toggle(self,client, userdata, msg):    
        '''Process messages from Frontend'''
        try:
            topic   = msg.topic
            payload = msg.payload.decode("utf-8")
            # print(payload) # UNCOMMENT WHEN DEBUGGING
            update  = loads(payload) # CONVERT FROM JSON STRING TO JSON OBJECT  
        
             
            print(update)

        except Exception as e:
            print(f"MQTT: toggle Error - {str(e)}")



     







# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
# client.loop_start()
# client.loop_forever(retry_first_connection=True)


# while True:
#     sleep(1)
#     # print(client.is_connected())
#     publish("620085969_sub", "messages")
#     pass