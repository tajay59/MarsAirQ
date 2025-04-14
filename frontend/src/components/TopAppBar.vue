<template>
    <VSheet  color="rgba(0,0,0,0)" style="position: relative;"  > 

    <VToolbar flat    color="rgba(0,0,0,0)"  >             
            
        <VContainer fluid    align="center"   >
            <VRow align="center" justify="center"   style="max-width: 1500px; width: 100%;"    >
               
                <VCol cols="3" v-if="smAndUp && route.name != 'Home'">
                    <VBtn icon="mdi:mdi-menu" @click="drawer = !drawer"  ></VBtn>
                    <span class="roboto-black-italic text-primary " style="font-size:xx-large ; cursor: pointer" @click="router.push({name:'Home'})">Mars </span><span class="roboto-condensed-200  ">Air</span><span class="text-primary font-weight-bold text-h4">Q</span> 
                    <!-- <span class="nunito-black text-error mx-2 " style="font-size:xx-large ;">CIMH</span> -->
                </VCol>
                <VCol cols="6" align="center" >                 
                    <VChip class="nunito-route  text-onSurface mx-3"  v-for="route in routes"  rounded="lg"  variant="text" @click="router.push({name:route.name})"><span :class="[($route.name == route.name)? 'text-primary font-weight-bold':'text-onSurface']">{{ route.title }}</span> </VChip>
                </VCol>
                <VCol :cols="(smAndDown)? '5':'3'" align="right" > 
                    
                    <VBtn color="secondary" variant="plain"  title="Profile" @click="router.push({name:'Profile'})" icon   >
                        <svg class="svgIcon" >
                            <circle cx="12" cy="6" r="4"   />
                            <path d="M19.9975 18C20 17.8358 20 17.669 20 17.5C20 15.0147 16.4183 13 12 13C7.58172 13 4 15.0147 4 17.5C4 19.9853 4 22 12 22C14.231 22 15.8398 21.8433 17 21.5634"  stroke-linecap="round"/>
                        </svg>
                    </VBtn>

                    <VBtn color="secondary" variant="plain"  :title="(UserStore.loggedIn)? 'Logout': 'Login'" @click="(UserStore.loggedIn)? UserStore.userLogout() : router.push({name:'Login'}) " icon   >
                        <svg v-if="UserStore.loggedIn" class="svgIcon"  >
                            <path d="M15 12L6 12M6 12L8 14M6 12L8 10"   stroke-linecap="round" stroke-linejoin="round"/>
                            <path d="M12 21.9827C10.4465 21.9359 9.51995 21.7626 8.87865 21.1213C8.11027 20.3529 8.01382 19.175 8.00171 17M16 21.9983C18.175 21.9862 19.3529 21.8897 20.1213 21.1213C21 20.2426 21 18.8284 21 16V14V10V8C21 5.17157 21 3.75736 20.1213 2.87868C19.2426 2 17.8284 2 15 2H14C11.1715 2 9.75733 2 8.87865 2.87868C8.11027 3.64706 8.01382 4.82497 8.00171 7"  stroke-linecap="round"/>
                            <path d="M3 9.5V14.5C3 16.857 3 18.0355 3.73223 18.7678C4.46447 19.5 5.64298 19.5 8 19.5M3.73223 5.23223C4.46447 4.5 5.64298 4.5 8 4.5"  stroke-linecap="round"/>
                        </svg>
                        <svg v-else  class="svgIcon"  >
                            <path d="M8 16C8 18.8284 8 20.2426 8.87868 21.1213C9.51998 21.7626 10.4466 21.9359 12 21.9827M8 8C8 5.17157 8 3.75736 8.87868 2.87868C9.75736 2 11.1716 2 14 2H15C17.8284 2 19.2426 2 20.1213 2.87868C21 3.75736 21 5.17157 21 8V10V14V16C21 18.8284 21 20.2426 20.1213 21.1213C19.3529 21.8897 18.175 21.9862 16 21.9983" stroke-linecap="round"/>
                            <path d="M3 9.5V14.5C3 16.857 3 18.0355 3.73223 18.7678C4.46447 19.5 5.64298 19.5 8 19.5M3.73223 5.23223C4.46447 4.5 5.64298 4.5 8 4.5" stroke-linecap="round"/>
                            <path d="M6 12L15 12M15 12L12.5 14.5M15 12L12.5 9.5" stroke-linecap="round" stroke-linejoin="round"/>
                        </svg>
                    </VBtn>                        
                    

                    
                    <VBtn  :elevation="0"  icon @click="darkmode = !darkmode" variant="plain">                  
                        <svg v-if="darkmode"  class="svgIcon"  >
                            <path d="M13.5 8H16.5L13.5 11H16.5"  stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                            <path d="M18 2H22L18 6H22"  stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                            <path stroke-width="0.5" id="moonIcon" d="M21.0672 11.8568L20.4253 11.469L21.0672 11.8568ZM12.1432 2.93276L11.7553 2.29085V2.29085L12.1432 2.93276ZM7.37554 20.013C7.017 19.8056 6.5582 19.9281 6.3508 20.2866C6.14339 20.6452 6.26591 21.104 6.62446 21.3114L7.37554 20.013ZM2.68862 17.3755C2.89602 17.7341 3.35482 17.8566 3.71337 17.6492C4.07191 17.4418 4.19443 16.983 3.98703 16.6245L2.68862 17.3755ZM21.25 12C21.25 17.1086 17.1086 21.25 12 21.25V22.75C17.9371 22.75 22.75 17.9371 22.75 12H21.25ZM2.75 12C2.75 6.89137 6.89137 2.75 12 2.75V1.25C6.06294 1.25 1.25 6.06294 1.25 12H2.75ZM15.5 14.25C12.3244 14.25 9.75 11.6756 9.75 8.5H8.25C8.25 12.5041 11.4959 15.75 15.5 15.75V14.25ZM20.4253 11.469C19.4172 13.1373 17.5882 14.25 15.5 14.25V15.75C18.1349 15.75 20.4407 14.3439 21.7092 12.2447L20.4253 11.469ZM9.75 8.5C9.75 6.41182 10.8627 4.5828 12.531 3.57467L11.7553 2.29085C9.65609 3.5593 8.25 5.86509 8.25 8.5H9.75ZM12 2.75C11.9115 2.75 11.8077 2.71008 11.7324 2.63168C11.6686 2.56527 11.6538 2.50244 11.6503 2.47703C11.6461 2.44587 11.6482 2.35557 11.7553 2.29085L12.531 3.57467C13.0342 3.27065 13.196 2.71398 13.1368 2.27627C13.0754 1.82126 12.7166 1.25 12 1.25V2.75ZM21.7092 12.2447C21.6444 12.3518 21.5541 12.3539 21.523 12.3497C21.4976 12.3462 21.4347 12.3314 21.3683 12.2676C21.2899 12.1923 21.25 12.0885 21.25 12H22.75C22.75 11.2834 22.1787 10.9246 21.7237 10.8632C21.286 10.804 20.7293 10.9658 20.4253 11.469L21.7092 12.2447ZM12 21.25C10.3139 21.25 8.73533 20.7996 7.37554 20.013L6.62446 21.3114C8.2064 22.2265 10.0432 22.75 12 22.75V21.25ZM3.98703 16.6245C3.20043 15.2647 2.75 13.6861 2.75 12H1.25C1.25 13.9568 1.77351 15.7936 2.68862 17.3755L3.98703 16.6245Z"/>
                        </svg>
                        <svg v-else  class="svgIcon"  >
                            <path d="M7.28451 10.3333C7.10026 10.8546 7 11.4156 7 12C7 14.7614 9.23858 17 12 17C14.7614 17 17 14.7614 17 12C17 9.23858 14.7614 7 12 7C11.4156 7 10.8546 7.10026 10.3333 7.28451"  stroke-linecap="round"/>
                            <path d="M12 2V4"  stroke-linecap="round"/>
                            <path d="M12 20V22"  stroke-linecap="round"/>
                            <path d="M4 12L2 12"  stroke-linecap="round"/>
                            <path d="M22 12L20 12"  stroke-linecap="round"/>
                            <path d="M19.7778 4.22266L17.5558 6.25424"  stroke-linecap="round"/>
                            <path d="M4.22217 4.22266L6.44418 6.25424"  stroke-linecap="round"/>
                            <path d="M6.44434 17.5557L4.22211 19.7779"  stroke-linecap="round"/>
                            <path d="M19.7778 19.7773L17.5558 17.5551"  stroke-linecap="round"/>
                        </svg>
                    </VBtn>
                </VCol>        
            </VRow>
        </VContainer>
    </VToolbar>

    <Transition name="slide-right"  >      
        <VSheet v-show="drawer" style="position: absolute; z-index: 20000; height: 90vh;" width="500" color="transparent" class="mt-5" >
            <VContainer align="center" class="bg- green-400 h-full " fluid>
                <VRow class="bg- red-900 h-full"  >
                    <VCol class="bg- blue-500 "    >
                        <figure class="highcharts-figure">
                            <div id="container"></div> 
                        </figure>   
                        <VDivider class="my-3" /> 
                        <figure class="highcharts-figure">
                            <div id="container1"></div> 
                        </figure>
                    </VCol>
                </VRow> 
                
            </VContainer>
        </VSheet>
    </Transition>
 

    <!-- <VNavigationDrawer v-model="drawer" rail   location="left" color="transparent"   class="mt-20" width="500"  >
        <VList>
          <VListItem
            prepend-avatar="@/assets/default.jpg"
            title="IoT Systems"
            subtitle="iot@yanacreations.com"
          ></VListItem>
        </VList>

        <v-divider></v-divider>
        <VContainer align="center" class="bg-green-400 h-48 " fluid>
                <VRow class="bg-red-900 h-full"  >
                    <VCol class="bg-blue-500 pa-0"    >
                        <figure class="highcharts-figure">
                            <div id="container"></div> 
                        </figure>                      
                    </VCol>
                </VRow> 
            </VContainer>

        <VList density="compact" nav>
        <VListItem   title="Home" value="Home" >
            
        </VListItem>
             <VListItem prepend-icon="mdi-walk" title="Virtual Tour" value="Virtual Tour" :to="{ name: 'Virtual' }"></VListItem>
          <VListItem prepend-icon="mdi-monitor-dashboard" title="Dashboard" value="Dashboard" :to="{ name: 'Dashboard' }"></VListItem>
          <VListItem prepend-icon="mdi-chart-line" title="Live" value="Live" :to="{ name: 'Live' }" ></VListItem>      
          <VListItem prepend-icon="mdi-chart-scatter-plot" title="Analysis" value="Analysis" :to="{ name: 'Analysis' }" ></VListItem>        
        </VList>
      </VNavigationDrawer> -->

    <!-- <Notification/> -->
    <Modal />
    <VDivider />
    </VSheet>
  </template>
  
  <script setup>

