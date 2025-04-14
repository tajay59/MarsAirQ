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
    // let p = event.ports;
    // console.log(p)
    // console.log(msg);   
    const keys = Object.keys(msg) 
    let result = await getAccounts(msg["user"], msg["cookie"]);
    
    // let {newRegistrations, staffs, users} = []
   
    if(result['status'] == 'ok'){
       delete result["status"]; 

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
       }

      // console.log(result)
        
       port.postMessage(result);
    }
    
  }

  
};

const caribbeanCountries = [
  {
    name: "Antigua and Barbuda",
    icon:"emojione-v1:flag-for-antigua-and-barbuda",
    center: {
      latitude: 17.0608,
      longitude: -61.7964
    }
  },
  {
    name: "Bahamas",
    icon:"emojione-v1:flag-for-bahamas",
    center: {
      latitude: 25.0239,
      longitude: -77.3963
    }
  },
  {
    name: "Barbados",
    icon:"emojione-v1:flag-for-barbados",
    center: {
      latitude: 13.1939,
      longitude: -59.5431
    }
  },
  {
    name: "Belize",
    icon:"emojione-v1:flag-for-belize",
    center: {
      latitude: 17.2510,
      longitude: -88.7719
    }
  },
  {
    name: "Cuba",
    icon:"emojione-v1:flag-for-cuba",
    center: {
      latitude: 21.5217,
      longitude: -77.7812
    }
  },
  {
    name: "Dominica",
    icon:"emojione-v1:flag-for-dominica",
    center: {
      latitude: 15.4150,
      longitude: -61.3710
    }
  },
  {
    name: "Dominican Republic",
    icon:"emojione-v1:flag-for-dominican-republic",
    center: {
      latitude: 19.1940,
      longitude: -70.6667
    }
  },
  {
    name: "Grenada",
    icon:"emojione-v1:flag-for-grenada",
    center: {
      latitude: 12.1165,
      longitude: -61.6790
    }
  },
  {
    name: "Guyana",
    icon:"emojione-v1:flag-for-guyana",
    center: {
      latitude: 4.9387,
      longitude: -58.9310
    }
  },
  {
    name: "Haiti",
    icon:"emojione-v1:flag-for-haiti",
    center: {
      latitude: 18.9712,
      longitude: -72.2852
    }
  },
  {
    name: "Jamaica",
    icon:"emojione-v1:flag-for-jamaica",
    center: {
      latitude: 18.1096,
      longitude: -77.2975
    }
  },
  {
    name: "Saint Kitts and Nevis",
    icon:"emojione-v1:flag-for-st-kitts-and-nevis",
    center: {
      latitude: 17.3571,
      longitude: -62.7829
    }
  },
  {
    name: "Saint Lucia",
    icon:"emojione-v1:flag-for-st-lucia",
    center: {
      latitude: 13.9094,
      longitude: -60.9789
    }
  },
  {
    name: "Saint Vincent and the Grenadines",
    icon:"emojione-v1:flag-for-st-vincent-and-grenadines",
    center: {
      latitude: 13.2541,
      longitude: -61.2072
    }
  },
  {
    name: "Suriname",
    icon:"emojione-v1:flag-for-suriname",
    center: {
      latitude: 3.9190,
      longitude: -56.0278
    }
  },
  {
    name: "Trinidad and Tobago",
    icon:"emojione-v1:flag-for-trinidad-and-tobago",
    center: {
      latitude: 10.6918,
      longitude: -61.2225
    }
  }
];



/*
self.addEventListener('message', async (e) => {
    let msg = e.data; 
    // console.log("WORKER RECEIVED: ", msg);
    // {"timestamp": timestamp,"param": "temperature","station":  selectedStation.value, "user": UserStore.getID}
    let param = msg["param"];
    // let timestamp = Math.floor(new Date().getTime() / 1000)
    let result = await getMapHistoryData(msg['timestamp'],msg['timestamp'], msg["param"], msg["station"], msg["user"], msg['cookie'])
    let data = result["data"];  
    let three = new Date(result["three"]).getTime();
    let seven = new Date(result["seven"]).getTime();
    let month     = [];
    let threedays = [];
    let sevendays = [];

    data.forEach(row => { 
        if (param in row){
            month.push({"x": row.timestamp, "y": parseFloat(row[param].toFixed(2))  });  

            if (row.timestamp >= three)
                threedays.push({"x": row.timestamp, "y": parseFloat(row[param].toFixed(2))  });  
            if(row.timestamp >= seven)
                sevendays.push({"x": row.timestamp, "y": parseFloat(row[param].toFixed(2))  });  
        }
        });  

    this.self.postMessage({threedays, sevendays, month});
});
*/


const print = () => {
  console.log("PRINTING......")
}
// FUNCTIONS
const getAccounts = async (userID, cookie) => {
    // FETCH REQUEST WILL TIMEOUT AFTER 20 SECONDS
    let funcName        = "getAccounts";
    const form          = new FormData();   
    const URL           = '/api/all/accounts';

    form.set("account", userID)     
    
    try {
      
      const [status, data] = await POST(URL, form, {  }, cookie );

      if(status){
              
        let keys        = Object.keys(data);
        if(keys.includes("status")){                    

          if(data["status"] === "ok"){              
            
            return   data; 
            // PUSH NOTIFICATION                   
          }
          if(data["status"] == "failed" ){                            
            // USER MUST SIGNIN FIRST
            console.log("Found NO Results"); 
            // PUSH NOTIFICATION
                    }    
          if(data["status"] == "formErrors" ){                            
            // USER MUST SIGNIN FIRST
            console.log("Form Errors"); 
            // PUSH NOTIFICATION
                    }  
        }
      }
      else {
          if(data == "unauthorized") {
              console.log(`${funcName}: Unauthorized User`);
          }
          else if(data == "token refreshed") {
              console.log(`${funcName}: Retrying in in 1 seconds`);
              setTimeout( () => { getAccounts(userID, cookie) } ,1000); 
          }
          else if(data == "unknown") {
              console.log(`${funcName}: Unknown response`);
          }
          else if(data == "aborted") {
              console.log(`${funcName}: Request aborted`);
              // PUSH NOTIFICATION 
              setTimeout( () => { getAccounts(userID, cookie)} ,5000); 
          }
      } 
  }
  catch(err){  
    console.error(`${funcName} error: ${err.message}`);             
  }   

  return []
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