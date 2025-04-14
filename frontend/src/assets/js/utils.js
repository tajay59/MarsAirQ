const getCookie = (cname) => { 
      
        // REQUIRED TO GET JWT CSRF COOKIE, OTHERWISE ACCESS TO PROTECTED ROUTES WILL FAIL
        let name = cname + "=";
        let ca = document.cookie.split(';');
        for(let i = 0; i < ca.length; i++) {
        let c = ca[i];
        while (c.charAt(0) == ' ') {
            c = c.substring(1);
        }
        if (c.indexOf(name) == 0) {
            return c.substring(name.length, c.length);
        }
        }
        return "";
          
    };

const deleteAllCookies = ()=> {
        const cookies = document.cookie.split(";");
      
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i];
            const eqPos = cookie.indexOf("=");
            const name = eqPos > -1 ? cookie.substr(0, eqPos) : cookie;
            document.cookie = name + "=;expires=Thu, 01 Jan 1970 00:00:00 GMT";
        }
      }

      /*
export const GET = async ( URL) => {    

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
                deleteAllCookies();              
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
  
  
export const POST = async ( URL, body, headers) => {    
  
      // FETCH REQUEST WILL TIMEOUT AFTER 60 SECONDS 
      const controller    = new AbortController();
      const signal        = controller.signal;
      const id            = setTimeout(() => { controller.abort() },60000);
  
      const cookie        = getCookie("csrf_access_token");  
      let allHeaders      = { "X-CSRF-TOKEN": cookie , ...headers }
       
      try { 
         
          const response  = await fetch(URL,{ method: 'POST',body: body, signal: signal ,headers: allHeaders });  
          let token = response.headers.get('X-Tokenized');
          // console.log(`Token? : ${token}`);
  
        if (response.status == 401) { 
                // UNAUTHORIZED. USER LOGGED OUT      
                deleteAllCookies();                          
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

    // NETWORK METHODS
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
    