import { useRoute, useRouter } from "vue-router";
import { ref,reactive, onMounted,onBeforeMount, onBeforeUnmount,watch,computed } from 'vue';
import { storeToRefs } from "pinia";
import { useDisplay } from 'vuetify'
import { useAppStore } from '@/stores/appStore';
import { useUserStore } from '@/stores/userStore'; 
import { useMqttStore } from '@/stores/mqttStore'; // Import Mqtt Store 
import { useNotificationStore } from '@/stores/notificationStore'; 
import { useTheme } from 'vuetify'
import Notification from "./Notification.vue"; 
import Modal from "./Modal.vue";
 
// Highcharts, Load the exporting module and Initialize exporting module.
import Highcharts from 'highcharts';
import more from 'highcharts/highcharts-more';
import Exporting from 'highcharts/modules/exporting';
Exporting(Highcharts); 
more(Highcharts);
 


// VARIABLES
const { xs,smAndDown,smAndUp, mdAndUp }   = useDisplay();
const AppStore                      = useAppStore();
const {appDarkMode}                 = storeToRefs(AppStore);
const UserStore                     = useUserStore(); 
const NotificationStore             = useNotificationStore(); 

const {id,loggedIn,image, darkmode} = storeToRefs(UserStore); 
const router                        = useRouter();
const route                         = useRoute(); 
const drawer                        = ref(false);
const theme                         = useTheme();
//const darkmode                      = ref(false);
const Mqtt                          = useMqttStore();
const {connected, payload, payloadTopic } = storeToRefs(Mqtt);
const tempChart     = ref(null); // Chart object
const humChart      = ref(null); // Chart object
const points        = ref(6000); // Specify the quantity of points to be shown on the live graph simultaneously.
const shift         = ref(false); // Delete a point from the left side and append a new point to the right side of the graph.
 

