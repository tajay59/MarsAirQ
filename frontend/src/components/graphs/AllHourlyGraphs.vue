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
                    <VSheet v-show="!loading" key="1"  class="pa-0 rounded-lg mt-5"  >                       
                        <figure  class="highcharts-figure highcharts-light">
                            <div id="ahgcontainer" class="rounded-xl overflow-clip"></div> 
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
    import  'highcharts/modules/drilldown'
    import  'highcharts/highcharts-more';
    import  'highcharts/modules/exporting';
   
  
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
    const maxData        = ref({});
    const minData        = ref({});
    const avgData        = ref({});
    const getDataToggle  = ref(false);
    const graphType      = ref("max");

    const selected       = ref({"name":'Max', "type":'max'});
    const options        = ref([{"name":'Max', "type":'max'},{"name":'Min', "type":'min'},{"name":'Avg', "type":'mean'}]);
    const units          = ref({"temperature":" °C","humidity":" %","pressure":" hPa", "radiation":" W/m2", "uva":" W/m2", "uvb":" W/m2", "uvc":" W/m2","co2":" ppm", "rainfall": " mm", "windspeed": " m/s","winddirection":" *","bat": " %", "voltage": " V"})

    
    let worker           = new Worker("/src/assets/js/mapHistoryDataWorker.js"); 

    let getDataID = ""

    // PROPS
    const props = defineProps({
        param :{type:String,default:""},
    })

    // FUNCTIONS
  
    const getData = async () => { 
             
        let start       = Math.floor(new Date().getTime() / 1000);
            let paramList   = []

            params.value.forEach(param => paramList.push(param.name))

            let result  = await AppStore.getColumnDrilldownData( props.param,start, loading); 

            if ('data' in result) {
                let data      = result["data"];  
                data['max']['drilldown'].forEach(row => row['tooltip']  = {pointFormat: `<span style="color:{point.color}"><b>{point.y:.2f} ${units.value[props.param]}</b></span><br/> <span>{point.x:%I:%M %p}</span>`})
                data['min']['drilldown'].forEach(row => row['tooltip']  = {pointFormat: `<span style="color:{point.color}"><b>{point.y:.2f} ${units.value[props.param]}</b></span><br/> <span>{point.x:%I:%M %p}</span>`})
                data['mean']['drilldown'].forEach(row => row['tooltip'] = {pointFormat: `<span style="color:{point.color}"><b>{point.y:.2f} ${units.value[props.param]}</b></span><br/> <span>{point.x:%I:%M %p}</span>`})

                maxData.value = {...data['max']};
                minData.value = {...data['min']};
                avgData.value = {...data['mean']};

            
                let name = graphType.value
        
                if(name == "max"){                   
                    chart.value.update({title:{ text: `Max ${_.capitalize(props.param)}`},series: maxData.value['series'],drilldown: {series: maxData.value["drilldown"]}}, true); 
                }    
                else if (name == "min"){
                    chart.value.update({title:{ text: `Min ${_.capitalize(props.param)}`},series: minData.value['series'],drilldown: {series: minData.value["drilldown"]}}, true); 
                }  
                else if(name == "mean") {
                    chart.value.update({title:{ text: `Mean ${_.capitalize(props.param)}`},series: avgData.value['series'],drilldown: {series: avgData.value["drilldown"]}}, true); 
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
        setChartParams(props.param);
        
        getData(props.param);
      
    });


    onBeforeUnmount(()=>{
        // THIS FUNCTION IS CALLED RIGHT BEFORE THIS COMPONENT IS UNMOUNTED
     
    });


 
    // WATCHERS
    watch(graphType,(name) => {       
        chart.value.drillUp();

       setTimeout(()=> {
        if(name == "max"){           
            chart.value.update({title:{ text: `Max ${_.capitalize(props.param)}`},series: maxData.value['series'],drilldown: {series: maxData.value["drilldown"]}}, true); 
        }    
        else if (name == "min"){
            chart.value.update({title:{ text: `Min ${_.capitalize(props.param)}`},series: minData.value['series'],drilldown: {series: minData.value["drilldown"]}}, true); 
        }  
        else if(name == "mean")    {
            chart.value.update({title:{ text: `Mean ${_.capitalize(props.param)}`},series: avgData.value['series'],drilldown: {series: avgData.value["drilldown"]}}, true); 
        }   
       },500) 
    });

    watch(getDataToggle,()=> {
        clearTimeout(getDataID);

        getDataID = setTimeout(()=>{
            getData(props.param);
        }, 1000)
    })

    

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
       
        chart.value = Highcharts.chart('ahgcontainer', {
            chart: { type: 'column', styledMode: true },
            title: { text: '' },
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
                        format: '{point.y:.2f} '
                    }
                },            
                
            },

            tooltip: {
                headerFormat: '<span style="font-size:11px">{series.name}</span><br>'
                // pointFormat: '<span style="color:{point.color}">{point.name}</span>: ' + '<b>{point.y:.2f} </b><br/>'
            },
            series: [{}],
            drilldown: {
                activeDataLabelStyle: { textDecoration: 'none', cursor: "pointer" },
                
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

    const setChartParams = (param) => {
        if(param == "temperature"){            
            chart.value.series[0].setData([]);
            chart.value.update({ title: { text: 'Temperature (Daily)', align: 'center' }, yAxis: {max:40, min: 15, labels: { format: '{value} °C' } },tooltip: { pointFormat: `<span style="color:{point.color}">{point.name}</span>:  <b>{point.y:.2f} °C</b><br/>` }, plotOptions: { series: { dataLabels: {  format: '{point.y:.2f} °C' } } }});
            chart.value.showLoading();
            getData(param); 
            chart.value.hideLoading();
        }        

        else if(param == "humidity"){
            chart.value.series[0].setData([]);
            chart.value.update({ title: { text: 'Humidity (Daily)', align: 'center' }, yAxis: {max:100, min: 0, labels: { format: '{value} %' } },tooltip: { pointFormat: `<span style="color:{point.color}">{point.name}</span>:  <b>{point.y:.2f} %</b><br/>` }, plotOptions: { series: { dataLabels: {  format: '{point.y:.2f} %' } } }}); 

            chart.value.showLoading();
            getData(param); 
            chart.value.hideLoading();
        }

        else if(param == "pressure"){            
            chart.value.series[0].setData([]);
            chart.value.update({ title: { text: 'Pressure (Daily)', align: 'center' }, yAxis: {max:1100, min: 900, labels: { format: '{value} hPa' } },tooltip: { pointFormat: `<span style="color:{point.color}">{point.name}</span>:  <b>{point.y:.2f} hPa</b><br/>` }, plotOptions: { series: { dataLabels: {  format: '{point.y:.2f} hPa' } } }}) 

            chart.value.showLoading();
            getData(param); 
            chart.value.hideLoading();
        }

        else if(param == "radiation"){
            chart.value.series[0].setData([]);
            chart.value.update({ title: { text: 'Radiation (Daily)', align: 'center' }, yAxis: {max:100, min: 0,   labels: { format: '{value} W/m2' } },tooltip: { pointFormat: `<span style="color:{point.color}">{point.name}</span>:  <b>{point.y:.2f} W/m2</b><br/>` },plotOptions: { series: { dataLabels: {  format: '{point.y:.2f} W/m2' } } }}) 

            chart.value.showLoading();
            getData(param); 
            chart.value.hideLoading();
        }
        
        else if(param == "uva"){
            chart.value.series[0].setData([]);
            chart.value.update({ title: { text: 'UVA (Daily)', align: 'center' }, yAxis: {max:100, min: 0,   labels: { format: '{value} W/m2' } },tooltip: { pointFormat: `<span style="color:{point.color}">{point.name}</span>:  <b>{point.y:.2f} W/m2</b><br/>` },plotOptions: { series: { dataLabels: {  format: '{point.y:.2f} W/m2' } } }}); 
             chart.value.showLoading();
            getData(param); 
            chart.value.hideLoading();
        }
                
        else if(param == "uvb"){
            chart.value.series[0].setData([]);
            chart.value.update({ title: { text: 'UVB (Daily)', align: 'center' }, yAxis: {max:100, min: 0,   labels: { format: '{value} W/m2' } },tooltip: { pointFormat: `<span style="color:{point.color}">{point.name}</span>:  <b>{point.y:.2f} W/m2</b><br/>` },plotOptions: { series: { dataLabels: {  format: '{point.y:.2f} W/m2' } } }}); 

            chart.value.showLoading();
            getData(param); 
            chart.value.hideLoading();
        }
                
        else if(param == "uvc"){
            chart.value.series[0].setData([]);
            chart.value.update({ title: { text: 'UVC (Daily)', align: 'center' }, yAxis: {max:100, min: 0,   labels: { format: '{value} W/m2' } },tooltip: { pointFormat: `<span style="color:{point.color}">{point.name}</span>:  <b>{point.y:.2f} W/m2</b><br/>` },plotOptions: { series: { dataLabels: {  format: '{point.y:.2f} W/m2' } } }}); 

            chart.value.showLoading();
            getData(param); 
            chart.value.hideLoading();
        }
                
        else if(param == "co2"){
            chart.value.series[0].setData([]);
            chart.value.update({ title: { text: 'CO2 (Daily)', align: 'center' }, yAxis: {max:5500, min: 0,   labels: { format: '{value} ppm' } },tooltip: { pointFormat: `<span style="color:{point.color}">{point.name}</span>:  <b>{point.y:.2f} ppm</b><br/>` },plotOptions: { series: { dataLabels: {  format: '{point.y:.2f} ppm' } } }}); 

            chart.value.showLoading();
            getData(param); 
            chart.value.hideLoading();
        }

        else if(param == "rainfall"){
            chart.value.series[0].setData([]);
            chart.value.update({ title: { text: 'Rainfall (Daily)', align: 'center' }, yAxis: {max:60, min: 0,   labels: { format: '{value} mm' } },tooltip: { pointFormat: `<span style="color:{point.color}">{point.name}</span>:  <b>{point.y:.2f} mm</b><br/>` },plotOptions: { series: { dataLabels: {  format: '{point.y:.2f} mm' } } }});

            chart.value.showLoading();
            getData(param); 
            chart.value.hideLoading(); 
        }

        else if(param == "winddirection"){
            chart.value.series[0].setData([]);
            chart.value.update({ title: { text: 'Wind Direction (Daily)', align: 'center' }, yAxis: {max:360, min: 0, labels: { format: '{value} °' } },tooltip: { pointFormat: `<span style="color:{point.color}">{point.name}</span>:  <b>{point.y:.2f} °</b><br/>` },plotOptions: { series: { dataLabels: {  format: '{point.y:.2f} °' } } }});

            chart.value.showLoading();
            getData(param); 
            chart.value.hideLoading(); 
        }

        else if(param == "windspeed"){
            chart.value.series[0].setData([]);
            chart.value.update({ title: { text: 'Wind Speed (Daily)', align: 'center' }, yAxis: {max:100, min: 0, labels: { format: '{value} m/s' } },tooltip: { pointFormat: `<span style="color:{point.color}">{point.name}</span>:  <b>{point.y:.2f} m/s</b><br/>` },plotOptions: { series: { dataLabels: {  format: '{point.y:.2f} m/s' } } }});

            chart.value.showLoading();
            getData(param); 
            chart.value.hideLoading(); 
        }

        else if(param == "bat"){
            chart.value.series[0].setData([]);
            chart.value.update({ title: { text: 'Battery (Daily)', align: 'center' }, yAxis: {max:100, min: 0, labels: { format: '{value} %' } },tooltip: { pointFormat: `<span style="color:{point.color}">{point.name}</span>:  <b>{point.y:.2f} %</b><br/>` },plotOptions: { series: { dataLabels: {  format: '{point.y:.2f} %' } } }});

            chart.value.showLoading();
            getData(param); 
            chart.value.hideLoading(); 
        }

        else if(param == "voltage"){
            chart.value.series[0].setData([]);
            chart.value.update({ title: { text: 'Voltage (Daily)', align: 'center' }, yAxis: {max:4.2, min: 0, labels: { format: '{value} V' } },tooltip: { pointFormat: `<span style="color:{point.color}">{point.name}</span>:  <b>{point.y:.2f} V</b><br/>` },plotOptions: { series: { dataLabels: {  format: '{point.y:.2f} W/m2' } } }});

            chart.value.showLoading();
            getData(param); 
            chart.value.hideLoading(); 
        }
    }
</script>


<style>

</style>