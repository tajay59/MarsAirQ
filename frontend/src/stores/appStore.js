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
    const overlay       = ref(false);
    const drawerItems   = ref([ 
        {"icon":"mdi:mdi-google-maps","title":"Map","route":"/analytics/map","name":"Map"},  
        {"icon":"mdi:mdi-play","title":"Live","route":"/analytics/live","name":"Live"},  
        {"icon":"mdi:mdi-view-dashboard","title":"Dashboard","route":"/analytics/dashboard","name":"Dashboard"},  
        {"icon":"mdi:mdi-chart-timeline-variant-shimmer","title":"Analysis","route":"/analytics/analysis","name":"Analysis"},  
    ])

    const routeItems   = ref([
        {"icon":"mdi:mdi-lock","title":"Research","route":"/research","name":"Research"},  
        {"icon":"mdi:mdi-lock","title":"Analytics","route":"/analytics/map","name":"Analytics"},   
        // {"icon":"mdi:mdi-lock","title":"Admin","route":"/admin","name":"Admin"},   
    ])

    const profileRouteItems   = ref([
        {"icon":"mage:edit-fill","title":"Edit Profile","route":"/profile/edit","name":"Edit"},  
        {"icon":"ion:notifications","title":"Notifications","route":"/profile/notifications","name":"Notifications"}, 
        {"icon":"mdi:map-markers","title":"sites","route":"/profile/sites","name":"Sites"}, 
        {"icon":"ph:device-mobile-camera-fill","title":"Devices","route":"/profile/devices","name":"Devices"}, 
        {"icon":"fluent:branch-request-16-filled","title":"Requests","route":"/profile/requests","name":"Requests"}, 
        // {"icon":"mdi:mdi-lock","title":"Analytics","route":"/analytics/map","name":"Analytics"},   
        // {"icon":"mdi:mdi-lock","title":"Admin","route":"/admin","name":"Admin"},   
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
    const getEntitiesLoading  = ref(false);
    const uddLoading = ref(false); // update Device Dashboard Loading
    const historyLoading    = ref(false);
    const accSearchLoading  = ref(false);
    const assignUserLoading = ref(false);
    const siteLoading       = ref(false);
    const edit              = ref(false); // Edit user account details
    const userSearch        = ref({"text":"","result":[]})
    const sites             = ref([]);
    const sitePages         = ref({"count": 0,"page":1,"pages":{}});
    const siteSearchPages   = ref({"count": 0,"search":"","page":1,"pages":{}});
    const sitePagesEntity         = ref({"count": 0,"page":1,"pages":{}});
    const siteSearchPagesEntity   = ref({"count": 0,"search":"","page":1,"pages":{}});
    const dashboardMenu     = ref(false);
    const openSiteSearch    = ref(false);
    const openCreateSite    = ref(false);  
    const openCreateEntity  = ref(false); 
    const createEntityLoading = ref(false);
    const requests          = ref([]);
    const entities          = ref([])
    
    const paramDetails      = ref({
        "temperature":{"units":"°C", "icon":"fluent:temperature-20-regular","max":40,"min":0, "htmlUnits":'<small class="text-xs"> °C</small>'},
        "dewpoint":{"units":"°C", "icon":"mdi:water-temperature","max":40,"min":0, "htmlUnits":'<small class="text-xs"> °C</small>'},
        "windchill":{"units":"°C", "icon":"fluent:temperature-20-regular","max":40,"min":0, "htmlUnits":'<small class="text-xs"> °C</small>'},
        "heatindex":{"units":"°C", "icon":"carbon:windy","max":40,"min":0, "htmlUnits":'<small class="text-xs"> °C</small>'},
        "boxtemperature":{"units":"°C", "icon":"mdi:home-temperature-outline","max":40,"min":0, "htmlUnits":'<small class="text-xs"> °C</small>'},

        "humidity":{"units":"%", "icon":"material-symbols:humidity-percentage-rounded","max":100,"min":0, "htmlUnits":'<small class="text-xs"> %</small>'},
        "pressure":{"units":"hPa", "icon":"lets-icons:pressure-light","max":1050,"min":900, "htmlUnits": '<small class="text-xs"> hPa</small>'},
        "altitude":{"units":"ft", "icon":"material-symbols-light:altitude-rounded","max":4000,"min":0, "htmlUnits":'<small class="text-xs"> ft</small>'}, 
        "windspeed":{"units":"m/s", "icon":"fa6-solid:wind","max":100,"min":0, "htmlUnits":'<small class="text-xs"> m/s</small>'},
        "winddirection":{"units":"°", "icon":"teenyicons:direction-solid","max":359,"min":0, "htmlUnits":'<small class="text-xs"> °</small>'},
        "rainfall":{"units":"mm", "icon":"mdi:weather-heavy-rain","max":20,"min":0, "htmlUnits":'<small class="text-xs"> mm</small>'},
        "voc":{"units":"ppm", "icon":"material-symbols-light:air-rounded","max":5000,"min":0, "htmlUnits":'<small class="text-xs"> ppm</small>'},
        "vocindex":{"units":"", "icon":"ic:baseline-gpp-good","max":5000,"min":0, "htmlUnits":'<small class="text-xs"> </small>'},
        "co2": {"units":"ppm","icon":"iwwa:co2","max":5000,"min":0, "htmlUnits":'<small class="text-xs"> ppm</small>'},
        "pm1": {"units":"ppm","icon":"fluent:dust-28-regular","max":5000,"min":0, "htmlUnits":'<small class="text-xs"> ppm</small>'},
        "pm25": {"units":"ppm","icon":"fluent:dust-28-regular","max":5000,"min":0, "htmlUnits":'<small class="text-xs"> ppm</small>'},
        "pm10": {"units":"ppm","icon":"fluent:dust-24-filled","max":5000,"min":0, "htmlUnits":'<small class="text-xs"> ppm</small>'},
        "radiation":{"units":"W/m2", "icon":"solar:sunset-bold","max":100,"min":0, "htmlUnits":'<small class="text-xs">W/m<sup>2</sup></small>'},
        "uva":{"units":"W/m2", "icon":"solar:sunset-bold","max":100,"min":0, "htmlUnits":'<small class="text-xs">W/m<sup>2</sup></small>'},
        "uvb":{"units":"W/m2", "icon":"solar:sunset-bold-duotone","max":100,"min":0, "htmlUnits":'<small class="text-xs">W/m<sup>2</sup></small>'},
        "uvc":{"units":"W/m2", "icon":"solar:sunset-line-duotone","max":100,"min":0, "htmlUnits":'<small class="text-xs">W/m<sup>2</sup></small>'},

        // NEED CORRECT ICONS FOR BELOW
        "voltage":{"units":"V", "icon":"ix:voltage-filled","max":4.2,"min":2.8, "htmlUnits":'<small class="text-xs"> V</small>'},
        "current":{"units":"mA", "icon":"mdi:current-dc","max":1000,"min":0, "htmlUnits":'<small class="text-xs"> mA</small>'},
        "bat":{"units":"%", "icon":"mdi:battery-high","max":100,"min":0, "htmlUnits":'<small class="text-xs"> %</small>'},
        "oxidised":{"units":"ppm", "icon":"iconoir:nitrogen","max":5000,"min":0, "htmlUnits":'<small class="text-xs"> ppm</small>'}, // nitrogen dioxide (oxidising), 
        "reduced":{"units":"ppm", "icon":"mdi:carbon-monoxide","max":5000,"min":0, "htmlUnits":'<small class="text-xs"> ppm</small>'}, // carbon monoxide (reducing),
        "nh3":{"units":"ppm", "icon":"lets-icons:chemistry-light","max":5000,"min":0, "htmlUnits":'<small class="text-xs"> ppm</small>'},
        "lux":{"units":"lux", "icon":"line-md:car-light","max":5000,"min":0, "htmlUnits":'<small class="text-xs"> ppm</small>'},

        "default":{"units":"", "icon":"line-md:car-light","max":100,"min":0, "htmlUnits":'<small class="text-xs"> </small>'},
    
    });

    const userSites        = ref([]);
    const userAccount      = ref({});
    const emailList         = reactive({registration:[], cancellation:[]});
    const allStaffAccounts  = ref([]);
    const spss              = ref(null); // Sites page selected site
    const assignListAdmin   = ref([]); // LIST OF STAFF NAMES USED FOR SELECT COMPONENT ON THE /ADMIN ROUTE
    
    const site              = ref(null);
    const device            = ref(null);
    const caribbeanCountries = ref([
     {
        "name": "Anguilla",
        "icon": "emojione-v1:flag-for-anguilla",
        "code": "AI",
        "center": {
            "latitude": 18.2206,
            "longitude": -63.0686
        }
    },
    {
        "name": "Antigua and Barbuda",
        "icon": "emojione-v1:flag-for-antigua-and-barbuda",
        "code": "AG",
        "center": {
            "latitude": 17.0608,
            "longitude": -61.7964
        }
    },
    {
        "name": "Bahamas",
        "icon": "emojione-v1:flag-for-bahamas",
        "code": "BS",
        "center": {
            "latitude": 25.0239,
            "longitude": -77.3963
        }
    },
    {
        "name": "Barbados",
        "icon": "emojione-v1:flag-for-barbados",
        "code": "BB",
        "center": {
            "latitude": 13.1939,
            "longitude": -59.5431
        }
    },
    {
        "name": "Belize",
        "icon": "emojione-v1:flag-for-belize",
        "code": "BZ",
        "center": {
            "latitude": 17.2510,
            "longitude": -88.7719
        }
    },
     {
        "name": "British Virgin Islands",
        "icon": "twemoji:flag-british-virgin-islands",
        "code": "VG",
        "center": {
            "latitude": 18.4207,
            "longitude": -64.6400
        }
    },
    {
        "name": "Cayman Islands",
        "icon": "emojione-v1:flag-for-cayman-islands",
        "code": "KY",
        "center": {
            "latitude": 19.3133,
            "longitude": -81.2546
        }
    },
    {
        "name": "Cuba",
        "icon": "emojione-v1:flag-for-cuba",
        "code": "CU",
        "center": {
            "latitude": 21.5217,
            "longitude": -77.7812
        }
    },
    {
        "name": "Dominica",
        "icon": "emojione-v1:flag-for-dominica",
        "code": "DM",
        "center": {
            "latitude": 15.4150,
            "longitude": -61.3710
        }
    },
    {
        "name": "Dominican Republic",
        "icon": "emojione-v1:flag-for-dominican-republic",
        "code": "DO",
        "center": {
            "latitude": 19.1940,
            "longitude": -70.6667
        }
    },
    {
        "name": "Grenada",
        "icon": "emojione-v1:flag-for-grenada",
        "code": "GD",
        "center": {
            "latitude": 12.1165,
            "longitude": -61.6790
        }
    },
    {
        "name": "Guyana",
        "icon": "emojione-v1:flag-for-guyana",
        "code": "GY",
        "center": {
            "latitude": 4.9387,
            "longitude": -58.9310
        }
    },
    {
        "name": "Haiti",
        "icon": "emojione-v1:flag-for-haiti",
        "code": "HT",
        "center": {
            "latitude": 18.9712,
            "longitude": -72.2852
        }
    },
    {
        "name": "Jamaica",
        "icon": "emojione-v1:flag-for-jamaica",
        "code": "JM",
        "center": {
            "latitude": 18.1096,
            "longitude": -77.2975
        }
    },
    {
        "name": "Montserrat",
        "icon": "emojione-v1:flag-for-montserrat",
        "code": "MS",
        "center": {
            "latitude": 16.7425,
            "longitude": -62.1874
        }
    },
    {
        "name": "Saint Kitts and Nevis",
        "icon": "emojione-v1:flag-for-st-kitts-and-nevis",
        "code": "KN",
        "center": {
            "latitude": 17.3571,
            "longitude": -62.7829
        }
    },
    {
        "name": "Saint Lucia",
        "icon": "emojione-v1:flag-for-st-lucia",
        "code": "LC",
        "center": {
            "latitude": 13.9094,
            "longitude": -60.9789
        }
    },
    {
        "name": "Sint Maarten",
        "icon": "twemoji:flag-sint-maarten",
        "code": "SX",
        "center": {
            "latitude": 18.0425,
            "longitude": -63.0548
        }
    },
    {
        "name": "Saint Vincent and the Grenadines",
        "icon": "emojione-v1:flag-for-st-vincent-and-grenadines",
        "code": "VC",
        "center": {
            "latitude": 13.2541,
            "longitude": -61.2072
        }
    },
    {
        "name": "Suriname",
        "icon": "emojione-v1:flag-for-suriname",
        "code": "SR",
        "center": {
            "latitude": 3.9190,
            "longitude": -56.0278
        }
    },
    {
        "name": "Trinidad and Tobago",
        "icon": "emojione-v1:flag-for-trinidad-and-tobago",
        "code": "TT",
        "center": {
            "latitude": 10.6918,
            "longitude": -61.2225
        }
    },
    {
        "name": "Turks and Caicos Islands",
        "icon": "twemoji:flag-turks-and-caicos-islands",
        "code": "TC",
        "center": {
            "latitude": 21.6940,
            "longitude": -71.7979
        }
    }
]);


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

    const createSite = async (name, lat, lon, entity) => { 
        // FETCH REQUEST WILL TIMEOUT AFTER 20 SECONDS
        createSiteLoading.value = true; 
        let funcName        = "createSite";
        const form          = new FormData();   
        const URL           = '/api/create/site';
    
        
        form.set("account", UserStore.getID) 
        form.set("name", name)
        form.set("lat", lat)
        form.set("lon", lon)
        form.set("entity", entity)
                
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

    const removeSite = async (site, loading) => {
            // FETCH REQUEST WILL TIMEOUT AFTER 20 SECONDS
            loading.value = true; 
            let funcName        = "removeSite";
            const form          = new FormData();   
            const URL           = '/api/delete/site';
                    
            form.set("account", UserStore.getID);
            form.set("site", site); 
                    
            try {
                
                const [status, data] = await FetchStore.POST(URL, form, {  } );
                loading.value = false;
                if(status){
                        
                let keys        = Object.keys(data);
                if(keys.includes("status")){                    
        
                    if(data["status"] == "deleted"){         
                        return   data["status"];                   
                    } 
                    else if(data["status"] == "failed" ){                            
                        // USER MUST SIGNIN FIRST                
                        console.log("Request failed"); 
                        return   data["status"]; 
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
                        setTimeout( () => { removeSite(site, loading) } ,1000); 
                    }
                    else if(data == "unknown") {
                        console.log(`${funcName}: Unknown response`);
                        return "unknown"  // Empty object
                    }
                    else if(data == "aborted") {
                        console.log(`${funcName}: Request aborted`);
                        // PUSH NOTIFICATION 
                        setTimeout( () => { removeSite(site, loading)} ,5000); 
                    }
                } 

                return "failed"
            }
            catch(err){  
            console.error(`${funcName} error: ${err.message}`);             
            }   

        
                }

    const createEntity = async (name, country ) => { 
        // FETCH REQUEST WILL TIMEOUT AFTER 20 SECONDS
        createEntityLoading.value = true; 
        let funcName        = "createEntity";
        const form          = new FormData();   
        const URL           = '/api/create/entity';
     
        let query            = {}
        query["account"]     = UserStore.getID;
        query["name"]        = name;
        query["code"]        = country; 
                
        try {
            
            const [status, data] = await FetchStore.POST(URL, JSON.stringify(query), {'Accept': 'application/json', 'Content-Type': 'application/json'} );
            createEntityLoading.value = false;
            if(status){
                    
            let keys        = Object.keys(data);
            if(keys.includes("status")){                    
    
                if(data["status"] == "created"){    
                    entities.value = [...data["entities"]];      
                    return   "created";                 
                } 
                if(data["status"] == "exist"){    
                    entities.value = [...data["entities"]];      
                    return   "exist";                 
                } 
                else if(data["status"] == "failed" ){                            
                    // USER MUST SIGNIN FIRST                
                    console.log("Request failed"); 
                    return   "failed"; 
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
                    setTimeout( () => { createEntity(name, country, loading) } ,1000); 
                }
                else if(data == "unknown") {
                    console.log(`${funcName}: Unknown response`);
                    return "unknown"  // Empty object
                }
                else if(data == "aborted") {
                    console.log(`${funcName}: Request aborted`);
                    // PUSH NOTIFICATION 
                    setTimeout( () => { createEntity(name, country, loading)} ,5000); 
                }
            } 

            return "failed"
        }
        catch(err){  
        console.error(`${funcName} error: ${err.message}`);             
        }   

    
            }

    const removeEntity = async (entity, loading) => {
            // FETCH REQUEST WILL TIMEOUT AFTER 20 SECONDS
            loading.value = true; 
            let funcName        = "removeEntity";
            const form          = new FormData();   
            const URL           = '/api/delete/entity';
                    
            form.set("account", UserStore.getID);
            form.set("id", entity); 
                    
            try {
                
                const [status, data] = await FetchStore.POST(URL, form, {  } );
                loading.value = false;
                if(status){
                        
                let keys        = Object.keys(data);
                if(keys.includes("status")){                    
        
                    if(data["status"] == "deleted"){         
                        return   data["status"];                   
                    } 
                    else if(data["status"] == "failed" ){                            
                        // USER MUST SIGNIN FIRST                
                        console.log("Request failed"); 
                        return   data["status"]; 
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
                        setTimeout( () => { removeEntity(entity, loading) } ,1000); 
                    }
                    else if(data == "unknown") {
                        console.log(`${funcName}: Unknown response`);
                        return "unknown"  // Empty object
                    }
                    else if(data == "aborted") {
                        console.log(`${funcName}: Request aborted`);
                        // PUSH NOTIFICATION 
                        setTimeout( () => { removeEntity(entity, loading)} ,5000); 
                    }
                } 

                return "failed"
            }
            catch(err){  
            console.error(`${funcName} error: ${err.message}`);             
            }   

        
                }

    const getEntities = async ( ) => { 
        // FETCH REQUEST WILL TIMEOUT AFTER 20 SECONDS
        getEntitiesLoading.value = true; 
        let funcName        = "createEntity";
        const form          = new FormData();   
        const URL           = '/api/get/entities';
     
        let query            = {}
        query["account"]     = UserStore.getID;
                
        try {
            
            const [status, data] = await FetchStore.POST(URL, JSON.stringify(query), {'Accept': 'application/json', 'Content-Type': 'application/json'} );
            getEntitiesLoading.value = false;
            if(status){
                    
            let keys        = Object.keys(data);
            if(keys.includes("status")){                    
    
                if(data["status"] == "ok"){    
                    entities.value = [...data["entities"]];      
                    return   "ok";                 
                } 
                if(data["status"] == "exist"){    
                    entities.value = [...data["entities"]];      
                    return   "exist";                 
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
                    setTimeout( () => { getEntities() } ,1000); 
                }
                else if(data == "unknown") {
                    console.log(`${funcName}: Unknown response`);
                    return "unknown"  // Empty object
                }
                else if(data == "aborted") {
                    console.log(`${funcName}: Request aborted`);
                    // PUSH NOTIFICATION 
                    setTimeout( () => { getEntities()} ,5000); 
                }
            } 

            return "failed"
        }
        catch(err){  
        console.error(`${funcName} error: ${err.message}`);             
        }   

    
            }

    const createSiteRequest = async (name, lat, lon, loading) => { 
        // FETCH REQUEST WILL TIMEOUT AFTER 20 SECONDS
        loading.value = true; 
        let funcName        = "createSiteRequest"; 
        const URL           = '/api/site/request';
 
        let query            = {}
        query["account"]     = UserStore.getID;
        query["id"]          = "";
        query["type"]        = "createsite";
        query["name"]        = name;
        query["lat"]         = lat;
        query["lon"]         = lon;
                
        try {
            
            const [status, data] = await FetchStore.POST(URL, JSON.stringify(query), {'Accept': 'application/json', 'Content-Type': 'application/json'} );
            loading.value = false;
            if(status){
                    
            let keys        = Object.keys(data);
            if(keys.includes("status")){                    
    
                if(data["status"] == "created"){         
                    return   "created"; 
                    // PUSH NOTIFICATION                   
                } 
                else if(data["status"] == "failed" ){                            
                    // USER MUST SIGNIN FIRST                
                    console.log("Request failed"); 
                    return   "failed"; 
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
                    setTimeout( () => { createSiteRequest(name, lat, lon, loading) } ,1000); 
                }
                else if(data == "unknown") {
                    console.log(`${funcName}: Unknown response`);
                    return "unknown"  // Empty object
                }
                else if(data == "aborted") {
                    console.log(`${funcName}: Request aborted`);
                    // PUSH NOTIFICATION 
                    setTimeout( () => { createSiteRequest(name, lat, lon, loading)} ,5000); 
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

    const updateSiteRequest = async (siteData, loading) => { 
        // FETCH REQUEST WILL TIMEOUT AFTER 20 SECONDS
        loading.value = true; 
        let funcName        = "updateSiteRequest"; 
        const URL           = '/api/site/request';
    
        const query         = {"type":"siteupdate","account": UserStore.getID,...siteData}
    
                
        try {
            
            const [status, data] = await FetchStore.POST(URL, JSON.stringify(query), { 'Accept': 'application/json', 'Content-Type': 'application/json' } );
            loading.value = false;
            if(status){
                    
            let keys        = Object.keys(data);
            if(keys.includes("status")){                    
    
                if(data["status"] == "submitted"){   
                    site.value = {...data["data"]}                        
                    return   "submitted" 
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
                    setTimeout( () => { updateSiteRequest(siteData) } ,1000); 
                }
                else if(data == "unknown") {
                    console.log(`${funcName}: Unknown response`);
                    return "unknown"  // Empty object
                }
                else if(data == "aborted") {
                    console.log(`${funcName}: Request aborted`);
                    // PUSH NOTIFICATION 
                    setTimeout( () => { updateSiteRequest(siteData)} ,5000); 
                }
            } 

            return "failed"
        }
        catch(err){  
        console.error(`${funcName} error: ${err.message}`);             
        }   

    
            }

    const updateDeviceDashboard = async (device) => {  
        // FETCH REQUEST WILL TIMEOUT AFTER 20 SECONDS
        uddLoading.value = true; 
        let funcName        = "updateDeviceDashboard"; 
        const URL           = '/api/update/device/dashboard';
    
        const query         = {"account": UserStore.getID,...device}
    
                
        try {
            
            const [status, data] = await FetchStore.POST(URL, JSON.stringify(query), { 'Accept': 'application/json', 'Content-Type': 'application/json' } );
            uddLoading.value = false;
            if(status){
                    
            let keys        = Object.keys(data);
            if(keys.includes("status")){                    
    
                if(data["status"] == "updated"){   
                    site.value = {...data["data"]} 
                    // resetDevice();     
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
                    setTimeout( () => { updateDeviceDashboard(device) } ,1000); 
                }
                else if(data == "unknown") {
                    console.log(`${funcName}: Unknown response`);
                    return "unknown"  // Empty object
                }
                else if(data == "aborted") {
                    console.log(`${funcName}: Request aborted`);
                    // PUSH NOTIFICATION 
                    setTimeout( () => { updateDeviceDashboard(device)} ,5000); 
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
                    setTimeout( () => { getPageCount(search) } ,1000); 
                }
                else if(data == "unknown") {
                    console.log(`${funcName}: Unknown response`);
                    // return "unknown"  // Empty object
                }
                else if(data == "aborted") {
                    console.log(`${funcName}: Request aborted`);
                    // PUSH NOTIFICATION 
                    setTimeout( () => { getPageCount(search)} ,5000); 
                }
            } 

           
        }
        catch(err){  
        console.error(`${funcName} error: ${err.message}`);             
        }   

    
            }

    const getPageCountEntity = async (search=false) => { 
        // FETCH REQUEST WILL TIMEOUT AFTER 20 SECONDS 
        let funcName        = "getPageCountEntity";
        const form          = new FormData();   
        const URL           = '/api/get/entity/pagecount';    
        
        form.set("account", UserStore.getID)
        form.set("search", siteSearchPagesEntity.value.search) 
        form.set("ops",  (search)? 'search' : '')   
                
        try {
            
            const [status, data] = await FetchStore.POST(URL, form, {  } );
         
            if(status){
                    
                let keys        = Object.keys(data);
                if(keys.includes("status")){                    
         
                    if(data["status"] == "ok"){     
                        if(search == true){
                            siteSearchPagesEntity.value.count = data["count"]; 
                        }                        
                        else{
                            sitePagesEntity.value.count = data["count"]; 
                        }     
                        
                        // PUSH NOTIFICATION                   
                    } 
                    else if(data["status"] == "failed" ){                            
                        // USER MUST SIGNIN FIRST                
                        console.log("Request failed");   
                        if(search == true){
                            siteSearchPagesEntity.value.count = 0; 
                        }                        
                        else{
                            sitePagesEntity.value.count = 0; 
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
                    setTimeout( () => { getPageCountEntity(search) } ,1000); 
                }
                else if(data == "unknown") {
                    console.log(`${funcName}: Unknown response`);
                    // return "unknown"  // Empty object
                }
                else if(data == "aborted") {
                    console.log(`${funcName}: Request aborted`);
                    // PUSH NOTIFICATION 
                    setTimeout( () => { getPageCountEntity(search)} ,5000); 
                }
            } 

           
        }
        catch(err){  
        console.error(`${funcName} error: ${err.message}`);             
        }   

    
            }

    const getPage = async (page, search=false) => { 
        // FETCH REQUEST WILL TIMEOUT AFTER 20 SECONDS 
        // historyLoading.value = true;
        let funcName        = "getPage";
        const form          = new FormData();   
        const URL           = '/api/get/page';    
        
        form.set("account", UserStore.getID) 
        form.set("search", siteSearchPages.value.search) 
        form.set("ops",  (search)? 'search' : '')   
        form.set("page", page - 1) 
                
        try {
            
            const [status, data] = await FetchStore.POST(URL, form, {  } );
            // historyLoading.value = false;
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

    const getPageEntity = async (page, search=false) => { 
        // FETCH REQUEST WILL TIMEOUT AFTER 20 SECONDS 
        // historyLoading.value = true;
        let funcName        = "getPageEntity";
        const form          = new FormData();   
        const URL           = '/api/get/entity/page';    
        
        form.set("account", UserStore.getID) 
        form.set("search", siteSearchPages.value.search) 
        form.set("ops",  (search)? 'search' : '')   
        form.set("page", page - 1) 
                
        try {
            
            const [status, data] = await FetchStore.POST(URL, form, {  } );
            // historyLoading.value = false;
            if(status){
                    
            let keys        = Object.keys(data);
            if(keys.includes("status")){                    
    
                if(data["status"] == "ok"){    
                    if(search){
                        siteSearchPagesEntity.value.pages[data["page"]] =  data["data"]; 
                    }
                    else {
                        sitePagesEntity.value.pages[data["page"]] =  data["data"]; 
                    }     
                    
                  
                    // PUSH NOTIFICATION                   
                } 
                else if(data["status"] == "failed" ){                            
                    // USER MUST SIGNIN FIRST                
                    console.log("Request failed"); 
                    if(search){
                        siteSearchPagesEntity.value.pages  =  {}; 
                    }
                    else {
                        sitePagesEntity.value.pages =  {}; 
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
                    setTimeout( () => { getPageEntity(page, search) } ,1000); 
                }
                else if(data == "unknown") {
                    console.log(`${funcName}: Unknown response`);
                    // return "unknown"  // Empty object
                }
                else if(data == "aborted") {
                    console.log(`${funcName}: Request aborted`);
                    // PUSH NOTIFICATION 
                    setTimeout( () => { getPageEntity(page, search)} ,5000); 
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

    const getSites = async ( loading) => { 
        // FETCH REQUEST WILL TIMEOUT AFTER 20 SECONDS 
        loading   = true;
        let funcName        = "getSites";
        const form          = new FormData();   
        const URL           = '/api/get/sites';    
        
        form.set("account", UserStore.getID)  
                
        try {
            
            const [status, data] = await FetchStore.POST(URL, form, {  } );
            loading   = false;
        
            if(status){
                    
            let keys        = Object.keys(data);
            if(keys.includes("status")){                    
    
                if(data["status"] == "ok"){    
                    userSites.value = {...data["data"]};  
                    return ["found",data["data"]];              
                } 
                else if(data["status"] == "failed" ){                            
                    // USER MUST SIGNIN FIRST                
                    console.log("Request failed"); 
                    return ["failed", []];
                    
                    // PUSH NOTIFICATION
                        }    
                else if(data["status"] == "formErrors" ){                            
                    // USER MUST SIGNIN FIRST
                    console.log("Form Errors"); 
                    return ["failed", []];
                        }  
            }
            }
            else {
                if(data == "unauthorized") {
                    console.log(`${funcName}: Unauthorized User`);
                    // return "unauthorized"  // Empty object
                    return ["failed", []];
                }
                else if(data == "token refreshed") {
                    console.log(`${funcName}: Retrying in in 1 seconds`);
                    setTimeout( () => { getSites( loading) } ,1000); 
                }
                else if(data == "unknown") {
                    console.log(`${funcName}: Unknown response`);
                    // return "unknown"  // Empty object
                    return ["failed", []];
                }
                else if(data == "aborted") {
                    console.log(`${funcName}: Request aborted`);
                    // PUSH NOTIFICATION 
                    setTimeout( () => { getSites(loading)} ,5000); 
                }
            } 

            
        }
        catch(err){  
        console.error(`${funcName} error: ${err.message}`);      
        return ["failed", []];    
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

    const getAccount = async  (loading) => { 
        // FETCH REQUEST WILL TIMEOUT AFTER 20 SECONDS 
        loading   = true;
        let funcName        = "getSite";
        const form          = new FormData();   
        const URL           = '/api/get/account';    
        
        form.set("account", UserStore.getID)
                
        try {
            
            const [status, data] = await FetchStore.POST(URL, form, {  } );
            loading   = false;
        
            if(status){
                    
            let keys        = Object.keys(data);
            if(keys.includes("status")){                    
    
                if(data["status"] == "ok"){    
                    userAccount.value = {...data["account"]};   
                    return ["found", data["account"]]  
                    
                    
                    // PUSH NOTIFICATION                   
                } 
                else if(data["status"] == "failed" ){                            
                    // USER MUST SIGNIN FIRST                
                    console.log("Request failed"); 
                    return ["failed", {}];
                                          }    
                else if(data["status"] == "formErrors" ){                            
                    // USER MUST SIGNIN FIRST
                    console.log("Form Errors"); 
                
                    return ["failed", {}];
                        }  
            }
            }
            else {
                if(data == "unauthorized") {
                    console.log(`${funcName}: Unauthorized User`);
                    // return "unauthorized"  // Empty object
                    return ["failed", {}];
                }
                else if(data == "token refreshed") {
                    console.log(`${funcName}: Retrying in in 1 seconds`);
                    setTimeout( () => { getAccount(loading) } ,1000); 
                }
                else if(data == "unknown") {
                    console.log(`${funcName}: Unknown response`);
                    // return "unknown"  // Empty object
                    return ["failed", {}];
                }
                else if(data == "aborted") {
                    console.log(`${funcName}: Request aborted`);
                    // PUSH NOTIFICATION 
                    setTimeout( () => { getAccount(loading)} ,5000); 
                }
            } 

            
        }
        catch(err){  
        console.error(`${funcName} error: ${err.message}`);             
        }   

    
            }


    const getRequests = async (loading) => { 
        // FETCH REQUEST WILL TIMEOUT AFTER 20 SECONDS 
        loading.value   = true;
        let funcName        = "getRequests";
        const form          = new FormData();   
        const URL           = '/api/get/requests';    
        
        form.set("account", UserStore.getID) 
                    
        try {
            
            const [status, data] = await FetchStore.POST(URL, form, {  } );
            loading.value   = false;
        
            if(status){
                    
            let keys        = Object.keys(data);
            if(keys.includes("status")){                    
    
                if(data["status"] == "ok"){    
                   requests.value = [...data["requests"]];                      
                    
                    // PUSH NOTIFICATION                   
                } 
                else if(data["status"] == "failed" ){                            
                    // USER MUST SIGNIN FIRST                
                    console.log("Request failed"); 
                    
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
                    setTimeout( () => { getRequests(loading) } ,1000); 
                }
                else if(data == "unknown") {
                    console.log(`${funcName}: Unknown response`);
                    // return "unknown"  // Empty object
                }
                else if(data == "aborted") {
                    console.log(`${funcName}: Request aborted`);
                    // PUSH NOTIFICATION 
                    setTimeout( () => { getRequests(loading)} ,5000); 
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
    uddLoading, 
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
    createEntityLoading,
    getEntitiesLoading,
    createDeviceLoading,
    updateAccLoading,
    removeAccLoading,
    selectedAccount,
    selectedAccEdited,
    allStaffAccounts,
    assignListAdmin,
    sitePages,
    overlay,
    emailList,
    entities,
    spss,
    site,
    siteSearchPagesEntity,
    sitePagesEntity,
    openCreateEntity,
    userSites,
    device,
    openSiteSearch,
    openCreateSite,
    dashboardMenu,
    userSearch,
    paramDetails,
    historyLoading,
    accSearchLoading,
    updateDeviceLoading,
    updateSiteLoading,
    assignUserLoading,
    deleteDeviceLoading,
    emailSelectedItem,
    profileRouteItems,
    caribbeanCountries,
    userAccount,
    requests,
    getPageEntity, 
    getPageCountEntity,
    removeEntity,
    removeSite,
    getEntities,
    getRequests,
    createSiteRequest,
    updateSiteRequest,
    updateDeviceDashboard,
    getAccount,
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
    getSites,
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
    approveOrDenyRequest,
    createEntity
        
       }
},{ persist: {storage: sessionStorage} });