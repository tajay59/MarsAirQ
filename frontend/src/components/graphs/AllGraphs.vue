<template>
    <VContainer align="center" class="h-full " fluid>         
        <VRow class=" fill-height" >
            <VCol cols="12" class="flex flex-wrap align-start sm:justify-end justify-center  gap-3 pa-0" >
                <SelectButton v-model="selected" :options="options"  optionLabel="name" class=""   aria-labelledby="basic"  :allowEmpty="false" @click="graphType =  selected.type"  size="small" >
                    <template #option="slotProps" >
                        <p class="text-sm font-semibold font-[Roboto]" >{{ slotProps.option.name }}</p>
                    </template>
                </SelectButton>

                <VBtn icon class="!text-black dark:!text-white !text-small" variant="text" density="compact" @click="getDataToggle = !getDataToggle">                      
                     <Icon icon="ion:reload-circle" width="32" height="32" class=""  />                 
                </VBtn>
            </VCol>

            <VCol cols="12" class="pa-0"  align="start" >    
                <TransitionGroup name="slide-right"  >
                    <VSheet v-show="graphType == 'live'"  key="0"    class="pa-0 !rounded-[12px]  mt-1"  >            
                        <figure class="highcharts-figure highcharts-light ">
                            <div :id="graphcontainer"   ></div> 
                        </figure>
                    </VSheet>
                    <VSheet v-show="graphType != 'live' && !historyLoading" key="1"    class="pa-0 !rounded-[12px]  mt-1"  >                       
                        <figure  class="highcharts-figure highcharts-light">
                            <div :id="graphcontainer1"  ></div> 
                        </figure>                    
                    </VSheet> 
                    <VSheet v-show="graphType != 'live' && historyLoading" key="2"  class="pa-0 size-full flex justify-center align-center"  >
                        <VProgressCircular   indeterminate></VProgressCircular> 
                    </VSheet>                
                </TransitionGroup> 
            </VCol>

            
        </VRow> 
    </VContainer>     
</template>
    
