<template> 

    <VBottomNavigation v-model="value" bg-color="surface"   :active="active" elevation="0"   border  class="rounded-t-[12px] bottom-0   overflow-visible"  > 
      
      <VBtn class="text-caption"  @click="router.push({name: 'Research'});toTop()"  >
        <svg  width="20" height="20" viewBox="0 0 48 48" class="dark:text-neutral-200 text-neutral-800"><g fill="currentColor"><path d="M27 27.84a11.74 11.74 0 0 1-7-2.334V41a1 1 0 0 0 1 1h5a1 1 0 0 0 1-1zM26 18h-4.605A5.98 5.98 0 0 0 27 22.021V19a1 1 0 0 0-1-1"/><path fill-rule="evenodd" d="M21.113 24.028a9.93 9.93 0 0 1-4.013-7.983c0-5.493 4.453-9.945 9.945-9.945s9.945 4.453 9.945 9.945a9.9 9.9 0 0 1-1.82 5.737l-.05.069l5.739 5.738l-1.498 1.497l-5.656-5.655l-.07.062a9.9 9.9 0 0 1-6.59 2.497H27V26c-2.242-.01-4.27-.74-5.887-1.973m13.759-7.983a7.827 7.827 0 1 1-15.654 0a7.827 7.827 0 0 1 15.654 0" clip-rule="evenodd"/><path d="M9 6a1 1 0 0 0-1 1v34a1 1 0 0 0 1 1h5a1 1 0 0 0 1-1V7a1 1 0 0 0-1-1zm23 27a1 1 0 0 1 1-1h5a1 1 0 0 1 1 1v8a1 1 0 0 1-1 1h-5a1 1 0 0 1-1-1z"/></g></svg>
        <span>Research</span>
      </VBtn>

      <VBtn class="text-caption"   @click="router.push({name: 'Map'});toTop()"  >
        <svg  width="20" height="20" viewBox="0 0 512 512"  class="dark:text-neutral-200 text-neutral-800" ><path fill="currentColor" d="M450 128a46 46 0 0 0-44.11 59l-71.37 71.36a45.88 45.88 0 0 0-29 0l-52.91-52.91a46 46 0 1 0-89.12 0L75 293.88A46.08 46.08 0 1 0 106.11 325l87.37-87.36a45.85 45.85 0 0 0 29 0l52.92 52.92a46 46 0 1 0 89.12 0L437 218.12A46 46 0 1 0 450 128"/></svg> 
        <span>Analytics</span>
      </VBtn>
 
      <SpeedDial :model="props.items"  pt:menuitem="m-2"  direction="up" pt:list="flex flex-col place-contents-center" > 
            <template #button="{ toggleCallback, visible }">
                <VBtn @click="toggleCallback(); overlay = !visible"   flat color="transparent" class=" text-caption !h-[50px]" >
                    <Icon icon="gg:menu-grid-o" width="20" height="20" :class="[ '!text-neutral-900 dark:!text-neutral-200']" />
                    <span class="!text-neutral-900 dark:!text-neutral-200" >Menu </span>
                </VBtn>                 
            </template>
            <template #item="{ item, toggleCallback }"> 
                <VSheet  @click="overlay = false" :class="['rounded-[50%] border',(route.path == '/analytics/map')?'!bg-neutral-700':'bg-neutral-100  dark:bg-neutral-700']"   >
                    <VBtn v-if="item.label == 'Login'" :title="(loggedIn)? 'Logout':'Login'" @click="toggleCallback"  icon size="40" :aria-labelledby="item.label" flat color="transparent" variant="text" >                    
                        <Icon v-if="loggedIn" :icon="item.icon" width="24" height="24" :class="[(route.path == '/analytics/map')?'!text-neutral-100':'!text-neutral-500 dark:!text-neutral-300']" />
                        <Icon v-else :icon="item.icon1" width="24" height="24" :class="[(route.path == '/analytics/map')?'!text-neutral-100':'!text-neutral-500 dark:!text-neutral-300']" />
                        <span v-if="loggedIn" class="text-none absolute right-12 !text-neutral-100 dark:!text-neutral-900" >Logout</span>
                        <span v-else class="text-none absolute right-12 !text-neutral-100 dark:!text-neutral-900" >Login</span>
                    </VBtn>  
                    <VBtn v-else-if="item.label == 'Theme'"  title="Theme"  @click="toggleCallback"  icon size="40"  :aria-labelledby="item.label" flat color="transparent" variant="text" >                    
                        <Icon v-if="darkmode" :icon="item.icon" width="24" height="24" :class="[(route.path == '/analytics/map')?'!text-neutral-100':'!text-neutral-500 dark:!text-neutral-300']" />
                        <Icon v-else :icon="item.icon1" width="24" height="24" :class="[(route.path == '/analytics/map')?'!text-neutral-100':'!text-neutral-500 dark:!text-neutral-300']" />
                        <span class="text-none absolute right-12 !text-neutral-100 dark:!text-neutral-900" >{{ item.label }}</span>
                    </VBtn>    
                    <VBtn v-else  @click="toggleCallback"  :title="item.label"  icon size="40"  :aria-labelledby="item.label" flat color="transparent" variant="text" class="relative" >                    
                        <Icon :icon="item.icon" width="24" height="24" :class="[(route.path == '/analytics/map')?'!text-neutral-100':'!text-neutral-500 dark:!text-neutral-300']" />
                        <span class="text-none absolute right-12 !text-neutral-100 dark:!text-neutral-900" >{{ item.label }}</span>
                    </VBtn>   
                </VSheet>              
            </template>
        </SpeedDial> 

    </VBottomNavigation>

  
    <Modal />
     

