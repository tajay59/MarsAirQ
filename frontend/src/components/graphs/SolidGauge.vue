<template>
    <figure  class=" highcharts-figure highcharts-light relative" :style="[`width: ${props.width}px; height:${aspectRatio * 100}%`]">
         <div :id="graphcontainer"  ></div> 
         <VBtn v-if="props.displaymode" title="Add to Dashboard" size="45" icon class="text-none text-xs absolute top-3 right-3    !text-neutral-200 dark:!text-neutral-900 font-semibold" color="transparent"   @click="$emit('add')"  variant="flat" >
            <Icon icon="basil:add-solid" class="!text-neutral-600 dark:!text-neutral-400" width="40" height="40"  />
       </VBtn>
       <VBtn v-else icon class="absolute top-1 right-1  !size-[40px]" color="transparent" @click="toggle"  density="compact" variant="text" >
            <Icon icon="solar:menu-dots-square-bold" class="!text-neutral-600 dark:!text-neutral-400" width="32" height="32"  />
       </VBtn>
      

         <Menu ref="menu" id="overlay_menu"   :model="items" :popup="true" :pt="{root:'mt-2 max-h-[170px] overflow-y-scroll'}" >
            <template #item="{ item, props }" >
                <div class="flex justify-start align-center cursor-pointer pl-2"  @click="param = _.lowerCase(item.label)">
                    <svg  v-if="_.lowerCase(item.label) == 'delete'"  width="24" title="Delete" height="24" viewBox="0 0 24 24" class="!text-neutral-600 dark:!text-neutral-400"><path fill="currentColor" d="M6 19c0 1.1.9 2 2 2h8c1.1 0 2-.9 2-2V7H6zM19 4h-3.5l-1-1h-5l-1 1H5v2h14z"/></svg>
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
     import { ref,reactive,watch ,onMounted,onBeforeUnmount,computed, onBeforeMount } from "vue";  
     import { useRoute ,useRouter } from "vue-router";
     import { useAppStore } from '@/stores/appStore';
     import { useMqttStore } from '@/stores/mqttStore'; // Import Mqtt Store
     import { useUserStore } from '@/stores/userStore'; 
     import { Icon } from "@iconify/vue";
     
     import { storeToRefs } from "pinia";
     import _ from "lodash";
 
     // Highcharts, Load the exporting module and Initialize exporting module.
     import Highcharts, { color } from 'highcharts';
     import  'highcharts/highcharts-more';
     import  'highcharts/modules/exporting';
     import 'highcharts/modules/accessibility';
     
     
     
     
     // VARIABLES
     const router         = useRouter();
     const route          = useRoute();  
     const AppStore       = useAppStore();
     const UserStore      = useUserStore(); 
     const Mqtt           = useMqttStore();
     const { connected, payload, payloadTopic } = storeToRefs(Mqtt);
     const { selectedStation, darkmode,userSites, layout}  = storeToRefs(UserStore);
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
    
     
     // COMPUTED
     const getParams = computed(()=> {
        let site =  userSites.value.filter( site => site.id == layout.value.site )
        let result = []
        if(site.length > 0){
            let device =  site[0].devices.filter( device => device.id == layout.value.device)
            if(device.length > 0)
                result = device[0].params            
        }
        return result
     })

     // PROPS
     const props = defineProps({
        param :{type:String,default:"default"},
        displaymode :{type: Boolean ,default: false},
        width: {type:Number,default:300},
        id :{type:String,default:""}
     })
      
     // FUNCTIONS
     const toggle = (event) => {
        menu.value.toggle(event);
    };    
 
    onBeforeMount(()=> {
        // UPDATES items.value VARIABLE TO ENSURE ONLY PARAMS ASSIGNED TO STATION SHOWS IN GRAPH MENU
        getParams.value.forEach( item => items.value[0]["items"].push({ label: _.capitalize(item), icon: paramDetails.value[item].icon }));
     })

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


    const gaugeOptions = {
    chart: { 
        type: 'solidgauge',
        styleMode: true, 
        width: props.width,
        height: (aspectRatio.value * 100) + '%', // 4:3 ratio
        borderRadius: 12, 
        borderWidth: 1,  
    },
    title: null,
    pane: {
        center: ['50%', '85%'],
        size: '140%',
        startAngle: -90,
        endAngle: 90,
        background: {
            borderRadius: 5,
            innerRadius: '60%',
            outerRadius: '100%',
            shape: 'arc'
        }
    },

    exporting: { enabled: false },
    tooltip: { enabled: false },

    // the value axis
    yAxis: {
        stops: [
            [0.1, '#55BF3B'], // green
            [0.5, '#DDDF0D'], // yellow
            [0.9, '#DF5353'] // red
        ],
        lineWidth: 0,
        tickWidth: 0,
        minorTickInterval: null,
        tickAmount: 2,
        title: { y: -70 },
        labels: { y: 16, style: { fontSize: '12px' } }
    },

    plotOptions: {
        solidgauge: {
            borderRadius: 3,
            dataLabels: {
                distance: 20,
                style: { fontSize: '24px', className:"textColor" },
                useHTML: true
            }
        }
    }
};

 
 
     const CreateCharts = async () => {  
         // TEMPERATURE CHART
         chart.value = Highcharts.chart(graphcontainer.value, Highcharts.merge(gaugeOptions, {
        yAxis: { title: { text: '' }, },
        credits: { enabled: false },

        series: [{
            name: '',
            data: [0], 
        }]

    }));
     }
 
     const setChartParams = (param) => {
         if(param == "temperature"){           
             chart.value.update({ title: { text: 'Temperature', align: 'center' }, yAxis: {max:40, min: 15},plotOptions: { series: { dataLabels: {  format: '<span class="!text-xl text-neutral-700 dark:text-neutral-200" >{point.y:.2f} <small class="text-sm"> °C</small></span>' } } }})
         }        
 
         else if(param == "humidity"){
             chart.value.update({ title: { text: 'Humidity', align: 'center' }, yAxis: {max:100, min: 0 }, plotOptions: { series: { dataLabels: {  format: '<span class="!text-xl text-neutral-700 dark:text-neutral-200" >{point.y:.2f} <small class="text-sm"> %</small></span>' } } }}); 
         }
 
         else if(param == "pressure"){         
             chart.value.update({ title: { text: 'Pressure', align: 'center' }, yAxis: {max:1100, min: 900 }, plotOptions: { series: { dataLabels: {  format: '<span class="!text-xl text-neutral-700 dark:text-neutral-200" >{point.y:.2f} <small class="text-sm"> hPa</small></span>' } } }}) 
         }
 
         else if(param == "radiation"){ 
             chart.value.update({ title: { text: 'Radiation', align: 'center' }, yAxis: {max:100, min: 0},plotOptions: { series: { dataLabels: {  format: '<span class="!text-xl text-neutral-700 dark:text-neutral-200" >{point.y:.2f} <small class="text-sm">W/m<sup>2</sup></small></span>' } } }}) 
         }
         
         else if(param == "uva"){  
             chart.value.update({ title: { text: 'UVA', align: 'center' }, yAxis: {max:100, min: 0  },plotOptions: { series: { dataLabels: {  format: '<span class="!text-xl text-neutral-700 dark:text-neutral-200" >{point.y:.2f} <small class="text-sm">W/m<sup>2</sup></small></span>' } } }}); 
         }
                 
         else if(param == "uvb"){  
             chart.value.update({ title: { text: 'UVB', align: 'center' }, yAxis: {max:100, min: 0  },plotOptions: { series: { dataLabels: {  format: '<span class="!text-xl text-neutral-700 dark:text-neutral-200" >{point.y:.2f} <small class="text-sm">W/m<sup>2</sup></small></span>' } } }}); 
         }
                 
         else if(param == "uvc"){  
             chart.value.update({ title: { text: 'UVC', align: 'center' }, yAxis: {max:100, min: 0  },plotOptions: { series: { dataLabels: {  format: '<span class="!text-xl text-neutral-700 dark:text-neutral-200" >{point.y:.2f} <small class="text-sm">W/m<sup>2</sup></small></span>' } } }}); 
         }
                 
         else if(param == "co2"){
             chart.value.update({ title: { text: 'CO2', align: 'center' }, yAxis: {max:5000, min: 0},plotOptions: { series: { dataLabels: {  format: '<span class="!text-xl text-neutral-700 dark:text-neutral-200" >{point.y:.2f} <small class="text-sm"> ppm</small></span>' } } }}); 
         }
 
         else if(param == "rainfall"){
             chart.value.update({ title: { text: 'Rainfall', align: 'center' }, yAxis: {max:60, min: 0 },plotOptions: { series: { dataLabels: {  format: '<span class="!text-xl text-neutral-700 dark:text-neutral-200" >{point.y:.2f} <small class="text-sm"> mm</small></span>' } } }});
         }
 
         else if(param == "winddirection"){
             chart.value.update({ title: { text: 'Wind Direction', align: 'center' }, yAxis: {max:359, min: 0},plotOptions: { series: { dataLabels: {  format: '<span class="!text-xl text-neutral-700 dark:text-neutral-200" >{point.y:.2f} <small class="text-sm"> °</small></span>' } } }});
         }
 
         else if(param == "windspeed"){
             chart.value.update({ title: { text: 'Wind Speed', align: 'center' }, yAxis: {max:100, min: 0 },plotOptions: { series: { dataLabels: {  format: '<span class="!text-xl text-neutral-700 dark:text-neutral-200" >{point.y:.2f} <small class="text-sm"> m/s</small></span>' } } }});
         }
 
         else if(param == "bat"){
             chart.value.update({ title: { text: 'Battery', align: 'center' }, yAxis: {max:100, min: 0 },plotOptions: { series: { dataLabels: {  format: '<span class="!text-xl text-neutral-700 dark:text-neutral-200" >{point.y:.2f} <small class="text-sm"> %</small></span>' } } }});
         }
 
         else if(param == "voltage"){
             chart.value.update({ title: { text: 'Voltage', align: 'center' }, yAxis: {max:4.2, min: 2.8 },plotOptions: { series: { dataLabels: {  format: '<span class="!text-xl text-neutral-700 dark:text-neutral-200" >{point.y:.2f} <small class="text-sm"> V</small></span>' } } }});
         }
         else if(param == "default"){           
             chart.value.update({ title: { text: 'Gauge', align: 'center' }, yAxis: {max:100, min: 0},plotOptions: { series: { dataLabels: {  format: '<span class="!text-xl text-neutral-700 dark:text-neutral-200" >{point.y:.2f} <small class="text-sm"> </small></span>' } } }})
         }
     }
 </script>
 
 
 <style >
  

 .highcharts-data-labels text {
        fill: var(--highcharts-title-color);
        font-size: 14px;
        text-shadow: none;
     }

.highcharts-axis-labels text{
    fill: var(--highcharts-axis-label-color);
}

.textColor {
    color: var(--highcharts-neutral-color-100);
 }
  
 
 </style>