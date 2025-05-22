<template>
    <figure class=" highcharts-figure highcharts-light relative" :style="[`width: ${props.width}px; height:${aspectRatio * 100}%`]" >
         <div :id="graphcontainer"   ></div> 
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
     import 'highcharts/highcharts-more';
     import 'highcharts/modules/exporting';
     import 'highcharts/modules/solid-gauge';
     import 'highcharts/modules/accessibility';
     
     
     
     
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
     const param          = ref("");
     const chartEl        = ref(null);
     const graphcontainer = ref(`container${_.random(0,100000)}_c_${_.random(0,100000)}}`);
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
 
     // PROPS
     const props = defineProps({
         param :{type:String, default:"default"},
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
 
 
  
     // WATCHERS
     watch(payload,(msg)=> {          
         // LIVE GRAPH
         if(msg.type == 'station')
             params.value = Object.keys(msg.data)
 
        if(msg.type == "station" && params.value.includes(param.value) && !props.displaymode){    
            if(msg.id == selectedStation.value){
                if(!!chart.value.series){ 
                    let size = Math.floor(msg.data[param.value])
                    chart.value.series[0].points[0].update(msg.data[param.value]);
                }  
            }             
         } 
         /* 
         if(msg.type == "station" && params.value.includes(param.value)){  
            
             if(!!chart.value){ 
                 let size = Math.floor(msg.data[param.value])
                 chart.value.series[0].points[0].update(msg.data[param.value]);
                 // chart.value.update({yAxis: { plotBands: { from: size, to: size+10, color: '#DF5353', thickness: '45%', outerRadius: '105%', className: 'tropicalstorm' }}},true,true)
             }  
             
         } */         
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
                 styledMode: true,
                 type: 'solidgauge',
                 width: props.width,
                 height: (aspectRatio.value * 100) + '%', // 4:3 ratio
                 margin: [1,1,1,1],
                 spacing: [0, 0, 0, 0],
                 borderRadius: 12,
                 borderWidth: 1,
             },
             credits: {
                 position: { align: 'right', x: -20 ,y: -10}
             },
 
             title: false,
 
             tooltip: {
                 enabled: false
             },
 
             pane: {
                 startAngle: 0,
                 endAngle: 360,
                 background: [  { 
                     outerRadius: '100%',
                     innerRadius: '83%', 
                     borderWidth: 0
                 } ]
             },
 
             yAxis: {
                 lineWidth: 0,
                 tickPositions: [],
                 // plotBands:[
                 // { from: 0, to: 360, thickness: 1, borderRadius: '50%', className: 'tropicalstorm' },
                 // ]
                 // plotBands: { from: 70, to: 71, color: '#DF5353', thickness: '45%', outerRadius: '105%', className: 'tropicalstorm' }
             },
             navigation: false,
 
             plotOptions: {
                 solidgauge: {                    
                     linecap: 'round',
                     stickyTracking: false,
                     rounded: true
                 },
             },
 
             series: [ {
                 name: `${_.capitalize(param.value)}`,
                 data: [{ radius: '100%', innerRadius: '83%', y: 0, className: 'datapoint'}],
                 dataLabels: { enabled: true, 
                     
                 // format: '<div style="text-align:center">' + '<span style="font-size:25px">{y}</span><br>' + '<i class="fas fa-tachometer-alt" style="font-size:30px; color:{point.color}"></i>' + '</div>', 
                 useHTML: true},                
                 marker: true
                 
             }]
             });
          
     }
    
 
     const setChartParams = (param) => { 
         let Options =  { solidgauge: { dataLabels: {  format: `<div style="text-align:center; margin-top: -30px"><div style="font-size:24px;">{y} <small class="text-sm">${paramDetails.value[param]['units']}</small></div><div style="font-size:14px; opacity:0.4;text-align: center;">${_.capitalize(param)}</div></div>` } } }
         let radiationOption = { solidgauge: { dataLabels: {  format: `<div style="text-align:center; margin-top: -30px"><div style="font-size:24px;">{y} <small class="text-sm">W/m<sup>2</sup></small></div><div style="font-size:14px; opacity:0.4;text-align: center;">${_.capitalize(param)}</div></div>` } } }
         
         if(param == "temperature")        
             chart.value.update({  yAxis: {max:40, min: 15}, plotOptions: Options});    
 
         else if(param == "humidity")
             chart.value.update({ yAxis: {max:100, min: 0}, plotOptions: Options}); 
         
         else if(param == "pressure")           
             chart.value.update({ yAxis: {max:1100, min: 900}, plotOptions: Options}); 
     
         else if(param == "radiation")
             chart.value.update({ yAxis: {max:100, min: 0}, plotOptions: radiationOption}); 
         
         else if(param == "uva")
             chart.value.update({ yAxis: {max:100, min: 0}, plotOptions: radiationOption}); 
              
         else if(param == "uvb")
             chart.value.update({ yAxis: {max:100, min: 0}, plotOptions: radiationOption}); 
              
         else if(param == "uvc")
             chart.value.update({ yAxis: {max:100, min: 0}, plotOptions: radiationOption}); 
              
         else if(param == "co2")
             chart.value.update({ yAxis: {max:5500, min: 0 },plotOptions: Options}); 
 
         else if(param == "rainfall")
             chart.value.update({ yAxis: {max:60, min: 0 },plotOptions: Options}); 
     
         else if(param == "winddirection")
             chart.value.update({ yAxis: {max:360, min: 0 },plotOptions: Options}); 
 
         else if(param == "windspeed")
             chart.value.update({  yAxis: {max:100, min: 0 },plotOptions: Options}); 
 
         else if(param == "bat")
             chart.value.update({ yAxis: {max:100, min: 0},plotOptions: Options}); 
         
         else if(param == "voltage")
             chart.value.update({  yAxis: {max:4.2, min: 0},plotOptions: Options}); 

        else if(param == "default")
             chart.value.update({  yAxis: {max:100, min: 0},plotOptions: Options}); 
         
     }
 </script>
 
 
 <style > 
 
 
 .highcharts-gauge-series .highcharts-dial {
     fill: var(--highcharts-color-cat2)
 }
 
 .highcharts-gauge-series .highcharts-point{
     fill:#b3597c
 }
 
 .highcharts-data-labels text {
        font-size: 14px;
     }
 
 
 
 .datapoint{  
     fill:   var(--highcharts-color-1);
     fill-opacity: 1;
 }
 
 
  
 
 </style>