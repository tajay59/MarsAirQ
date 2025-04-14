import {defineStore} from 'pinia';
import { useUserStore } from './userStore';
import { useFetchStore } from '@/stores/fetchStore'; 
import {ref, reactive, computed} from 'vue'


export const useAppStore =  defineStore('app', ()=>{

    /*  
    The composition API way of defining a Pinia store
    ref() s become state properties
    computed() s become getters
    function() s become actions  
    */ 

    //VARIBLES
    const UserStore = useUserStore();
    const FetchStore          = useFetchStore(); 

    // STATES 
    const appDarkMode   = ref(false);
    const drawerItems   = ref([ 
        {"icon":"mdi:mdi-google-maps","title":"Map","route":"/analytics/map","name":"Map"},  
        {"icon":"mdi:mdi-play","title":"Live","route":"/analytics/live","name":"Live"},  
        {"icon":"mdi:mdi-view-dashboard","title":"Dashboard","route":"/analytics/dashboard","name":"Dashboard"},  
        {"icon":"mdi:mdi-chart-timeline-variant-shimmer","title":"Analysis","route":"/analytics/analysis","name":"Analysis"},  
    ])

    const routeItems   = ref([
        {"icon":"mdi:mdi-lock","title":"Research","route":"/research","name":"Research"},  
        {"icon":"mdi:mdi-lock","title":"Analytics","route":"/analytics/map","name":"Analytics"},   
        {"icon":"mdi:mdi-lock","title":"Admin","route":"/admin","name":"Admin"},   
    ])

    const month             = ref([]);
    const threedays         = ref([]);
    const sevendays         = ref([]);
    

    // ADMIN VARIABLES
    const newRegistrations  = ref([]);
    const staffs            = ref([]);
    const users             = ref([]);
    const selectedAccount   = ref(null);
    const selectedAccEdited = ref(null);
    const aodLoading        = ref(false);
    const removeAccLoading  = ref(false);
    const updateAccLoading  = ref(false);
    const updateSiteLoading = ref(false);
    const createSiteLoading = ref(false);
    const createDeviceLoading = ref(false);
    const updateDeviceLoading = ref(false);
    const deleteDeviceLoading = ref(false);
    const historyLoading = ref(false);
    const accSearchLoading  = ref(false);
    const assignUserLoading  = ref(false);
    const siteLoading       = ref(false);
    const edit              = ref(false); // Edit user account details
    const userSearch        = ref({"text":"","result":[]})
    const sites             = ref([]);
    const sitePages         = ref({"count": 0,"page":1,"pages":{}});
    const siteSearchPages   = ref({"count": 0,"search":"","page":1,"pages":{}});
    const paramDetails      = ref({
        "temperature":{"units":"°C", "icon":"fluent:temperature-20-regular"},
        "humidity":{"units":"%", "icon":"material-symbols:humidity-percentage-rounded"},
        "pressure":{"units":"hPa", "icon":"lets-icons:pressure-light"},
        "altitude":{"units":"ft", "icon":"material-symbols-light:altitude-rounded"},
        "voc":{"units":"ppm", "icon":"material-symbols-light:air-rounded"},
        "vocindex":{"units":"", "icon":"ic:baseline-gpp-good"},
        "co2": {"units":"ppm","icon":"iwwa:co2"},
        "pm2": {"units":"ppm","icon":"fluent:dust-28-regular"},
        "pm10": {"units":"ppm","icon":"fluent:dust-24-filled"},
    });
    const emailList         = reactive({registration:[], cancellation:[]});
    const allStaffAccounts  = ref([]);
    const spss              = ref(null); // Sites page selected site
    const assignListAdmin   = ref([]); // LIST OF STAFF NAMES USED FOR SELECT COMPONENT ON THE /ADMIN ROUTE
    
    const site              = ref(null);
    const device            = ref(null);
  


    // ACTIONS
    const setThree = (data) => threedays.value = data;
    const setSeven = (data) => sevendays.value = data;
    const setMonth = (data) => month.value = data;

    const resetGraphData = () => {
        threedays.value = [];
        sevendays.value = [];
        month.value     = [];
    }

    
 
	
    const getData = async (start,end) => {
        // FETCH REQUEST WILL TIMEOUT AFTER 20 SECONDS
        const controller = new AbortController();
        const signal = controller.signal;
        const id = setTimeout(()=>{controller.abort()},60000);
        const URL = `/api/data/${start}/${end}`;
        try {
            const response = await fetch(URL,{ method: 'GET', signal: signal });
            if (response.ok){
                const data = await response.json();
                let keys = Object.keys(data);
                if(keys.includes("status")){
                    if(data["status"] == "found" ){
                        // console.log(data["data"] )
                        return data["data"];
                    }
                    if(data["status"] == "failed" ){
                        console.log("No data returned");
                    }
                }
            }
            else{
            const data = await response.text();
            console.log(data);
            }
        }
        catch(err){
            console.error('getData error: ', err.message);
        }
        return []
        }
          

    const getMapHistoryData = async (start,end, param)=> {
        // FETCH REQUEST WILL TIMEOUT AFTER 20 SECONDS
        let funcName        = "getMapHistoryData";
        const form          = new FormData();   
        const URL           = '/api/map/data/history';
  
        form.set("id", UserStore.getSelectedStation)
        form.set("account", UserStore.getID)
        form.set("start", start)
        form.set("end", end)
        form.set("param", param)
                
        try {
          
          const [status, data] = await FetchStore.POST(URL, form, {  } );
  
          if(status){
                  
            let keys        = Object.keys(data);
            if(keys.includes("status")){                    
  
              if(data["status"] === "found"){         
                return   data["data"]; 
                // PUSH NOTIFICATION                   
              }
              if(data["status"] == "failed" ){                            
                // USER MUST SIGNIN FIRST                
                console.log("Found NO Results"); 
                return {}  // Empty object
                // PUSH NOTIFICATION
                        }    
              if(data["status"] == "formErrors" ){                            
                // USER MUST SIGNIN FIRST
                console.log("Form Errors"); 
                return {}  // Empty object
                // PUSH NOTIFICATION
                        }  
            }
          }
          else {
              if(data == "unauthorized") {
                  console.log(`${funcName}: Unauthorized User`);
                  return {}  // Empty object
              }
              else if(data == "token refreshed") {
                  console.log(`${funcName}: Retrying in in 1 seconds`);
                  setTimeout( () => { getMapHistoryData(start,end, param) } ,1000); 
              }
              else if(data == "unknown") {
                  console.log(`${funcName}: Unknown response`);
                  return {}  // Empty object
              }
              else if(data == "aborted") {
                  console.log(`${funcName}: Request aborted`);
                  // PUSH NOTIFICATION 
                  setTimeout( () => { getMapHistoryData(start,end, param)} ,5000); 
              }
          } 
      }
      catch(err){  
        console.error(`${funcName} error: ${err.message}`);             
      }   

      return {}  // Empty object
            }

    //ADMIN GETTERS AND SETTERS

    const setPage = (page) => {
        sitePages.value.page = page;
    }

    const setDevice = (dev) => {
        device.value = {...dev};
    }

    const resetDevice = () => {
        device.value = null;
    }

    const setAdminAccountVariables = (name, data) => {
        if(name == "newRegistrations")
            newRegistrations.value = data;
        if(name =="staffs")
            staffs.value = data;
        if(name == "users")
            users.value = data;
    }

    const setSelectedAccount = (account) => {
        selectedAccount.value = {...account};
        selectedAccEdited.value = {...account};
        edit.value = false;
    }

    const setSPSS = (site) => {
        spss.value = {...site};
    }

    const setSite = (data) => {
        site.value = {...data};
    }

    const resetSite = () => {
        site.value = null;
    }

    const emailSelectedItem = computed(()=>{
        if(allStaffAccounts.value.length > 0){
            return allStaffAccounts.value.map((account)  =>  { return {'name':`${UserStore.capitalize(account.firstname) } ${UserStore.capitalize(account.lastname) }`,'value': account.id} });
        }
        return []        
        });  

    const setSites = (data) => {
        if(!!data){
            sites.value = data;
        }
        else {
            sites.value = []; 
        }
    }

    const clearSelectedAccount = () => {
        selectedAccount.value = null;
        selectedAccEdited.value = null;
    }

    const approveOrDenyRequest = async (id, decision)=> {
        // FETCH REQUEST WILL TIMEOUT AFTER 20 SECONDS
        aodLoading.value    = true;
        let funcName        = "approveOrDenyRequest";
        const form          = new FormData();   
        const URL           = '/api/aod';
  
        form.set("id", id)
        form.set("account", UserStore.getID)
        form.set("decision", decision) 
                
        try {
          
          const [status, data] = await FetchStore.POST(URL, form, {  } );
          aodLoading.value    = false;

          if(status){
                  
            let keys        = Object.keys(data);
            if(keys.includes("status")){                    
  
              if(data["status"] == "approved"){         
                return   data["status"]; 
                // PUSH NOTIFICATION                   
              }
              else if(data["status"] == "denied"){         
                return   data["status"]; 
                // PUSH NOTIFICATION                   
              }
             else if(data["status"] == "failed" ){                            
                // USER MUST SIGNIN FIRST                
                console.log("Request failed"); 
                return   data["status"]; 
                // PUSH NOTIFICATION
                        }    
            else if(data["status"] == "formErrors" ){                            
                // USER MUST SIGNIN FIRST
                console.log("Form Errors"); 
                return   data["status"]; 
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
                  setTimeout( () => { approveOrDenyRequest(id, decision) } ,1000); 
              }
              else if(data == "unknown") {
                  console.log(`${funcName}: Unknown response`);
                  return "unknown"  // Empty object
              }
              else if(data == "aborted") {
                  console.log(`${funcName}: Request aborted`);
                  // PUSH NOTIFICATION 
                  setTimeout( () => { approveOrDenyRequest(id, decision)} ,5000); 
              }
          } 

          return "failed"
      }
      catch(err){  
        console.error(`${funcName} error: ${err.message}`);             
      }   

   
            }

    const removeAccount = async () => {
        // FETCH REQUEST WILL TIMEOUT AFTER 20 SECONDS
        removeAccLoading.value = true; 
        let funcName        = "removeAccount";
        const form          = new FormData();   
        const URL           = '/api/remove/account';
    
        form.set("id", selectedAccount.value.id)
        form.set("account", UserStore.getID) 
                
        try {
            
            const [status, data] = await FetchStore.POST(URL, form, {  } );
            removeAccLoading.value = false;
            if(status){
                    
            let keys        = Object.keys(data);
            if(keys.includes("status")){                    
    
                if(data["status"] == "deleted"){         
                    return   data["status"]; 
                    // PUSH NOTIFICATION                   
                } 
                else if(data["status"] == "failed" ){                            
                    // USER MUST SIGNIN FIRST                
                    console.log("Request failed"); 
                    return   data["status"]; 
                    // PUSH NOTIFICATION
                        }    
                else if(data["status"] == "formErrors" ){                            
                    // USER MUST SIGNIN FIRST
                    console.log("Form Errors"); 
                    return   data["status"]; 
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
                    setTimeout( () => { removeAccount() } ,1000); 
                }
                else if(data == "unknown") {
                    console.log(`${funcName}: Unknown response`);
                    return "unknown"  // Empty object
                }
                else if(data == "aborted") {
                    console.log(`${funcName}: Request aborted`);
                    // PUSH NOTIFICATION 
                    setTimeout( () => { removeAccount()} ,5000); 
                }
            } 

            return "failed"
        }
        catch(err){  
        console.error(`${funcName} error: ${err.message}`);             
        }   

    
            }

    const updateAccount = async () => {
        // FETCH REQUEST WILL TIMEOUT AFTER 20 SECONDS
        updateAccLoading.value = true; 
        let funcName         = "updateAccount";
     
        const URL            = '/api/update/account';
        let query            = {}
        query["account"]     = UserStore.getID;
        query["id"]          = selectedAccEdited.value.id;
        query["role"]        = selectedAccEdited.value.role;
        query["activated"]   = selectedAccEdited.value.activated;
        query["suball"]      = selectedAccEdited.value.suball;

        try {
            
            const [status, data] = await FetchStore.POST(URL, JSON.stringify(query), {'Accept': 'application/json', 'Content-Type': 'application/json'} );
            updateAccLoading.value = false;
            if(status){
                    
            let keys        = Object.keys(data);
            if(keys.includes("status")){                    
    
                if(data["status"] == "updated"){         
                    return   data["status"]; 
                    // PUSH NOTIFICATION                   
                } 
                else if(data["status"] == "failed" ){                            
                    // USER MUST SIGNIN FIRST                
                    console.log("Request failed"); 
                    return   data["status"]; 
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
                    setTimeout( () => { updateAccount() } ,1000); 
                }
                else if(data == "unknown") {
                    console.log(`${funcName}: Unknown response`);
                    return "unknown"  // Empty object
                }
                else if(data == "aborted") {
                    console.log(`${funcName}: Request aborted`);
                    // PUSH NOTIFICATION 
                    setTimeout( () => { updateAccount()} ,5000); 
                }
            } 

            return "failed"
        }
        catch(err){  
        console.error(`${funcName} error: ${err.message}`);             
        }   

    
            }

    const createSite = async (name, lat, lon) => { 
        // FETCH REQUEST WILL TIMEOUT AFTER 20 SECONDS
        createSiteLoading.value = true; 
        let funcName        = "createSite";
        const form          = new FormData();   
        const URL           = '/api/create/site';
    
        
        form.set("account", UserStore.getID) 
        form.set("name", name)
        form.set("lat", lat)
        form.set("lon", lon)
                
        try {
            
            const [status, data] = await FetchStore.POST(URL, form, {  } );
            createSiteLoading.value = false;
            if(status){
                    
            let keys        = Object.keys(data);
            if(keys.includes("status")){                    
    
                if(data["status"] == "added"){         
                    return   data["status"]; 
                    // PUSH NOTIFICATION                   
                } 
                else if(data["status"] == "failed" ){                            
                    // USER MUST SIGNIN FIRST                
                    console.log("Request failed"); 
                    return   data["status"]; 
                    // PUSH NOTIFICATION
                        }    
                else if(data["status"] == "formErrors" ){                            
                    // USER MUST SIGNIN FIRST
                    console.log("Form Errors"); 
                    return   data["status"]; 
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
                    setTimeout( () => { createSite(name, lat, lon) } ,1000); 
                }
                else if(data == "unknown") {
                    console.log(`${funcName}: Unknown response`);
                    return "unknown"  // Empty object
                }
                else if(data == "aborted") {
                    console.log(`${funcName}: Request aborted`);
                    // PUSH NOTIFICATION 
                    setTimeout( () => { createSite(name, lat, lon)} ,5000); 
                }
            } 

            return "failed"
        }
        catch(err){  
        console.error(`${funcName} error: ${err.message}`);             
        }   

    
            }


    const createDevice = async (device,id) => { 
        // FETCH REQUEST WILL TIMEOUT AFTER 20 SECONDS
        createDeviceLoading.value = true; 
        let funcName        = "createDevice"; 
        const URL           = '/api/create/device';
    
        const query         = {"account": UserStore.getID,"id": id,...device}
    
                
        try {
            
            const [status, data] = await FetchStore.POST(URL, JSON.stringify(query), { 'Accept': 'application/json', 'Content-Type': 'application/json' } );
            createDeviceLoading.value = false;
            if(status){
                    
            let keys        = Object.keys(data);
            if(keys.includes("status")){                    
    
                if(data["status"] == "added"){   
                    site.value = {...data["data"]}      
                    return   "added" 
                    // PUSH NOTIFICATION                   
                } 
                else if(data["status"] == "failed" ){                            
                    // USER MUST SIGNIN FIRST                
                    console.log("Request failed"); 
                    return   "failed" 
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
                    setTimeout( () => { createDevice(device, site) } ,1000); 
                }
                else if(data == "unknown") {
                    console.log(`${funcName}: Unknown response`);
                    return "unknown"  // Empty object
                }
                else if(data == "aborted") {
                    console.log(`${funcName}: Request aborted`);
                    // PUSH NOTIFICATION 
                    setTimeout( () => { createDevice(device, site)} ,5000); 
                }
            } 

            return "failed"
        }
        catch(err){  
        console.error(`${funcName} error: ${err.message}`);             
        }   

    
            }

    const updateSite = async (siteData) => { 
        // FETCH REQUEST WILL TIMEOUT AFTER 20 SECONDS
        updateSiteLoading.value = true; 
        let funcName        = "updateSite"; 
        const URL           = '/api/update/site';
    
        const query         = {"account": UserStore.getID,...siteData}
    
                
        try {
            
            const [status, data] = await FetchStore.POST(URL, JSON.stringify(query), { 'Accept': 'application/json', 'Content-Type': 'application/json' } );
            updateSiteLoading.value = false;
            if(status){
                    
            let keys        = Object.keys(data);
            if(keys.includes("status")){                    
    
                if(data["status"] == "updated"){   
                    site.value = {...data["data"]}                        
                    return   "updated" 
                    // PUSH NOTIFICATION                   
                } 
                else if(data["status"] == "failed" ){                            
                    // USER MUST SIGNIN FIRST                
                    console.log("Request failed"); 
                    return   "failed" 
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
                    setTimeout( () => { updateSite(siteData) } ,1000); 
                }
                else if(data == "unknown") {
                    console.log(`${funcName}: Unknown response`);
                    return "unknown"  // Empty object
                }
                else if(data == "aborted") {
                    console.log(`${funcName}: Request aborted`);
                    // PUSH NOTIFICATION 
                    setTimeout( () => { updateSite(siteData)} ,5000); 
                }
            } 

            return "failed"
        }
        catch(err){  
        console.error(`${funcName} error: ${err.message}`);             
        }   

    
            }

    const updateDevice = async (device) => { 
        // FETCH REQUEST WILL TIMEOUT AFTER 20 SECONDS
        updateDeviceLoading.value = true; 
        let funcName        = "updateDevice"; 
        const URL           = '/api/update/device';
    
        const query         = {"account": UserStore.getID,...device}
    
                
        try {
            
            const [status, data] = await FetchStore.POST(URL, JSON.stringify(query), { 'Accept': 'application/json', 'Content-Type': 'application/json' } );
            updateDeviceLoading.value = false;
            if(status){
                    
            let keys        = Object.keys(data);
            if(keys.includes("status")){                    
    
                if(data["status"] == "updated"){   
                    site.value = {...data["data"]} 
                    resetDevice();     
                    return   "updated" 
                    // PUSH NOTIFICATION                   
                } 
                else if(data["status"] == "failed" ){                            
                    // USER MUST SIGNIN FIRST                
                    console.log("Request failed"); 
                    return   "failed" 
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
                    setTimeout( () => { updateDevice(device) } ,1000); 
                }
                else if(data == "unknown") {
                    console.log(`${funcName}: Unknown response`);
                    return "unknown"  // Empty object
                }
                else if(data == "aborted") {
                    console.log(`${funcName}: Request aborted`);
                    // PUSH NOTIFICATION 
                    setTimeout( () => { updateDevice(device)} ,5000); 
                }
            } 

            return "failed"
        }
        catch(err){  
        console.error(`${funcName} error: ${err.message}`);             
        }   

    
            }

    const getPageCount = async (search=false) => { 
        // FETCH REQUEST WILL TIMEOUT AFTER 20 SECONDS 
        let funcName        = "getPageCount";
        const form          = new FormData();   
        const URL           = '/api/get/pagecount';    
        
        form.set("account", UserStore.getID)
        form.set("search", siteSearchPages.value.search) 
        form.set("ops",  (search)? 'search' : '')   
                
        try {
            
            const [status, data] = await FetchStore.POST(URL, form, {  } );
         
            if(status){
                    
                let keys        = Object.keys(data);
                if(keys.includes("status")){                    
        
                    if(data["status"] == "ok"){    
                        if(search == true){
                            siteSearchPages.value.count = data["count"]; 
                        }                        
                        else{
                            sitePages.value.count = data["count"]; 
                        }     
                        
                        // PUSH NOTIFICATION                   
                    } 
                    else if(data["status"] == "failed" ){                            
                        // USER MUST SIGNIN FIRST                
                        console.log("Request failed");   
                        if(search == true){
                            siteSearchPages.value.count = 0; 
                        }                        
                        else{
                            sitePages.value.count = 0; 
                        }                  
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
                    setTimeout( () => { getPageCount() } ,1000); 
                }
                else if(data == "unknown") {
                    console.log(`${funcName}: Unknown response`);
                    // return "unknown"  // Empty object
                }
                else if(data == "aborted") {
                    console.log(`${funcName}: Request aborted`);
                    // PUSH NOTIFICATION 
                    setTimeout( () => { getPageCount()} ,5000); 
                }
            } 

           
        }
        catch(err){  
        console.error(`${funcName} error: ${err.message}`);             
        }   

    
            }

    const getPage = async (page, search=false) => { 
        // FETCH REQUEST WILL TIMEOUT AFTER 20 SECONDS 
        historyLoading.value = true;
        let funcName        = "getPage";
        const form          = new FormData();   
        const URL           = '/api/get/page';    
        
        form.set("account", UserStore.getID) 
        form.set("search", siteSearchPages.value.search) 
        form.set("ops",  (search)? 'search' : '')   
        form.set("page", page - 1) 
                
        try {
            
            const [status, data] = await FetchStore.POST(URL, form, {  } );
            historyLoading.value = false;
            if(status){
                    
            let keys        = Object.keys(data);
            if(keys.includes("status")){                    
    
                if(data["status"] == "ok"){    
                    if(search){
                        siteSearchPages.value.pages[data["page"]] =  data["data"]; 
                    }
                    else {
                        sitePages.value.pages[data["page"]] =  data["data"]; 
                    }     
                    
                  
                    // PUSH NOTIFICATION                   
                } 
                else if(data["status"] == "failed" ){                            
                    // USER MUST SIGNIN FIRST                
                    console.log("Request failed"); 
                    if(search){
                        siteSearchPages.value.pages  =  {}; 
                    }
                    else {
                        sitePages.value.pages =  {}; 
                    }   
                    
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
                    setTimeout( () => { getPage(page, search) } ,1000); 
                }
                else if(data == "unknown") {
                    console.log(`${funcName}: Unknown response`);
                    // return "unknown"  // Empty object
                }
                else if(data == "aborted") {
                    console.log(`${funcName}: Request aborted`);
                    // PUSH NOTIFICATION 
                    setTimeout( () => { getPage(page, search)} ,5000); 
                }
            } 

           
        }
        catch(err){  
        console.error(`${funcName} error: ${err.message}`);             
        }   

    
            }

    const getSite = async (id) => { 
        // FETCH REQUEST WILL TIMEOUT AFTER 20 SECONDS 
        siteLoading.value   = true;
        let funcName        = "getSite";
        const form          = new FormData();   
        const URL           = '/api/get/site';    
        
        form.set("account", UserStore.getID) 
        form.set("id", id)  
                
        try {
            
            const [status, data] = await FetchStore.POST(URL, form, {  } );
            siteLoading.value   = false;
        
            if(status){
                    
            let keys        = Object.keys(data);
            if(keys.includes("status")){                    
    
                if(data["status"] == "ok"){    
                   site.value = {...data["site"]};     
                    
                    
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
                    setTimeout( () => { getSite(id) } ,1000); 
                }
                else if(data == "unknown") {
                    console.log(`${funcName}: Unknown response`);
                    // return "unknown"  // Empty object
                }
                else if(data == "aborted") {
                    console.log(`${funcName}: Request aborted`);
                    // PUSH NOTIFICATION 
                    setTimeout( () => { getSite(id)} ,5000); 
                }
            } 

            
        }
        catch(err){  
        console.error(`${funcName} error: ${err.message}`);             
        }   

    
            }

    const searchUser = async (search) => {
        // FETCH REQUEST WILL TIMEOUT AFTER 20 SECONDS
        accSearchLoading.value = true; 
        let funcName        = "searchUser";
        const form          = new FormData();   
        const URL           = '/api/search/user';
    
        form.set("search", search)
        form.set("account", UserStore.getID) 
                
        try {
            
            const [status, data] = await FetchStore.POST(URL, form, {  } );
            accSearchLoading.value = false;
            if(status){
                    
            let keys        = Object.keys(data);
            if(keys.includes("status")){                    
    
                if(data["status"] == "ok"){  
                    userSearch.value.result =     data["data"]   
                    return   data["status"]; 
                    // PUSH NOTIFICATION                   
                } 
                else if(data["status"] == "failed" ){                            
                    // USER MUST SIGNIN FIRST                
                    console.log("Request failed"); 
                    return   data["status"]; 
                    // PUSH NOTIFICATION
                        }    
                else if(data["status"] == "formErrors" ){                            
                    // USER MUST SIGNIN FIRST
                    console.log("Form Errors"); 
                    return   data["status"]; 
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
                    setTimeout( () => { searchUser(search) } ,1000); 
                }
                else if(data == "unknown") {
                    console.log(`${funcName}: Unknown response`);
                    return "unknown"  // Empty object
                }
                else if(data == "aborted") {
                    console.log(`${funcName}: Request aborted`);
                    // PUSH NOTIFICATION 
                    setTimeout( () => { searchUser(search)} ,5000); 
                }
            } 

            return "failed"
        }
        catch(err){  
        console.error(`${funcName} error: ${err.message}`);             
        }   

    
            }

    const assignUser = async (siteID,userID) => {
        // FETCH REQUEST WILL TIMEOUT AFTER 20 SECONDS
        assignUserLoading.value = true; 
        let funcName        = "assignUser";
        const form          = new FormData();   
        const URL           = '/api/assign/user';
    
        
        form.set("account", UserStore.getID) 
        form.set("site", siteID)
        form.set("id", userID)
                
        try {
            
            const [status, data] = await FetchStore.POST(URL, form, {  } );
            assignUserLoading.value = false;
            if(status){
                    
            let keys        = Object.keys(data);
            if(keys.includes("status")){                    
    
                if(data["status"] == "assigned"){  
                    site.value =  {...data["data"]}
                    return   data["status"]; 
                    // PUSH NOTIFICATION                   
                } 
                else if(data["status"] == "failed" ){                            
                    // USER MUST SIGNIN FIRST                
                    console.log("Request failed"); 
                    return   data["status"]; 
                    // PUSH NOTIFICATION
                        }    
                else if(data["status"] == "formErrors" ){                            
                    // USER MUST SIGNIN FIRST
                    console.log("Form Errors"); 
                    return   data["status"]; 
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
                    setTimeout( () => { assignUser(siteID,userID) } ,1000); 
                }
                else if(data == "unknown") {
                    console.log(`${funcName}: Unknown response`);
                    return "unknown"  // Empty object
                }
                else if(data == "aborted") {
                    console.log(`${funcName}: Request aborted`);
                    // PUSH NOTIFICATION 
                    setTimeout( () => { assignUser(siteID,userID)} ,5000); 
                }
            } 

            return "failed"
        }
        catch(err){  
        console.error(`${funcName} error: ${err.message}`);             
        }   

    
            }

    const deleteDevice = async (siteID,deviceID) => {
        // FETCH REQUEST WILL TIMEOUT AFTER 20 SECONDS
        deleteDeviceLoading.value = true; 
        let funcName        = "deleteDevice";
        const form          = new FormData();   
        const URL           = '/api/delete/device';
    
        
        form.set("account", UserStore.getID) 
        form.set("site", siteID)
        form.set("id", deviceID)
                
        try {
            
            const [status, data] = await FetchStore.POST(URL, form, {  } );
            deleteDeviceLoading.value = false;
            if(status){
                    
            let keys        = Object.keys(data);
            if(keys.includes("status")){                    
    
                if(data["status"] == "deleted"){  
                    site.value =  {...data["data"]}
                    return   data["status"]; 
                    // PUSH NOTIFICATION                   
                } 
                else if(data["status"] == "failed" ){                            
                    // USER MUST SIGNIN FIRST                
                    console.log("Request failed"); 
                    return   data["status"]; 
                    // PUSH NOTIFICATION
                        }    
                else if(data["status"] == "formErrors" ){                            
                    // USER MUST SIGNIN FIRST
                    console.log("Form Errors"); 
                    return   data["status"]; 
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
                    setTimeout( () => { deleteDevice(siteID,deviceID) } ,1000); 
                }
                else if(data == "unknown") {
                    console.log(`${funcName}: Unknown response`);
                    return "unknown"  // Empty object
                }
                else if(data == "aborted") {
                    console.log(`${funcName}: Request aborted`);
                    // PUSH NOTIFICATION 
                    setTimeout( () => { deleteDevice(siteID,deviceID)} ,5000); 
                }
            } 

            return "failed"
        }
        catch(err){  
        console.error(`${funcName} error: ${err.message}`);             
        }   

    
            }

    const getEmailList = async () => {
        // FETCH REQUEST WILL TIMEOUT AFTER 20 SECONDS  
        let funcName        = "getEmailList";
        const   id          = UserStore.getID;  
        const URL           = `/api/misc/emaillist`;    
            
        try {
            const [status, data] = await FetchStore.GET(URL);      
            
            if(status){
                let keys        = Object.keys(data);

                if(keys.includes("status")){

                    if(data["status"] == "found" || data["status"] == "created"){  
                        // console.log(data["data"]); 
                        emailList.cancellation  = data["data"]["cancellation"];   
                        emailList.registration  = data["data"]["registration"];                             
                        }
                    if(data["status"] == "none found" ){  
                            console.log(`${funcName}: No emails found`);                          
                        }  
                }    
        
            }
            else {
                if(data == "unauthorized") {
                    console.log(`${funcName}: Unauthorized User`);
                }
                else if(data == "token refreshed") {
                    console.log(`${funcName}: Retrying in in 1 seconds`);
                    setTimeout( () => { getEmailList() } ,1000); 
                }
                else if(data == "unknown") {
                    console.log(`${funcName}: Unknown response`);
                }
                else if(data == "aborted") {
                    console.log(`${funcName}: Request aborted`);
                    // PUSH NOTIFICATION 
                     setTimeout( () => { getEmailList()} ,5000); 
                }
            } 
        }
        catch(err){     
            console.error(`${funcName} error: ${err.message}`);         
        }           
    }

    const updateEmailList = async (firstname,lastname, email, account, type)=>{
        // FETCHES ALL PRODUCTS TYPES(MET,RAD,PRO,MISC,EQUIP, SUPP) ETC IN SYSTEM
        // RETURNS PAGE COUNT FOR ALL PRODUCT TYPES (MET, RAD, PRO, MISC, EQUIP, SUPP)
        // LOADS FIRST PAGE FOR SEARCH RESULT BY INVOKING getCurrentPage(); 
        
        let funcName  = "updateEmailList";
        const user    = ref(UserStore.getID);
        const URL     = `/api/misc/emaillist/update`;     
        const form    = new FormData();      
        
        form.append("User",UserStore.getID);
        form.append("Firstname", firstname); 
        form.append("Lastname", lastname); 
        form.append("Email", email); 
        form.append("Account",account); 
        form.append("Type",type); 

        try {
                
            const [status, data] = await FetchStore.POST(URL, form, {} );
        
            if(status){
                let keys        = Object.keys(data);
                if(keys.includes("status")){                   

                    if(data["status"] === "added"){ 
                        console.log(data["data"]);                    
                        emailList.cancellation  = data["data"]["cancellation"];   
                        emailList.registration  = data["data"]["registration"];                     
                        }
                    if(data["status"] === "already"){ 
                        // PUSH NOTIFICATION 
                                           
                    }
                    if(data["status"] == "failed" ){                            
                        // USER MUST SIGNIN FIRST
                        console.log(`${funcName}: Unable to add Email to list`); 
                          }               
                }    
            }
            else {
                if(data == "unauthorized") {
                    console.log(`${funcName}: Unauthorized User`);
                }
                else if(data == "token refreshed") {
                    setTimeout( () => { updateEmailList(firstname,lastname, email,account, type) } ,5000); 
                }
                else if(data == "unknown") {
                    console.log(`${funcName}: Unknown response`);
                }
                else if(data == "aborted") {
                    console.log(`${funcName}: Request aborted`);
                    // PUSH NOTIFICATION                      
                    setTimeout( () => { updateEmailList(firstname, lastname, email, account, type)} ,5000); 
                }
            } 
                
            
            }
        catch(err) {  
            console.error(`${funcName} error: ${err.message}`);   
            // setTimeout( ()=>{ updateEmailList(firstname,lastname, email,account) } ,5000);         
        }   
            
    }

    const deleteFromEmailList = async (account, type)=>{
        // FETCHES ALL PRODUCTS TYPES(MET,RAD,PRO,MISC,EQUIP, SUPP) ETC IN SYSTEM
        // RETURNS PAGE COUNT FOR ALL PRODUCT TYPES (MET, RAD, PRO, MISC, EQUIP, SUPP)
        // LOADS FIRST PAGE FOR SEARCH RESULT BY INVOKING getCurrentPage(); 
        
        let funcName  = "deleteFromEmailList";
        const user    = ref(UserStore.getID);
        const URL     = `/api/misc/emaillist/delete`;     
        const form    = new FormData();      
        
        form.append("User",UserStore.getID);  
        form.append("Account",account); 
        form.append("Type",type); 

        try {
                
            const [status, data] = await FetchStore.POST(URL, form, {} );
        
            if(status){
                let keys        = Object.keys(data);
                if(keys.includes("status")){                   

                    if(data["status"] === "deleted"){                          
                        emailList.cancellation  = data["data"]["cancellation"];   
                        emailList.registration  = data["data"]["registration"];  
                      } 
                    if(data["status"] == "failed" ){                            
                        // USER MUST SIGNIN FIRST
                        console.log(`${funcName}: Unable to delete Email from list`); 
                              }               
                }    
            }
            else {
                if(data == "unauthorized") {
                    console.log(`${funcName}: Unauthorized User`);
                }
                else if(data == "token refreshed") {
                    setTimeout( () => { deleteFromEmailList(account, type) } ,5000); 
                }
                else if(data == "unknown") {
                    console.log(`${funcName}: Unknown response`);
                }
                else if(data == "aborted") {
                    console.log(`${funcName}: Request aborted`);
                     setTimeout( () => { deleteFromEmailList( account, type)} ,5000); 
                }
            } 
                
            
            }
        catch(err) {  
            console.error(`${funcName} error: ${err.message}`);   
            // setTimeout( ()=>{ deleteFromEmailList(account, type) } ,5000);         
        }   
            
    }

    const getAllStaff = async ()=> {
        // FETCH REQUEST WILL TIMEOUT AFTER 60 SECONDS 
        let funcName        = "getAllStaff"; 
        const id            = UserStore.getID; 
        const URL           = `/api/staff/all/${id}`;    
     
        try {
            const [status, data] = await FetchStore.GET(URL);   
    
            if(status){
                let keys        = Object.keys(data);
    
                if(keys.includes("status")){
    
                    if(data["status"] == "found" ){                                              
                            allStaffAccounts.value = data["data"];
                            assignListAdmin.value = [];
                            
                            allStaffAccounts.value.forEach((staff)=>{
                              assignListAdmin.value.push(`${staff.firstname} ${staff.lastname}`);
                            })
                        }
                    if(data["status"] == "not found" ){                                            
                            console.log("None Found");
                            allStaffAccounts.value = [];                           
                        } 
                }       
            }
            else {
                if(data == "unauthorized") {
                    console.log(`${funcName}: Unauthorized User`);
                }
                else if(data == "token refreshed") {
                    console.log(`${funcName}: Retrying in in 1 seconds`);
                    setTimeout( () => { getAllStaff() } ,1000); 
                }
                else if(data == "unknown") {
                    console.log(`${funcName}: Unknown response`);
                }
                else if(data == "aborted") {
                    console.log(`${funcName}: Request aborted`);
                    // PUSH NOTIFICATION 
                     setTimeout( () => { getAllStaff()} ,5000); 
                }
            } 
        }
        catch(err){     
            console.error(`${funcName} error: ${err.message}`);            
        }           
      }

    return { 
    // EXPORTS	
    drawerItems,
    routeItems,
    month,
    threedays,
    sevendays,
    setThree,
    setSeven,
    setMonth,
    getData,
    getMapHistoryData, 
    appDarkMode,

    // ADMIN EXPORTS
    newRegistrations,
    staffs,
    edit,
    users,
    sites,
    sitePages,
    aodLoading,
    siteLoading,
    siteSearchPages,
    createSiteLoading,
    createDeviceLoading,
    updateAccLoading,
    removeAccLoading,
    selectedAccount,
    selectedAccEdited,
    allStaffAccounts,
    assignListAdmin,
    sitePages,
    emailList,
    spss,
    site,
    device,
    userSearch,
    paramDetails,
    historyLoading,
    accSearchLoading,
    updateDeviceLoading,
    updateSiteLoading,
    assignUserLoading,
    deleteDeviceLoading,
    emailSelectedItem,
    resetGraphData,
    getAllStaff,
    getEmailList,
    updateEmailList,
    deleteFromEmailList,
    deleteDevice,
    assignUser,
    resetDevice,
    setDevice,
    resetSite,
    setSite,
    getSite,
    setSPSS,
    setPage,
    getPage,
    getPageCount,
    createDevice,
    updateDevice,
    updateSite,
    setSites,
    searchUser,
    createSite,
    removeAccount,
    updateAccount,
    setAdminAccountVariables,
    setSelectedAccount,
    clearSelectedAccount,
    approveOrDenyRequest
        
       }
},{ persist: {storage: sessionStorage} });