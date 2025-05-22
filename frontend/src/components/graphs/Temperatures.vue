<template>
    <figure   class=" highcharts-figure highcharts-light relative" :style="[`width: ${props.width}px; height:${aspectRatio * 100}%`]" >
         <VBtn v-if="props.displaymode" title="Add to Dashboard" size="45" icon class="text-none text-xs absolute top-3 right-3 z-[200000]   !text-neutral-200 dark:!text-neutral-900 font-semibold" color="transparent"   @click="$emit('add')"  variant="flat" >
             <Icon icon="basil:add-solid" class="!text-neutral-600 dark:!text-neutral-400" width="40" height="40"  />
        </VBtn>
        <VBtn v-else icon class="z-[20]  absolute top-1 right-1  !size-[40px]" title="Delete" color="transparent" @click="emit('delete')"  density="compact" variant="text" >
             <svg  width="24" height="24" viewBox="0 0 24 24" class="!text-neutral-600 dark:!text-neutral-400"><path fill="currentColor" d="M6 19c0 1.1.9 2 2 2h8c1.1 0 2-.9 2-2V7H6zM19 4h-3.5l-1-1h-5l-1 1H5v2h14z"/></svg>
        </VBtn>
         <div :id="graphcontainer"  ></div>  
       
     </figure>    
 </template>
     
 <script setup>
     /** JAVASCRIPT HERE */
 
     // IMPORTS
     import { ref,reactive,watch ,onMounted,onBeforeUnmount,computed } from "vue";  
     import { useRoute ,useRouter } from "vue-router";
     import { useAppStore } from '@/stores/appStore';
     import { useMqttStore } from '@/stores/mqttStore'; // Import Mqtt Store
     import { useUserStore } from '@/stores/userStore'; 
     import { Icon } from "@iconify/vue";
     
     import { storeToRefs } from "pinia";
     import _ from "lodash";
 
     // Highcharts, Load the exporting module and Initialize exporting module.
     import Highcharts from 'highcharts';
     import  'highcharts/highcharts-more';
     import  'highcharts/modules/exporting';
     import  'highcharts/modules/solid-gauge';
     import  'highcharts/modules/accessibility';
     
     
     
     // VARIABLES
     const router         = useRouter();
     const route          = useRoute();  
     const AppStore       = useAppStore();
     const UserStore      = useUserStore(); 
     const Mqtt           = useMqttStore();
     const { connected, payload, payloadTopic } = storeToRefs(Mqtt);
     const { selectedStation, darkmode, layout}  = storeToRefs(UserStore);
     const { liveData,paramDetails } = storeToRefs(AppStore);
     const chart          = ref(null); // Chart object
     const points         = ref(300); // Specify the quantity of points to be shown on the live graph simultaneously.
     const shift          = ref(false); // Delete a point from the left side and append a new point to the right side of the graph. 
     const params         = ref([]);
     const chartEl        = ref(null);
     const graphcontainer = ref(`container${_.random(0,100000)}`);
     const aspectRatio    = ref(1/(4/3)); // 4:3
 
       
     // EMITTERS
     const emit = defineEmits(["delete","add"]);
 
     // PROPS
     const props = defineProps({
         param :{type:String,default:""},
         displaymode :{type: Boolean ,default: false},
         width: {type:Number,default:300},
         id :{type:String,default:""}
     })
 
 
     // FUNCTIONS
       
     onMounted(() => {
         // THIS FUNCTION IS CALLED AFTER THIS COMPONENT HAS BEEN MOUNTED
         chartEl.value = document.querySelectorAll(".highcharts-figure");
 
         if(darkmode.value)
             chartEl.value.forEach(el => { el.classList.replace('highcharts-light','highcharts-dark') });  
         else if (!darkmode.value)
             chartEl.value.forEach(el => { el.classList.replace('highcharts-dark','highcharts-light') });   
 
         CreateCharts();       
         
            
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
         
        if(msg.type == "station"  && params.value.includes("dewpoint") && params.value.includes("heatindex") && params.value.includes("windchill") && !props.displaymode){    
            if(msg.id == selectedStation.value){
                if(!!chart.value.series){ 
                    chart.value.series[0].setData([['Heat Index', msg.data.heatindex], ['Wind Chill', msg.data.windchill], ['Dew Point', msg.data.dewpoint]],true,true, true);
                }  
            }             
         } 
         /*
         if(msg.type == "station" && params.value.includes("temperature")){         
             if(!!chart.value){               
                 chart.value.series[0].setData([['Heat Index', msg.data.heatindex], ['Wind Chill', msg.data.windchill], ['Dew Point', msg.data.dewpoint]],true,true, true);
             }               
         }  */        
     });
 
    
 
     watch(darkmode,(mode)=> {           
        if(mode)
             chartEl.value.forEach(el => { el.classList.replace('highcharts-light','highcharts-dark') });  
        else if (!mode)
             chartEl.value.forEach(el => { el.classList.replace('highcharts-dark','highcharts-light') });         
    });
 
 
     const CreateCharts = async () => {  
         // TEMPERATURE CHART
         chart.value = Highcharts.chart(graphcontainer.value, {
        chart: { 
            type: 'column', 
            styledMode: true, 
            width: props.width,
            height: (aspectRatio.value * 100) + '%', // 4:3 ratio
            borderRadius: 12,
            borderWidth: 1, 
        },
     title: { text: 'Temperatures' },
     subtitle: false,
     xAxis: {
         type: 'category',
         labels: { 
             style: {
                 fontSize: '10px',
                 fontFamily: 'Verdana, sans-serif'
             }
         } 
     },
     yAxis: {
         visible: false
     },
     legend: { enabled: false },
     navigation: false,
     tooltip: {enabled: false} ,///{ pointFormat: '<b>{point.y:.1f} °C</b>' },
     series: [{
         name: 'Temperatures',
         colorByPoint: true,
         groupPadding: 0,
         data: [
             ['Heat Index', 31.18],
             ['Wind Chill', 27.79],
             ['Dew Point', 22.23],
         ],
         dataLabels: { 
             enabled: true,
             // rotation: -90,
             color: '#FFFFFF',
             inside: true,
             verticalAlign: 'top',
             format: '{point.y:.1f} °C', // one decimal
             y: 10, // 10 pixels down from the top
             style: {
                 fontSize: '13px',
                 fontFamily: 'Verdana, sans-serif'
             }
         }
     }]
 });
          
     }
    
 
   
 </script>
 
 
 <style > 
 .highcharts-light {      
     /** CUSTTOM VARIABLES */
     --highcharts-title-color: hsl(0, 0%, 30%);
     --highcharts-subtitle-color: hsl(0, 0%, 10%); 
     --highcharts-axis-label-color: hsl(0, 0%, 30%);
     --highcharts-border-radius-color: hsl(0, 0%, 80%);
   }
 
 .highcharts-dark {  
 /** CUSTTOM VARIABLES */
 --highcharts-title-color: hsl(0, 0%, 70%);
 --highcharts-subtitle-color: hsl(0, 0%, 90%); 
 --highcharts-axis-label-color: hsl(0, 0%, 70%);
 --highcharts-border-radius-color: hsl(0, 0%, 30%);   
 }
 
 .highcharts-axis-labels text {
     fill: var(--highcharts-title-color);
     font-size: 14px;
     }
 
     
 .highcharts-data-label text { 
   fill: var(--highcharts-subtitle-color);
 }
  
 </style>