</template>

<script setup>
// IMPORTS 
 
 
import { useUserStore} from '@/stores/userStore';
import { useAppStore } from "@/stores/appStore";
import { ref,watch ,onMounted, onBeforeMount, computed } from "vue";  
import { useRoute, useRouter } from "vue-router";
import { storeToRefs } from "pinia"; 
import { useDisplay } from 'vuetify';
import { useToast } from 'primevue/usetoast';
import { useTheme } from 'vuetify';
import { Icon } from '@iconify/vue';
import Notification from './Notification.vue';
import Modal from "./Modal.vue";
import _ from 'lodash';
 

// VARIABLES
const { xs,smAndDown,smAndUp, mdAndUp }   = useDisplay(); 
const theme             = useTheme();
const router            = useRouter();
const route             = useRoute(); 
const UserStore         = useUserStore(); 
const AppStore          = useAppStore();
const toast             = useToast(); 
const {account, darkmode, loggedIn,layout}         = storeToRefs(UserStore);
const {overlay,dashboardMenu, adminRouteItems, openBBMenu} = storeToRefs(AppStore); 
const value             = ref(1);
const menu              = ref(false);


// PROPS
const props = defineProps({
    active:{type:Boolean,default:false},
    items: {type:Array, default:[]}
})

// WATCHERS

watch(darkmode,  (mode) => {
  theme.global.name.value = mode ?  'darkMode' : 'lightMode';
  localStorage.setItem("theme",mode ? 'darkMode' : 'lightMode');  
});


// COMPUTED PROPERTIES


// FUNCTIONS
onMounted(()=>{
    // console.log("TEMPLATE COMPONENT CREATED"); 

});

onBeforeMount(()=>{
  // SAVE THEME TO LOCALSTORAGE MAKING IT PERSIST BROWSER REFRESH
 
});

const toTop =()=> {
        window.scrollTo({
          top: 0,
          behavior: "smooth"
        });
      }

const loginLogout = () => {
  if(loggedIn.value){
    menu.value = false; 
    UserStore.userLogout();
    toTop();
  }

  else{
    router.push({name:'Login'})
  }
}

</script>

<style>
/*   Style */

 
</style>