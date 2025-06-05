<template> 
 <VContainer class="bg- blue size-full  " fluid align="center">
  <!-- bg-[url('@/assets/bg4.png')] -->
  <VRow  justify="center" class="bg- red  size-full">
      <VCol v-if="smAndUp" cols="12" class="bg- green pa-0" align-self="start" justify="center" align="start" >
       <div class="bg- green flex align-center mt-7 ">
        <!-- <VImg v-if="!darkmode" src="@/assets/logo6_light.png" width="200" min-width="200" height="30" min-height="30"   />
        <VImg v-else src="@/assets/logo6_white.png" width="200" min-width="200" height="30" min-height="30"   /> -->
        <VImg v-if="!darkmode" src="@/assets/KS_Final.png" width="300" min-width="300" height="50" min-height="50"   />
        <VImg v-else src="@/assets/KS_Final.png" width="300" min-width="300" height="50" min-height="50"   />
        

        <VBtn v-for="route in routeItems"   color="black" density="compact"   variant="text" :to="route.route" class="no-underline !text-neutral-950 dark:!text-neutral-200 [&>*]:!text-sm mt-1  hover:no-underline " >
          <span class="text-none nunito-route  no-underline" >{{  route.title }}</span>
        </VBtn>  
        <VSpacer />

       
       </div>      
      </VCol>
   
      <VCol cols="12"  class="mt-15 bg- purple bg-[url('@/assets/hero2.png')] bg-top flex flex-col justify-between min-h-[900px]"  align="center" justify="center">
       
         <div   >
          <p class="text-6xl" > Breathe Clean, Live Green</p>
          <p class="mt-10 nunito font-semibold text-lg text-center text-neutral-900  dark:text-neutral-200/[0.8] mb-10 " style="max-width: 500px;">Join the growing community that relies on Mars AirQ to monitor and improve air quality</p>

          <div class="mt-5 flex gap-2 justify-center align-center" >  
            <VBtn text="Login" color="transparent" width="150" height="50" @click="router.push({name:'Login'})" class="text-none !text-base !bg-neutral-100 dark:!bg-neutral-700  !text-neutral-900 dark:!text-neutral-100 !border" ></VBtn>
            <VBtn text="Register" color="transparent" width="150" height="50" @click="router.push({name:'Signup'})"  class="text-none text-base !bg-neutral-700 dark:!bg-neutral-100  !text-neutral-100 dark:!text-neutral-900 !border" ></VBtn>
          </div>
         </div>



        <div class=" bg- red flex flex-col justify-end align-center" >
          <VCard  border class="glass !rounded-[30px]"    rounded="md" density="compact" self-align="end" > 
            <div  class=" flex h-full pa-5 flex-wrap gap-10 " >       
                <div class="  flex-1 min-w-[300px] " > 
                  <p class="text-3xl font-bold mb-5">What We Are About</p>
                  <p class="text-xl font-semibold" >Information on air quality is provided by sensors installed across the region.</p>
                </div>
                <div class=" flex-1 flex justify-center align-center gap-2" >
                  <VCard v-for="(item, index) in heroCards" :key="index" width="100" height="140"  border flat class="!rounded-xl py-2  bg-neutral-200 dark:bg-neutral-800">
                    <VCardItem>
                    <VSheet  class="bg-neutral-300 dark:bg-neutral-600 flex justify-center align-center rounded-[50%]"  width="60" height="60" >
                        <Icon  :icon="item.icon" width="32" height="32" class="!text-neutral-600 dark:!text-neutral-400"  />      
                    </VSheet>
                    </VCardItem>
                    <VCardItem>
                      <p class="text-sm" >{{ item.title }}</p>
                      <!-- <p class="text-sm" >{{ item.subtitle }}</p> -->
                    </VCardItem>
                  </VCard>
                </div>       
              </div>
          </VCard>
       
        </div>
      </VCol>
           
    </VRow>
  </VContainer>
</template>

<script setup> 
import { ref,reactive, onMounted, computed} from 'vue';
import { useRoute, useRouter } from "vue-router";
import { useAppStore} from '@/stores/appStore';   
import { useUserStore} from '@/stores/userStore';
import { storeToRefs } from 'pinia'
import { useDisplay } from 'vuetify';
import { Icon } from '@iconify/vue';
// import anime from 'animejs/lib/anime.es.js';



// VARIABLES
const { xs,smAndDown,smAndUp, mdAndUp }   = useDisplay();
const AppStore          = useAppStore()
const UserStore         = useUserStore(); 
const router            = useRouter();
const route             = useRoute();  
const sheet             = ref(false);
const { darkmode }      = storeToRefs(UserStore);
const {drawerItems, routeItems}     = storeToRefs(AppStore)
const page              = ref(1);
const sparetype         = reactive({met:null,radar:null});
let USDollar            = new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' });
const heroCards         = ref([{"title":"Users","subtitle": "Region wide","icon": "iconamoon:profile-light"},{"title":"AWS","subtitle": "Sensor networks","icon": "lucide:network"}, {"title":"Data","subtitle": "Real-Time","icon": "solar:play-bold"}])



// PROPS
const props = defineProps({
    item:{type:String,default:""},
})

 
// EMITTERS
// const emit = defineEmits(["currentRoute"]);

// ANIMATIONS
// Create a timeline with default parameters
// var tl = anime.timeline({ easing: 'easeOutExpo', duration: 2000 });

// FUNCTIONS
onMounted(() => {
  AppStore.currentRoute = "Home"; 
  toTop();

  // tl.add({ targets: '.client', opacity:1, translateY: 70, })
})

const toTop =()=> {
        window.scrollTo({
          top: 0,
          behavior: "smooth"
        });
      }
</script>


<style >
 

</style>