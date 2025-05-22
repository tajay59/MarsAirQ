<template>
    <figure   class=" highcharts-figure highcharts-light relative " :style="[`width: ${props.width}px; height:${aspectRatio * 100}%`]"  >
        <div :id="graphcontainer" ></div>   
        <VBtn v-if="props.displaymode" title="Add to Dashboard" size="45" icon class="text-none text-xs absolute top-3 right-3    !text-neutral-200 dark:!text-neutral-900 font-semibold" color="transparent"   @click="$emit('add')"  variant="flat" >
             <Icon icon="basil:add-solid" class="!text-neutral-600 dark:!text-neutral-400" width="40" height="40"  />
        </VBtn>
        <VBtn v-else icon class="absolute top-1 right-1  !size-[40px]" color="transparent" @click="toggle"  density="compact" variant="text" >
             <Icon icon="solar:menu-dots-square-bold" class="!text-neutral-600 dark:!text-neutral-400" width="32" height="32"  />
        </VBtn>
       
        <Menu ref="menu" id="overlay_menu"   :model="items" :popup="true" :pt="{root:'mt-2 max-h-[170px] overflow-y-scroll'}" >
         <template #item="{ item, props }" >
             <div class="flex justify-start align-center cursor-pointer pl-2"  @click="param = _.lowerCase(item.label)"> 
                 <svg  v-if="_.lowerCase(item.label) == 'delete'"  width="24" height="24" title="Delete" viewBox="0 0 24 24" class="!text-neutral-600 dark:!text-neutral-400"><path fill="currentColor" d="M6 19c0 1.1.9 2 2 2h8c1.1 0 2-.9 2-2V7H6zM19 4h-3.5l-1-1h-5l-1 1H5v2h14z"/></svg>
                 <Icon v-else :icon="item.icon" width="24" height="24"  />
                 <p class="text-sm ml-2" >{{ item.label }}</p>
             </div>
         </template>
        </Menu>
     </figure>      
 </template>
     
 <script setup>
     /** JAVASCRIPT HERE */
 
     // IMPORTS
     import { ref, watch ,onMounted,onBeforeUnmount } from "vue";  
     import { useRoute ,useRouter } from "vue-router";
     import { useAppStore }  from '@/stores/appStore';
     import { useMqttStore } from '@/stores/mqttStore'; // Import Mqtt Store
     import { useUserStore } from '@/stores/userStore'; 
     import { Icon } from "@iconify/vue";
     
     import { storeToRefs } from "pinia";
     import _ from "lodash";
 
     // Highcharts, Load the exporting module and Initialize exporting module.
     import Highcharts from 'highcharts';
     import 'highcharts/highcharts-more';
     import 'highcharts/modules/exporting';
     import 'highcharts/modules/accessibility';
  
     
 
     
     // VARIABLES
     const router         = useRouter();
     const route          = useRoute();  
     const AppStore       = useAppStore();
     const UserStore      = useUserStore(); 
     const Mqtt           = useMqttStore();
     const { connected, payload, payloadTopic } = storeToRefs(Mqtt);
     const { selectedStation, darkmode, layout}  = storeToRefs(UserStore);
     const { liveData, paramDetails } = storeToRefs(AppStore);
     const chart          = ref(null); // Chart object
     const points         = ref(300); // Specify the quantity of points to be shown on the live graph simultaneously.
     const shift          = ref(false); // Delete a point from the left side and append a new point to the right side of the graph. 
     const params         = ref([]);
     const param          = ref("");
     const chartEl        = ref(null);
     const graphcontainer = ref(`container${_.random(0,100000)}`);
     const aspectRatio    = ref(1/(4/3)); // 4:3
 
 
     // EMITTERS
     const emit = defineEmits(["delete","add"]);
 
 
     const menu = ref();    
     const items = ref([{ label: 'Params', items: [] }, { label: 'Actions',  items: [ {label: "Delete", icon:"ic:baseline-delete", command: () => { emit('delete'); } }]}  ]);
      
     const parameters = Object.keys(paramDetails.value)
     parameters.forEach( item => items.value[0]["items"].push({ label: _.capitalize(item), icon: paramDetails.value[item].icon }))
 
     const toggle = (event) => {
         menu.value.toggle(event);
     };
         
     // WATCHERS
     watch(()=> param.value, (item)=> {
         setChartParams(item); 
         // Update station dashboard
         layout.value.dashboard.forEach( plot => {
            if(plot.id == props.id){ 
                plot.param = param.value;
            }
         })
     })

     watch(payload,(msg)=> {          
         // LIVE GRAPH
         if(msg.type == 'station')
            params.value = Object.keys(msg.data)
          
         if(msg.type == "station" && params.value.includes(param.value) && !props.displaymode){    
            if(msg.id == selectedStation.value){
                if(!!chart.value.series){ 
                    chart.value.series[0].points[0].update(msg.data[param.value]);
                }  
            }             
         }          
     });
 
  
 
    
 
     watch(darkmode,(mode)=> {           
        if(mode)
             chartEl.value.forEach(el => { el.classList.replace('highcharts-light','highcharts-dark') });  
        else if (!mode)
             chartEl.value.forEach(el => { el.classList.replace('highcharts-dark','highcharts-light') });         
    });
 
     // PROPS
     const props = defineProps({
         param :{type:String,default:"default"},
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
         param.value = props.param;
         setChartParams(props.param);    
         
     });
 
 
     onBeforeUnmount(()=>{
         // THIS FUNCTION IS CALLED RIGHT BEFORE THIS COMPONENT IS UNMOUNTED
         // Mqtt.unsubscribeAll();
     });
 
   
 
 
     const CreateCharts = async () => {  
         // TEMPERATURE CHART
         chart.value = Highcharts.chart(graphcontainer.value, {
 
         chart: {
             type: 'gauge',
             styledMode: true,
             plotBackgroundColor: null,
             plotBackgroundImage: null,
             plotBorderWidth: 0,
             plotShadow: false, 
             width: props.width,
             height: (aspectRatio.value * 100) + '%', // 4:3 ratio
             borderRadius: 12,
             borderWidth: 1,
         },
         credits: {
             position: { align: 'right', x: -20 ,y: -10}
         },
         title: { text: 'Gauge', },
         pane: {
             startAngle: -90,
             endAngle: 90,
             background: null,
             center: ['50%', '75%'],
             size: '120%'
         },
         navigation: false,
         tooltip:{enabled: false},
         // plotOptions: {
         //     series: {
         //         dataLabels: {
         //             enabled: true,
         //             borderRadius: 5,
         //             backgroundColor: 'rgba(252, 255, 197, 0.7)',
         //             borderWidth: 1,
         //             borderColor: '#AAA',
         //             y: -50
         //         }
         //     }
         // },
         // the value axis
         yAxis: {
             min: 0,
             max: 100,
             tickPixelInterval: 72,
             tickPosition: 'inside', 
             tickLength: 20,
             tickWidth: 2,
             minorTickInterval: null,
             labels: {
                 distance: 20,
                 style: {
                     fontSize: '14px',
                     useHTML:true
                 }
             },
             lineWidth: 0,
             plotBands: [
             { from: 0, to: 18, thickness: 10, borderRadius: '50%', className: 'tropicaldepression' },
             { from: 17, to: 32, thickness: 10, className: 'tropicalstorm' }, 
             { from: 32, to: 42, thickness: 10, className: 'cat1' }, 
             { from: 42, to: 49, thickness: 10, className: 'cat2' }, 
             { from: 49, to: 58, thickness: 10, className: 'cat3' }, 
             { from: 58, to: 70, thickness: 10, className: 'cat5' }, 
             { from: 69, to: 100, thickness: 10, borderRadius: '50%', className: 'cat5' }
         ]
         },
 
         series: [{
             name: '',
             data: [0],           
             dataLabels: {className: "highlight"},/*{                 
                 useHTML: true ,
                 style: { fontSize: '16px' },
                 borderRadius: 5,
                 borderWidth: 0, 
                 backgroundColor: '#ff0000',
                 y: 30
             },*/
             dial: {
                 radius: '80%',
                 backgroundColor: 'gray',
                 backgroundColor: null,
                 baseWidth: 12,
                 baseLength: '0%',
                 rearLength: '0%'
             },
             pivot: { backgroundColor: 'gray', radius: 6 }
         }]
         }); 
     }
 
     const setChartParams = (param) => {
         if(param == "temperature" || param == "dewpoint" || param == "heatindex" || param == "windchill"    ){     
             let plotBands= [ 
                 { from: 15, to: 20, thickness: 10, borderRadius: '50%', className: 'tropicaldepression' }, 
                 { from: 19, to: 25, thickness: 10, className: 'tropicalstorm' }, 
                 { from: 24, to: 30, thickness: 10, className: 'cat2' }, 
                 { from: 29, to: 35, thickness: 10, className: 'cat3' }, 
                 { from: 34, to: 40, thickness: 10, className: 'cat4' }, 
                 { from: 34, to: 40, thickness: 10, borderRadius: '50%', className: 'cat5' } ]         
             chart.value.update({ title: { text: _.capitalize(param), align: 'center' }, yAxis: {max:40, min: 15, labels: { format: '{value}' }, plotBands: plotBands }, plotOptions: { series: { dataLabels: {  format: '<p class="text-lg font-bold"> {point.y:.2f} <small class="text-xs"> °C</small></p>' } } }})
         }        
 
         else if(param == "humidity"){
             let plotBands= [ 
                 { from: 0, to: 25, thickness: 10, borderRadius: '50%', className: 'tropicaldepression' }, 
                 { from: 24, to: 50, thickness: 10, className: 'tropicalstorm' }, 
                 { from: 49, to: 75, thickness: 10, className: 'cat2' }, 
                 { from: 74, to: 100, thickness: 10, borderRadius: '50%', className: 'cat3' } ]  
             chart.value.update({ title: { text: 'Humidity', align: 'center' }, yAxis: {max:100, min: 0, labels: { format: '{value}' }, plotBands: plotBands },plotOptions: { series: { dataLabels: {  format: '<p class="text-lg font-bold"> {point.y:.2f} <small class="text-xs"> %</small></p>' } } }}); 
         }
 
         else if(param == "pressure"){         
             let plotBands= [ 
                 { from: 900, to: 951, thickness: 10, borderRadius: '50%', className: 'cat2' }, 
                 { from: 949, to: 1000, thickness: 10, className: 'cat3' }, 
                 { from: 1000, to: 1051, thickness: 10, className: 'cat4' }, 
                 { from: 1049, to: 1100, thickness: 10, borderRadius: '50%', className: 'cat5' } ]   
             chart.value.update({ title: { text: 'Pressure', align: 'center' }, yAxis: {max:1100, min: 900, labels: { format: '{value}' }, plotBands: plotBands }, plotOptions: { series: { dataLabels: {  format: '<p class="text-lg font-bold"> {point.y:.2f} <small class="text-xs"> hPa</small></p>' } } }}) 
         }
 
         else if(param == "radiation"){
             let plotBands= [ 
                 { from: 0, to: 20, thickness: 10, borderRadius: '50%', className: 'cat2' }, 
                 { from: 19, to: 40, thickness: 10, className: 'cat3' }, 
                 { from: 39, to: 60, thickness: 10, className: 'cat4' }, 
                 { from: 59, to: 80, thickness: 10, className: 'cat5' },  
                 { from: 79, to: 100, thickness: 10, borderRadius: '50%', className: 'cat5' } ]  
             chart.value.update({ title: { text: 'Radiation', align: 'center' }, yAxis: {max:100, min: 0,   labels: { format: '{value}' }, plotBands: plotBands },plotOptions: { series: { dataLabels: {  format: '<p class="text-lg font-bold"> {point.y:.2f} <small class="text-xs">W/m<sup>2</sup></small></p>'} } }}) 
         }
         
         else if(param == "uva"){
             let plotBands= [ 
                 { from: 0, to: 20, thickness: 10, borderRadius: '50%', className: 'cat2' }, 
                 { from: 19, to: 40, thickness: 10, className: 'cat3' }, 
                 { from: 39, to: 60, thickness: 10, className: 'cat4' }, 
                 { from: 59, to: 80, thickness: 10, className: 'cat5' },  
                 { from: 79, to: 100, thickness: 10, borderRadius: '50%', className: 'cat5' } ]  
             chart.value.update({ title: { text: 'UVA', align: 'center' }, yAxis: {max:100, min: 0,   labels: { format: '{value}' }, plotBands: plotBands  },plotOptions: { series: { dataLabels: {  format: '<p class="text-lg font-bold"> {point.y:.2f} <small class="text-xs">W/m<sup>2</sup></small></p>' } } }}); 
         }
                 
         else if(param == "uvb"){
             let plotBands= [ 
                 { from: 0, to: 20, thickness: 10, borderRadius: '50%', className: 'cat2' }, 
                 { from: 19, to: 40, thickness: 10, className: 'cat3' }, 
                 { from: 39, to: 60, thickness: 10, className: 'cat4' }, 
                 { from: 59, to: 80, thickness: 10, className: 'cat5' },  
                 { from: 79, to: 100, thickness: 10, borderRadius: '50%', className: 'cat5' } ]  
             chart.value.update({ title: { text: 'UVB', align: 'center' }, yAxis: {max:100, min: 0,   labels: { format: '{value}' }, plotBands: plotBands  },plotOptions: { series: { dataLabels: {  format: '<p class="text-lg font-bold"> {point.y:.2f} <small class="text-xs">W/m<sup>2</sup></small></p>' } } }}); 
         }
                 
         else if(param == "uvc"){
             let plotBands= [ 
                 { from: 0, to: 20, thickness: 10, borderRadius: '50%', className: 'cat2' }, 
                 { from: 19, to: 40, thickness: 10, className: 'cat3' }, 
                 { from: 39, to: 60, thickness: 10, className: 'cat4' }, 
                 { from: 59, to: 80, thickness: 10, className: 'cat5' },  
                 { from: 79, to: 100, thickness: 10, borderRadius: '50%', className: 'cat5' } ]  
             chart.value.update({ title: { text: 'UVC', align: 'center' }, yAxis: {max:100, min: 0,   labels: { format: '{value}' }, plotBands: plotBands  },plotOptions: { series: { dataLabels: {  format: '<p class="text-lg font-bold"> {point.y:.2f} <small class="text-xs">W/m<sup>2</sup></small></p>' } } }}); 
         }
                 
         else if(param == "co2"){
             let plotBands= [ 
                 { from: 0, to: 1000, thickness: 10, borderRadius: '50%', className: 'cat1' }, 
                 { from: 999, to: 2000, thickness: 10, className: 'cat2' }, 
                 { from: 1999, to: 3000, thickness: 10, className: 'cat3' },  
                 { from: 2999, to: 5000, thickness: 10, borderRadius: '50%', className: 'cat5' } ]  
             chart.value.update({ title: { text: 'CO2', align: 'center' }, yAxis: {max:5000, min: 0,   labels: { format: '{value}' } , plotBands: plotBands },plotOptions: { series: { dataLabels: {  format: '<p class="text-lg font-bold"> {point.y:.2f} <small class="text-xs"> ppm</small></p>' } } }}); 
         }
 
         else if(param == "rainfall"){
             let plotBands= [ 
                 { from: 0, to: 3, thickness: 10, borderRadius: '50%', className: 'cat2' }, 
                 { from: 2, to: 8, thickness: 10, className: 'cat3' }, 
                 { from: 7, to: 10, thickness: 10, className: 'cat3' }, 
                 { from: 9, to: 60, thickness: 10, borderRadius: '50%', className: 'cat5' } ]  
             chart.value.update({ title: { text: 'Rainfall', align: 'center' }, yAxis: {max:60, min: 0,   labels: { format: '{value}' }, plotBands: plotBands  },plotOptions: { series: { dataLabels: {  format: '<p class="text-lg font-bold"> {point.y:.2f} <small class="text-xs"> mm</small></p>' } } }});
         }
 
         else if(param == "winddirection"){
             let plotBands= [ 
                 { from: 0, to: 359, thickness: 10, borderRadius: '50%', className: 'tropicaldepression' },  ]  
             chart.value.update({ title: { text: 'Wind Direction', align: 'center' }, yAxis: {max:359, min: 0, labels: { format: '{value}' }, plotBands: plotBands },plotOptions: { series: { dataLabels: {  format: '<p class="text-lg font-bold"> {point.y:.2f} <small class="text-xs"> °</small></p>' } } }});
         }
 
         else if(param == "windspeed"){
             let plotBands= [
             { from: 0, to: 18, thickness: 10, borderRadius: '50%', className: 'tropicaldepression' },
             { from: 17, to: 32, thickness: 10, className: 'tropicalstorm' }, 
             { from: 32, to: 42, thickness: 10, className: 'cat1' }, 
             { from: 42, to: 49, thickness: 10, className: 'cat2' }, 
             { from: 49, to: 58, thickness: 10, className: 'cat3' }, 
             { from: 58, to: 70, thickness: 10, className: 'cat5' }, 
             { from: 69, to: 100, thickness: 10, borderRadius: '50%', className: 'cat5' }
         ]
             chart.value.update({ title: { text: 'Wind Speed', align: 'center' }, yAxis: {max:100, min: 0, labels: { format: '{value}' }, plotBands: plotBands  },plotOptions: { series: { dataLabels: {  format: '<p class="text-lg font-bold"> {point.y:.2f} <small class="text-xs"> m/s</small></p>' } } }});
         }
 
         else if(param == "bat"){
             let plotBands= [
             { from: 80, to: 100, thickness: 10, borderRadius: '50%', className: 'cat1' },
             { from: 50, to: 80, thickness: 10, className: 'cat2' }, 
             { from: 30, to: 50, thickness: 10, className: 'cat3' }, 
             { from: 20, to: 30, thickness: 10, className: 'cat4' }, 
             { from: 0, to: 21, thickness: 10, borderRadius: '50%', className: 'cat5' }
         ]
             chart.value.update({ title: { text: 'Battery', align: 'center' }, yAxis: {max:100, min: 0, labels: { format: '{value}' }, plotBands: plotBands  },plotOptions: { series: { dataLabels: {  format: '<p class="text-lg font-bold"> {point.y:.2f} <small class="text-xs"> %</small></p>' } } }});
         }
 
         else if(param == "voltage"){
             let plotBands= [
             { from: 4.0, to: 4.2, thickness: 10, borderRadius: '50%', className: 'cat1' },
             { from: 3.8, to: 4.0, thickness: 10, className: 'cat2' }, 
             { from: 3.5, to: 3.8, thickness: 10, className: 'cat3' }, 
             { from: 3.0, to: 3.5, thickness: 10, className: 'cat4' }, 
             { from: 2.8, to: 3.0, thickness: 10, borderRadius: '50%', className: 'cat5' }
         ]
             chart.value.update({ title: { text: 'Voltage', align: 'center' }, yAxis: {max:4.2, min: 2.8, labels: { format: '{value}' }, plotBands: plotBands  },plotOptions: { series: { dataLabels: {  format: '<p class="text-lg font-bold"> {point.y:.2f} <small class="text-xs"> V</small></p>' } } }});
         }

         else if(param == "default"){
             let plotBands= [
             { from: 4.0, to: 4.2, thickness: 10, borderRadius: '50%', className: 'cat1' },
             { from: 3.8, to: 4.0, thickness: 10, className: 'cat2' }, 
             { from: 3.5, to: 3.8, thickness: 10, className: 'cat3' }, 
             { from: 3.0, to: 3.5, thickness: 10, className: 'cat4' }, 
             { from: 2.8, to: 3.0, thickness: 10, borderRadius: '50%', className: 'cat5' }
         ]
             chart.value.update({ title: { text: '', align: 'center' }, yAxis: {max: 100, min: 0, labels: { format: '{value}' }, plotBands: plotBands  },plotOptions: { series: { dataLabels: {  format: '<p class="text-lg font-bold"> {point.y:.2f} <small class="text-xs"> </small></p>' } } }});
         }
     }
 </script>
 
 
 <style >
 
 .highcharts-gauge-series .highcharts-dial {
     fill: var(--highcharts-color-td)
 }
 
 .highcharts-gauge-series .highcharts-point{
     fill:#b3597c
 }
 
 .highcharts-data-labels text {  
        font-size: 14px;
     }
 
 /**######################################## */
 .highcharts-title {
     fill: var(--highcharts-title-color);
     font-weight: bold;
     /* letter-spacing: 0.3em;
     font-size: 3em; */
 }
 
 .highcharts-subtitle {
     font-family: "Courier New", monospace;
     font-style: italic;
     fill: var(--highcharts-subtitle-color);;
 }
 
 .highcharts-caption {
     font-family: "Courier New", monospace;
     font-style: italic;
     fill: var(--highcharts-subtitle-color);
 }
 
 .highcharts-axis-labels text{
     fill: var(--highcharts-axis-label-color);
 }
 
 .highcharts-background {
     stroke: var(--highcharts-border-radius-color);
 }
 
  
 .highcharts-data-label-box {
   stroke-width: 2px;
   fill: rgba(255, 0, 0, 0);
   stroke: rgba(0, 0, 0, 0);
 }
 
 .highcharts-data-label {
   font-weight: normal;
 }
 
 .highlight .highcharts-data-label-box {    
   stroke-width: 2px;
   fill: rgba(255, 0, 0, 0);
   stroke: rgba(0, 0, 0, 0);
 }
 
 .highlight.highcharts-data-label text {
   font-weight: bold;
   fill: var(--highcharts-title-color);
 } 
 /**######################################## */
 
 .cat {
     fill: #df5353;
     fill-opacity: 1;
 }
 
 .tropicaldepression{ 
     fill: var(--highcharts-color-td);
     fill-opacity: 1;
 }
 
 .tropicalstorm{
     fill: var(--highcharts-color-ts);
     fill-opacity: 1;
 }
 
 .cat1 {
     fill: var(--highcharts-color-cat1);
     fill-opacity: 1; 
 }
 
 .cat2 {
     fill: var(--highcharts-color-cat2);
     fill-opacity: 1; 
 }
 
 
 .cat3 {
     fill: var(--highcharts-color-cat3);
     fill-opacity: 1; 
 }
 
 .cat4 {
     fill: var(--highcharts-color-cat4);
     fill-opacity: 1; 
 }
 
 .cat5 {
     fill: var(--highcharts-color-cat5);
     fill-opacity: 1; 
 }
 
 </style>