const drawerItems = [
{"icon":"mdi:mdi-view-dashboard","title":"Protected","route":"/protected","name":"Protected"},  
{"icon":"mdi:mdi-view-dashboard","title":"Map","route":"/map","name":"Map"},  
]
 
const routes = [
    // {"icon":"mdi:mdi-view-dashboard","title":"Home","route":"/","name":"Home"}, 
    {"icon":"mdi:mdi-view-dashboard","title":"Protected","route":"/protected","name":"Protected"},  
    {"icon":"mdi:mdi-view-dashboard","title":"Map","route":"/map","name":"Map"},  
    {"icon":"mdi:mdi-view-dashboard","title":"Live","route":"/live","name":"Live"},  
    {"icon":"mdi:mdi-view-dashboard","title":"Dashboard","route":"/dashboard","name":"Dashboard"},  
    {"icon":"mdi:mdi-view-dashboard","title":"Analysis","route":"/analysis","name":"Analysis"},  
]


// WATCHERS
watch(darkmode,  (mode) => {
    appDarkMode.value = mode;

    theme.global.name.value = mode ?  'dark' : 'light';
    localStorage.setItem("theme",mode ? 'dark' : 'light');  

    if(theme.global.current.value.dark)
          document.documentElement.classList.replace('light','dark');            
    else 
        document.documentElement.classList.replace('dark','light'); 
});


