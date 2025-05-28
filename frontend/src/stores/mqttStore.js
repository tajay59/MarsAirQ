import {defineStore} from 'pinia'
import {ref,reactive, shallowReactive,shallowRef, toRaw} from 'vue'


const makeid = (length) =>{
    var result           = '';
    var characters       = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
    var charactersLength = characters.length;

    for ( var i = 0; i < length; i++ ) {
        result += characters.charAt(Math.floor(Math.random() * charactersLength));
        }
    return "IOT_WEB_"+result;
    };


export const useMqttStore =  defineStore('mqtt', ()=>{

    /*  
    The composition API way of defining a Pinia store
    ref() s become state properties
    computed() s become getters
    function() s become actions 
    MQTT Paho Documentation:
        1. https://eclipse.dev/paho/index.php?page=clients/js/index.php 
        2. https://eclipse.dev/paho/files/jsdoc/Paho.MQTT.Client.html
    */ 

    // STATES  
    const username          = ref(null);
    const password          = ref(null);
    const host              = ref("mqtt.cimh.edu.bb");  // Host Name or IP address
    const port              = ref(443);                 // Port number
    const mqtt              = ref(new Paho.MQTT.Client( host.value ,port.value,"/mqtt", makeid(12) ));
    const payload           = ref(null); // Set initial values for payload
    const payloadTopic      = ref("");
    const subTopics         = shallowReactive(new Set([])); // "a","b","c"
    const dashboardTopic    = ref({"dashboard":""})
    const dashboardPayload  = ref(null);
    const connected         = ref(false);
    const subs              = reactive(new Set([]));
    const unsubs            = reactive(new Set([]));
 


    // ACTIONS
    
    const onSuccess = () => {
        // called when the connect acknowledgement has been received from the server.
        // console.log(`Connected to: ${host.value}`);      
    }

    const onConnected = (reconnect,URI) => {
        // called when a connection is successfully made to the server. after a connect() method.
        console.log(`Connected to: ${URI} , Reconnect: ${reconnect} `); 
        connected.value = true;  

        // let topics = toRaw(subTopics); 
        // topics.forEach( topic => {subs.add(topic); subTopics.delete(topic)} );
        let topics = toRaw(subs); 
        topics.forEach( topic => {subscribe(topic)} );

        if(reconnect){
            let topics = toRaw(subTopics); 
            topics.forEach( topic => {subs.add(topic); subTopics.delete(topic)} );
        }
        
    }
 
    const onConnectionLost = (response)=> {
        // called when a connection has been lost. after a connect() method has succeeded. 
        // Establish the call back used when a connection has been lost. The connection may be 
        // lost because the client initiates a disconnect or because the server or network cause 
        // the client to be disconnected. The disconnect call back may be called without the 
        // connectionComplete call back being invoked if, for example the client fails to connect. 
        if (response.errorCode !== 0) {
            console.log(`MQTT: Connection lost - ${response.errorMessage}`);
            connected.value = false;
        }
        }
  
    const onFailure = (response) => {
        // called when the connect request has failed or timed out.
        connected.value = false;
        const host = response.invocationContext.host;   
        console.log(`MQTT: Connection to ${host} failed. \nError message : ${response.errorMessage}`);    
        setTimeout(()=> { console.log("Retrying...."); connect()},5000)              
        };
    
    const onMessageArrived = (response) => {
           // called when a message has arrived in this Paho.MQTT.client.
           try {
                payload.value       = JSON.parse(response.payloadString); 
                payloadTopic.value  = response.destinationName;
                // console.log(`Topic : ${payloadTopic.value} \nPayload : ${response.payloadString}`);  
                // console.log(`Received new MQTT message,  Topic : ${payloadTopic.value}`);                   
            } 
           catch (error) {
                console.log(`onMessageArrived Error: ${error}`);
           }
            finally {
                
            }
        }
 
    

    // SUBCRIBE UTIL FUNCTIONS
    const sub_onSuccess = (response) => {   
        // called when the subscribe acknowledgement has been received from the server.          
        const topic = response.invocationContext.topic;  
        console.log(`MQTT: Subscribed  to - ${topic}`);   
        subTopics.add(topic);
        subs.delete(topic);
        }

    const sub_onFailure = (response) => {       
        // called when the subscribe request has failed or timed out.     
        // console.log(response)    
        const topic = response.invocationContext.topic;  
        console.log(`MQTT: Failed to subscribe to - ${topic} \nError message : ${response.errorMessage}`);   
        }

    const subscribe = (topic) => {
        // Subscribe for messages, request receipt of a copy of messages sent to the destinations described by the filter.
        console.log(`MQTT: Subscribing to - ${topic} `);
        try {
            var subscribeOptions = { onSuccess: sub_onSuccess, onFailure: sub_onFailure, invocationContext:{"topic":topic} }
            mqtt.value.subscribe(topic,subscribeOptions);   
        } catch (error) {
            console.log(`MQTT: Unable to Subscribe ${error} `);
        }
              
        }

    
    // UNSUBSCRIBE UTIL FUNCTIONS
    const unSub_onSuccess = (response) => {    
        // called when the unsubscribe acknowledgement has been received from the server.        
        const topic = response.invocationContext.topic;  
        // console.log(`MQTT: Unsubscribed from a topic `);      
         console.log(`MQTT: Unsubscribed from - ${topic}`);        
         subTopics.delete(topic);
         unsubs.delete(topic);
        }

    const unSub_onFailure = (response) => {   
        // called when the unsubscribe request has failed or timed out.        
        const topic = response.invocationContext.topic;  
        console.log(`MQTT: Failed to unsubscribe from - ${topic} \nError message : ${response.errorMessage}`);  
        // console.log(`MQTT: Failed to unsubscribe from a topic \nError message : ${response.errorMessage}`);  
        }

    const unsubscribe = (topic) => {     
        // Unsubscribe for messages, stop receiving messages sent to destinations described by the filter.      
        var unsubscribeOptions	 = { onSuccess: unSub_onSuccess, onFailure: unSub_onFailure, invocationContext:{"topic":topic} }
        mqtt.value.unsubscribe(topic, unsubscribeOptions);         
        }
    
    const unsubscribeAll = () => {   
        // Unsubscribe for messages, stop receiving messages sent to destinations described by the filter.      
        const topics = toRaw(subTopics);                 
        topics.values().forEach((topic)=>{ 
            var unsubscribeOptions	 = { onSuccess: unSub_onSuccess, onFailure: unSub_onFailure, invocationContext:{"topic":topic} }
            mqtt.value.unsubscribe(topic, unsubscribeOptions);
        });        
            
        disconnect();       
        }


    // PUBLISH UTIL FUNCTION
    const publish = (topic, payload) => { 
        const message           = new Paho.MQTT.Message(payload);
        message.destinationName = topic;
        mqtt.value.publish(message);                     
         }

    // DISCONNECT UTIL FUNCTION
    const disconnect = () => {  
        mqtt.value.disconnect();                     
        }
 

    const connect = () => {      
       try {
        console.log(`MQTT: Connecting to Server : ${host.value} Port : ${port.value},  USER: ${username.value} PASSWORD: ${password.value}` );
        // mqtt.value    = new Paho.MQTT.Client( host.value ,port.value,"/mqtt",IDstring );   
    
        var options   = {userName: username.value, password: password.value, timeout: 3, onSuccess: onSuccess, onFailure: onFailure, invocationContext: {"host":host.value,"port": port.value }, useSSL: true, reconnect: true, uris:[`ws://${host.value}:${port.value}/mqtt`] }; 
        
        mqtt.value.onConnectionLost   = onConnectionLost;
        mqtt.value.onMessageArrived   = onMessageArrived;
        mqtt.value.onConnected        = onConnected;
        mqtt.value.connect(options);    
       } catch (error) {
         console.log(error)
       }
                     
    };

    const isConnected = () => {
        return mqtt.value.isConnected()
     }

     const subTo = async (topic) => { 
        subs.add(topic)
     }

     const unsubTo = async (topic) => { 
        unsubs.add(topic)
     }

     const clearSubs = () => {
        subTopics.clear();
        subs.clear();
        unsubs.clear();
     }
    
 
    return {  
        
        mqtt,
        subs,
        unsubs,
        username,
        password,
        subTo,
        unsubTo,
        clearSubs,
        payload,
        subTopics,
        payloadTopic,
        dashboardTopic,
        dashboardPayload,
        isConnected,
        subscribe,
        unsubscribe,
        unsubscribeAll,
        publish,
        connect,
        connected,
        disconnect,
       }
},{ persist: true  });

 