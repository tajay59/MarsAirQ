<template>
    <VContainer align="center" class="h-full" fluid>         
        <VRow class=" fill-height" >
            <VCol cols="12" class="flex align-start justify-end gap-3 pa-0" >
                <SelectButton v-model="selected" :options="options"  optionLabel="name" class=""   aria-labelledby="basic"  :allowEmpty="false" @click="graphType =  selected.type"  size="small" >
                    <template #option="slotProps" >
                        <p class="text-sm font-semi-bold font-[Roboto]" >{{ slotProps.option.name }}</p>
                    </template>
                </SelectButton>

                <Button    severity="primary"    class="dark:!bg-[hsl(0,0%,3%)] !bg-[hsl(0,0%,90%)]  !text-black dark:!text-white !text-small h-[37px]  border" size="small" @click="getDataToggle = !getDataToggle">                  
                    <p class="font-normal text-sm" >Refresh</p>                
                </Button>
            </VCol>

            <VCol cols="12" class="pa-0"  align="start" >    
                <TransitionGroup name="slide-right"  >
                    <VSheet v-show="graphType == 'live'"  key="0"   class="pa-0 rounded-lg mt-5"  >            
                        <figure class="highcharts-figure highcharts-light ">
                            <div id="container"  class="rounded-xl overflow-clip"></div> 
                        </figure>
                    </VSheet>
                    <VSheet v-show="graphType != 'live' && !historyLoading" key="1"  class="pa-0 rounded-lg mt-5"  >                       
                        <figure  class="highcharts-figure highcharts-light">
                            <div id="container1" class="rounded-xl overflow-clip"></div> 
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

    const selected       = ref({"name":'Live', "type":'live'});
    const options        = ref([{"name":'Live', "type":'live'},{"name":'3 Days', "type":'three'},{"name":'7 Days', "type":'seven'},{"name":'1 Month', "type":'month'}]);
    
    let worker           = new Worker("/src/assets/js/mapHistoryDataWorker.js"); 

    let getDataID = ""

    
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
                
                // console.log(data);
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

            getData("temperature");
    });


    onBeforeUnmount(()=>{
        // THIS FUNCTION IS CALLED RIGHT BEFORE THIS COMPONENT IS UNMOUNTED
        // Mqtt.unsubscribeAll();
    });


 
    // WATCHERS
    watch(()=> selected.value,(name)=> {
        console.log(`value : ${name}`)
        console.log(name)

    })


    watch(getDataToggle,()=> {
        clearTimeout(getDataID);

        getDataID = setTimeout(()=>{
            getData("temperature");
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

        if(msg.type == "station" && params.value.includes('temperature')){    
            liveData.value.temperature = msg.data.temperature          
            chart.value.setTitle({text: _.toUpper(msg.name)});
            chart1.value.setTitle({text: _.toUpper(msg.name)});
            chart.value.series[0].addPoint({y:parseFloat(msg.data.temperature.toFixed(2)) ,x: msg.timestamp * 1000 }, true, shift.value);   
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
                color: Highcharts.getOptions().colors[1]
            }  ],
    
    });

    chart1.value = Highcharts.chart('container1', {
        chart: { styledMode: true, zoomType: 'x',height: 500, marginTop: 60 },
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
                color: Highcharts.getOptions().colors[1]
            }  ],
    
    });
    }
</script>


<style>

</style>