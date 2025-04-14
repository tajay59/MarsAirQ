import {defineStore} from 'pinia'
import {ref,computed, reactive} from 'vue' 
import { useNotificationStore } from '@/stores/notificationStore'; 
import { useRoute, useRouter } from "vue-router";
import { useFetchStore } from '@/stores/fetchStore'; 
import { useMqttStore} from '@/stores/mqttStore';


export const useUserStore =  defineStore('user', ()=>{

    /*  
    The composition API way of defining a Pinia store
    ref() s become state properties
    computed() s become getters
    function() s become actions 
    */ 

    // VARIABLES  
    const NotificationStore   = useNotificationStore();
    const FetchStore          = useFetchStore(); 
    const Mqtt                = useMqttStore();
    const router              = useRouter();
    const route               = useRoute(); 

    // ####################################### 
    // #               STATES                #  
    // ####################################### 

    const loggedIn          = ref(false);
    const user              = ref("");
    const userType          = ref("external");
    const email             = ref("");
    const role              = ref("");
    const id                = ref("");
    const suball            = ref(false);
    const csrf_token        = ref("");
    const account           = ref({"firstname":"John","lastname":"Doe","email":"jd@gmail.com"}); 
    const mqtt_sub_credentials = ref(null);
    const image             = ref("");
    const selected          = ref({});
    const barcodes          = ref([]);
    const currency          = ref(false); 
    const selectedStation   = ref(null);
    const siteLoading       = ref(false);
    const userSites         = ref([]);

    // CONFIGURATIONS
    const modelTab          = ref("");
    const darkmode          = ref(false);
    const resetPasswordPage = ref(0);
    const resetTimer        = ref(0); 

    // FUNCTIONS
    const capitalize  = (phrase) => {
          let words = phrase.split(" ");
          let result = "";
          if(!!phrase){
            words.forEach( word => {
              result += word[0].toUpperCase() + word.substring(1)
          });
          }
          return result;
      }

    const setSelectedStation = (station) => {
      selectedStation.value = station;
    }
    // ####################################### 
    // #               GETTERS               #  
    // #######################################  
    const getSelectedStation = computed( ()=>{           
      return selectedStation.value;
  });

    const GetCSRFToken = computed( ()=>{           
        return csrf_token.value;
    });

    const getID = computed(()=>{ return id.value;})

    const getCookie = computed(()=>{
        // Since getters do not take arguments a dynamic getter should be used instead
        // This is a dynamic getter, which is a function that returns another function
        // The returned function takes an argument, which is the only way a getter can 
        // take an argument
        return (cname)=> {
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
            }
    });

    const setSelectedItem = computed(()=>{
      // THIS IS A DYNAMIC GETTER
      return (item, barcode)=>{
          selected.value = item;
          barcodes.value = barcode;
      }
  }); 


    // ####################################### 
    // #               ACTIONS               #  
    // #######################################  

    const getStatus = ()=>{
        if(!loggedIn.value){
            console.log("PINIA STORE SAYS YOUR NOT LOGGED IN")
        }
    }

    const clearUser = ()=>{
       loggedIn.value          = false;
       user.value              = "";
       userType.value          = "external";
       email.value             = "";
       role.value              = "";
       id.value                = "";
  }

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

    const Auth = async ()=> {
      // DO NOT DELETE THIS AUTH IN PRODUCTION EVEN THO ANOTHER ONE EXIST IN index.js
      // FETCH REQUEST WILL TIMEOUT AFTER 20 SECONDS 

      let funcName        = "Auth"; 
      const URL           = '/api/status';
      
  
      try {
         
          const [status, data] = await FetchStore.GET(URL);  
          
          if(status){
                
            let keys        = Object.keys(data);          
            // console.log(data);
    
            if (keys.includes("status")){
    
                if (data["status"] === "Authorized"){
                  //User is already logged in                
                   
                  loggedIn.value  = true 
                  role.value      = data["role"]
                  user.value      = data["user"]   
                  id.value        = data["id"]              
                } 
               
                else{               
                  loggedIn.value  = false 
                  role.value      = ""
                  user.value      = "" 
                  id.value        = ""  
                }
            }
          }
          else {
              if(data == "unauthorized") {
                  console.log(`${funcName}: Unauthorized User`);
              }
              else if(data == "token refreshed") {
                  console.log(`${funcName}: Retrying in in 1 seconds`);
                  setTimeout( () => { Auth() } ,1000); 
              }
              else if(data == "unknown") {
                  console.log(`${funcName}: Unknown response`);
              }
              else if(data == "aborted") {
                  console.log(`${funcName}: Request aborted`);
                  // PUSH NOTIFICATION 
                  // NotificationStore.pushNotification("Re-trying in 5 seconds" ,"secondary","text-onSecondary","flat","fas fa-triangle-exclamation","onSecondary",true,3000); 
                  setTimeout( () => { Auth()} ,5000); 
              }
          } 
      }
      catch(err){
        console.error(`${funcName} error: ${err.message}`);     
      }      
  
  }

  const getAccount = async ()=> {
    // FETCH REQUEST WILL TIMEOUT AFTER 20 SECONDS     
    let funcName        = "getAccount";   
    const URL           = `/api/user/${id.value}`;    
   

    try {
         
        const [status, data] = await FetchStore.GET(URL);  
        
        if(status){
          let keys        = Object.keys(data);

          if(keys.includes("status")){

              if(data["status"] == "found" ){
                      // products.value  = [];  // EMPTY THE LIST                                               
                      account.value = data["data"]                            
                  }
              if(data["status"] == "not found" ){
                      // products.value  = [];  // EMPTY THE LIST                                               
                      console.log("Account Not Found")                           
                  }
          }    
    
        }
        else {
            if(data == "unauthorized") {
                console.log(`${funcName}: Unauthorized User`);
            }
            else if(data == "token refreshed") {
                console.log(`${funcName}: Retrying in in 1 seconds`);
                setTimeout( () => { getAccount() } ,1000); 
            }
            else if(data == "unknown") {
                console.log(`${funcName}: Unknown response`);
            }
            else if(data == "aborted") {
                console.log(`${funcName}: Request aborted`);
                // PUSH NOTIFICATION 
                // NotificationStore.pushNotification("Re-trying in 5 seconds" ,"secondary","text-onSecondary","flat","fas fa-triangle-exclamation","onSecondary",true,3000); 
                setTimeout( () => { getAccount()} ,5000); 
            }
        } 
    }
    catch(err){     
      console.error(`${funcName} error: ${err.message}`);       
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
  clearUser();     
  deleteAllCookies();  
}

const userLogout = async () => {
  // COLLECT USER INPUT FROM LOGIN FORM THEN POST TO FLASK API
  
  // let Loader      = document.querySelector("#loader");
  const address       = '/api/logout';

  // FETCH REQUEST WILL TIMEOUT AFTER 20 SECONDS 
  const controller    = new AbortController();
  const signal        = controller.signal;
  const id            = setTimeout(()=>{controller.abort()},60000);



  try {
      const response  = await fetch(address,{ method: 'GET', signal: signal  });
      const data      = await response.json();
      let keys        = Object.keys(data);
    
    if (response.status == 401) { 
      
          if(keys.includes("message")){
            //console.log(data);
            if( data['message'] === "loggedOut" ) {   

                // PUSH NOTIFICATION              message,color,      textColor,      variant, icon,                 iconColor,   state
                NotificationStore.pushNotification("Logged out!","secondary","text-onSecondary","flat","fas fa-circle-check","onSecondary",true,2000); 

                // UPDATE PINIA STORES
                clearUser();      
                deleteAllCookies(); 
                    mqtt_sub_credentials.value = null;
                    Mqtt.username = null;
                    Mqtt.password = null;
                    Mqtt.unsubscribeAll();
           
                // REDIRECT TO EXPLORE PAGE SINCE LOGOUT WAS SUCCESSFUL 
                setTimeout(()=>{ router.replace( { name:"Home"});},1000);
                
            }                                    
            else{             
                // PUSH NOTIFICATION 
                NotificationStore.pushNotification( "Unable to logout" ,"error","text-onError","flat","fas fa-triangle-exclamation","onError",true,2000);  
            }
        
        }
        else{              
            // PUSH NOTIFICATION 
            // NotificationStore.pushNotification( "Unable to logout"  ,"error","text-onError","flat","fas fa-triangle-exclamation","onError",true,2000);  
             // UPDATE PINIA STORES
             clearUser();      
             deleteAllCookies(); 
        
             // REDIRECT TO EXPLORE PAGE SINCE LOGOUT WAS SUCCESSFUL 
             setTimeout(()=>{ router.replace( { name:"Home"});},1000);
        }
    }                                        
    else {             
      // PUSH NOTIFICATION 
      NotificationStore.pushNotification( "Unable to logout" ,"error","text-onError","flat","fas fa-triangle-exclamation","onError",true,2000);  
  }

    }
    catch(err){
       
      if( err.message === "The user aborted a request."){
          console.log("REQUEST TIMEDOUT");
              // UPDATE PINIA STORE
              loggedIn.value  = false;
              user.value      = "";

              // PUSH NOTIFICATION 
              NotificationStore.pushNotification("Request timed out"  ,"error","text-onError","flat","fas fa-triangle-exclamation","onError",true,2000);  
      }
      // console.error('Logout error: ', err.message);    
      
    }   

}

const getAllSites = async () => { 
  // FETCH REQUEST WILL TIMEOUT AFTER 20 SECONDS 
  siteLoading.value   = true;
  let funcName        = "getAllSites";
  const form          = new FormData();   
  const URL           = '/api/all/sites';    
  
  form.set("account", id.value)   
          
  try {
      
      const [status, data] = await FetchStore.POST(URL, form, {  } );
      siteLoading.value   = false;
  
      if(status){
              
      let keys        = Object.keys(data);
      if(keys.includes("status")){                    

          if(data["status"] == "ok"){    
            userSites.value = data["sites"];     
            suball.value = data["suball"];  
              
              // PUSH NOTIFICATION                   
          } 
          else if(data["status"] == "failed" ){                            
              // USER MUST SIGNIN FIRST                
              console.log("Request failed"); 
              
              // PUSH NOTIFICATION
                  }    
          else if(data["status"] == "formErrors" ){                            
              // USER MUST SIGNIN FIRST
              console.log("Form Errors"); 
          
              // PUSH NOTIFICATION
                  }  
      }
      }
      else {
          if(data == "unauthorized") {
              console.log(`${funcName}: Unauthorized User`);
              // return "unauthorized"  // Empty object
          }
          else if(data == "token refreshed") {
              console.log(`${funcName}: Retrying in in 1 seconds`);
              setTimeout( () => { getAllSites() } ,1000); 
          }
          else if(data == "unknown") {
              console.log(`${funcName}: Unknown response`);
              // return "unknown"  // Empty object
          }
          else if(data == "aborted") {
              console.log(`${funcName}: Request aborted`);
              // PUSH NOTIFICATION 
              setTimeout( () => { getAllSites()} ,5000); 
          }
      } 

      
  }
  catch(err){  
  console.error(`${funcName} error: ${err.message}`);             
  }   


      }

const getUserSuball = async () => { 
    // FETCH REQUEST WILL TIMEOUT AFTER 20 SECONDS 
    siteLoading.value   = true;
    let funcName        = "getUserSuball";
    const form          = new FormData();   
    const URL           = '/api/get/suball';    
    
    form.set("account", id.value)   
            
    try {
        
        const [status, data] = await FetchStore.POST(URL, form, {  } );
        siteLoading.value   = false;
    
        if(status){
                
        let keys        = Object.keys(data);
        if(keys.includes("status")){                 
  
            if(data["status"] == "ok"){    
                suball.value = data["suball"];                 
            } 
        }
        }
        else {
            if(data == "unauthorized") {
                console.log(`${funcName}: Unauthorized User`);
                // return "unauthorized"  // Empty object
            }
            else if(data == "token refreshed") {
                console.log(`${funcName}: Retrying in in 1 seconds`);
                setTimeout( () => { getUserSuball() } ,1000); 
            }
            else if(data == "unknown") {
                console.log(`${funcName}: Unknown response`);
                // return "unknown"  // Empty object
            }
            else if(data == "aborted") {
                console.log(`${funcName}: Request aborted`);
                // PUSH NOTIFICATION 
                setTimeout( () => { getUserSuball()} ,5000); 
            }
        } 
  
        
    }
    catch(err){  
    console.error(`${funcName} error: ${err.message}`);             
    }   
  
  
        }
    // INIT
    // getCsrfToken();

    return {
      loggedIn,
      email,
      role,
      user,
      id,
      getCookie,
      getID,
      userType,
      account, 
      image,
      suball,
      selected,
      setSelectedItem,
      barcodes,
      modelTab,
      GetCSRFToken,
      darkmode,
      resetPasswordPage,
      resetTimer,
      selectedStation,
      getSelectedStation,
      mqtt_sub_credentials,
      userSites,
      getUserSuball,
      getAllSites,
      setSelectedStation,
      localLogout,
      capitalize,
      getAccount, 
      Auth,
      userLogout,
      clearUser,
      getStatus,
      getCsrfToken}
},{persist: true});

 