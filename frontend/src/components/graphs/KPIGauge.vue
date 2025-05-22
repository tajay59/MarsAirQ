<template> 
    <figure  class=" highcharts-figure highcharts-light relative" :style="[`width: ${props.width}px; height:${aspectRatio * 100}%`]" >   
        <Icon icon="tdesign:letters-a" width="16" height="16"  class="absolute top-[32px]  right-[calc(50%-10px)] z-[2]" ></Icon>
        <Icon icon="tdesign:letters-b" width="16" height="16"  class="absolute top-[49px]  right-[calc(50%-10px)] z-[2]" ></Icon>
        <Icon icon="tdesign:letters-c" width="16" height="16"  class="absolute top-[66px]  right-[calc(50%-10px)] z-[2]" ></Icon>

        <VBtn v-if="props.displaymode" title="Add to Dashboard" size="45" icon class="z-[1] text-none text-xs absolute top-3 right-3    !text-neutral-200 dark:!text-neutral-900 font-semibold" color="transparent"   @click="$emit('add')"  variant="flat" >
            <Icon icon="basil:add-solid" class="!text-neutral-600 dark:!text-neutral-400" width="40" height="40"  />
        </VBtn>
        <VBtn v-else icon class="z-[20]  absolute top-1 right-1  !size-[40px]" title="Delete" color="transparent" @click="emit('delete')"  density="compact" variant="text" >
             <svg  width="24" height="24" viewBox="0 0 24 24" class="!text-neutral-600 dark:!text-neutral-400"><path fill="currentColor" d="M6 19c0 1.1.9 2 2 2h8c1.1 0 2-.9 2-2V7H6zM19 4h-3.5l-1-1h-5l-1 1H5v2h14z"/></svg>
        </VBtn>  
        
        <div :id="graphcontainer"  >  </div> 

    </figure>  
      
</template>
    
