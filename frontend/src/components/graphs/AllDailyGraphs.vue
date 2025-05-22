<template>
    <VContainer align="center" class="h-full" fluid>         
        <VRow class=" fill-height" >
            <VCol cols="12" class="flex align-start justify-end gap-3 pa-0" >
                <Button    severity="primary"    class="dark:!bg-[hsl(0,0%,3%)] !bg-[hsl(0,0%,90%)]  !text-black dark:!text-white !text-small h-[37px]  border" size="small" @click="getDataToggle = !getDataToggle">                  
                    <p class="font-normal text-sm" >Refresh</p>                
                </Button>
            </VCol>

            <VCol cols="12" class="pa-0"  align="start" >    
                <TransitionGroup name="slide-right"  >
                    <VSheet v-show="!loading" key="1"  class="pa-0 rounded-lg mt-5"  >                       
                        <figure  class="highcharts-figure highcharts-light">
                            <div id="adgcontainer" class="rounded-xl overflow-clip"></div> 
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
    import { useUserStore } from '@/stores/userStore'; 
    
    import { storeToRefs } from "pinia";
    import _ from "lodash";

    // Highcharts, Load the exporting module and Initialize exporting module.
    import Highcharts from 'highcharts';
    import 'highcharts/highcharts-more';
    import 'highcharts/modules/exporting';
    
    
    
    
    // VARIABLES
    const router         = useRouter();
    const route          = useRoute();  
    const AppStore       = useAppStore();
    const UserStore      = useUserStore();  
    const { selectedStation, darkmode, layout}  = storeToRefs(UserStore);
    const { liveData } = storeToRefs(AppStore);
    const chart          = ref(null); // Chart object
    const params         = ref([]);
    const chartEl        = ref(null);
    const loading        = ref(false);
    const getDataToggle  = ref(false);
    const rangesData     = ref([]);
    const avgData        = ref([]);

    
    let worker           = new Worker("/src/assets/js/mapHistoryDataWorker.js"); 

    let getDataID = ""

    // PROPS
    const props = defineProps({
        param :{type:String,default:""},
    })

    // FUNCTIONS 
    const getData = async (param) => { 
            
        let start       = Math.floor(new Date().getTime() / 1000);
        let paramList   = []

        params.value.forEach(param => paramList.push(param.name))

        let data  = await AppStore.getMMAData( param,start, loading);

        if ('ranges' in data) { 
            rangesData.value = data['ranges']; 
            avgData.value    = data['avg'];
            
            chart.value.series[0].setData(avgData.value,true,true, false);
            chart.value.series[1].setData(rangesData.value,true,true, false);
            
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
        getData(props.param);
    });


    onBeforeUnmount(()=>{
        // THIS FUNCTION IS CALLED RIGHT BEFORE THIS COMPONENT IS UNMOUNTED
     
    });


 
    // WATCHERS

    watch(getDataToggle,()=> {
        clearTimeout(getDataID);

        getDataID = setTimeout(()=>{
            getData(props.param);
        }, 1000)
    })



    watch(()=> props.param, async(param) => {         
        setChartParams(param)
    })


    watch(darkmode,(mode)=> {           
       if(mode)
            chartEl.value.forEach(el => { el.classList.replace('highcharts-light','highcharts-dark') });  
       else if (!mode)
            chartEl.value.forEach(el => { el.classList.replace('highcharts-dark','highcharts-light') });         
   });


    const CreateCharts = async () => {  
       
        chart.value = Highcharts.chart('adgcontainer', {
            chart: {  styledMode: true },
            title: { text: '' },
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
                // valueSuffix: '°C'
            },
            /*
            tooltip: {
                headerFormat: '<span style="font-size:11px">{series.name}</span><br>',
                pointFormat: '<span style="color:{point.color}">{point.name}</span>: ' + '<b>{point.y:.2f}°C</b><br/>'
            },*/
            series: [
                {
                    name: '',
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
                    color: { linearGradient: { x1: 0, x2: 0, y1: 0, y2: 1 }, stops: [ [0, '#ff0000'], [1, '#0000ff'] ] },
                    fillOpacity: 0.3,
                    zIndex: 0,
                    marker: {
                        enabled: false
                    },
                }
                ]
                   
        });
    }

    const setChartParams = (param) => {
        if(param == "temperature"){            
            chart.value.series[0].setData([]);
            chart.value.update({series:{type: "spline", name: _.capitalize(props.param)}, title: { text: 'Temperature (Daily)', align: 'center' }, yAxis: {max:40, min: 15, labels: { format: '{value} °C' } }, tooltip: { valueSuffix: ' °C' }});
            chart.value.showLoading();
            getData(param); 
            chart.value.hideLoading();
        }        

        else if(param == "humidity"){
            chart.value.series[0].setData([]);
            chart.value.update({series:{type: "spline", name: _.capitalize(props.param)}, title: { text: 'Humidity (Daily)', align: 'center' }, yAxis: {max:100, min: 0, labels: { format: '{value} %' } },tooltip: { valueSuffix: ' %' }}); 

            chart.value.showLoading();
            getData(param); 
            chart.value.hideLoading();
        }

        else if(param == "pressure"){            
            chart.value.series[0].setData([]);
            chart.value.update({series:{type: "spline", name: _.capitalize(props.param)}, title: { text: 'Pressure (Daily)', align: 'center' }, yAxis: {max:1100, min: 900, labels: { format: '{value} hPa' } },tooltip: { valueSuffix: ' hPa' }}) 

            chart.value.showLoading();
            getData(param); 
            chart.value.hideLoading();
        }

        else if(param == "radiation"){
            chart.value.series[0].setData([]);
            chart.value.update({series:{type: "spline", name: _.capitalize(props.param)}, title: { text: 'Radiation (Daily)', align: 'center' }, yAxis: {max:100, min: 0,   labels: { format: '{value} W/m2' } },tooltip: { valueSuffix: ' W/m2' }}) 

            chart.value.showLoading();
            getData(param); 
            chart.value.hideLoading();
        }
        
        else if(param == "uva"){
            chart.value.series[0].setData([]);
            chart.value.update({series:{type: "spline", name: _.capitalize(props.param)}, title: { text: 'UVA (Daily)', align: 'center' }, yAxis: {max:100, min: 0,   labels: { format: '{value} W/m2' } },tooltip: { valueSuffix: ' W/m2' }}); 
             chart.value.showLoading();
            getData(param); 
            chart.value.hideLoading();
        }
                
        else if(param == "uvb"){
            chart.value.series[0].setData([]);
            chart.value.update({series:{type: "spline", name: _.capitalize(props.param)}, title: { text: 'UVB (Daily)', align: 'center' }, yAxis: {max:100, min: 0,   labels: { format: '{value} W/m2' } },tooltip: { valueSuffix: ' W/m2' }}); 

            chart.value.showLoading();
            getData(param); 
            chart.value.hideLoading();
        }
                
        else if(param == "uvc"){
            chart.value.series[0].setData([]);
            chart.value.update({series:{type: "spline", name: _.capitalize(props.param)}, title: { text: 'UVC (Daily)', align: 'center' }, yAxis: {max:100, min: 0,   labels: { format: '{value} W/m2' } },tooltip: { valueSuffix: ' W/m2' }}); 

            chart.value.showLoading();
            getData(param); 
            chart.value.hideLoading();
        }
                
        else if(param == "co2"){
            chart.value.series[0].setData([]);
            chart.value.update({series:{type: "spline", name: _.capitalize(props.param)}, title: { text: 'CO2 (Daily)', align: 'center' }, yAxis: {max:5500, min: 0,   labels: { format: '{value} ppm' } },tooltip: { valueSuffix: ' ppm' }}); 

            chart.value.showLoading();
            getData(param); 
            chart.value.hideLoading();
        }

        else if(param == "rainfall"){
            chart.value.series[0].setData([]);
            chart.value.update({series:{type: "spline", name: _.capitalize(props.param)}, title: { text: 'Rainfall (Daily)', align: 'center' }, yAxis: {max:60, min: 0,   labels: { format: '{value} mm' } },tooltip: { valueSuffix: ' mm' }});

            chart.value.showLoading();
            getData(param); 
            chart.value.hideLoading(); 
        }

        else if(param == "winddirection"){
            chart.value.series[0].setData([]);
            chart.value.update({series:{type: "spline", name: _.capitalize(props.param)}, title: { text: 'Wind Direction (Daily)', align: 'center' }, yAxis: {max:360, min: 0, labels: { format: '{value} °' } },tooltip: { valueSuffix: ' °' }});

            chart.value.showLoading();
            getData(param); 
            chart.value.hideLoading(); 
        }

        else if(param == "windspeed"){
            chart.value.series[0].setData([]);
            chart.value.update({series:{type: "spline", name: _.capitalize(props.param)}, title: { text: 'Wind Speed (Daily)', align: 'center' }, yAxis: {max:100, min: 0, labels: { format: '{value} m/s' } },tooltip: { valueSuffix: ' m/s' }});

            chart.value.showLoading();
            getData(param); 
            chart.value.hideLoading(); 
        }

        else if(param == "bat"){
            chart.value.series[0].setData([]);
            chart.value.update({series:{type: "spline", name: _.capitalize(props.param)}, title: { text: 'Battery (Daily)', align: 'center' }, yAxis: {max:100, min: 0, labels: { format: '{value} %' } },tooltip: { valueSuffix: ' %' }});

            chart.value.showLoading();
            getData(param); 
            chart.value.hideLoading(); 
        }

        else if(param == "voltage"){
            chart.value.series[0].setData([]);
            chart.value.update({series:{type: "spline", name: _.capitalize(props.param)}, title: { text: 'Voltage (Daily)', align: 'center' }, yAxis: {max:4.2, min: 0, labels: { format: '{value} V' } },tooltip: { valueSuffix: ' V' }});

            chart.value.showLoading();
            getData(param); 
            chart.value.hideLoading(); 
        }
    }
    
</script>


<style>

</style>