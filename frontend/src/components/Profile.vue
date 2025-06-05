<template>
  <div class="bg-neutral-100 dark:bg-neutral-800 size-full" :class="[(!smAndDown)?'pa-10':'pa-0']"> 
      <RouterView />
     


      <VNavigationDrawer v-model="profileDrawer" width="270"   :floating="false"   >
      <template #prepend >
        <div class="my-3 my-15 flex justify-center align-center  "  >
          <VImg v-if="!darkmode" src="@/assets/logo6_light.png" max-width="130"    />
          <VImg v-else src="@/assets/logo6_white.png" max-width="130"   />
            <!-- <VImg  src="@/assets/logo.png"  max-height="100" height="100%" style=" cursor: pointer" @click="router.push({name:'Home'})">              
              <template v-slot:placeholder>
                <div class="d-flex align-center justify-center fill-height">
                  <VProgressCircular color="grey-lighten-4" indeterminate ></VProgressCircular>
                </div>
              </template>
            </VImg>  -->
             
          </div>     
      </template>

        <VList nav    >
          <VDivider :opacity="100" class="border-neutral-300 dark:border-neutral-600 mb-5"  />
                    
          <!-- <VListItem>
            <p class="text-subtitle-1" >Admin</p>
          </VListItem>       -->

          <VListItem v-for="route in profileRouteItems" class="mr-1 " style="text-decoration: none;" :title="route.title" :value="route.name" :to="route.route">
            <template #prepend >
              <VBadge  v-if="route.name == 'Requests'" floating :content="requests.length" color="!bg-green-500 dark:!bg-green-700" class="" :offset-y="7" >
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
  import { useToast } from 'primevue/usetoast';
  import { ref,watch ,onMounted,computed } from "vue";   
  
  import { useUserStore } from '@/stores/userStore'; 
  import { useRoute ,useRouter } from "vue-router";
  import { useAppStore } from '@/stores/appStore';
  import { storeToRefs } from 'pinia';
  import { Icon } from '@iconify/vue';
  import { useDisplay } from 'vuetify';


  
  // VARIABLES 
  const { xs,smAndDown,smAndUp, mdAndUp }   = useDisplay();
  const router                    = useRouter();
  const route                     = useRoute(); 
  const UserStore         = useUserStore(); 
  const AppStore          = useAppStore();
  const {id,loggedIn,image, darkmode}           = storeToRefs(UserStore);
  const {profileRouteItems,profileDrawer, requests}  = storeToRefs(AppStore);
  const requestLoading = ref(false);

 

  
  // PROPS
  const props = defineProps({
      item:{type:String,default:""},
  })
  
  // WATCHERS
  // watch(text,  (newText, oldText) => {
  //   console.log(newText); 
  //   changedText.value = newText ;
  // });
  
  // COMPUTED PROPERTIES
  // const fullname = computed(()=>{    
  //     return `${firstname.value} ${lastname.value}`;
  // });
  
  
  // FUNCTIONS
  onMounted(()=>{
      // AppStore.getSites();
      AppStore.getAccount();
      AppStore.getPageCount();
      AppStore.getPage(1);
      AppStore.getRequests(requestLoading);
      // pingPong();
  })
  
  
   
  </script>
  
  <style>
  /*   Style */
  
   
  </style>