<script setup>
    /** JAVASCRIPT HERE */

    // IMPORTS
    import { ref,reactive,watch ,onMounted,onBeforeUnmount,computed } from "vue";  
    import { useRoute ,useRouter } from "vue-router";
    import { useAppStore } from '@/stores/appStore';
    import { useMqttStore } from '@/stores/mqttStore'; // Import Mqtt Store
    import { useUserStore } from '@/stores/userStore'; 
    import { Icon } from "@iconify/vue";
    
    import { storeToRefs } from "pinia";
    import _ from "lodash";

    // Highcharts, Load the exporting module and Initialize exporting module.
    import  Highcharts from 'highcharts';
    import  'highcharts/highcharts-more';
    import  'highcharts/modules/exporting';
    import  'highcharts/modules/solid-gauge';
    import  'highcharts/modules/accessibility';
 
    
    
    
    
    // VARIABLES
    const router         = useRouter();
    const route          = useRoute();  
    const AppStore       = useAppStore();
    const UserStore      = useUserStore(); 
    const Mqtt           = useMqttStore();
    const { connected, payload, payloadTopic } = storeToRefs(Mqtt);
    const { selectedStation, darkmode, layout}  = storeToRefs(UserStore);
    const { liveData, paramDetails } = storeToRefs(AppStore);
    const chart          = ref(null); // Chart object
    const points         = ref(300); // Specify the quantity of points to be shown on the live graph simultaneously.
    const shift          = ref(false); // Delete a point from the left side and append a new point to the right side of the graph. 
    const params         = ref([]);
    const chartEl        = ref(null);
    const graphcontainer = ref(`container${_.random(0,100000)}`);
    const aspectRatio    = ref(1/(4/3)); // 4:3


    // EMITTERS
    const emit = defineEmits(["delete","add"]);

   
    // PROPS
    const props = defineProps({
        params :{type:Array,default: ['uva','uvb','uvc']},
        displaymode :{type: Boolean ,default: false},
        width: {type:Number,default:300},
        id :{type:String,default:""}
    })
     
    // FUNCTIONS      
    onMounted(() => {
        // THIS FUNCTION IS CALLED AFTER THIS COMPONENT HAS BEEN MOUNTED
        chartEl.value = document.querySelectorAll(".highcharts-figure");

        if(darkmode.value)
            chartEl.value.forEach(el => { el.classList.replace('highcharts-light','highcharts-dark') });  
        else if (!darkmode.value)
            chartEl.value.forEach(el => { el.classList.replace('highcharts-dark','highcharts-light') });   

        CreateCharts();    
        setChartParams(props.params);       
     
    });


    onBeforeUnmount(()=>{
        // THIS FUNCTION IS CALLED RIGHT BEFORE THIS COMPONENT IS UNMOUNTED
        // Mqtt.unsubscribeAll();
    });
 
    // WATCHERS
    watch(payload,(msg)=> {      
        // LIVE GRAPH
        if(msg.type == 'station')
            params.value = Object.keys(msg.data)

        if(msg.type == "station" && !props.displaymode ){    
            if(msg.id == selectedStation.value){
                chart.value.series[0].points[0].update(msg.data[props.params[0]]);
                chart.value.series[1].points[0].update(msg.data[props.params[1]]);
                chart.value.series[2].points[0].update(msg.data[props.params[2]]);   
            }          
        }          
    });

    const trackColors = Highcharts.getOptions().colors.map(color =>
    new Highcharts.Color(color).setOpacity(0.3).get()
);


    function renderIcons() {
        this.series.forEach(series => {
            if (!series.icon) {
                series.icon = this.renderer               
                    // .text(`<Icon icon="solar:temperature-broken" width="24" height="24" />`, 0, 0, true )
                    .text( `<i class="fa fa-${series.options.custom.icon}"></i>`, 0, 0, true )
                    .attr({ zIndex: 10})
                    .css({ color: series.options.custom.iconColor, fontSize: '16px' })
                    .add();  // this.series[1].group
            }
            series.icon.attr({
                x: this.chartWidth / 2 - 5,
                y: this.plotHeight / 2 - series.points[0].shapeArgs.innerR - ( series.points[0].shapeArgs.r - series.points[0].shapeArgs.innerR ) / 2 + 55
            });
        });
    }


    watch(darkmode,(mode)=> {           
       if(mode)
            chartEl.value.forEach(el => { el.classList.replace('highcharts-light','highcharts-dark') });  
       else if (!mode)
            chartEl.value.forEach(el => { el.classList.replace('highcharts-dark','highcharts-light') });         
   });


    const CreateCharts = async () => {  
        // TEMPERATURE CHART
        chart.value = Highcharts.chart(graphcontainer.value, {

            chart: {
                styledMode:true,
                type: 'solidgauge',
                width: props.width,
                height: (aspectRatio.value * 100) + '%', // 4:3 ratio
                borderRadius: 12,
                borderWidth: 1,
                // events: { render: renderIcons } //Works but limited to awesome fonts..
            },

            title: false, //{ text: 'Multiple KPI gauge', style: { fontSize: '14px' } },
            credits: {
                position: { align: 'right', x: -20 ,y: -20}
            },
            tooltip: {
                backgroundColor: 'none',
                fixed: true,
                pointFormat: `<div class="flex flex-col justify-center align-center bg-transparent ma-0 pa-0" > <p>{series.name}</p> <p style="font-size: 16px; color: {point.color};  font-weight: bold">{point.y}</p> </div>`,
                position: { align: 'center', verticalAlign: 'middle' },
                style: { fontSize: '16px', padding: 0, backgroundColor: null },
                backgroundColor: null,  
                useHTML: true
            },
            navigation: false,

            pane: {
                startAngle: 0,
                endAngle: 360,
                background: [{ // Series 0
                    outerRadius: '120%',
                    innerRadius: '100%',
                    backgroundColor: trackColors[0],
                    borderWidth: 0
                }, { //  Series 1
                    outerRadius: '99%',
                    innerRadius: '79%',
                    backgroundColor: trackColors[1],
                    borderWidth: 0
                }, { //  Series 2
                    outerRadius: '78%',
                    innerRadius: '56%',
                    backgroundColor: trackColors[2],
                    borderWidth: 0
                }]
            },

            yAxis: { 
                lineWidth: 0,
                tickPositions: []
            },

            plotOptions: {
                solidgauge: {
                    dataLabels: {
                        enabled: false
                    },
                    linecap: 'round',
                    stickyTracking: false,
                    rounded: true
                }
            },

            series: [{
               
                data: [{
                    color: Highcharts.getOptions().colors[0],
                    radius: '120%',
                    innerRadius: '100%',
                    y: 0
                }], 
                marker: {
                        symbol: 'cross',
                        lineColor: null,
                        lineWidth: 2
                    },
                custom: {
                    icon: 'square-check',
                    iconColor: '#303030'
                }
            }, {
                 
                data: [{
                    color: Highcharts.getOptions().colors[1],
                    radius: '99%',
                    innerRadius: '79%',
                    y: 0
                }], 
                custom: {
                    icon: 'location-dot',
                    iconColor: '#ffffff'
                },
                marker: {
                    symbol: 'url(https://www.highcharts.com/samples/graphics/sun.png)', 
                    // symbol: 'url(@/assets/solar--temperature-broken.png)', // Enable HTML for the marker  solar--temperature-broken.png 
                    // symbol: 'url(/api/images/solar--temperature-broken.png)', // Enable HTML for the marker  solar--temperature-broken.png
                    // useHTML: true,
                    // marker: {
                    // className: 'fa fa-star', // Replace with your Font Awesome class
                    // }
                }
            }, { 
                data: [{
                    color: Highcharts.getOptions().colors[2],
                    radius: '78%',
                    innerRadius: '56%',
                    y: 0
                }], 
                marker: {
                    symbol: 'cross',
                    lineColor: null,
                    lineWidth: 2
                },
                custom: {
                    icon: 'house',
                    iconColor: '#303030'
                }
            }]
            });

         
    }

    const setChartParams = (param) => {
        // let Options =  { solidgauge: { dataLabels: {  format: `<div style="text-align:center; margin-top: -30px"><div style="font-size:24px;">{y} <small class="text-sm">${paramDetails.value[param]['units']}</small></div><div style="font-size:14px; opacity:0.4;text-align: center;">${_.capitalize(param)}</div></div>` } } }
        // let radiationOption = { solidgauge: { dataLabels: {  format: `<div style="text-align:center; margin-top: -30px"><div style="font-size:24px;">{y} <small class="text-sm">W/m<sup>2</sup></small></div><div style="font-size:14px; opacity:0.4;text-align: center;">${_.capitalize(param)}</div></div>` } } }
        

        let Options =  { title:{ text:"UV"},series:[{name: _.upperCase(param[0]),valueSuffix: `<p class="text-sm font-semibold" style="color: {point.color};" >${paramDetails.value[param[0]]['units']}</p>`},{name: _.upperCase(param[1]),valueSuffix: `<p class="text-sm font-semibold" style="color: {point.color};" >${paramDetails.value[param[1]]['units']}</p>`},{name: _.upperCase(param[2]),valueSuffix: `<p class="text-sm font-semibold" style="color: {point.color};" >${paramDetails.value[param[2]]['units']}</p>`}]  }
        let radiationOption = { title:{ text:"UV"},series:[{name: _.upperCase(param[0])},{name: _.upperCase(param[1])},{name: _.upperCase(param[2])}],tooltip: { valueSuffix: '<p class="text-sm font-semibold" style="color: {point.color};" >W/m<sup>2</sup></p>'} }
        // valueSuffix: '<p class="text-sm font-semibold" style="color: {point.color};" >W/m<sup>2</sup></p>'

        if(param.includes("temperature"))        
            chart.value.update({ yAxis: {max:40, min: 15}, ...Options},true,true);    

        else if(param.includes("humidity"))
            chart.value.update({ yAxis: {max:100, min: 0}, ...Options},true,true); 
        
        else if(param.includes("pressure"))           
            chart.value.update({ yAxis: {max:1100, min: 900}, ...Options},true,true); 
    
        else if(param.includes("radiation"))
            chart.value.update({ yAxis: {max:100, min: 0}, ...radiationOption},true,true); 
        
        else if(param.includes("uva"))
            chart.value.update({ yAxis: {max:100, min: 0}, ...radiationOption },true,true); 
             
        // else if(param.includes("uvb"))
        //     chart.value.update({ yAxis: {max:100, min: 0}, ...radiationOption},true,true); 
             
        // else if(param.includes("uvc"))
        //     chart.value.update({ yAxis: {max:100, min: 0}, ...radiationOption},true,true); 
             
        else if(param.includes("co2"))
            chart.value.update({ yAxis: {max:5500, min: 0 },...Options},true,true); 

        else if(param.includes("rainfall"))
            chart.value.update({ yAxis: {max:60, min: 0 },...Options},true,true); 
    
        else if(param.includes("winddirection"))
            chart.value.update({ yAxis: {max:360, min: 0 },...Options},true,true); 

        else if(param.includes("windspeed"))
            chart.value.update({  yAxis: {max:100, min: 0 },...Options},true,true); 

        else if(param.includes("bat"))
            chart.value.update({ yAxis: {max:100, min: 0},...Options},true,true); 
        
        else if(param.includes("voltage"))
            chart.value.update({  yAxis: {max:4.2, min: 0},...Options},true,true); 
        
    }
