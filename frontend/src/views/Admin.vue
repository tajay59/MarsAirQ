<template>
  <div  class="relative" >
    <RouterView />
    <!-- image="https://cdn.vuetifyjs.com/images/backgrounds/bg-2.jpg" -->

    <VNavigationDrawer v-model="adminDrawer" width="270" :floating="(route.name == 'Admin')? false : true"   >
      <template #prepend >
        <div class="my-3 mt-7"  >
          <VImg v-if="!darkmode" src="@/assets/logo6_light.png" width="200" max-height="150" class="mx-15" style=" cursor: pointer;" @click="router.push({name:'Home'})"  >
                <template v-slot:placeholder>
                    <div class="d-flex align-center justify-center fill-height">
                        <VProgressCircular color="grey-lighten-4" indeterminate ></VProgressCircular>
                    </div>
                </template>
            </VImg>
            <VImg v-else src="@/assets/logo6_white.png" width="200"  max-height="150" class="mx-15" style=" cursor: pointer;" @click="router.push({name:'Home'})"  >
                <template v-slot:placeholder>
                    <div class="d-flex align-center justify-center fill-height">
                        <VProgressCircular color="grey-lighten-4" indeterminate ></VProgressCircular>
                    </div>
                </template>
            </VImg>
            <!-- <VImg  src="@/assets/logo.png"  max-height="100" height="100%">              
              <template v-slot:placeholder>
                <div class="d-flex align-center justify-center fill-height">
                  <VProgressCircular color="grey-lighten-4" indeterminate ></VProgressCircular>
                </div>
              </template>
            </VImg>  -->
            <!-- <div class="mt-n5 text-center" >
              <span class="roboto-black-italic !text-purple-800  dark:!text-purple-300 text-xl font-bold " style=" cursor: pointer" @click="router.push({name:'Home'})">Mars </span><span class="roboto-condensed-200 !text-gray-500 dark:!text-gray-400">Air</span><span class="!text-purple-800  dark:!text-purple-300 font-weight-bold text-h4">Q</span> 
            </div> -->
          </div>     
      </template>

        <VList nav    >
          
          <VDivider :opacity="100" class="border-neutral-300 dark:border-neutral-600 mb-5"  />
          <VListItem>
            <p class="text-subtitle-1" >Admin</p>
          </VListItem>      

          <VListItem v-for="route in routeItems" class="mr-10" style="text-decoration: none;"   :title="route.title" :value="route.name" :to="route.route">
            <template #prepend >
              <VBadge  v-if="route.name == 'AdminRequests'" floating :content="requests.length" color="!bg-green-500 dark:!bg-green-700" class="" :offset-y="7" >
                  <Icon  :icon="route.icon" width="24" height="24" class="!text-neutral-500 dark:!text-neutral-300" /> 
              </VBadge>             
              <Icon v-else :icon="route.icon" width="24" height="24" class="!text-neutral-500 dark:!text-neutral-300 mr-3" /> 
            </template>
          </VListItem>        
        
        </VList>
      </VNavigationDrawer>
  </div>
 
      
</template>

<script setup>
// IMPORTS    
import { ref,watch ,onMounted,computed } from "vue";   
import { useUserStore } from '@/stores/userStore'; 
import { useAppStore } from "@/stores/appStore";
import { useRoute ,useRouter } from "vue-router";
import { useDisplay } from 'vuetify';
import { storeToRefs } from 'pinia';
import { Icon } from '@iconify/vue';

// VARIABLES 
const router            = useRouter();
const route             = useRoute(); 
const UserStore         = useUserStore(); 
const AppStore          = useAppStore();
const { xs,smAndDown,smAndUp, mdAndUp }   = useDisplay();
const {id,loggedIn,image, darkmode}       = storeToRefs(UserStore);
const {newRegistrations, staffs, users,adminDrawer, selectedAccount, requests}   = storeToRefs(AppStore);
const myWorker          = ref(null);
const siteWorker        = ref(null);
const requestLoading    = ref(false);



const routeItems   = ref([
        {"icon":"mdi:accounts-group","title":"Accounts","route":"/admin/accounts","name":"Accounts"},  
        {"icon":"mdi:map-markers","title":"Entities","route":"/admin/entities","name":"Entities"}, 
        {"icon":"streamline:send-email-solid","title":"Email List","route":"/admin/emails","name":"Emails"},
        {"icon":"fluent:branch-request-16-filled","title":"Requests","route":"/admin/requests","name":"AdminRequests"}
    ])



// FUNCTIONS
const getAccounts = () => {
    if (!!window.SharedWorker) {
        if(!!myWorker.value){
            const cookie        = UserStore.getCookie("csrf_access_token"); 
            // myWorker.value.port.postMessage({"user": UserStore.getID, "cookie": cookie});   
            myWorker.value.port.postMessage({"user": UserStore.getID, "cookie": cookie, "selected": (!!selectedAccount.value)? selectedAccount.value.id : null, "role": (!!selectedAccount.value)? selectedAccount.value.role :null });     
        }
    }
}

const getSites = () => {
    if (!!window.SharedWorker) {
        if(!!siteWorker.value){
            const cookie        = UserStore.getCookie("csrf_access_token");         
            siteWorker.value.port.postMessage({"user": UserStore.getID, "cookie": cookie });      
        }
    }
}

onMounted(()=>{
    // console.log("TEMPLATE COMPONENT CREATED");
 
    if (!!window.SharedWorker) {
        myWorker.value    = new SharedWorker("/src/assets/js/adminAccountsWorker.js");
        siteWorker.value  = new SharedWorker("/src/assets/js/siteWorker.js");
    
        myWorker.value.port.onmessage = (e) => { 
            let {newRegistrations, staffs, users, selected} = e.data;
            AppStore.setAdminAccountVariables("newRegistrations",newRegistrations);
            AppStore.setAdminAccountVariables("staffs",staffs);
            AppStore.setAdminAccountVariables("users",users); 
            if(!!selected)
              AppStore.setSelectedAccount(selected);
        };

        myWorker.value.onerror = (error) => {
        console.log(`New Registrations Worker error: ${error.message}`);
        throw error;       
      };   

        // SITE WORKER   
        siteWorker.value.port.onmessage = (e) => { 
            let {sites} = e.data;
            if(!!sites){
                AppStore.setSites(sites);
            }            
        };

        siteWorker.value.onerror = (error) => {
        console.log(`Site Worker error: ${error.message}`);
        throw error;
      }; 

      getAccounts();
      getSites(); // NOT USED.  REPLACED BY getPageCount()
    }

    AppStore.getPageCount();
    AppStore.getPage(1);
    AppStore.getRequests(requestLoading);
    
})

 
 
</script>

<style>
/*   Style */

 
</style>