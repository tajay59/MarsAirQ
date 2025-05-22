<template>
    <VContainer align="center" class="h-full" fluid>
         
        <VRow class="bg- green fill-height" >
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
            <VCol cols="12" class="bg- blue pa-0  "  align="start" >                    
                <TransitionGroup name="slide-right"  > 
                    <VSheet v-show="!windroseDataLoading" key="1"  class="pa-0 rounded-lg mt-2 overflow-clip"  >                              
                        <figure  class="highcharts-figure highcharts-light">
                            <div id="windrosecontainer"></div> 
                        </figure>                    
                    </VSheet> 
                    <VSheet v-show="windroseDataLoading" key="2"  class="pa-0 size-full flex justify-center align-center"  >
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
    const { liveData, windroseDataLoading } = storeToRefs(AppStore); 
    const chart         = ref(null); // Chart object
    const points         = ref(300); // Specify the quantity of points to be shown on the live graph simultaneously.
    const shift          = ref(false); // Delete a point from the left side and append a new point to the right side of the graph.
    const graphType      = ref("three");
    const params         = ref([]);
    const chartEl        = ref(null);
    const stationName    = ref("");
    const historyLoading = ref(false);
    const getDataToggle  = ref(false);
    const month          = ref([]);
    const threedays      = ref([]);
    const sevendays      = ref([]);

    const selected       = ref({"name":'3 Days', "type":'three'});
    const options        = ref([{"name":'3 Days', "type":'three'},{"name":'7 Days', "type":'seven'},{"name":'1 Month', "type":'month'}]);
    
    let worker           = new Worker("/src/assets/js/mapHistoryDataWorker.js"); 

    let getDataID = ""
 

    
    // FUNCTIONS 


    const getData = async () => { 

        let timestamp = Math.floor(new Date().getTime() / 1000)
        let result    = await AppStore.getWindRoseData(timestamp);
        let name = graphType.value

        if ('data' in result) {
            month.value      = result["data"];  
            threedays.value  = result["three"]; 
            sevendays.value  = result["seven"];            
            
            if(name == "three"){ chart.value.update({series: threedays.value},true) }
            else if (name == "seven"){ chart.value.update({series: sevendays.value},true) }  
            else if(name == "month") { chart.value.update({series: month.value},true) }   

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
        if(name == "three"){ chart.value.update({series: threedays.value},true) }
        else if (name == "seven"){ chart.value.update({series: sevendays.value},true) }  
        else if(name == "month") { chart.value.update({series: month.value},true) }       
    });


    watch(darkmode,(mode)=> {           
       if(mode)
            chartEl.value.forEach(el => { el.classList.replace('highcharts-light','highcharts-dark') });  
       else if (!mode)
            chartEl.value.forEach(el => { el.classList.replace('highcharts-dark','highcharts-light') });         
   });


    const CreateCharts = async () => {  
        // CHART

        chart.value = Highcharts.chart('windrosecontainer', {
            chart: { polar: true, type: 'column', styledMode: true, zoomType: 'xy',height: 500, marginTop: 60 },
            title: { text: '', align: 'center' },
            subtitle: { text: 'Wind Rose', align: 'center' },
            /*
            yAxis: { 
                title:null,// title: { text: 'Wind Speed' , style:{color:'#000000'}},
                labels: { format: '{value} %' },             
                // max:150,
                // min:0        
            },*/
            yAxis: {
                min: 0,
                endOnTick: false,
                showLastLabel: true,
                title: {
                    text: 'Frequency (%)'
                },
                labels: {
                    format: '{value}%'
                },
                reversedStacks: false
            },
                
            xAxis: [{
                tickmarkPlacement: 'on',
                categories: [ 'N', 'NNE', 'NE', 'ENE', 'E', 'ESE', 'SE', 'SSE', 'S', 'SSW', 'SW', 'WSW', 'W', 'WNW', 'NW', 'NNW' ],              
            }],
            legend: {
            align: 'right',
            verticalAlign: 'top',
            y: 100,
            layout: 'vertical'
            },
            navigation: {
                buttonOptions: {
                    verticalAlign: 'top',
                    x: 0
                }
            },  
            pane: { size: '85%' },  

            tooltip: { 
                shared:true, 
                xDateFormat: '%A, %b %e, %I:%M %p',
                valuePrefix: '',
                valueSuffix: ' %' ,
                // pointFormat: "{point.y:.2f}% : {series.name}\n" // "{point.y:.2f} % {series.name}"
            },
            plotOptions: {
                series: {
                    stacking: 'normal',
                    shadow: false,
                    groupPadding: 0,
                    pointPlacement: 'on',                    
                }
            },
            series:[               
                {data:[]},
                {data:[]},
                {data:[]},
                {data:[]},
                {data:[]},
                {data:[]},
              ],
                
            //   series:[ 
            //     {name:"&gt; 10 m/s",data:[]},
            //     {name:"8-10 m/s",data:[]},
            //     {name:"6-8 m/s",data:[]},
            //     {name:"4-6 m/s",data:[]},
            //     {name:"2-4 m/s",data:[]},
            //     {name:"&lt; 2 m/s",data:[]},
            // ]
        });
    }
</script>

    
<style>

</style>