watch(id,   (user) => {
//   console.log(`USER : ${user}  ACTIVE ${!!user}`);   
  if(!!user == false) {
    setTimeout(async ()=>{
        if(loggedIn){
        await UserStore.Auth() 
    }
    },5000)
    
  }
});


// FUNCTIONS
onBeforeMount(()=> {
  // SAVE THEME TO LOCALSTORAGE MAKING IT PERSIST BROWSER REFRESH

  if(localStorage.getItem("theme") != null){
    console.log("YH BRO")
    theme.global.name.value = localStorage.getItem("theme");
    darkmode.value = theme.global.current.value.dark;

    if(theme.global.current.value.dark) 
        document.documentElement.classList.add('dark');                  
    else  
        document.documentElement.classList.add('light');
    
        
  }
  else{
    // localStorage.setItem("theme",theme.global.current.value.dark ? 'dark' : 'light');
    // darkmode.value = theme.global.current.value.dark; 
    localStorage.setItem("theme",theme.global.current.value.dark ? 'darkMode' : 'lightMode');
    darkmode.value = theme.global.current.value.dark;   

 
 
    if(theme.global.current.value.dark)
        document.documentElement.classList.add('dark');           
    else 
        document.documentElement.classList.add('light');
        
  }  
});

onMounted(()=>{
    // THIS FUNCTION IS CALLED AFTER THIS COMPONENT HAS BEEN MOUNTED
    CreateCharts(); 
     
});

onBeforeUnmount(() => {
    /*
    if(Mqtt.isConnected()){
        Mqtt.unsubscribe("/references");
        Mqtt.unsubscribe("/devices");
    }*/
})

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
  tempChart.value = Highcharts.chart('container', {
      chart: { zoomType: 'x',width: 400, height:200 },
      title: { text: 'Live Analysis', align: 'left'},
      yAxis: { 
          title: { text: 'Temperature & Humidity' , style:{color:'#000000'}, enabled: false },
          labels: { format: '{value} ', enabled: false },
       
          max:1100,
          min:800        
      },
  
      xAxis: {
          type: 'datetime', 
          title: { text: 'Time', style:{color:'#000000'}, enabled: false  },        
      },
   
      tooltip: { shared:true, },
      legend: { enabled: false },
  
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

  humChart.value = Highcharts.chart('container1', {
      chart: { zoomType: 'x',width: 400, height:200 },
      title: { text: 'Live Analysis', align: 'left'},
      yAxis: { 
          title: { text: 'Temperature & Humidity' , style:{color:'#000000'}, enabled: false },
          labels: { format: '{value} ', enabled: false },
       
          max:1100,
          min:800        
      },
  
      xAxis: {
          type: 'datetime', 
          title: { text: 'Time', style:{color:'#000000'}, enabled: false  },        
      },
   
      tooltip: { shared:true, },
      legend: { enabled: false },
  
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
 