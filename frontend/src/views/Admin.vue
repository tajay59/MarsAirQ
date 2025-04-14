<template>
  <div  class="relative" >
    <RouterView />
    <!-- image="https://cdn.vuetifyjs.com/images/backgrounds/bg-2.jpg" -->

    <VNavigationDrawer width="270" permanent :floating="(route.name == 'Admin')? false : true" v-if="mdAndUp" >
      <template #prepend >
        <div class="my-3 mt-7"  >
            <VImg  src="@/assets/logo.png"  max-height="100" height="100%">              
              <template v-slot:placeholder>
                <div class="d-flex align-center justify-center fill-height">
                  <VProgressCircular color="grey-lighten-4" indeterminate ></VProgressCircular>
                </div>
              </template>
            </VImg> 
            <div class="mt-n5 text-center" >
              <span class="roboto-black-italic !text-purple-800  dark:!text-purple-300 text-xl font-bold " style=" cursor: pointer" @click="router.push({name:'Home'})">Mars </span><span class="roboto-condensed-200 !text-gray-500 dark:!text-gray-400">Air</span><span class="!text-purple-800  dark:!text-purple-300 font-weight-bold text-h4">Q</span> 
            </div>
          </div>     
      </template>

        <VList nav    >
          <VListItem class="justify-center" justify="center" >
            <div class="flex justify-center " >
              <VBtn class="mx-1"  variant="text"  title="Home" @click="router.push({name:'Home'})" icon density="compact"  >
                  <Icon icon="iconamoon:home-fill" width="24" height="24" class="!text-neutral-600 dark:!text-neutral-400" />
              </VBtn>

              <VBtn   variant="text"  title="Profile" @click="router.push({name:'Profile'})" icon density="compact"  >
                  <Icon icon="iconamoon:profile-fill" width="24" height="24" class="!text-neutral-600 dark:!text-neutral-400" />
              </VBtn>

              <VBtn  class="mx-1"  variant="text"  :title="(UserStore.loggedIn)? 'Logout': 'Login'" @click="(UserStore.loggedIn)? UserStore.userLogout() : router.push({name:'Login'}) "  icon density="compact"     >
                  <Icon v-if="UserStore.loggedIn"  icon="majesticons:login" width="24" height="24" class="!text-neutral-600 dark:!text-neutral-400"  />
                  <Icon v-else icon="majesticons:logout" width="24" height="24" class="!text-neutral-600 dark:!text-neutral-400"  />
              </VBtn> 

              <VBtn  :elevation="0"  variant="text"  @click="darkmode = !darkmode"   title="Theme"  icon density="compact"  >     
                  <Icon v-if="darkmode" icon="line-md:sun-rising-filled-loop" width="24" height="24" class="!text-neutral-600 dark:!text-neutral-400"  />       
                  <Icon v-else   icon="line-md:sunny-filled-loop-to-moon-filled-loop-transition" width="24" height="24" class="!text-neutral-600 dark:!text-neutral-400"  />   
              </VBtn> 
            </div>
          </VListItem>
          <VDivider :opacity="100" class="border-neutral-300 dark:border-neutral-600 mb-5"  />
          <VListItem>
            <p class="text-subtitle-1" >Admin</p>
          </VListItem>      

          <VListItem v-for="route in routeItems" class="mr-10" style="text-decoration: none;"  :prepend-icon="route.icon" :title="route.title" :value="route.name" :to="route.route"></VListItem>        
        
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
const {newRegistrations, staffs, users, selectedAccount}   = storeToRefs(AppStore);
const myWorker          = ref(null);
const siteWorker        = ref(null);



const routeItems   = ref([
        {"icon":"mdi:mdi-account-group","title":"Accounts","route":"/admin/accounts","name":"Accounts"},  
        {"icon":"mdi:mdi-map-marker-multiple","title":"Sites","route":"/admin/sites","name":"Sites"}, 
        {"icon":"mdi mdi-email-fast","title":"Email List","route":"/admin/emails","name":"Emails"}, 
        // {"icon":"mdi:mdi-lock","title":"Analytics","route":"/analytics/map","name":"Analytics"},   
        // {"icon":"mdi:mdi-lock","title":"Admin","route":"/admin","name":"Admin"},   
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
            console.log(e.data);
            AppStore.setAdminAccountVariables("newRegistrations",newRegistrations);
            AppStore.setAdminAccountVariables("staffs",staffs);
            AppStore.setAdminAccountVariables("users",users);
            // console.log(e.lastEventId);
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
})

 
 
</script>

<style>
/*   Style */

 
</style>