<script setup>
    /** JAVASCRIPT HERE */

    // IMPORTS
    import { ref,reactive,watch ,onMounted,onBeforeUnmount,computed, onBeforeMount } from "vue";  
    import { useRoute ,useRouter } from "vue-router";
    import { useAppStore } from '@/stores/appStore';
    import { useMqttStore } from '@/stores/mqttStore'; // Import Mqtt Store
    import { useUserStore } from '@/stores/userStore'; 
    
    import { storeToRefs } from "pinia";
    import _ from "lodash";
    import { useDisplay } from 'vuetify';
    import { Icon } from "@iconify/vue";

    // Highcharts, Load the exporting module and Initialize exporting module.
    import Highcharts from 'highcharts';
    import  'highcharts/highcharts-more';
    import  'highcharts/modules/exporting';
    
    
    
    
    // VARIABLES
    const router         = useRouter();
    const route          = useRoute();  
    const AppStore       = useAppStore();
    const UserStore      = useUserStore(); 
    const Mqtt           = useMqttStore();
    const { xs,smAndDown,smAndUp, mdAndUp }   = useDisplay();
    const { connected, payload, payloadTopic } = storeToRefs(Mqtt);
    const { selectedStation, darkmode }  = storeToRefs(UserStore);
    const { liveData, paramDetails,  } = storeToRefs(AppStore);
    const chart          = ref(null); // Chart object
    const chart1         = ref(null); // Chart object
    const points         = ref(300); // Specify the quantity of points to be shown on the live graph simultaneously.
    const shift          = ref(false); // Delete a point from the left side and append a new point to the right side of the graph.
    const graphType      = ref("live");
    const params         = ref([]);
    const chartEl        = ref(null);
    const stationName    = ref("");
    const historyLoading = ref(false);
    const getDataToggle  = ref(false);
    const month          = ref([]);
    const threedays      = ref([]);
    const sevendays      = ref([]);
    const graphcontainer    = ref(`container${_.random(0,100000)}`);
    const graphcontainer1   = ref(`container${_.random(0,100000)}`);


    const selected       = ref({"name":'Live', "type":'live'});
    const options        = ref([{"name":'Live', "type":'live'},{"name":'3D', "type":'three'},{"name":'7D', "type":'seven'},{"name":'1M', "type":'month'}]);
    
    let worker           = new Worker("/src/assets/js/mapHistoryDataWorker.js"); 

    let getDataID = ""

    // PROPS
    const props = defineProps({
        param :{type:String,default:""},
    })

    // FUNCTIONS
    const setChartParams = (param) => {
        let data = paramDetails.value[param]; 

        if(!!data){
            chart.value.series[0].setData([]);
            chart.value.update({series:{type: "spline", name: _.capitalize(param)}, subtitle: { text:  _.capitalize(param), align: 'center' }, yAxis: {max: data.max, min: data.min, labels: { format: `{value} ${data.units}` } }, tooltip: { valueSuffix: ` ${data.units}` }});

            chart1.value.series[0].setData([]);
            chart1.value.update({series:{type: "spline", name: _.capitalize(props.param)}, subtitle: { text: _.capitalize(param), align: 'center' }, yAxis: {max: data.max, min: data.min, labels: { format: `{value} ${data.units}` } }, tooltip: { valueSuffix: ` ${data.units}` }});
            chart1.value.showLoading();
            getData(param); 
            chart1.value.hideLoading();
        }
    }

    const clearChart = () => {
        chart.value.series[0].setData([]);
    }

    const getData = async (param) => { 
      
        if (!!window.Worker) {  
            historyLoading.value = true;
            // const { selectedStation }  = storeToRefs(UserStore);
             
            let timestamp = Math.floor(new Date().getTime() / 1000);
            const cookie        = UserStore.getCookie("csrf_access_token"); 
            worker.postMessage({"timestamp": timestamp,"param": param,"station":  UserStore.getSelectedStation, "user": UserStore.getID, "cookie": cookie});
        }
        else {  
            let timestamp = Math.floor(new Date().getTime() / 1000)
            let result    = await AppStore.getMapHistoryData(timestamp, timestamp, param);

            if ('data' in result) {
                let data      = result["data"];  
                let three     = new Date(result["three"]).getTime();
                let seven     = new Date(result["seven"]).getTime();

                data.forEach(row => { 
                    if (param in row){
                        month.value.push({"x": row.timestamp, "y": parseFloat(row[param].toFixed(2))  });  

                        if (row.timestamp >= three)
                            threedays.value.push({"x": row.timestamp, "y": parseFloat(row[param].toFixed(2))  });  
                        if(row.timestamp >= seven)
                            sevendays.value.push({"x": row.timestamp, "y": parseFloat(row[param].toFixed(2))  });  
                    }
                    }); 
            }
        }

        
        }

    onBeforeMount(()=> {
        
    })
      
    onMounted(() => {
        // THIS FUNCTION IS CALLED AFTER THIS COMPONENT HAS BEEN MOUNTED
        chartEl.value = document.querySelectorAll(".highcharts-figure");

        if(darkmode.value)
            chartEl.value.forEach(el => { el.classList.replace('highcharts-light','highcharts-dark') });  
        else if (!darkmode.value)
            chartEl.value.forEach(el => { el.classList.replace('highcharts-dark','highcharts-light') });   

        CreateCharts();   
         
        
        if(window.Worker){
            // WORKER EVENTS
            worker.onmessage = (e) => {
                historyLoading.value = false;
                let data =  e.data;                
                
                threedays.value = data["threedays"];
                sevendays.value = data["sevendays"];
                month.value     = data["month"];
                
                if(graphType.value == "three")
                    chart1.value.series[0].setData(threedays.value,true,true, false);    
                else if (graphType.value == "seven")
                    chart1.value.series[0].setData(sevendays.value,true,true, false);    
                else if(graphType.value == "month")    
                    chart1.value.series[0].setData(month.value,true,true, false); 
                        }
            }

            setChartParams(props.param); 
            getData(props.param);
    });


    onBeforeUnmount(()=>{
        // THIS FUNCTION IS CALLED RIGHT BEFORE THIS COMPONENT IS UNMOUNTED
        // Mqtt.unsubscribeAll();
    });


 
    // WATCHERS

    watch(getDataToggle,()=> {
        clearTimeout(getDataID);

        getDataID = setTimeout(()=>{
            getData(props.param);
        }, 1000)
    })


    watch(payload,(msg)=> {          
        // LIVE GRAPH
        if(msg.type == 'station' && msg.id == selectedStation.value){
            params.value = Object.keys(msg.data)
        
            if(points.value > 0)
                points.value --;    
            else
                shift.value = true;    

            if(params.value.includes(props.param)){    
                liveData.value[props.param] = msg.data[props.param]   
                if(!!chart.value.series){
                    chart.value.setTitle({text: _.toUpper(msg.name)}); 
                    chart.value.series[0].addPoint({y:parseFloat(msg.data[props.param].toFixed(2)) ,x: msg.timestamp * 1000 }, true, shift.value);   
                }              
            }  
        }
                  
    });

    watch(graphType,(name) => {       
        if(name == "three")
            chart1.value.series[0].setData(threedays.value,true,true, false);    
        else if (name == "seven")
            chart1.value.series[0].setData(sevendays.value,true,true, false);    
        else if(name == "month")    
            chart1.value.series[0].setData(month.value,true,true, false);          
    });

    watch(()=> props.param, async(param) => {         
        setChartParams(param);       
    })


    watch(darkmode,(mode)=> {           
       if(mode)
            chartEl.value.forEach(el => { el.classList.replace('highcharts-light','highcharts-dark') });  
       else if (!mode)
            chartEl.value.forEach(el => { el.classList.replace('highcharts-dark','highcharts-light') });         
   });


    const CreateCharts = async () => {  
        // TEMPERATURE CHART
        chart.value = Highcharts.chart(graphcontainer.value, {
            chart: { styledMode: true,   zoomType: 'x',height: 320, marginTop: 60,borderRadius: 12, borderWidth: 1 },
            title: { text: '', align: 'center' },
            subtitle: { text: 'Temperature', align: 'center' },
            yAxis: { 
                title:null,// title: { text: 'Temperature' , style:{color:'#000000'}},
                labels: { format: '{value} °C' },   
                max:50,
                min:10        
            },
        
            xAxis: {
                type: 'datetime', 
                title: null, //{ text: 'Time', style:{color:'#000000'} }, 
                crosshair: true,
                labels: { format: '{value:%I:%M %p}' } },  // value:%H:%M  value:%Y-%b-%e
            legend: false,
            navigation: {
                buttonOptions: {
                    verticalAlign: 'top',
                    x: 0
                }
            },
        
            tooltip: { 
                shared:true, 
                xDateFormat: '%A, %b %e, %I:%M %p',
                valuePrefix: '',
                valueSuffix: ' °C' },
        
            plotOptions: {
                series: {
                    marker: {
                        enabled: false
                    },
                    lineWidth: 1
                }
            },
        
            series: [
                {
                    name: 'Temperature',
                    type: 'spline',
                    data: [],
                    turboThreshold: 0,
                    marker:{type:null},
                    lineWidth:3, 
                }  ],
        
        });

        chart1.value = Highcharts.chart(graphcontainer1.value, {
            chart: { styledMode: true, zoomType: 'x',height: 320, marginTop: 60,borderRadius: 12, borderWidth: 1 },
            title: { text: '', align: 'center' },
            subtitle: { text: 'Temperature', align: 'center' },
            yAxis: { 
                title:null,// title: { text: 'Temperature' , style:{color:'#000000'}},
                labels: { format: '{value} °C' },   
                max:50,
                min:10        
            },
        
            xAxis: {
                type: 'datetime', 
                title: null, // { text: 'Time', style:{color:'#000000'} }, 
                crosshair: true,
                labels: { format: '{value:%I:%M %p}' } ,  // value:%H:%M  value:%Y-%b-%e       
            },
            legend: false,
            navigation: {
                buttonOptions: {
                    verticalAlign: 'top',
                    x: 0
                }
            },
        
            tooltip: { 
                shared:true, 
                xDateFormat: '%A, %b %e, %I:%M %p',
                valuePrefix: '',
                valueSuffix: ' °C' },
        
            plotOptions: {
                series: {
                    marker: {
                        enabled: false
                    },
                    lineWidth: 1
                }
            },
        
            series: [
                {
                    name: 'Temperature',
                    type: 'spline',
                    data: [],
                    turboThreshold: 0,
                    marker:{type:null},
                    lineWidth:3, 
                }  ],
        
        });
    }
</script>


<style>
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
 
</style>