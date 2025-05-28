<template>
    <VContainer align="center" class="fill-height" fluid>
        <VRow class="bg- green fill-height" >
            <VCol class="bg- blue pa-0"    >
                <VSheet color="surface"  class="pa-0"  >                
                    <figure class="highcharts-figure">
                        <div id="container2"></div> 
                    </figure>
                </VSheet>
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
import { storeToRefs } from "pinia";

// Highcharts, Load the exporting module and Initialize exporting module.
import Highcharts from 'highcharts';
import  'highcharts/highcharts-more';
import  'highcharts/modules/exporting';


 
 
// VARIABLES
const router      = useRouter();
const route       = useRoute();  
const AppStore    = useAppStore();
const Mqtt        = useMqttStore();
const {connected, payload, payloadTopic } = storeToRefs(Mqtt);
const tempChart     = ref(null); // Chart object
const points        = ref(6000); // Specify the quantity of points to be shown on the live graph simultaneously.
const shift         = ref(false); // Delete a point from the left side and append a new point to the right side of the graph.


// FUNCTIONS
onMounted(()=>{
    // THIS FUNCTION IS CALLED AFTER THIS COMPONENT HAS BEEN MOUNTED
    CreateCharts(); 
    /*
    // fm.setPercentage(percentage);
    Mqtt.connect(); // Connect to Broker located on the backend
    setTimeout( ()=>{
    // Subscribe to each topic
    Mqtt.subscribe("/references");
    Mqtt.subscribe("/devices");
    },3000);
 */
});


onBeforeUnmount(()=>{
    // THIS FUNCTION IS CALLED RIGHT BEFORE THIS COMPONENT IS UNMOUNTED
    // Mqtt.unsubscribeAll();
});


 // WATCHERS
watch(payload,(data)=> {   
    
    if(points.value > 0)
            points.value --;    
    else
        shift.value = true;    

    if(data.model == "PTB330"){   
        tempChart.value.series[0].addPoint({y:parseFloat(data.pressure.toFixed(2)) ,x: data.timestamp * 1000 }, true, shift.value);   
        }

    if(data.model == "BMP390"){     
        tempChart.value.series[1].addPoint({y:parseFloat(data.pressure.toFixed(2)) ,x: data.timestamp * 1000 }, true, shift.value);   
    }    
});


const CreateCharts = async () => {  
  // TEMPERATURE CHART
  tempChart.value = Highcharts.chart('container2', {
      chart: { zoomType: 'x' },
      title: { text: 'Live Analysis', align: 'left' },
      yAxis: { 
          title: { text: 'Temperature & Humidity' , style:{color:'#000000'}},
          labels: { format: '{value} ' },
          max:1100,
          min:800        
      },
  
      xAxis: {
          type: 'datetime', 
          title: { text: 'Time', style:{color:'#000000'} },        
      },
   
      tooltip: { shared:true, },
  
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
            name: 'PTB330',
            type: 'spline',
            data: [],
            turboThreshold: 0,
            marker:{type:null},
            color: Highcharts.getOptions().colors[0]
        } ,
        {
            name: 'BMP390',
            type: 'spline',
            data: [],
            turboThreshold: 0,
            marker:{type:null},
            color: Highcharts.getOptions().colors[1]
        }  ],
  
  });
  }
</script>


<style scoped>
/** CSS STYLE HERE */


</style>
  