</script>


<style >

/* https://jsfiddle.net/gh/get/library/pure/highcharts/highcharts/tree/master/samples/highcharts/css/gauge/ */

@media (prefers-color-scheme: dark) {
  :root {
    /* Colors for data series and points */
    --highcharts-color-td: #00B4FF;
    --highcharts-color-ts: #1E90FF;

    --highcharts-color-cat1: #3CB371;
    --highcharts-color-cat2: #FFD700;
    --highcharts-color-cat3: #FF8C00;
    --highcharts-color-cat4: #DC143C;
    --highcharts-color-cat5: #B22222;
    
  }
}

.highcharts-dark {
  /* Colors for data series and points */
  --highcharts-color-td: #00C8FF; /*#b3597c; Line colour */
  --highcharts-color-ts: #3A9AFF;

--highcharts-color-cat1: #4CAF50;
--highcharts-color-cat2: #FFC107;
--highcharts-color-cat3: #FF7043;
--highcharts-color-cat4: #F44336;
--highcharts-color-cat5: #D32F2F;
  
}



.highcharts-gauge-series .highcharts-dial {
    fill: var(--highcharts-color-1)
}

.highcharts-gauge-series .highcharts-point{
    fill:#b3597c
}

.highcharts-data-labels text {
       font-size: 14px;
    }



.cat {
    fill: #df5353;
    fill-opacity: 1;
}

.tropicaldepression{ 
    fill: var(--highcharts-color-td);
    fill-opacity: 1;
}

.tropicalstorm{
    fill: var(--highcharts-color-ts);
    fill-opacity: 1;
}

.cat1 {
    fill: var(--highcharts-color-cat1);
    fill-opacity: 1; 
}

.cat2 {
    fill: var(--highcharts-color-cat2);
    fill-opacity: 1; 
}


.cat3 {
    fill: var(--highcharts-color-cat3);
    fill-opacity: 1; 
}

.cat4 {
    fill: var(--highcharts-color-cat4);
    fill-opacity: 1; 
}

.cat5 {
    fill: var(--highcharts-color-cat5);
    fill-opacity: 1; 
}

</style>