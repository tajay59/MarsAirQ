<template>   
    <VCard  class="bg-neutral-50  dark:bg-neutral-800 relative !rounded-[12px]" :width="props.width" :height="height" :class="[` !w-[${props.width}px] !h-[${height}px]`]" color="trans parent" flat border >
     <template #subtitle ><p class="font-bold text-start" >Wind</p></template>   
        
        <VBtn v-if="props.displaymode" title="Add to Dashboard" size="45" icon class="z-[10] text-none text-xs absolute top-3 right-3    !text-neutral-200 dark:!text-neutral-900 font-semibold" color="transparent"   @click="$emit('add')"  variant="flat" >
             <Icon icon="basil:add-solid" class="!text-neutral-600 dark:!text-neutral-400" width="40" height="40"  />
        </VBtn>
        <VBtn v-else icon class="z-[20]  absolute top-1 right-1  !size-[40px]" color="transparent" @click="emit('delete')"  density="compact" variant="text" >
             <svg  width="24" height="24" viewBox="0 0 24 24" title="Delete" class="!text-neutral-600 dark:!text-neutral-400"><path fill="currentColor" d="M6 19c0 1.1.9 2 2 2h8c1.1 0 2-.9 2-2V7H6zM19 4h-3.5l-1-1h-5l-1 1H5v2h14z"/></svg>
        </VBtn>

            
         <VSheet  class="pa-0 absolute top-0  bg-transparent z-[1] "  >    
             <div class=" flex place-content-center">
                 <svg class="compass-svg " viewBox="0 0 200 200">
                     <!-- Compass background circle -->
                     <circle cx="100" cy="100" r="79" stroke="#e0e0e0" stroke-width="2" fill="none"/>
 
                     <g id="wind-arrow" :transform="`rotate(${displayAngle}, 100, 100)`" class="z-[200000]" >
                         <svg x="85" y="10"   width="30" height="30" viewBox="0 0 100 100"><path class="arrowcolor"  d="m47.655 1.634l-35 95c-.828 2.24 1.659 4.255 3.68 2.98l33.667-21.228l33.666 21.228c2.02 1.271 4.503-.74 3.678-2.98l-35-95C51.907.514 51.163.006 50 .008c-1.163.001-1.99.65-2.345 1.626m-.155 14.88v57.54L19.89 91.461Z" /></svg>
                     </g>
                 </svg>
                 <div style="text-align:center" class=" bg-transparent w-full h-[210px] dark:text-neutral-200  text-neutral-700 absolute top-2 right-0 flex flex-col justify-center align-center"  >                
                     <p style="font-size:32px;" class="font-bold">{{ windSpeed }} <small class="text-xs" >m/s</small></p>
                     <p style="font-size:18px; opacity:0.4;text-align: center;" class="font-bold" >{{ cardinalDirection }}  </p> 
                     <small style="  opacity:0.4;text-align: center;" class="text-sm" >{{ displayAngle.toFixed(0) }}°</small> 
                 </div>
             </div>
         </VSheet>  
 
    </VCard> 
  
 </template>
     
 <script setup>
     /** JAVASCRIPT HERE */
 
     // IMPORTS
     import { ref,reactive,watch ,onMounted,onBeforeUnmount,computed, onBeforeMount } from "vue";  
     import { useRoute ,useRouter } from "vue-router";
     import { useAppStore } from '@/stores/appStore';
     import { useMqttStore } from '@/stores/mqttStore'; // Import Mqtt Store
     import { useUserStore } from '@/stores/userStore'; 
     import { Icon } from "@iconify/vue";
     
     import { storeToRefs } from "pinia";
     import _ from "lodash";
 
     // Highcharts, Load the exporting module and Initialize exporting module.
     import Highcharts from 'highcharts';
     import 'highcharts/highcharts-more';
     import 'highcharts/modules/exporting';
     import 'highcharts/modules/solid-gauge';
     import 'highcharts/modules/accessibility';
 
     import gsap from 'gsap'
   
     
     // VARIABLES
     const router         = useRouter();
     const route          = useRoute();  
     const AppStore       = useAppStore();
     const UserStore      = useUserStore(); 
     const Mqtt           = useMqttStore();
     const { connected, payload, payloadTopic } = storeToRefs(Mqtt);
     const { selectedStation, darkmode, layout}  = storeToRefs(UserStore);
     const { liveData,paramDetails } = storeToRefs(AppStore); 
     const points         = ref(300); // Specify the quantity of points to be shown on the live graph simultaneously.
     const shift          = ref(false); // Delete a point from the left side and append a new point to the right side of the graph. 
     const params         = ref([]); 
     const aspectRatio    = ref(1/(4/3)); // 4:3
     const height         = ref(200);
 
    // EMITTERS
    const emit = defineEmits(["delete","add"]);
  
 
     // PROPS
     const props = defineProps({
         param :{type:String,default:""},
         displaymode :{type: Boolean ,default: false},
         width: {type:Number,default:300},
         id :{type:String,default:""}
     })
 
     // COMPUTED
     const plotHeight = computed(()=> {
         return parseInt(aspectRatio.value * props.width)
     })
 
  
     // FUNCTIONS
 
     //###########################
    // Wind data (in a real app, this would come from an API)
     const windDirection = ref(0) // degrees (0-359)
     const windSpeed     = ref(0.0) // knots
     const displayAngle  = ref(0) // animated angle for display
 
     // Cardinal direction names
     const directions = ['N', 'NNE', 'NE', 'ENE', 'E', 'ESE', 'SE', 'SSE', 'S', 'SSW', 'SW', 'WSW', 'W', 'WNW', 'NW', 'NNW']
 
     // Compute cardinal direction
     const cardinalDirection = computed(() => {
     const index = Math.round(windDirection.value / 22.5) % 16
     return directions[index]
     })
 
     // Animation function
     const animateCompass = (newAngle) => {
     // Calculate shortest path for rotation (handles 360° boundary)
     const diff = ((newAngle - displayAngle.value + 540) % 360) - 180
     const targetAngle = displayAngle.value + diff
     
     gsap.to(displayAngle, {
         duration: 1.5,
         value: targetAngle,
         ease: "elastic.out(1, 0.9)",
         onUpdate: () => {
         // Normalize to 0-360 range
         displayAngle.value = (displayAngle.value % 360 + 360) % 360
         }
     })
     }
 
     // Watch for wind direction changes
     watch(windDirection, (newVal) => {
     animateCompass(newVal)
     })
 
     //###########################
 
     onBeforeMount(() => {
         // THIS FUNCTION IS CALLED AFTER THIS COMPONENT HAS BEEN MOUNTED 
         height.value = parseInt(aspectRatio.value * props.width) 
         
     });
 
  
     onMounted(() => {
         // THIS FUNCTION IS CALLED AFTER THIS COMPONENT HAS BEEN MOUNTED  
         windDirection.value = 0;
         
     });
 
 
     onBeforeUnmount(()=>{
         // THIS FUNCTION IS CALLED RIGHT BEFORE THIS COMPONENT IS UNMOUNTED
         // Mqtt.unsubscribeAll();
     });
 
 
  
     // WATCHERS
     watch(payload,(msg)=> {          
         // LIVE GRAPH
         if(msg.type == 'station')
             params.value = Object.keys(msg.data)

        if(msg.type == "station" && params.value.includes("winddirection") && params.value.includes("windspeed") && !props.displaymode){    
            if(msg.id == selectedStation.value){
                windDirection.value =  Math.floor(msg.data["winddirection"])  
                windSpeed.value = msg.data["windspeed"] 
            }             
         } 
         /*
         if(msg.type == "station" && params.value.includes("winddirection") && params.value.includes("windspeed")){ 
             windDirection.value =  Math.floor(msg.data["winddirection"])  
             windSpeed.value = msg.data["windspeed"]           
         }  */        
     });
 
     const trackColors = Highcharts.getOptions().colors.map(color =>
     new Highcharts.Color(color).setOpacity(0.3).get()
 );
 
 </script>
 
 
 <style >  
    
 .compass-svg {
   width: 80%;
   height: 80%;
   filter: drop-shadow(0 0 2px rgba(0, 0, 0, 0.1));
 }
 
 #wind-arrow {
   will-change: transform;
 }
 
 
 .arrowcolor{  
     fill:  var(--highcharts-color-0);
     fill-opacity: 1;
 }
 


 
 </style>