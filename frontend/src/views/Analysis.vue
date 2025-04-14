<template>
    <VContainer align="center" fluid>
        <VRow style="max-width: 1200px;" class="mb-5"  >
       
             <VCard border rounded="md"  density="compact" width="300" >
                <template #subtitle>
                <span class="text-2xl font-light " >Date Range</span>
                </template>

                <VCardItem class="pa-0" >
                    
                    <FloatLabel variant="on" class="ma-2" >
                        <DatePicker id="datepicker-24h"  v-model="start" inputId="on_label" :showOnFocus="true" showIcon  showTime hourFormat="24" variant="filled" size="small"  fluid />
                        <label for="on_label">Start</label>
                    </FloatLabel>

                    <FloatLabel variant="on" class="ma-2" >
                        <DatePicker id="datepicker-24h" v-model="end" inputId="on_label" :showOnFocus="true" showIcon  showTime hourFormat="24" variant="filled" size="small"  fluid />                    
                        <label for="on_label"   >End</label>
                    </FloatLabel>
                </VCardItem>

             </VCard>
         
             <VCard border rounded="md" density="compact" class="ml-5" >
                <template #subtitle>
                <span class="text-2xl font-light" >Parameter</span>
                </template>

                <VCardItem  class="pa-0" > 
                    <Select v-model="params.parameter" :options="params.options" optionLabel="name" placeholder="Parameter"  variant="filled" class="w-full md:w-56 ma-2" />
                </VCardItem>

             </VCard>
             <Button label="Plot" class="bg-amber-500 dark:bg-sky-500 pa-2 ml-3" @click="updateLineCharts" />
           
            
                <VSpacer />
                <VBtn text="Analyze" class="text-caption" @click="updateLineCharts"></VBtn>
           
        </VRow>
        <VRow  class=" fill-height pa-0 mt-14" >
            <VCol cols="12" class="pa-0" >
                <VCard flat border >
                    <figure  class="highcharts-figure  ">
                        <div id="container3" ></div>
                    </figure>
                </VCard>
            </VCol>
        </VRow>
  
    </VContainer>
     
</template>

<script setup>
/** JAVASCRIPT HERE */

// IMPORTS
import { ref,reactive,watch ,onMounted,onBeforeUnmount,computed } from "vue";  
import { useRoute ,useRouter } from "vue-router";
import { storeToRefs } from 'pinia';
import { useAppStore } from '@/stores/appStore';
 
// Highcharts, Load the exporting module and Initialize exporting module.
import Highcharts from 'highcharts';
import more from 'highcharts/highcharts-more';
import Exporting from 'highcharts/modules/exporting';
import Accessibility from 'highcharts/modules/accessibility'
Exporting(Highcharts); 
more(Highcharts);
Accessibility(Highcharts);

// VARIABLES
const router      = useRouter();
const route       = useRoute();  
const start       = ref("");
const end         = ref("");
const average     = ref(0);
const tempChart  = ref(null); // Chart object
const humidChart  = ref(null); // Chart object
const AppStore    = useAppStore(); 
const {appDarkMode} = storeToRefs(AppStore);
const params      = reactive({parameter: {}, options: [{name: "Temperature", param:"temperature"}, {name: "Humidity", param:"humidity"}, {name: "Pressure", param:"pressure"}]});

   // Define the light theme
   const lightTheme = {
        chart: {
            backgroundColor: '#FFFFFF',
            style: { fontFamily: 'Arial, sans-serif' },
            styledMode: true
        },
        title: {
            style: { color: '#000000' }
        },
        xAxis: {
            gridLineColor: '#DDDDDD',
            labels: {
                style: { color: '#000000' }
            }
        },
        yAxis: {
            gridLineColor: '#DDDDDD',
            labels: {
                style: { color: '#000000' }
            }
        },
        series: [{
            color: '#1E90FF'
        }]
    };

    // Define the dark theme
    const darkTheme = {
        chart: {
            backgroundColor: '#2C2C2C',
            style: { fontFamily: 'Arial, sans-serif' },
            styledMode: true
        },
        title: {
            style: { color: '#FFFFFF' }
        },
        xAxis: {
            gridLineColor: '#444444',
            labels: {
                style: { color: '#FFFFFF' }
            }
        },
        yAxis: {
            gridLineColor: '#444444',
            labels: {
                style: { color: '#FFFFFF' }
            }
        },
        series: [{
            color: '#FF6347'
        }]
    };


// WATCHERS

watch(()=> params.parameter.param,(param)=>{
    if(param == "temperature")
        createTemperatureChart()
    else if(param == "humidity")
        createHumidityChart();
})


