// IMPORTS
importScripts("utils.js"); 

let ports = []

// WORKER
const onconnect = async (e) => {
  const port = e.ports[0]; 
  // console.log("CONNECTED TO PORT") 
  // console.log(e)
  // ports.push(port)
  

  port.onmessage = async(event) => {

    let msg = event.data;  
    const keys = Object.keys(msg) 
    let result = await getAllSites(msg["user"], msg["cookie"]);
    
 
    if(result['status'] == 'ok'){
       delete result["status"]; 

       /*
       if( keys.includes("selected")){
        if(!!msg["selected"]){  

          if(msg["role"] == "user"){ 
            let found = result["users"].filter( account => account.id == msg["selected"] );             
            if (found.length > 0) 
              result["selected"] = {...found[0]}
          }
          else { 
            let found = result["staffs"].filter( account => account.id == msg["selected"] );            
            if (found.length > 0)
              result["selected"] = {...found[0]}
          }
        }
       }*/

           
       port.postMessage(result);
    }
    else {
      port.postMessage([]);
    }
    
  }

  
};



// FUNCTIONS 
const getAllSites = async (userID, cookie) => { 
    // FETCH REQUEST WILL TIMEOUT AFTER 20 SECONDS
 
    let funcName        = "getAllSites";
    const form          = new FormData();   
    const URL           = '/api/all/sites';

    
    form.set("account", userID) 
            
    try {
        
        const [status, data] = await POST(URL, form, {  }, cookie );
 
        if(status){
                
        let keys        = Object.keys(data);
        if(keys.includes("status")){                    

            if(data["status"] == "ok"){         
                return   data; 
                // PUSH NOTIFICATION                   
            } 
            else if(data["status"] == "failed" ){                            
                // USER MUST SIGNIN FIRST                
                console.log("Request failed"); 
                return   data; 
                // PUSH NOTIFICATION
                    }    
            else if(data["status"] == "formErrors" ){                            
                // USER MUST SIGNIN FIRST
                console.log("Form Errors"); 
                return   data; 
                // PUSH NOTIFICATION
                    }  
        }
        }
        else {
            if(data == "unauthorized") {
                console.log(`${funcName}: Unauthorized User`);
                return "unauthorized"  // Empty object
            }
            else if(data == "token refreshed") {
                console.log(`${funcName}: Retrying in in 1 seconds`);
                setTimeout( () => { getAllSites(userID, cookie) } ,1000); 
            }
            else if(data == "unknown") {
                console.log(`${funcName}: Unknown response`);
                return "unknown"  // Empty object
            }
            else if(data == "aborted") {
                console.log(`${funcName}: Request aborted`);
                // PUSH NOTIFICATION 
                setTimeout( () => { getAllSites(userID, cookie,name)} ,5000); 
            }
        } 

        return "failed"
    }
    catch(err){  
    console.error(`${funcName} error: ${err.message}`);             
    }   


        }

self.addEventListener("connect", onconnect);

// NETWORK METHODS
/*
const GET = async ( URL) => {    

    // FETCH REQUEST WILL TIMEOUT AFTER 60 SECONDS 
    const controller    = new AbortController();
    const signal        = controller.signal;
    const id            = setTimeout(() => { controller.abort() },60000);
    
    try { 
        const response  = await fetch( URL , { method: 'GET', signal: signal, headers:{ }  });        
      
        let token = response.headers.get('X-Tokenized');
        // console.log(`Token? : ${token}`);
        
        if (response.status == 401) { 
                // UNAUTHORIZED. USER LOGGED OUT                
                return [false, "unauthorized"];
            }  
    
        else if(token == "Tokenized") {             
                // TOKEN REFRESHED
                console.log("TOKEN REFRESHED. RESENDING REQUEST");
                return [false,"token refreshed"];            
            }     
    
        else if(response.ok){             
            // REQUEST SUCCESSFUL. RETURN RESPONSE
            const data      = await response.json(); 
            return [true, data]
            }
    
        else {
            return [false, "unknown"];
        }
      }
    
    catch(err){
         
        if( err.message === "The user aborted a request."){
          console.log("REQUEST TIMEDOUT"); 
        } 
        return [false, "aborted"];
      }   
    
    }
    
    
    const POST = async ( URL, body, headers, cookie) => {    
    
      // FETCH REQUEST WILL TIMEOUT AFTER 60 SECONDS 
      const controller    = new AbortController();
      const signal        = controller.signal;
      const id            = setTimeout(() => { controller.abort() },60000);
    
    //   const cookie        = getCookie("csrf_access_token");  
      let allHeaders      = { "X-CSRF-TOKEN": cookie ,'Cookie': cookie, ...headers }
       
      try { 
         
          const response  = await fetch(URL,{ method: 'POST',body: body, signal: signal ,headers: allHeaders });  
          let token = response.headers.get('X-Tokenized');
          // console.log(`Token? : ${token}`);
    
        if (response.status == 401) { 
                // UNAUTHORIZED. USER LOGGED OUT                              
                return [false, "unauthorized"];
            }  
    
        else if(token == "Tokenized") {             
                // TOKEN REFRESHED
                console.log("TOKEN REFRESHED. RESENDING REQUEST");
                return [false,"token refreshed"];            
            }    
    
        else if(response.ok){             
            // REQUEST SUCCESSFUL. RETURN RESPONSE
            const data      = await response.json(); 
            return [true, data]
            }
    
        else {
            return [false, "unknown"];
        }
        }
    
      catch(err){
    
          console.error(`POST error: ${err.message}`);  
          if( err.message === "The user aborted a request."){
            console.log("REQUEST TIMEDOUT"); 
          } 
          return [false, "aborted"];
        } 
    
    }
*/    