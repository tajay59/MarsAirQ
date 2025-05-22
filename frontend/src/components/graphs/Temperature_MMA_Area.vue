<template>
    <VContainer align="center" class="h-full" fluid>         
        <VRow class=" fill-height" >
            <VCol cols="12" class="flex align-start justify-end pa-0" >
                <Button    severity="primary"    class="dark:!bg-[hsl(0,0%,3%)] !bg-[hsl(0,0%,90%)]  !text-black dark:!text-white !text-small h-[37px]  border" size="small" @click="getDataToggle = !getDataToggle">                  
                    <p class="font-normal text-sm" >Refresh</p>                
                </Button>
            </VCol>
            <VCol cols="12" class="  pa-0 "  align="start" >  
                <TransitionGroup name="slide-right"  > 
                    <VSheet v-show="!loading" key="1"  class="pa-0 rounded-lg mt-2  overflow-clip"  >                       
                        <figure  class="highcharts-figure highcharts-light">
                            <div id="container5"></div> 
                        </figure>                    
                    </VSheet> 
                    <VSheet v-show="loading" key="2"  class="pa-0 size-full flex justify-center align-center"  >
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
    import Drilldown from 'highcharts/modules/drilldown'
    
    
    Drilldown(Highcharts);
    
    
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
    const points         = ref(300); // Specify the quantity of points to be shown on the live graph simultaneously.
    const shift          = ref(false); // Delete a point from the left side and append a new point to the right side of the graph.
    const graphType      = ref("max");
    const params         = ref([{"name":"temperature","units":"°C"}]);
    const chartEl        = ref(null);
    const stationName    = ref("");
    const historyLoading = ref(false);
    const getDataToggle  = ref(false);
    const loading        = ref(false);
    const rangesData     = ref([]);
    const avgData        = ref([]);
    
    let worker           = new Worker("/src/assets/js/getMultiDataWorker.js"); 
    let getDataID        = ""

    
    // FUNCTIONS
 

    const clearChart = () => { 
        chart.value.series[0].setData([],true,true, false);
        chart.value.series[1].setData([],true,true, false);
    }

    const getData = async () => { 
             
        let start       = Math.floor(new Date().getTime() / 1000);
            let paramList   = []

            params.value.forEach(param => paramList.push(param.name))

            let data  = await AppStore.getMMAData( paramList[0],start, loading);

            if ('ranges' in data) { 
                rangesData.value = data['ranges']; 
                avgData.value   = data['avg'];

                clearChart(); 
                
                chart.value.series[0].setData(avgData.value,true,true, false);
                chart.value.series[1].setData(rangesData.value,true,true, false);
                
                    }
            /*
        if (!!window.Worker) {   //!!window.Worker
            loading.value = true;
           
            let start       = Math.floor(new Date().getTime() / 1000);
            let paramList   = []

            params.value.forEach(param => paramList.push(param.name))
            const cookie    = UserStore.getCookie("csrf_access_token"); 
            worker.postMessage({"params": paramList,"start":  start, "cookie": cookie});
        }
        else {  
            
            let start       = Math.floor(new Date().getTime() / 1000);
            let paramList   = []

            params.value.forEach(param => paramList.push(param.name))

            let result  = await AppStore.getMultiData( paramList,start, loading);

            if ('data' in result) {
                let data  = result["data"];  
                let max = new Date(result["max"]).getTime() / 1000;
                let min = new Date(result["min"]).getTime() / 1000;

                data.forEach(row => {           
                    avg.value.push({"x": row[_.capitalize(params.value[1].name)], "y": row[_.capitalize(params.value[0].name)]   });  

                    if (row.timestamp >= max)
                        maxdays.value.push({"x": row[_.capitalize(params.value[1].name)], "y": row[_.capitalize(params.value[0].name)] });  
                    if(row.timestamp >= min)
                        mindays.value.push({"x": row[_.capitalize(params.value[1].name)], "y": row[_.capitalize(params.value[0].name)] });               
                });  

                if(graphType.value == "max"){
                    clearChart()
                    chart.value.series[0].setData(maxdays.value,true,true, false);}    
                else if (graphType.value == "min"){
                    clearChart()
                    chart.value.series[0].setData(mindays.value,true,true, false);  }  
                else if(graphType.value == "avg")    {
                    clearChart()
                    chart.value.series[0].setData(avg.value,true,true, false); }
            }
        } 

        */
        
        }

      
    onMounted(() => {
        // THIS FUNCTION IS CALLED AFTER THIS COMPONENT HAS BEEN MOUNTED
        chartEl.value = document.querySelectorAll(".highcharts-figure");
        ;

        if(darkmode.value)
            chartEl.value.forEach(el => { el.classList.replace('highcharts-light','highcharts-dark') });  
        else if (!darkmode.value)
            chartEl.value.forEach(el => { el.classList.replace('highcharts-dark','highcharts-light') });   

        CreateCharts();      
        
        if(window.Worker){
            // WORKER EVENTS
            worker.onmessage = (e) => {
                loading.value = false;
                let data =  e.data;
                
                // console.log(data);
                rangesData.value = {...data['max']};
                minData.value = {...data['min']};
                avgData.value = {...data['mean']};

                let name = graphType.value
                
                if(name == "max"){
                    clearChart(); 
                    chart.value.update({title:{ text:"Max Temperatures"},series: rangesData.value['series'],drilldown: {series: rangesData.value["drilldown"]}}, true); //
                }    
                else if (name == "min"){
                    clearChart() 
                    chart.value.update({title:{ text:"Min Temperatures"},series: minData.value['series'],drilldown: {series: minData.value["drilldown"]}}, true); 
                }  
                else if(name == "avg")    {
                    clearChart() 
                    chart.value.update({title:{ text:"Mean Temperatures"},series: avgData.value['series'],drilldown: {series: avgData.value["drilldown"]}}, true); 
                } 
                
            }

            getData();
    }
});


    onBeforeUnmount(()=>{
        // THIS FUNCTION IS CALLED RIGHT BEFORE THIS COMPONENT IS UNMOUNTED
        // Mqtt.unsubscribeAll();
    });


 
    // WATCHERS
    watch(getDataToggle,()=> {
        clearTimeout(getDataID);

        getDataID = setTimeout(()=>{
            getData();
        }, 1000)
    })


  
    watch(darkmode,(mode)=> {           
       if(mode)
            chartEl.value.forEach(el => { el.classList.replace('highcharts-light','highcharts-dark') });  
       else if (!mode)
            chartEl.value.forEach(el => { el.classList.replace('highcharts-dark','highcharts-light') });         
   });



    const CreateCharts = async () => {  
        // CHART
        chart.value = Highcharts.chart('container5', {
            chart: {  styledMode: true },
            title: { text: 'Temperatures (Daily)' },
            subtitle: {
                text: 'Daily Minimum, Maximum and Average'
            },
            accessibility: {
                announceNewData: {
                    enabled: true
                }
            },
            xAxis: {type: 'datetime', labels: { format: '{value:%a, %b %d}' } , },// // type: 'category'
              
            yAxis: {
                title: null

            },
            legend: {
                enabled: false
            },
            plotOptions: {
                series: {
                    borderWidth: 0,                    
                },
                
            },
            tooltip: {
                crosshairs: true,
                shared: true,
                valueSuffix: '°C'
            },
            /*
            tooltip: {
                headerFormat: '<span style="font-size:11px">{series.name}</span><br>',
                pointFormat: '<span style="color:{point.color}">{point.name}</span>: ' + '<b>{point.y:.2f}°C</b><br/>'
            },*/
            series: [
                {
                    name: 'Temperature',
                    type: 'line',
                    data: [],
                    zIndex: 1,
                    marker: {
                        fillColor: 'white',
                        lineWidth: 6,
                        lineColor: Highcharts.getOptions().colors[0]
                    },
                }, 
                {
                    name: 'Range',
                    data: [],
                    type: 'arearange',
                    lineWidth: 0,
                    linkedTo: ':previous',
                    color: Highcharts.getOptions().colors[0],
                    fillOpacity: 0.3,
                    zIndex: 0,
                    marker: {
                        enabled: false
                    },
                }
                ]
                   
        });
    }
</script>


<style>
.highcharts-drilldown-data-label text {
  text-decoration: none !important;
}

.highcharts-xaxis-labels text {
  text-decoration: none !important;
}


</style>