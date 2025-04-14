<template>
<VContainer fluid class=" ma-0 pa-0"  >
    <VRow>
        <!-- expand-on-hover -->
        <VNavigationDrawer   rail  :hidden="smAndDown" color="secon dary"  >
            <!-- <VList density="compact" nav router>
                <VListItem class="text-caption" >
                    <span class="roboto-black-italic text-primary " style="font-size:xx-large ; cursor: pointer" @click="router.push({name:'Home'})">Mars </span><span class="roboto-condensed-200  ">Air</span><span class="text-primary font-weight-bold text-h4">Q</span> 
                </VListItem>
            </VList>
            <VDivider></VDivider> -->
            <VList style="cursor: pointer;" @click="router.push({name:'Profile'})" >
                <VListItem :title="UserStore.user" :subtitle="UserStore.email" class="pa-1" >
                    <template v-slot:prepend>
                        <VImg v-if="UserStore.loggedIn" style="border-radius: 50%; border: 2px solid grey; margin-right: 10px;" cover :src="`/api/images/${image}`" width="50" height="50" >
                            <template v-slot:placeholder>
                                <div class="d-flex align-center justify-center fill-height">
                                <VProgressCircular color="grey-lighten-4" indeterminate ></VProgressCircular>
                                </div>
                            </template>
                        </VImg> 
                    </template>
                </VListItem>
            </VList>

            <VDivider></VDivider>
            

            <VList density="compact" nav router>           
                <VListItem class="text-caption !no-underline "  :active="(route.name == item.name)? true: false" density="compact" v-for="item in drawerItems" :key="item.title"     :value="item.title" :to="item.route">                      
                    <VBtn :icon="item.icon" v-tooltip.bottom="item.title " density="compact" variant="text"  class="!text-purple-800 dark:!text-purple-400"  />                       
                </VListItem>               
            </VList>

                
            
            <template v-slot:append> 
                <VList density="compact" nav router class="rounded-lg" color="red">
                    <VListItem >
                        
                        <VBtn   variant="text"  title="Profile" @click="router.push({name:'Profile'})" icon density="compact"  >
                            <Icon icon="iconamoon:profile-fill" width="24" height="24" class="!text-purple-800 dark:!text-purple-400" />
                        </VBtn>

                        <VBtn class="my-5"  variant="text"  :title="(UserStore.loggedIn)? 'Logout': 'Login'" @click="(UserStore.loggedIn)? UserStore.userLogout() : router.push({name:'Login'}) "  icon density="compact"     >
                            <Icon v-if="UserStore.loggedIn"  icon="majesticons:login" width="24" height="24" class="!text-purple-800 dark:!text-purple-400"  />
                            <Icon v-else icon="majesticons:logout" width="24" height="24" class="!text-purple-800 dark:!text-purple-400"  />
                        </VBtn> 

                        <VBtn  :elevation="0"  variant="text"  @click="darkmode = !darkmode"   title="Theme"  icon density="compact"  >     
                            <Icon v-if="darkmode" icon="line-md:sun-rising-filled-loop" width="24" height="24" class="!text-purple-800 dark:!text-purple-400"  />       
                            <Icon v-else   icon="line-md:sunny-filled-loop-to-moon-filled-loop-transition" width="24" height="24" class="!text-purple-800 dark:!text-purple-400"  />   
                        </VBtn>
 
                    </VListItem>                     
                </VList>
                 
            </template>
        </VNavigationDrawer>
        <!-- <Notification/> -->
        <Modal />
    </VRow>
</VContainer>

  </template>
  
  <script setup>

import { useRoute, useRouter } from "vue-router";
import { ref,reactive, onMounted,onBeforeMount,watch,computed } from 'vue';
import { storeToRefs } from "pinia";
import { useDisplay } from 'vuetify'
import { useAppStore } from '@/stores/appStore';
import { useUserStore } from '@/stores/userStore'; 
import { useNotificationStore } from '@/stores/notificationStore';
import { useTheme } from 'vuetify'
import Notification from "./Notification.vue";
import Modal from "./Modal.vue";
import { Icon } from '@iconify/vue';
 


