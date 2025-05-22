<template>
    <VContainer align="center" class="h-full " fluid>         
        <VRow class=" fill-height" >
            <VCol cols="12" class="flex align-center justify-end gap-3 pa-0  h-[50px] pr-5" >
                <SelectButton v-model="selected" :options="options"  optionLabel="name" class=""   aria-labelledby="basic"  :allowEmpty="false" @click="graphType =  selected.type"  size="small" >
                    <template #option="slotProps" >
                        <p class="text-sm font-semibold font-[Roboto]" >{{ slotProps.option.name }}</p>
                    </template>
                </SelectButton>

                <VBtn    title="Refresh Graphs" icon size="35" flat class="dark:!bg-[hsl(0,0%,3%)] !bg-[hsl(0,0%,90%)]  !text-black dark:!text-white !text-small h-[37px]  border"  @click="getDataToggle = !getDataToggle">      
                    <svg  width="30" height="30" viewBox="0 0 24 24"  class="dark:text-neutral-200 text-neutral-800"><path fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 11A8.1 8.1 0 0 0 4.5 9M4 5v4h4m-4 4a8.1 8.1 0 0 0 15.5 2m.5 4v-4h-4"/></svg>            
                    <!-- <svg   width="24" height="24" viewBox="0 0 24 24" class="dark:text-neutral-200 text-neutral-800"><path fill="currentColor" fill-rule="evenodd" d="M3.464 3.464C2 4.93 2 7.286 2 12s0 7.071 1.464 8.535C4.93 22 7.286 22 12 22s7.071 0 8.535-1.465C22 19.072 22 16.714 22 12s0-7.071-1.465-8.536C19.072 2 16.714 2 12 2S4.929 2 3.464 3.464m1.997 7.62A6.59 6.59 0 0 1 12.01 5.25c1.982 0 3.76.875 4.967 2.257a.75.75 0 0 1-1.13.986A5.08 5.08 0 0 0 12.01 6.75a5.09 5.09 0 0 0-5.037 4.333h.364a.75.75 0 0 1 .53 1.281l-1.169 1.167a.75.75 0 0 1-1.06 0L4.47 12.364a.75.75 0 0 1 .53-1.28zm11.84-.615a.75.75 0 0 1 1.06 0l1.169 1.167a.75.75 0 0 1-.53 1.28h-.46a6.59 6.59 0 0 1-6.55 5.834a6.58 6.58 0 0 1-4.967-2.256a.75.75 0 0 1 1.13-.987a5.08 5.08 0 0 0 3.838 1.743a5.09 5.09 0 0 0 5.036-4.333h-.363a.75.75 0 0 1-.53-1.281z" clip-rule="evenodd"/></svg>             -->
                </VBtn>
                <VBtn icon="mdi:mdi-close" title="Close" color="onSurface" size="24" variant="flat" density="compact" @click="UserStore.setSelectedStation(null)" />   
            </VCol>

            <VCol cols="12" class="pa-0 "  align="start" >    
                <TransitionGroup name="slide-right"  >
                    <VSheet v-show="graphType == 'live'"  key="0"   class="pa-0  "  >            
                        <figure class="highcharts-figure highcharts-light ">
                            <div :id="graphcontainer"   ></div> 
                        </figure>
                    </VSheet>
                    <VSheet v-show="graphType != 'live' && !historyLoading" key="1"  class="pa-0   "  >                       
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
    import { ref,reactive,watch ,onMounted,onBeforeUnmount,computed } from "vue";  
    import { useRoute ,useRouter } from "vue-router";
    import { useAppStore } from '@/stores/appStore';
    import { useMqttStore } from '@/stores/mqttStore'; // Import Mqtt Store
    import { useUserStore } from '@/stores/userStore'; 
    
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
    const { liveData } = storeToRefs(AppStore);
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
    const options        = ref([{"name":'Live', "type":'live'},{"name":'3 Days', "type":'three'},{"name":'7 Days', "type":'seven'},{"name":'1 Month', "type":'month'}]);
    
    let worker           = new Worker("/src/assets/js/mapHistoryDataWorker.js"); 

    let getDataID = ""

    // PROPS
    const props = defineProps({
        param :{type:String,default:""},
    })

    // FUNCTIONS

    const clearChart = () => {
        chart.value.series[0].setData([]);
    }

    const getData = async (param) => { 
      
        if (!!window.Worker) {  
            historyLoading.value = true;
            // const { selectedStation, layout}  = storeToRefs(UserStore);
             
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
        if(msg.type == 'station')
            params.value = Object.keys(msg.data)
        
        if(points.value > 0)
            points.value --;    
        else
            shift.value = true;    

        if(msg.type == "station" && params.value.includes(props.param)){    
            // liveData.value[props.param] = msg.data[props.param]   
            if(!!chart.value.series && selectedStation.value == msg.id){
                chart.value.setTitle({text: _.toUpper(msg.name)}); 
                chart.value.series[0].addPoint({y:parseFloat(msg.data[props.param].toFixed(2)) ,x: msg.timestamp * 1000 }, true, shift.value);   
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

    watch(()=> props.param, async(param) =>{
         
        if(param == "temperature"){            
            chart.value.series[0].setData([]);
            chart.value.update({series:{type: "spline", name: _.capitalize(props.param)}, subtitle: { text: 'Temperature', align: 'center' }, yAxis: {max:50, min: 0, labels: { format: '{value} °C' } }, tooltip: { valueSuffix: ' °C' }});

            chart1.value.series[0].setData([]);
            chart1.value.update({series:{type: "spline", name: _.capitalize(props.param)}, subtitle: { text: 'Temperature', align: 'center' }, yAxis: {max:50, min: 0, labels: { format: '{value} °C' } }, tooltip: { valueSuffix: ' °C' }});
            chart1.value.showLoading();
            getData(param); 
            chart1.value.hideLoading();
        }        

        else if(param == "humidity"){
            chart.value.series[0].setData([]);
            chart.value.update({series:{type: "spline", name: _.capitalize(props.param)}, subtitle: { text: 'Humidity', align: 'center' }, yAxis: {max:100, min: 0, labels: { format: '{value} %' } },tooltip: { valueSuffix: ' %' }}); 

            chart1.value.series[0].setData([]);
            chart1.value.update({series:{type: "column", name: _.capitalize(props.param)}, subtitle: { text: 'Humidity', align: 'center' }, yAxis: {max:100, min: 0, labels: { format: '{value} %' } },tooltip: { valueSuffix: ' %' }}); 
            chart1.value.showLoading();
            getData(param); 
            chart1.value.hideLoading();
        }

        else if(param == "pressure"){            
            chart.value.series[0].setData([]);
            chart.value.update({series:{type: "spline", name: _.capitalize(props.param)}, subtitle: { text: 'Pressure', align: 'center' }, yAxis: {max:1100, min: 900, labels: { format: '{value} hPa' } },tooltip: { valueSuffix: ' hPa' }}) 
                  
            chart1.value.series[0].setData([]);
            chart1.value.update({series:{type: "spline", name: _.capitalize(props.param)}, subtitle: { text: 'Pressure', align: 'center' }, yAxis: {max:1100, min: 900, labels: { format: '{value} hPa' } },tooltip: { valueSuffix: ' hPa' }}) 
            chart1.value.showLoading();
            getData(param); 
            chart1.value.hideLoading();
        }

        else if(param == "radiation"){
            chart.value.series[0].setData([]);
            chart.value.update({series:{type: "spline", name: _.capitalize(props.param)}, subtitle: { text: 'Radiation', align: 'center' }, yAxis: {max:100, min: 0,   labels: { format: '{value} W/m2' } },tooltip: { valueSuffix: ' W/m2' }}) 

            chart1.value.series[0].setData([]);
            chart1.value.update({series:{type: "spline", name: _.capitalize(props.param)}, subtitle: { text: 'Radiation', align: 'center' }, yAxis: {max:100, min: 0,   labels: { format: '{value} W/m2' } },tooltip: { valueSuffix: ' W/m2' }}) 
            chart1.value.showLoading();
            getData(param); 
            chart1.value.hideLoading();
        }
        
        else if(param == "uva"){
            chart.value.series[0].setData([]);
            chart.value.update({series:{type: "spline", name: _.capitalize(props.param)}, subtitle: { text: 'UVA', align: 'center' }, yAxis: {max:100, min: 0,   labels: { format: '{value} W/m2' } },tooltip: { valueSuffix: ' W/m2' }}); 

            chart1.value.series[0].setData([]);
            chart1.value.update({series:{type: "spline", name: _.capitalize(props.param)}, subtitle: { text: 'UVA', align: 'center' }, yAxis: {max:100, min: 0,   labels: { format: '{value} W/m2' } },tooltip: { valueSuffix: ' W/m2' }}); 
            chart1.value.showLoading();
            getData(param); 
            chart1.value.hideLoading();
        }

                
        else if(param == "uvb"){
            chart.value.series[0].setData([]);
            chart.value.update({series:{type: "spline", name: _.capitalize(props.param)}, subtitle: { text: 'UVB', align: 'center' }, yAxis: {max:100, min: 0,   labels: { format: '{value} W/m2' } },tooltip: { valueSuffix: ' W/m2' }}); 

            chart1.value.series[0].setData([]);
            chart1.value.update({series:{type: "spline", name: _.capitalize(props.param)}, subtitle: { text: 'UVB', align: 'center' }, yAxis: {max:100, min: 0,   labels: { format: '{value} W/m2' } },tooltip: { valueSuffix: ' W/m2' }}); 
            chart1.value.showLoading();
            getData(param); 
            chart1.value.hideLoading();
        }

                
        else if(param == "uvc"){
            chart.value.series[0].setData([]);
            chart.value.update({series:{type: "spline", name: _.capitalize(props.param)}, subtitle: { text: 'UVC', align: 'center' }, yAxis: {max:100, min: 0,   labels: { format: '{value} W/m2' } },tooltip: { valueSuffix: ' W/m2' }}); 

            chart1.value.series[0].setData([]);
            chart1.value.update({series:{type: "spline", name: _.capitalize(props.param)}, subtitle: { text: 'UVC', align: 'center' }, yAxis: {max:100, min: 0,   labels: { format: '{value} W/m2' } },tooltip: { valueSuffix: ' W/m2' }}); 
            chart1.value.showLoading();
            getData(param); 
            chart1.value.hideLoading();
        }

                
        else if(param == "co2"){
            chart.value.series[0].setData([]);
            chart.value.update({series:{type: "spline", name: _.capitalize(props.param)}, subtitle: { text: 'CO2', align: 'center' }, yAxis: {max:5500, min: 0,   labels: { format: '{value} ppm' } },tooltip: { valueSuffix: ' ppm' }}); 

            chart1.value.series[0].setData([]);
            chart1.value.update({series:{type: "spline", name: _.capitalize(props.param)}, subtitle: { text: 'CO2', align: 'center' }, yAxis: {max:5500, min: 0,   labels: { format: '{value} ppm' } },tooltip: { valueSuffix: ' ppm' }}); 
            chart1.value.showLoading();
            getData(param); 
            chart1.value.hideLoading();
        }

        else if(param == "rainfall"){
            chart.value.series[0].setData([]);
            chart.value.update({series:{type: "spline", name: _.capitalize(props.param)}, subtitle: { text: 'Rainfall', align: 'center' }, yAxis: {max:60, min: 0,   labels: { format: '{value} mm' } },tooltip: { valueSuffix: ' mm' }});

            chart1.value.series[0].setData([]);
            chart1.value.update({series:{type: "column", name: _.capitalize(props.param)}, subtitle: { text: 'Rainfall', align: 'center' }, yAxis: {max:60, min: 0,   labels: { format: '{value} mm' } },tooltip: { valueSuffix: ' mm' }});
            chart1.value.showLoading();
            getData(param); 
            chart1.value.hideLoading(); 
        }

        else if(param == "winddirection"){
            chart.value.series[0].setData([]);
            chart.value.update({series:{type: "spline", name: _.capitalize(props.param)}, subtitle: { text: 'Wind Direction', align: 'center' }, yAxis: {max:360, min: 0, labels: { format: '{value} °' } },tooltip: { valueSuffix: ' °' }});

            chart1.value.series[0].setData([]);
            chart1.value.update({series:{type: "spline", name: _.capitalize(props.param)}, subtitle: { text: 'Wind Direction', align: 'center' }, yAxis: {max:360, min: 0, labels: { format: '{value} °' } },tooltip: { valueSuffix: ' °' }});
            chart1.value.showLoading();
            getData(param); 
            chart1.value.hideLoading(); 
        }

        else if(param == "windspeed"){
            chart.value.series[0].setData([]);
            chart.value.update({series:{type: "spline", name: _.capitalize(props.param)}, subtitle: { text: 'Wind Speed', align: 'center' }, yAxis: {max:100, min: 0, labels: { format: '{value} m/s' } },tooltip: { valueSuffix: ' m/s' }});

            chart1.value.series[0].setData([]);
            chart1.value.update({series:{type: "spline", name: _.capitalize(props.param)}, subtitle: { text: 'Wind Speed', align: 'center' }, yAxis: {max:100, min: 0, labels: { format: '{value} m/s' } },tooltip: { valueSuffix: ' m/s' }});
            chart1.value.showLoading();
            getData(param); 
            chart1.value.hideLoading(); 
        }

        else if(param == "bat"){
            chart.value.series[0].setData([]);
            chart.value.update({series:{type: "spline", name: _.capitalize(props.param)}, subtitle: { text: 'Battery', align: 'center' }, yAxis: {max:100, min: 0, labels: { format: '{value} %' } },tooltip: { valueSuffix: ' %' }});

            chart1.value.series[0].setData([]);
            chart1.value.update({series:{type: "column", name: _.capitalize(props.param)}, subtitle: { text: 'Battery', align: 'center' }, yAxis: {max:100, min: 0, labels: { format: '{value} %' } },tooltip: { valueSuffix: ' %' }});
            chart1.value.showLoading();
            getData(param); 
            chart1.value.hideLoading(); 
        }

        else if(param == "voltage"){
            chart.value.series[0].setData([]);
            chart.value.update({series:{type: "spline", name: _.capitalize(props.param)}, subtitle: { text: 'Voltage', align: 'center' }, yAxis: {max:4.2, min: 0, labels: { format: '{value} V' } },tooltip: { valueSuffix: ' V' }});

            chart1.value.series[0].setData([]);
            chart1.value.update({series:{type: "area", name: _.capitalize(props.param)}, subtitle: { text: 'Voltage', align: 'center' }, yAxis: {max:4.2, min: 0, labels: { format: '{value} V' } },tooltip: { valueSuffix: ' V' }});
            chart1.value.showLoading();
            getData(param); 
            chart1.value.hideLoading(); 
        }
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
            chart: { styledMode: true,   zoomType: 'x',height: 335, marginTop: 60,borderRadius: 12, borderWidth: 1, },
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
            chart: { styledMode: true, zoomType: 'x',height: 335, marginTop: 60,borderRadius: 12, borderWidth: 1 },
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