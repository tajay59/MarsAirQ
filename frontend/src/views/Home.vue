<template> 
 <VContainer class="bg-blue h-screen pa-0" fluid>
    <VRow  justify="center" class="bg-red h-screen bg-[url('@/assets/bg4.png')] bg-center bg-cover">
      <VCol cols="12" class="bg- green" align-self="start" justify="center" align="center" >
          <VBtn v-for="route in routeItems"   color="black" density="compact"   variant="text" :to="route.route" class="mt-15 no-underline !text-neutral-600 hover:!text-neutral-950 hover:font-medium  hover:no-underline mx-1" >
            <span class="text-none nunito-route  no-underline" >{{ route.title }}</span>
          </VBtn>        
      </VCol>

      <VCol cols="12"  class="bg- purple h-40" align-self="center" >
        <!-- <VBtn text="LOGIN"  to="/login" />
        <Button label="Submit" class="" /> -->
      </VCol>
      
      <VCol cols="12"   class="bg- yellow flex flex-row justify-center gap-2 pb-15"  align-self="end" >
        <!-- <DatePicker   showIcon fluid iconDisplay="input" >
          <template #inputicon="slotProps">
            <i class="pi pi-calendar" @click="slotProps.clickCallback" />
          </template>
        </DatePicker> -->

        <VCard v-for="x in ['One','Two','Three','Four']" :key="x"  width="300" border class="glass" rounded="md" density="compact" >
          <template #title ><span class="text-neutral-900  dark:text-neutral-200/[0.8]" >{{ x }}</span> </template>
          <VCardItem v-for="route in drawerItems" class="py-1" >
            <VIcon :icon="route.icon" width="24" height="24" class="!text-purple-800 dark:!text-purple-400" />
            <span class="ml-5" >{{ route.title }}</span>
          </VCardItem>
        </VCard>
      </VCol>
      
    </VRow>

    <VRow  align="center" justify="center" class="bg-green fill-height">
      two
      <v-btn size="x-large" text="Click Me" @click="sheet = !sheet" class="z-[21000]" ></v-btn>

<VBottomSheet v-model="sheet">
  <VCard class="text-center" height="200" >
    <VCardText>
      <v-btn variant="text" @click="sheet = !sheet" > close </v-btn>

      <br>
      <br>

      <div>
        This is a bottom sheet using the controlled by v-model instead of activator
      </div>
    </VCardText>
  </VCard>
</VBottomSheet>
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
import anime from 'animejs/lib/anime.es.js';
import TopAppBar from '@/components/TopAppBar.vue';



// VARIABLES
const { xs,smAndDown,smAndUp, mdAndUp }   = useDisplay();
const AppStore          = useAppStore()
const UserStore         = useUserStore(); 
const router            = useRouter();
const route             = useRoute();  
const sheet                     = ref(false);
const { darkmode }      = storeToRefs(UserStore);
const {drawerItems, routeItems}     = storeToRefs(AppStore)
const page              = ref(1);
const sparetype         = reactive({met:null,radar:null});
let USDollar            = new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' });


const heroInfo          = reactive({
  radar:{"image":"radarhero.webp","text":"Explore Radar Spares","title": "Discover the latest Radar Equipment","message":"Explore our comprehensive range of radar spare parts designed to ensure optimal performance and reliability for your radar systems.","type":"RAD"},
  met:{"image":"awshero.webp","text":"Explore Met-Service Spares","title": "Browse our inventory of Meteorological-service parts","message":"From temperature and humidity sensors to wind vanes and rain gauges, we offer a wide selection of spare parts for all your meteorological needs.","type":"MET"}
});
// PROPS
const props = defineProps({
    item:{type:String,default:""},
})

 
// EMITTERS
// const emit = defineEmits(["currentRoute"]);

// ANIMATIONS
// Create a timeline with default parameters
var tl = anime.timeline({ easing: 'easeOutExpo', duration: 2000 });

// FUNCTIONS
onMounted(() => {
  AppStore.currentRoute = "Home"; 
  toTop();
  tl.add({
  targets: '.client',
  opacity:1,
  translateY: 70,
})
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