// VARIABLES
const { xs,smAndDown,smAndUp, mdAndUp }   = useDisplay();
const AppStore                      = useAppStore();
const UserStore                     = useUserStore(); 
const NotificationStore             = useNotificationStore();
const {id,loggedIn,image, darkmode}           = storeToRefs(UserStore);
const {drawerItems}           = storeToRefs(AppStore)
const router                        = useRouter();
const route                         = useRoute(); 
const drawer                        = ref(false);
const theme                         = useTheme();
//const darkmode                      = ref(false);
 


// WATCHERS
watch(darkmode,  (mode) => {
  theme.global.name.value = mode ?  'darkMode' : 'lightMode';
  localStorage.setItem("theme",mode ? 'darkMode' : 'lightMode');  
});

watch(id,   (user) => {
//   console.log(`USER : ${user}  ACTIVE ${!!user}`);   
  if(!!user == false) {
    setTimeout(async ()=>{
        if(loggedIn){
        await UserStore.Auth() 
    }
    },5000)
    
  }
});


// FUNCTIONS
onBeforeMount(()=>{
  // SAVE THEME TO LOCALSTORAGE MAKING IT PERSIST BROWSER REFRESH

  if(localStorage.getItem("theme") != null){
    theme.global.name.value = localStorage.getItem("theme");
    darkmode.value = theme.global.current.value.dark;
  }
  else{
    // localStorage.setItem("theme",theme.global.current.value.dark ? 'dark' : 'light');
    // darkmode.value = theme.global.current.value.dark;
    localStorage.setItem("theme",theme.global.current.value.dark ? 'darkMode' : 'lightMode');
    darkmode.value = theme.global.current.value.dark;    
  }  
});

onMounted(()=>{
    // console.log(`CURRENT ${AppStore.currentRoute}`)
})

const userLogout = async () =>{
    // COLLECT USER INPUT FROM LOGIN FORM THEN POST TO FLASK API
    
    // let Loader      = document.querySelector("#loader");
    const address       = '/api/logout';

    // FETCH REQUEST WILL TIMEOUT AFTER 20 SECONDS 
    const controller    = new AbortController();
    const signal        = controller.signal;
    const id            = setTimeout(()=>{controller.abort()},60000);

    // UPDATE PINIA STORES
    UserStore.clearUser()    
    deleteAllCookies()  

    try {
        const response  = await fetch(address,{ method: 'GET', signal: signal  });
        const data      = await response.json();
        let keys        = Object.keys(data);

        // console.log(data);
        

        if(keys.includes("message")){
            //console.log(data);
            if( data['message'] === "loggedOut"  ){   

                // PUSH NOTIFICATION              message,color,      textColor,      variant, icon,                 iconColor,   state
                NotificationStore.pushNotification("Logged out!","secondary","text-onSecondary","flat","fas fa-circle-check","onSecondary",true,2000); 

                
                // REDIRECT TO EXPLORE PAGE SINCE LOGOUT WAS SUCCESSFUL 
                setTimeout(()=>{router.replace( {name:"Login"});},1000);
                
            }
                                            
            else{
                
                // PUSH NOTIFICATION 
                NotificationStore.pushNotification( "Unable to logout" ,"error","text-onError","flat","fas fa-triangle-exclamation","onError",true,2000);  
            }
        }else{
                
            // PUSH NOTIFICATION 
            NotificationStore.pushNotification( "Unable to logout"  ,"error","text-onError","flat","fas fa-triangle-exclamation","onError",true,2000);  
        }
  
      }
      catch(err){
        if( err.message === "The user aborted a request."){
            console.log("REQUEST TIMEDOUT");
                // UPDATE PINIA STORE
                UserStore.loggedIn  = false;
                UserStore.user      = "";

                // PUSH NOTIFICATION 
                NotificationStore.pushNotification("Request timed out"  ,"error","text-onError","flat","fas fa-triangle-exclamation","onError",true,2000);  
        }
        // console.error('Logout error: ', err.message);    
        if( data['message'] === "loggedOut"  ){   

            // PUSH NOTIFICATION              message,color,      textColor,      variant, icon,                 iconColor,   state
            NotificationStore.pushNotification("Logged out!","secondary","text-onSecondary","flat","fas fa-circle-check","onSecondary",true,2000); 

            // REDIRECT TO EXPLORE PAGE SINCE LOGOUT WAS SUCCESSFUL 
            setTimeout(()=>{router.replace( {name:"Login"});},1000);

            }     
        
  
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
  </script>
  