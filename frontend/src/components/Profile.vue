<template>
  <div class="bg-neutral-100 dark:bg-neutral-800 size-full pa-10" > 
      <RouterView />
     


      <VNavigationDrawer width="200" permanent :floating="false" v-if="mdAndUp" >
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
              <Icon :icon="route.icon" width="24" height="24" class="!text-neutral-600 dark:!text-neutral-400 mr-3"  />  
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
  const {profileRouteItems}  = storeToRefs(AppStore);

 

  
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
      // pingPong();
  })
  
  
   
  </script>
  
  <style>
  /*   Style */
  
   
  </style>