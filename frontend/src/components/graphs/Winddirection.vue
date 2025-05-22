<template>
    <VContainer align="center" class="h-full" fluid>
         
        <VRow class="bg- green fill-height" >
            <VCol class="bg- blue pa-0  "  align="start" >    
                <VBtnGroup  variant="outlined" divided density="compact" rounded="lg" class=" "   >
                    <VBtn text="Live"       :active="(graphType == 'live')"    :class="[(graphType == 'live')?   'font-bold': 'font-regular']"   color="onSurface"   class="text-caption " @click="graphType = 'live'"    size="x-small" ></VBtn>
                    <VBtn text="3 Days"     :active="(graphType == 'three')"   :class="[(graphType == 'three')?  'font-bold': 'font-regular']"   color="onSurface"   class="text-caption"  @click="graphType = 'three' "  size="x-small" ></VBtn>
                    <VBtn text="7 Days"     :active="(graphType == 'seven')"   :class="[(graphType == 'seven')?  'font-bold': 'font-regular']"   color="onSurface"   class="text-caption"  @click="graphType = 'seven'"  size="x-small" ></VBtn>
                    <VBtn text="1 Month"    :active="(graphType == 'month')"   :class="[(graphType == 'month')?  'font-bold': 'font-regular']"   color="onSurface"   class="text-caption"  @click="graphType = 'month'"  size="x-small" ></VBtn> 
                </VBtnGroup> 

                <VBtn text="Refresh" variant="text" rounded="lg" class="ml-5 text-none"  @click="getDataToggle = !getDataToggle" ></VBtn>
                
                <TransitionGroup name="slide-right"  >
                    <VSheet v-show="graphType == 'live'"  key="0"   class="pa-0"  >                
                        <figure class="highcharts-figure highcharts-light">
                            <div id="container"></div> 
                        </figure>
                    </VSheet>
                    <VSheet v-show="graphType != 'live' && !historyLoading" key="1"  class="pa-0"  >                              
                        <figure  class="highcharts-figure highcharts-light">
                            <div id="container1"></div> 
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
   import  'highcharts/highcharts-more';
    import  'highcharts/modules/exporting';
    
    
    
    
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
    
    let worker           = new Worker("/src/assets/js/mapHistoryDataWorker.js"); 

    let getDataID = ""

    
    // FUNCTIONS
 

    const clearChart = () => {
        chart.value.series[0].setData([]);
    }

    const getData = async (param) => { 

        if (!!window.Worker) { 
            historyLoading.value = true;
            const { selectedStation, layout}  = storeToRefs(UserStore);
            let timestamp = Math.floor(new Date().getTime() / 1000);
            const cookie        = UserStore.getCookie("csrf_access_token"); 
            worker.postMessage({"timestamp": timestamp,"param": param,"station":  selectedStation.value, "user": UserStore.getID, "cookie": cookie});
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

            getData("winddirection");
    });


    onBeforeUnmount(()=>{
        // THIS FUNCTION IS CALLED RIGHT BEFORE THIS COMPONENT IS UNMOUNTED
        // Mqtt.unsubscribeAll();
    });


 
    // WATCHERS
    watch(getDataToggle,()=> {
        clearTimeout(getDataID);

        getDataID = setTimeout(()=>{
            getData("winddirection");
        }, 1000)
    })


    watch(payload,(msg)=> {          
        // LIVE GRAPH
        if (msg.type == 'station')
            params.value = Object.keys(msg.data)
        
        if(points.value > 0)
            points.value --;    
        else
            shift.value = true;    

        if(msg.type == "station" && params.value.includes('winddirection')){    
            liveData.value.winddirection = msg.data.winddirection          
            chart.value.setTitle({text: _.toUpper(msg.name)});
            chart1.value.setTitle({text: _.toUpper(msg.name)});
            chart.value.series[0].addPoint({y:parseFloat(msg.data.winddirection.toFixed(2)) ,x: msg.timestamp * 1000 }, true, shift.value);   
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

    watch(darkmode,(mode)=> {           
       if(mode)
            chartEl.value.forEach(el => { el.classList.replace('highcharts-light','highcharts-dark') });  
       else if (!mode)
            chartEl.value.forEach(el => { el.classList.replace('highcharts-dark','highcharts-light') });         
   });


    const CreateCharts = async () => {  
    // TEMPERATURE CHART
    chart.value = Highcharts.chart('container', {
        chart: { styledMode: true,   zoomType: 'x',height: 500, marginTop: 60 },
        title: { text: '', align: 'center' },
        subtitle: { text: 'Wind Direction', align: 'center' },
        yAxis: { 
            title:null,// title: { text: 'Wind Direction' , style:{color:'#000000'}},
            labels: { format: '{value} °' },   
            max:360,
            min:0        
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
            valueSuffix: ' °' },
    
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
                name: 'Wind Direction',
                type: 'spline',
                data: [],
                turboThreshold: 0,
                marker:{type:null},
                lineWidth:3,
                color: Highcharts.getOptions().colors[1]
            }  ],
    
    });

    chart1.value = Highcharts.chart('container1', {
        chart: { styledMode: true, zoomType: 'x',height: 500, marginTop: 60 },
        title: { text: '', align: 'center' },
        subtitle: { text: 'Wind Direction', align: 'center' },
        yAxis: { 
            title:null,// title: { text: 'Wind Direction' , style:{color:'#000000'}},
            labels: { format: '{value} °' },   
            max:360,
            min:0        
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
            valueSuffix: ' °' },
    
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
                name: 'Wind Direction',
                type: 'spline',
                data: [],
                turboThreshold: 0,
                marker:{type:null},
                lineWidth:3,
                color: Highcharts.getOptions().colors[1]
            }  ],
    
    });
    }
</script>

<style>

</style>