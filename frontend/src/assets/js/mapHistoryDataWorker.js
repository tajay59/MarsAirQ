// IMPORTS
importScripts("utils.js"); 

// WORKER
self.addEventListener('message', async (e) => {
    let msg = e.data; 
    // console.log("WORKER RECEIVED: ", msg);
    // {"timestamp": timestamp,"param": "temperature","station":  selectedStation.value, "user": UserStore.getID}
    let param = msg["param"];
    // let timestamp = Math.floor(new Date().getTime() / 1000)
    let result = await getMapHistoryData(msg['timestamp'],msg['timestamp'], msg["param"], msg["station"], msg["user"], msg['cookie'])
    let month     = [];
    let threedays = [];
    let sevendays = [];

    if(!!result){
        let data = result["data"];  
        let three = new Date(result["three"]).getTime();
        let seven = new Date(result["seven"]).getTime();

        data.forEach(row => { 
          if (param in row){
              month.push({"x": row.timestamp, "y": parseFloat(row[param].toFixed(2))  });  

              if (row.timestamp >= three)
                  threedays.push({"x": row.timestamp, "y": parseFloat(row[param].toFixed(2))  });  
              if(row.timestamp >= seven)
                  sevendays.push({"x": row.timestamp, "y": parseFloat(row[param].toFixed(2))  });  
          }
          });  
    }

    this.self.postMessage({threedays, sevendays, month});
});



// FUNCTIONS
const getMapHistoryData = async (start,end, param, station, userID, cookie)=> {
    // FETCH REQUEST WILL TIMEOUT AFTER 20 SECONDS
    let funcName        = "getMapHistoryData";
    const form          = new FormData();   
    const URL           = '/api/map/data/history';

    form.set("id", station)
    form.set("account", userID)
    form.set("start", start)
    form.set("end", end)
    form.set("param", param)
    
    
    try {
      
      const [status, data] = await POST(URL, form, {  }, cookie );

      if(status){
              
        let keys        = Object.keys(data);
        if(keys.includes("status")){                    

          if(data["status"] === "found"){             
            return   data;                  
          } 
        }

      }
      else {
          if(data == "unauthorized") {
              console.log(`${funcName}: Unauthorized User`);
          }
          else if(data == "token refreshed") {
              console.log(`${funcName}: Retrying in in 1 seconds`);
              setTimeout( () => { getMapHistoryData(start,end, param, station, userID, cookie) } ,1000); 
          }
          else if(data == "unknown") {
              console.log(`${funcName}: Unknown response`);
          }
          else if(data == "aborted") {
              console.log(`${funcName}: Request aborted`);
              // PUSH NOTIFICATION 
              setTimeout( () => { getMapHistoryData(start,end, param, station, userID, cookie)} ,5000); 
          }
      } 
      
  }
  catch(err){  
    console.error(`${funcName} error: ${err.message}`);             
  }   

  return null
        }

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