watch(appDarkMode ,(darkmode)=>{
  
    console.log("APP MODE", darkmode)

    if (darkmode) {
        // Apply dark theme
        Highcharts.setOptions(darkTheme);
        tempChart.value.update(darkTheme);
    } else {
        // Apply light theme
        Highcharts.setOptions(lightTheme);
        tempChart.value.update(lightTheme);
    }

    // Re-render the chart after applying new theme
   
})


// FUNCTIONS
onMounted(()=>{
    // THIS FUNCTION IS CALLED AFTER THIS COMPONENT HAS BEEN MOUNTED
    // CreateCharts();
});


onBeforeUnmount(()=>{
    // THIS FUNCTION IS CALLED RIGHT BEFORE THIS COMPONENT IS UNMOUNTED
});



const createTemperatureChart = () => {
    tempChart.value = Highcharts.chart('container3', {
    chart: { zoomType: 'xy', styledMode: false },
    title: { text: 'Temperature Analysis', align: 'left' },
    yAxis: { 
        title: { text: '°C' , style:{color:'#000000'}},
        labels: { format: '{value} °C' }        
    },

    xAxis: {
        type: 'datetime', 
        title: { text: 'Time', style:{color:'#000000'} },
    },
 
    tooltip: { shared:true, },

    series: [ ],

});

if (appDarkMode.value)  
    tempChart.value.update(darkTheme);   
else  
    tempChart.value.update(lightTheme);
    
}

const createHumidityChart = () => {
    tempChart.value = Highcharts.chart('container3', {
    chart: { zoomType: 'xy',styledMode: false },
    title: { text: 'Humidity Analysis', align: 'left' },
    yAxis: { 
        title: { text: '%' , style:{color:'#000000'}},
        labels: { format: '{value} %' }        
    },

    xAxis: {
        type: 'datetime', 
        title: { text: 'Time', style:{color:'#000000'} },
    },

    yAxis: { 
        title: { text: 'Humidity', style:{color:'#000000'} },
        labels:{ format: '{value} %'}
    },
 
    tooltip: { shared:true, pointFormat: 'Humidity: {point.y} %' },

    series: [
        {
          name: 'Humidity',
          type: 'area',
          data: [],
          turboThreshold: 0,
          color: Highcharts.getOptions().colors[1]
      }  ],

});

if (appDarkMode.value)  
    tempChart.value.update(darkTheme);   
else  
    tempChart.value.update(lightTheme);
}
 
const CreateCharts = async () => {
  
// TEMPERATURE CHART
tempChart.value = Highcharts.chart('container3', {
    chart: { zoomType: 'xy' },
    title: { text: 'Temperature Analysis', align: 'left' },
    yAxis: { 
        title: { text: '°C' , style:{color:'#000000'}},
        labels: { format: '{value} °C' }        
    },

    xAxis: {
        type: 'datetime', 
        title: { text: 'Time', style:{color:'#000000'} },
    },
 
    tooltip: { shared:true, },

    series: [ ],

});

humidChart.value = Highcharts.chart('container3', {
    chart: { zoomType: 'xy' },
    title: { text: 'Humidity Analysis', align: 'left' },
    yAxis: { 
        title: { text: '%' , style:{color:'#000000'}},
        labels: { format: '{value} %' }        
    },

    xAxis: {
        type: 'datetime', 
        title: { text: 'Time', style:{color:'#000000'} },
    },

    yAxis: { 
        title: { text: 'Humidity', style:{color:'#000000'} },
        labels:{ format: '{value} %'}
    },
 
    tooltip: { shared:true, pointFormat: 'Humidity: {point.y} %' },

    series: [
        {
          name: 'Humidity',
          type: 'area',
          data: [],
          turboThreshold: 0,
          color: Highcharts.getOptions().colors[1]
      }  ],

});
};

const updateLineCharts = async ()=>{
   
    if(!!start.value && !!end.value){        
        console.log("SENDING");
        // Convert output from Textfield components to 10 digit timestamps
        let startDate = new Date(start.value).getTime() / 1000;
        let endDate   = new Date(end.value).getTime() / 1000; 

        // Fetch data from backend
        const data = await AppStore.getCollocationData(startDate,endDate, params.parameter.param);         

        data.forEach( variable => {
            let points = [];
            let name = variable["_id"];
            let values =  variable["values"];

            values.forEach(row => {
                points.push({"x": row.timestamp * 1000, "y": parseFloat(row[params.parameter.param].toFixed(2))  });  
                });
            
            tempChart.value.addSeries({
                name: name,
                type: 'spline',
                data: points,
                turboThreshold: 0,
                marker:{ enabled: false, states: { hover: { enabled: true } }},
                color: Highcharts.getOptions().colors[0]            
            });            
        });
 
    }
}

</script>


<style scoped>
/** CSS STYLE HERE */
/* @import "https://code.highcharts.com/dashboards/css/dashboards.css"; */
Figure {
  /* border: 2px solid black; */
}


</style>
  