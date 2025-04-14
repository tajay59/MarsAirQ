<template>
<div  > 
    <RouterView />
    <SpeedDial :model="items"  pt:menuitem="m-2" :radius="80"  direction="left" style="position: absolute; top: calc(10% - 2rem); right: 220px; z-index: 20000;"  :tooltipOptions="{ position: 'top' }" >    </SpeedDial>
    <Toast />
    <VCard  position="absolute" style="z-index: 21000;  top: calc(10% - 2rem); right: 50px" flat density="compact">
      <VList density="compact" nav router class="rounded-lg pa-0" color="red" >
          <VListItem >     
            <VBtn class="mx-1"  variant="text"  title="Home" @click="router.push({name:'Home'})" icon density="compact"  >
                  <Icon icon="iconamoon:home-fill" width="24" height="24" class="!text-purple-800 dark:!text-purple-400" />
              </VBtn>

              <VBtn   variant="text"  title="Profile" @click="router.push({name:'Profile'})" icon density="compact"  >
                  <Icon icon="iconamoon:profile-fill" width="24" height="24" class="!text-purple-800 dark:!text-purple-400" />
              </VBtn>

              <VBtn  class="mx-1"  variant="text"  :title="(UserStore.loggedIn)? 'Logout': 'Login'" @click="(UserStore.loggedIn)? UserStore.userLogout() : router.push({name:'Login'}) "  icon density="compact"     >
                  <Icon v-if="UserStore.loggedIn"  icon="majesticons:login" width="24" height="24" class="!text-purple-800 dark:!text-purple-400"  />
                  <Icon v-else icon="majesticons:logout" width="24" height="24" class="!text-purple-800 dark:!text-purple-400"  />
              </VBtn> 

              <VBtn  :elevation="0"  variant="text"  @click="darkmode = !darkmode"   title="Theme"  icon density="compact"  >     
                  <Icon v-if="darkmode" icon="line-md:sun-rising-filled-loop" width="24" height="24" class="!text-purple-800 dark:!text-purple-400"  />       
                  <Icon v-else   icon="line-md:sunny-filled-loop-to-moon-filled-loop-transition" width="24" height="24" class="!text-purple-800 dark:!text-purple-400"  />   
              </VBtn>

 
          </VListItem>                     
      </VList>
    </VCard>
</div>       
</template>

<script setup>
// IMPORTS   
import { useToast } from 'primevue/usetoast';
import { ref,watch ,onMounted,computed } from "vue";   

import { useUserStore } from '@/stores/userStore'; 
import { useRoute ,useRouter } from "vue-router";
import { storeToRefs } from 'pinia';
import { Icon } from '@iconify/vue';

// VARIABLES 
const router                    = useRouter();
const route                     = useRoute(); 
const UserStore         = useUserStore(); 
const {id,loggedIn,image, darkmode}           = storeToRefs(UserStore);
const firstname         = ref("John");
const lastname          = ref("Doe");
const text              = ref("");
const changedText       = ref(""); 

const items = ref([
    /*
    {
        label: 'Add',
        icon: 'pi pi-pencil',
        command: () => {
            toast.add({ severity: 'info', summary: 'Add', detail: 'Data Added', life: 3000 });
        }
    },*/
    {
        label: 'Analysis',
        icon: 'pi pi-sparkles',
        command: () => {
            // toast.add({ severity: 'success', summary: 'Update', detail: 'Data Updated', life: 3000 });  
            router.push('/analytics/analysis');
        }
    },
    {
        label: 'Live',
        icon: 'pi pi-caret-right',
        command: () => {
            // toast.add({ severity: 'error', summary: 'Delete', detail: 'Data Deleted', life: 3000 });
            router.push('/analytics/live');
        }
    },
    {
        label: 'Dashboard',
        icon: 'pi pi-objects-column',
        command: () => {
            router.push('/analytics/dashboard');
        }
    },
    {
        label: 'Map',
        icon: 'pi pi-map',
        command: () => {
          router.push('/analytics/map');
        }
    }
])

// PROPS
const props = defineProps({
    item:{type:String,default:""},
})

// WATCHERS
watch(text,  (newText, oldText) => {
  console.log(newText); 
  changedText.value = newText ;
});

// COMPUTED PROPERTIES
const fullname = computed(()=>{    
    return `${firstname.value} ${lastname.value}`;
});


// FUNCTIONS
onMounted(()=>{
    console.log("TEMPLATE COMPONENT CREATED");
    // pingPong();
})


const pingPong = async ()=>{
        // FETCH REQUEST WILL TIMEOUT AFTER 20 SECONDS 
        // const UserStore     = useUserStore(); 
        const controller    = new AbortController();
        const signal        = controller.signal;
        const id            = setTimeout(()=>{controller.abort()},10000);
        const request       = {"message":"ping"}
        const token         = UserStore.GetCSRFToken;
        const cookie        = UserStore.getCookie("csrf_access_token"); 
    
        try {
            const response  = await fetch('/api/ping',{ method: 'POST', body:JSON.stringify(request), signal: signal ,headers: { 'Accept': 'application/json', 'Content-Type': 'application/json','X-CSRFToken': token,"X-CSRF-TOKEN": cookie } });
            const data      = await response.json(); 
            let keys        = Object.keys(data);
            
            console.log(data);
    
            if (keys.includes("status")){
    
                if (data["status"] === "pong"){
                  //User is already logged in                
                  console.log("GOT PONG FROM PING") ;    
                } 
               
                
            }
            
    
        }
        catch(err){
          if( err.message === "The user aborted a request."){
            console.log("REQUEST TIMEDOUT"); 
          }
          console.error('PING PONG error: ', err.message);   
    
        }    
      
    
    }
 
</script>

<style>
/*   Style */

 
</style>