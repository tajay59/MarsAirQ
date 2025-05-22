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
                    <VSheet v-show="!loading" key="1"  class="pa-0 rounded-lg mt-2 overflow-clip"  >                       
                        <figure  class="highcharts-figure highcharts-light">
                            <div id="container4"></div> 
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
    const graphType      = ref("three");
    const params         = ref([{"name":"temperature","units":"°C"}]);
    const chartEl        = ref(null);
    const stationName    = ref("");
    const historyLoading = ref(false);
    const getDataToggle  = ref(false);
    const loading        = ref(false);
    const maxData        = ref({});
    const minData        = ref({});
    const avgData        = ref({});
    
    let worker           = new Worker("/src/assets/js/getMultiDataWorker.js"); 
    let getDataID        = ""

    const selected       = ref({"name":'Max', "type":'three'});
    const options        = ref([{"name":'Max', "type":'three'},{"name":'Min', "type":'seven'},{"name":'Avg', "type":'month'}]);

    
    // FUNCTIONS
 

    const clearChart = () => {
        chart.value.update({series: [],drilldown: {series: []}}, true); 
    }

    const getData = async () => { 
             
        let start       = Math.floor(new Date().getTime() / 1000);
            let paramList   = []

            params.value.forEach(param => paramList.push(param.name))

            let result  = await AppStore.getColumnDrilldownData( paramList[0],start, loading);

            if ('data' in result) {
                let data      = result["data"];  
                data['max']['drilldown'].forEach(row => row['tooltip'] = { pointFormat: `<span style="color:{point.color}"><b>{point.y:.2f} °C</b></span><br/> <span>{point.x:%I:%M %p}</span>`})
                data['min']['drilldown'].forEach(row => row['tooltip'] = {pointFormat: `<span style="color:{point.color}"><b>{point.y:.2f} °C</b></span><br/> <span>{point.x:%I:%M %p}</span>`})
                data['mean']['drilldown'].forEach(row => row['tooltip'] = {pointFormat: `<span style="color:{point.color}"><b>{point.y:.2f} °C</b></span><br/> <span>{point.x:%I:%M %p}</span>`})

                maxData.value = {...data['max']};
                minData.value = {...data['min']};
                avgData.value = {...data['mean']};

               
                let name = graphType.value

                if(name == "three"){
                    clearChart(); 
                    chart.value.update({title:{ text:"Max Temperatures"},series: maxData.value['series'],drilldown: {series: maxData.value["drilldown"]}}, true); 
                }    
                else if (name == "seven"){
                    clearChart() 
                    chart.value.update({title:{ text:"Min Temperatures"},series: minData.value['series'],drilldown: {series: minData.value["drilldown"]}}, true); 
                }  
                else if(name == "month")    {
                    clearChart() 
                    chart.value.update({title:{ text:"Mean Temperatures"},series: avgData.value['series'],drilldown: {series: avgData.value["drilldown"]}}, true); 
                }  
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
                threedays.value = data["threedays"];
                sevendays.value = data["sevendays"];
                month.value     = data["month"];

                let name = graphType.value
                
                if(name == "three"){
                    clearChart()
                    // chart.value.series[0].setData(maxData.value,true,true, false);
                    chart.value.update({series: maxData.value['series'],drilldown: {series: maxData.value["drilldown"]}}, true); 
                }    
                else if (name == "seven"){
                    clearChart()
                    chart.value.update({series: minData.value['series'],drilldown: {series: minData.value["drilldown"]}}, true); 
                }  
                else if(name == "month")    {
                    clearChart()
                    chart.value.update({series: avgData.value['series'],drilldown: {series: avgData.value["drilldown"]}}, true); 
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


    watch(graphType,(name) => {       
        if(name == "three"){
            clearChart(); 
            chart.value.update({title:{ text:"Max Temperatures"},series: maxData.value['series'],drilldown: {series: maxData.value["drilldown"]}}, true); //
        }    
        else if (name == "seven"){
            clearChart() 
            chart.value.update({title:{ text:"Min Temperatures"},series: minData.value['series'],drilldown: {series: minData.value["drilldown"]}}, true); 
        }  
        else if(name == "month")    {
            clearChart() 
            chart.value.update({title:{ text:"Mean Temperatures"},series: avgData.value['series'],drilldown: {series: avgData.value["drilldown"]}}, true); 
        }      
    });

    watch(darkmode,(mode)=> {           
       if(mode)
            chartEl.value.forEach(el => { el.classList.replace('highcharts-light','highcharts-dark') });  
       else if (!mode)
            chartEl.value.forEach(el => { el.classList.replace('highcharts-dark','highcharts-light') });         
   });

   

    const CreateCharts = async () => {  
        // CHART
        chart.value = Highcharts.chart('container4', {
            chart: { type: 'column', styledMode: true },
            title: { text: 'Temperatures' },
            subtitle: {
                text: 'Click a column to view its hourly breakdown'
            },
            accessibility: {
                announceNewData: {
                    enabled: true
                }
            },
            xAxis: [{
                // type: 'category'
                type: 'datetime', 
                title: null, // { text: 'Time', style:{color:'#000000'} }, 
                crosshair: true,
                labels: { format: '{value: %a, %b %d}' } ,  // value:%H:%M  value:%Y-%b-%e   
            },
            {
                // type: 'category'
                type: 'datetime', 
                title: null, // { text: 'Time', style:{color:'#000000'} }, 
                crosshair: true,
                labels: { format: '{value: %I:%M %p}' } ,  // value:%H:%M  value:%Y-%b-%e   
            }],
            yAxis: {
                title: null

            },
            legend: {
                enabled: false
            },
            plotOptions: {
                series: {
                    borderWidth: 0,
                    dataLabels: {
                        enabled: true,
                        format: '{point.y:.2f} °C'
                    }
                },            
                
            },

            tooltip: {
                headerFormat: '<span style="font-size:11px">{series.name}</span><br>',
                pointFormat: '<span style="color:{point.color}">{point.name}</span>: ' + '<b>{point.y:.2f} °C</b><br/>'
                /*
                formatter: function () {
                    let isDrilldown = !['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday'].includes(this.key)
                
                if (!isDrilldown) {
                    return `<span style="color:${this.point.color}">${this.point.name}</span>:  <b>${this.point.y}:.2f °C</b><br/>`;
                } else {
                    console.log(this.point, this.series)
                    console.log(new Date(this.point.x).toTimeString())
                    let time = new Date(this.point.x).toLocaleTimeString()
                    console.log(time)
                    return `<span style="color:${this.point.color}">${this.series.name}</span><br><span>${time}</span> <br><br><b>${this.point.y} °C</b><br/>`;
                }
            }*/
            },
            series: [{}],
            drilldown: {
                activeDataLabelStyle: { textDecoration: 'none' },
                
                breadcrumbs: {
                    position: {
                        align: 'right'
                    },
                    format: '{level.name}{level.x:,  %b %d}'
                },
                series: [ ]
            }
        
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