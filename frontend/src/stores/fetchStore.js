import {defineStore} from 'pinia';
import {ref,computed, reactive} from 'vue'; 
import { useRoute, useRouter } from "vue-router"; 
import { useNotificationStore } from '@/stores/notificationStore';  
import { useUserStore} from '@/stores/userStore';



export const useFetchStore =  defineStore('fetch', () => {

    /*  
    The composition API way of defining a Pinia store
    ref() s become state properties
    computed() s become getters
    function() s become actions 
    */ 

    // ####################################### 
    // #               STATES                #  
    // #######################################  

    // VARIABLES 
    const NotificationStore   = useNotificationStore(); 
    const UserStore           = useUserStore(); 
    const router              = useRouter();
    const route               = useRoute(); 

    // STORE VARIABLES 

    // STATES
 

    // CONFIGURATIONS
 
  
    

    // ####################################### 
    // #               GETTERS               #  
    // #######################################   
 
 
    // ####################################### 
    // #               ACTIONS               #  
    // #######################################        

 
    const getCsrfToken = async ()=> {  
        const URL = "/api/csrf-token";    
        const response  = await fetch(URL);

        if(response.ok){
          const data        = await response.json(); 
          // csrf_token.value  = data.csrf_token;
        }
        else{
          console.error("Unable to Fetch new CSRF Token");
        }         
    }

 
 
const deleteAllCookies = ()=> {
  const cookies = document.cookie.split(";");

  for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i];
      const eqPos = cookie.indexOf("=");
      const name = eqPos > -1 ? cookie.substr(0, eqPos) : cookie;
      document.cookie = name + "=;expires=Thu, 01 Jan 1970 00:00:00 GMT";
  }
}


const localLogout = () => {  
  deleteAllCookies();  
}

const GET = async ( URL) => {    

  // FETCH REQUEST WILL TIMEOUT AFTER 60 SECONDS 
  const controller    = new AbortController();
  const signal        = controller.signal;
  const id            = setTimeout(() => { controller.abort() },60000);


  let user = UserStore.user
        
  if(user === undefined || user === null || !!!user){
      
      if(URL !== "/api/some/metradar/10") {
        controller.abort();        
      }    
      localLogout(); 
  }
 
  try { 
      const response  = await fetch( URL , { method: 'GET', signal: signal, headers:{ "X-User":UserStore.userType }  });
    //   const response  = await fetch(URL,{ method: 'POST',body: form_data, signal: signal ,headers: { "X-CSRF-TOKEN": cookie ,"X-User":UserStore.userType } });
    
    let token = response.headers.get('X-Tokenized');
    // console.log(`Token? : ${token}`);
    
    if (response.status == 401) { 
            // UNAUTHORIZED. USER LOGGED OUT

            // UPDATE PINIA STORES
            UserStore.clearUser();       
            deleteAllCookies();  
        
            // REDIRECT TO EXPLORE PAGE SINCE LOGOUT WAS SUCCESSFUL 
            if(!['Signup','PasswordReset','Login' ].includes(route.name)){
              setTimeout(() => { router.replace( { name:"Home"});},1000);
            }          
        
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

        // PUSH NOTIFICATION 
        NotificationStore.pushNotification("Request timed out"  ,"error","text-onError","flat","fas fa-triangle-exclamation","onError",true,2000);  
      } 
      return [false, "aborted"];
    }   

}
 
const POST = async ( URL, body, headers) => {    

    // FETCH REQUEST WILL TIMEOUT AFTER 60 SECONDS 
    const controller    = new AbortController();
    const signal        = controller.signal;
    const id            = setTimeout(() => { controller.abort() },60000);

    const cookie        = UserStore.getCookie("csrf_access_token"); 
    // console.log("COOKIE", cookie);
    let allHeaders      = { "X-CSRF-TOKEN": cookie ,"X-User": UserStore.userType, ...headers }

    let user = UserStore.user
    
    if(['/api/get/signup/entities'].includes(URL)){
      //Allow on Signup routes
    }
    else if(user === undefined || user === null || !!!user){
        controller.abort();
        localLogout();
    }
   
    try { 
       
        const response  = await fetch(URL,{ method: 'POST',body: body, signal: signal ,headers: allHeaders });  
        let token = response.headers.get('X-Tokenized');
        // console.log(`Token? : ${token}`);

      if (response.status == 401) { 
              // UNAUTHORIZED. USER LOGGED OUT
  
              // UPDATE PINIA STORES
              UserStore.clearUser();       
              deleteAllCookies();  
          
              // REDIRECT TO EXPLORE PAGE SINCE LOGOUT WAS SUCCESSFUL 
              if(!['Signup','PasswordReset','Login' ].includes(route.name)){
                setTimeout(() => { router.replace( { name:"Home"});},1000);
              }
          
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
  
          // PUSH NOTIFICATION 
          NotificationStore.pushNotification("Request timed out"  ,"error","text-onError","flat","fas fa-triangle-exclamation","onError",true,2000);  
        } 
        return [false, "aborted"];
      } 
  
  }

const getFile = async (URL, body, headers, name) => {
    // FETCHES ALL PRODUCTS TYPES(MET,RAD,PRO,MISC,EQUIP, SUPP) ETC IN SYSTEM
    // RETURNS PAGE COUNT FOR ALL PRODUCT TYPES (MET, RAD, PRO, MISC, EQUIP, SUPP)
    // LOADS FIRST PAGE FOR SEARCH RESULT BY INVOKING getCurrentPage(); 
    
    const controller    = new AbortController();
    const signal        = controller.signal;
    const id            = setTimeout(()=>{controller.abort()},60000); // FETCH REQUEST WILL TIMEOUT AFTER 60 SECONDS 

    const cookie        = UserStore.getCookie("csrf_access_token"); 
    let allHeaders      = { "X-CSRF-TOKEN": cookie ,"X-User": UserStore.userType, ...headers } 

    try {
        
        const response  = await fetch(URL,{ method: 'POST',body: body, signal: signal ,headers: allHeaders });  
   
        if (response.ok){ 
            const blob      = await response.blob();
            const fileName = `${name}.pdf`;

            //Check the Browser type and download the File.
            var isIE = false || !!document.documentMode;
            if (isIE) {
                console.log("SUPPORTS");
                window.navigator.msSaveBlob(blob, fileName);
            } else {
                console.log("NOT SUPPORTS");
                var url   = window.URL || window.webkitURL;
                var link  = url.createObjectURL(blob);
                var a     = document.createElement("a");
                a.setAttribute("download", fileName);
                a.setAttribute("href", link);
                document.body.appendChild(a);
                a.click();
                document.body.removeChild(a);
            }
            
                              
            
        }
        else{
                     
            const data      = await response.text();
            console.warn(" un auth",data);
            setTimeout( ()=>{ getPageCountForTypes()} ,5000);  

            if(data.includes("Unauthorized")){
              console.log("NEED TO REFRESH CSRF TOKEN");
              UserStore.userLogout();
                   

            }

          }

    }
    catch(err){  
    console.error('downloadFile error: ', err.message);   
    setTimeout( ()=>{ downloadFile()} ,5000);         
    }   
     
}


    return { 
      localLogout ,
      GET, 
      POST,
      getCsrfToken,
      getFile
    }
},{persist: true});

 