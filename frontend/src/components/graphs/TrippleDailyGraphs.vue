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
                            <div id="tripplecontainer" class="rounded-xl overflow-clip"></div> 
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
    const { liveData, paramDetails } = storeToRefs(AppStore);
    const chart          = ref(null); // Chart object
    const params         = ref([]);
    const chartEl        = ref(null);
    const loading        = ref(false);
    const getDataToggle  = ref(false);
    const dataset        = ref({});
    

    
    let worker           = new Worker("/src/assets/js/mapHistoryDataWorker.js"); 

    let getDataID = ""

    // PROPS
    const props = defineProps({
        params :{type:Array, default:[]},
    })

    // FUNCTIONS 
    /*
    const getData = async (param) => { 
            
        let start       = Math.floor(new Date().getTime() / 1000);
        let paramList   = []

        params.value.forEach(param => paramList.push(param.name))

        let data  = await AppStore.getMMAData( param,start, loading);

        if ('ranges' in data) { 
            rangesData.value = data['ranges']; 
            avgData.value   = data['avg'];

 
            
            chart.value.series[0].setData(avgData.value,true,true, false);
            chart.value.series[1].setData(rangesData.value,true,true, false);
            
                }
            }
        */

    const getData = async (params) => { 
        let start     = new Date();
        start.setDate(start.getDate()-14);
        start = Math.floor(start /1000);
        let end       = Math.floor(new Date().getTime() / 1000);
        
         
        let result  = await AppStore.getDailyMultiData( params,start,end, loading);

        if ('data' in result) {
            let data  = result["data"];  

            let paramsList = Object.keys(data[0])
            if(paramsList.length > 3){
                // let params = paramsList.filter( param => param != 'timestamp');
                // console.log(params);
                dataset.value[params[0]] = [];
                dataset.value[params[1]] = [];
                dataset.value[params[2]] = [];

                data.forEach(row => {    
                    dataset.value[params[0]].push({"x": row['timestamp'], "y": row[params[0]]});   
                    dataset.value[params[1]].push({"x": row['timestamp'], "y": row[params[1]]});   
                    dataset.value[params[2]].push({"x": row['timestamp'], "y": row[params[2]]});   
                });  

        
                chart.value.series[0].setData(dataset.value[params[0]],true,true, true);
                chart.value.series[1].setData(dataset.value[params[1]],true,true, true);
                chart.value.series[2].setData(dataset.value[params[2]],true,true, true);
             
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
        setChartParams(props.params)
        getData(props.params);
    });


    onBeforeUnmount(()=>{
        // THIS FUNCTION IS CALLED RIGHT BEFORE THIS COMPONENT IS UNMOUNTED
     
    });


 
    // WATCHERS

    watch(getDataToggle,()=> {
        clearTimeout(getDataID);

        getDataID = setTimeout(()=>{
            getData(props.params);
        }, 1000)
    })



    // watch(()=> props.param, async(param) => {         
    //     setChartParams(param)
    // })


    watch(darkmode,(mode)=> {           
       if(mode)
            chartEl.value.forEach(el => { el.classList.replace('highcharts-light','highcharts-dark') });  
       else if (!mode)
            chartEl.value.forEach(el => { el.classList.replace('highcharts-dark','highcharts-light') });         
   });


    const CreateCharts = async () => {
        chart.value = Highcharts.chart('tripplecontainer', {
            chart: { styledMode: true, zooming: { type: 'xy' } },
            title: { text: 'Average Daily Weather Data' },
            subtitle: { text: 'Last 14 Days' },
            xAxis: {type: 'datetime', labels: { format: '{value:%a, %b %d}' } ,crosshair: true },// // type: 'category'
            
            yAxis: [
                { // Primary yAxis
                labels: { format: '{value} ', style: { color: Highcharts.getOptions().colors[2] } },
                title: { text: '', style: { color: Highcharts.getOptions().colors[2] } },
                opposite: true

            }, { // Secondary yAxis
                gridLineWidth: 0,
                title: { text: '', style: { color: Highcharts.getOptions().colors[0] } },
                labels: { format: '{value} ', style: { color: Highcharts.getOptions().colors[0] } }

            }, { // Tertiary yAxis
                gridLineWidth: 0,
                title: { text: '', style: { color: Highcharts.getOptions().colors[1] } },
                labels: { format: '{value} ', style: { color: Highcharts.getOptions().colors[1] } },
                opposite: true
            }],
            tooltip: {
                shared: true
            },
            legend: { 
                backgroundColor:
                    Highcharts.defaultOptions.legend.backgroundColor || // theme
                    'rgba(255,255,255,0.25)'
            },
            series: [
            {
                name: '',
                type: 'spline',
                yAxis: 0,
                data: [],
                tooltip: { valueSuffix: ' ' }
            },
                {
                name: '',
                type: 'column',
                yAxis: 1,
                data: [],
                tooltip: { valueSuffix: ' ' }
            }, {
                name: '',
                type: 'spline',
                yAxis: 2,
                data: [],
                marker: { enabled: false },
                dashStyle: 'shortdot',
                tooltip: { valueSuffix: ' ' }

            }],
            responsive: {
                rules: [{
                    condition: {
                        maxWidth: 500
                    },
                    chartOptions: {
                        legend: true,
                        yAxis: [{
                            labels: {
                                align: 'right',
                                x: 0,
                                y: -6
                            },
                            showLastLabel: false
                        }, {
                            labels: {
                                align: 'left',
                                x: 0,
                                y: -6
                            },
                            showLastLabel: false
                        }, {
                            visible: false
                        }]
                    }
                }]
            }
        });
    }

    /*
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
    }*/

    const setChartParams = (params) => {
        let plottypes = ['spline','column','spline']
        let series = []
        let yAxis  = [] 

        params.forEach((param, index) => { 
            series.push({
                name: _.capitalize(param),
                type: plottypes[params.indexOf(param)],
                yAxis: params.indexOf(param),
                data: [],
                tooltip: { valueSuffix: ` ${paramDetails.value[param].units}` }
            })

            yAxis.push(
                { 
                labels: { format: `{value} ${paramDetails.value[param].units}`, style: { color: Highcharts.getOptions().colors[2] } },
                title: { text: _.capitalize(param), style: { color: Highcharts.getOptions().colors[2] } },
                opposite: (index == 1)? false : true
            }
            )
        }) 
        
        chart.value.update({series: series, yAxis: yAxis}, true)
   
      
    }
    
</script>


<style>

</style>