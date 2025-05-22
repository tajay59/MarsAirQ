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
            <VCol cols="12" class="  pa-0 "  align="start" >                    
                <TransitionGroup name="slide-right"  > 
                    <VSheet v-show="!loading" key="1"  class="pa-0  rounded-lg mt-2 overflow-clip"  >                       
                        <figure  class="highcharts-figure highcharts-light">
                            <div id="container3"></div> 
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
    const graphType      = ref("three");
    const params         = ref([{"name":"pressure","units":"mb"},{"name":"rainfall","units":"mm"}]);
    const chartEl        = ref(null);
    const stationName    = ref("");
    const historyLoading = ref(false);
    const getDataToggle  = ref(false);
    const month          = ref([]);
    const threedays      = ref([]);
    const sevendays      = ref([]);
    const loading        = ref(false);
    
    let worker           = new Worker("/src/assets/js/getMultiDataWorker.js"); 
    let getDataID        = ""

    const selected       = ref({"name":'3 Days', "type":'three'});
    const options        = ref([{"name":'3 Days', "type":'three'},{"name":'7 Days', "type":'seven'},{"name":'1 Month', "type":'month'}]);

    
    // FUNCTIONS
 

    const clearChart = () => {
        chart.value.series[0].setData([]);
    }

    const getData = async () => { 
             
        
        if (!!window.Worker) {   //
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
                let three = new Date(result["three"]).getTime() / 1000;
                let seven = new Date(result["seven"]).getTime() / 1000;

                data.forEach(row => {           
                    month.value.push({"x": row[params.value[1].name], "y": row[params.value[0].name]   });  

                    if (row.timestamp >= three)
                        threedays.value.push({"x": row[params.value[1].name], "y": row[params.value[0].name] });  
                    if(row.timestamp >= seven)
                        sevendays.value.push({"x": row[params.value[1].name], "y": row[params.value[0].name] });               
                });  

                if(graphType.value == "three"){
                    clearChart()
                    chart.value.series[0].setData(threedays.value,true,true, false);}    
                else if (graphType.value == "seven"){
                    clearChart()
                    chart.value.series[0].setData(sevendays.value,true,true, false);  }  
                else if(graphType.value == "month")    {
                    clearChart()
                    chart.value.series[0].setData(month.value,true,true, false); }
            }
        } 

        
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
                threedays.value = data["threedays"];
                sevendays.value = data["sevendays"];
                month.value     = data["month"];
                
                if(graphType.value == "three"){
                    clearChart()
                    chart.value.series[0].setData(threedays.value,true,true, false);}    
                else if (graphType.value == "seven"){
                    clearChart()
                    chart.value.series[0].setData(sevendays.value,true,true, false);  }  
                else if(graphType.value == "month")    {
                    clearChart()
                    chart.value.series[0].setData(month.value,true,true, false); }
                        }
                
            }

            getData();
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


    watch(graphType,(name) => {       
        if(name == "three"){
            clearChart()
            chart.value.series[0].setData(threedays.value,true,true, false);}    
        else if (name == "seven"){
            clearChart()
            chart.value.series[0].setData(sevendays.value,true,true, false);  }  
        else if(name == "month")    {
            clearChart()
            chart.value.series[0].setData(month.value,true,true, false); }         
    });

    watch(darkmode,(mode)=> {           
       if(mode)
            chartEl.value.forEach(el => { el.classList.replace('highcharts-light','highcharts-dark') });  
       else if (!mode)
            chartEl.value.forEach(el => { el.classList.replace('highcharts-dark','highcharts-light') });         
   });


    const CreateCharts = async () => {  
        // CHART
        chart.value = Highcharts.chart('container3', {
            chart: { type: 'scatter', styledMode: true, zoomType: 'xy',height: 500, marginTop: 60 },
            title: { text: '', align: 'center' },
            subtitle: { text: `${params.value[0].name} vs ${params.value[1].name}`, align: 'center' },
            yAxis: { 
                title: { text: params.value[0].name },
                labels: { format: `{value} ${params.value[0].units}` }     
            },
        
            xAxis: {
                title: { text: params.value[1].name },
                labels: { format: `{value} ${params.value[1].units}` },  
                startOnTick: true,
                endOnTick: true,
                showLastLabel: true     
            },
            legend: true,
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
    
            series: [
                {
                    name: `${params.value[0].name} vs ${params.value[1].name}`,                    
                    data: [],
                    turboThreshold: 0, 
                    color: Highcharts.getOptions().colors[3]
                }  ],
        
        });
    }
</script>


<style>

</style>