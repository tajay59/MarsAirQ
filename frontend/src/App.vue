<template>
  <VApp class="bg-surface relative "   > 
    <Notification/>

    <SpeedDial v-if="smAndUp"  :model="items" pt:menuitem="m-2"    direction="left" style="position: absolute; top: 25px; right: 50px; z-index: 20000;"   > 
        <template #button="{ toggleCallback }">
            <VBtn @click="toggleCallback" icon size="50" flat color="transparent" class="" >
                <Icon icon="gg:menu-grid-o" width="32" height="32" :class="[(route.path == '/analytics/map')?'!text-neutral-100':'!text-neutral-900 dark:!text-neutral-200']" />
            </VBtn>                 
        </template>
        <template #item="{ item, toggleCallback }"> 
            <VSheet  :class="['rounded-[50%]',(route.path == '/analytics/map')?'!bg-neutral-700':'bg-neutral-100  dark:bg-neutral-700']"   border >
                <VBtn v-if="item.label == 'Login'" :title="(loggedIn)? 'Logout':'Login'" @click="toggleCallback"  icon size="40" flat color="transparent" variant="outlined" >                    
                    <Icon v-if="loggedIn" :icon="item.icon" width="24" height="24" :class="[(route.path == '/analytics/map')?'!text-neutral-100':'!text-neutral-500 dark:!text-neutral-300']" />
                    <Icon v-else :icon="item.icon1" width="24" height="24" :class="[(route.path == '/analytics/map')?'!text-neutral-100':'!text-neutral-500 dark:!text-neutral-300']" />
                </VBtn>  
                <VBtn v-else-if="item.label == 'Theme'"  title="Theme"  @click="toggleCallback"  icon size="40" flat color="transparent" variant="outlined" >                    
                    <Icon v-if="darkmode" :icon="item.icon" width="24" height="24" :class="[(route.path == '/analytics/map')?'!text-neutral-100':'!text-neutral-500 dark:!text-neutral-300']" />
                    <Icon v-else :icon="item.icon1" width="24" height="24" :class="[(route.path == '/analytics/map')?'!text-neutral-100':'!text-neutral-500 dark:!text-neutral-300']" />
                </VBtn>    
                <VBtn v-else  @click="toggleCallback"  :title="item.label"  icon size="40" flat color="transparent" variant="outlined" >                    
                    <Icon :icon="item.icon" width="24" height="24" :class="[(route.path == '/analytics/map')?'!text-neutral-100':'!text-neutral-500 dark:!text-neutral-300']" />
                </VBtn>   
            </VSheet>              
        </template>
    </SpeedDial>   
   
    <VMain  > 
      <RouterView v-slot="{ Component, route}"> 
        <transition :name="route.meta.transition || 'fade'" mode="out-in" >
          <component :is="Component" />
        </transition>
      </RouterView> 
    </VMain>

    <VOverlay v-model="overlay"  :z-index="1000" :opacity="0.7" ></VOverlay>      
    <BottomNavBar v-if="!['Login','Signup','PasswordReset'].includes(route.name)"  :active="!smAndUp" :items="items" />    
    <Toast pt:root="!w-[300px]" />
  </VApp>
</template>

<script setup>
  // IMPORTS
  import { ref,reactive, onMounted,computed, watch,onBeforeMount, onBeforeUnmount, toRaw} from 'vue';
  import BottomNavBar from '@/components/BottomNavBar.vue';
  import { RouterLink, RouterView } from 'vue-router'
  import { useToast } from 'primevue/usetoast';
  import { useRoute, useRouter } from "vue-router";
  import { useAppStore } from '@/stores/appStore';
  import { useUserStore } from '@/stores/userStore';
  import { useMqttStore } from '@/stores/mqttStore'; // Import Mqtt Store
  import { storeToRefs } from "pinia";
  import { useTheme } from 'vuetify';
  import { useDisplay } from 'vuetify';
  import { Icon } from '@iconify/vue';
  

// VARIABLES
const router            = useRouter();
const route             = useRoute(); 
const toast             = useToast(); 
const { xs,smAndDown,smAndUp, mdAndUp }   = useDisplay();
const UserStore         = useUserStore();
const {id,loggedIn,image,suball, selectedStation, darkmode, mqtt_sub_credentials, layout} = storeToRefs(UserStore); 
 
const theme             = useTheme();
const Mqtt              = useMqttStore();
const AppStore          = useAppStore();

const {
  username,
  password,
   subs,
   unsubs,
   subTopics,
   connected,
   isConnected,
   payload,
   payloadTopic } = storeToRefs(Mqtt);

  const {overlay,
    openSiteSearch,
    openEntitySearch,
    openCreateSite,
    openCreateEntity,
    dashboardMenu
  }  = storeToRefs(AppStore)

let subsID = "";
let unsubsID = "";

const show     = ref(["Home","Dashboard","Graphs","Login","Theme","Profile","Analysis","Map","Save"])
const items    = ref([]);
const allItems = ref([
    {
        label: 'Login',
        icon: 'majesticons:login',
        icon1: 'majesticons:logout', 
        command: () => { (UserStore.loggedIn)? UserStore.userLogout() : router.push({name:'Login'}) }
    },
{
        label: 'Theme',
        icon: 'line-md:sun-rising-filled-loop',
        icon1: 'line-md:sunny-filled-loop-to-moon-filled-loop-transition', 
        command: () => { darkmode.value = !darkmode.value; }
    },
{
        label: 'Home',
        icon: 'iconamoon:home-fill', 
        command: () => { router.push({name:'Home'}); }
    },
    {
        label: 'Profile',
        icon: 'iconamoon:profile-fill', 
        command: () => { router.push({name:'Profile'}); }
    },
    {
        label: 'Settings',
        icon: 'mingcute:settings-3-fill', 
        command: () => { router.push('/admin/accounts'); }
    },
    {
        label: 'Analysis',
        icon: 'logos:google-analytics', 
        command: () => { router.push('/analytics/analysis'); }
    },
    {
        label: 'Map',
        icon: 'fa6-solid:map-location', 
        command: () => { router.push('/analytics/map'); }
    },    
    {
        label: 'Add Graphs',
        icon: 'si:dashboard-customize-fill', 
        command: () => { dashboardMenu.value = true; }
    },
    {
        label: 'Save Dashboard',
        icon: 'fluent:save-arrow-right-24-filled', 
        command: () => { updateDashboard(); }
    },
    {
        label: 'Dashboard',
        icon: 'material-symbols:dashboard-rounded', 
        command: () => { router.push('/analytics/dashboard'); }
    },
    {
        label: 'Search Site',
        icon: 'tdesign:map-search-filled', 
        command: () => { openSiteSearch.value = true; }
    },
    {
        label: 'Search Entity',
        icon: 'mdi:home-search', 
        command: () => { openEntitySearch.value = true; }
    },
    {
        label: 'Create Entity',
        icon: 'fluent:organization-48-filled', 
        command: () => { openCreateEntity.value = true; }
    },
    {
        label: 'Create Site',
        icon: 'line-md:map-marker-plus-filled', 
        command: () => { openCreateSite.value = true; }
    },
]);
 
    

// theme.global.current.value.colors.onSurfaceVariant

// WATCHERS
watch(()=>route.fullPath,(route)=> {
    configSpeedDial(route);
});

watch(darkmode,  (mode) => {
    // appDarkMode.value = mode;

    theme.global.name.value = mode ?  'dark' : 'light';
    localStorage.setItem("theme",mode ? 'dark' : 'light');  

    if(theme.global.current.value.dark)
          document.documentElement.classList.replace('light','dark');            
    else 
        document.documentElement.classList.replace('dark','light'); 
});

watch(username ,(name) => {
    if(!!name){
      if(loggedIn.value){
        Mqtt.connect();        
      }      
    }
},{ immediate: true })

 

watch(() => subs.value.size, (list) => { 
  
  setTimeout(() => {      
    if(Mqtt.isConnected()){ 
      let topics = toRaw(subs.value); 
      topics.forEach( topic => Mqtt.subscribe(topic) );
    }
  },1000)

},{ immediate: true })


watch(() => unsubs.value.size, (list) => { 

  setTimeout(() => {      
      if(Mqtt.isConnected()){ 
        let unsubtopics = toRaw(unsubs.value); 
        unsubtopics.forEach( topic => Mqtt.unsubscribe(topic) ); 
      }
        },1000)

},{ immediate: true })


// FUNCTIONS
const configSpeedDial = (route)=> {
    items.value = [];
    switch (route) {
        case "/":
              show.value = ["Home","Settings","Dashboard","Login","Theme","Profile","Analysis","Map"]
              break;
        case "/admin":
              show.value = ["Home","Dashboard","Login","Theme","Profile","Analysis","Map"]
              break;
        case "/admin/entities":
              show.value = ["Home","Dashboard","Login","Theme","Profile","Analysis","Map","Search Site","Create Entity","Search Entity"]
              break;
        
        case "/analytics/map":
            show.value = ["Home","Settings","Dashboard","Login","Theme","Profile","Analysis"]
            break;
        case "/profile/devices":
            show.value = ["Home","Settings","Dashboard","Login","Theme","Analysis","Map"]
            break;
        case "/profile/entities":
            show.value = ["Home","Settings","Dashboard","Login","Theme","Analysis","Map","Search Site","Create Site","Create Entity"]
            break;
        case "/analytics/dashboard":
            show.value = ["Home","Settings","Add Graphs","Login","Theme","Profile","Analysis","Map","Save Dashboard"]
            break;
        case "/analytics/analysis":
            show.value = ["Home","Settings","Dashboard" ,"Login","Theme","Profile", "Map"]
            break;
            
        default:
            break;    
    }   
    
    allItems.value.forEach(button => {
        if(show.value.includes(button.label)){
          items.value.push(button);
        }
      })
  }


onBeforeMount(()=> {
  // SAVE THEME TO LOCALSTORAGE MAKING IT PERSIST BROWSER REFRESH
  // Mqtt.clearSubs();
  
  if(loggedIn.value){
    console.log("FETCHING ALL SITES");
    UserStore.getAllSites();
  }
 
 

  if(localStorage.getItem("theme") != null){
 
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

  configSpeedDial(route.fullPath);
});

onMounted(() => {
    // THIS FUNCTION IS CALLED AFTER THIS COMPONENT HAS BEEN MOUNTED
    if(suball.value){
      Mqtt.subTo("/station/data/#");
    }
    else {
    
      if(!!mqtt_sub_credentials.value)
        Mqtt.subTo(mqtt_sub_credentials.value.topic);
    }
    
});


onBeforeUnmount(()=>{
    // THIS FUNCTION IS CALLED RIGHT BEFORE THIS COMPONENT IS UNMOUNTED
    Mqtt.unsubscribeAll();
    clearInterval(subsID);
});

const updateDashboard = async () => {

  if(!!selectedStation.value){
    let result = await AppStore.updateDeviceDashboard(layout.value);

    switch (result) {
        case "updated": 
            toast.add({ severity: 'success', summary: 'UPDATED', detail: 'Dashboard UPDATED!', life: 3000 });  
            break;
        
        case "failed":  
            toast.add({ severity: 'error', summary: 'FAILED', detail: 'Unable to UPDATED Dashboard', life: 3000 });  
            break;  

        default:
            toast.add({ severity: 'error', summary: 'Request Failed', detail: 'Dashboard UPDATED request failed!', life: 3000 });  
            break;
    }
  }
  else{
    toast.add({ severity: 'warn', summary: 'FAILED', detail: 'Station must be selected', life: 5000 }); 
  }
    
    }
 
</script>

<style >

/* @import url("./node_modules/highcharts/css/themes/dark-unica.css"); */
/* @import url("./node_modules/highcharts/css/themes/grid-light.css");  */
/* @import url("./node_modules/highcharts/css/themes/sand-signika.css"); */

@import url("https://fonts.googleapis.com/css?family=Unica+One");
@import url("./node_modules/highcharts/css/highcharts.css");

*,
*::before,
*::after {
  box-sizing: border-box;
}

@media (prefers-color-scheme: dark) {
  :root {
    --highcharts-color-0-light: #b3597c;
    --highcharts-color-0-dark: #4ca683;
     /* Colors for data series and points  */
    --highcharts-color-0: #b3597c;
    --highcharts-color-1: #c4688c;
    --highcharts-color-2: #78a8d1;
    --highcharts-color-3: #7991d2;
    --highcharts-color-4: #7d7bd4;
    --highcharts-color-5: #977dd5;
    --highcharts-color-6: #b3597c;
    --highcharts-color-7: #b27fd6;

    /* UI colors  */
    --highcharts-background-color: #c42626;  /* #333;*/

    
      /* Neutral color variations */
      /* https://www.highcharts.com/samples/highcharts/css/palette-helper */
    
    --highcharts-neutral-color-100:#ffffff;
    --highcharts-neutral-color-80: #d6d6d6;
    --highcharts-neutral-color-60: #adadad;
    --highcharts-neutral-color-40: #858585;
    --highcharts-neutral-color-20: #5c5c5c;
    --highcharts-neutral-color-10: #474747;
    --highcharts-neutral-color-5:  #3d3d3d;
    --highcharts-neutral-color-3:  #393939;

    /* Highlight color variations  */
    --highcharts-highlight-color-100:#7aa7ff;
    --highcharts-highlight-color-80: #6c90d6;
    --highcharts-highlight-color-60: #5e79ad;
    --highcharts-highlight-color-20: #414a5c;
    --highcharts-highlight-color-10: #3a3f47;
    
  }
}
 
.highcharts-light {
    /* Colors for data series and points #b3597c,#c4688c,#78a8d1,#7991d2,#7d7bd4,#977dd5,#b3597c,#b27fd6 */
    --highcharts-color-0: #b3597c;
    --highcharts-color-1: #7d7bd4;
    --highcharts-color-2: #78a8d1;
    --highcharts-color-3: #7991d2;
    --highcharts-color-4: #c4688c;
    --highcharts-color-5: #977dd5;
    --highcharts-color-6: #b3597c;
    --highcharts-color-7: #b27fd6;

    /* UI colors */
    --highcharts-background-color: #fafafa;  /* Transparent background #fafafa #f4f4f5 #e4e4e7 #d4d4d8*/

    /*
      Neutral color variations
      https://www.highcharts.com/samples/highcharts/css/palette-helper
    */
    --highcharts-neutral-color-100:#ffffff;
    --highcharts-neutral-color-80: #d6d6d6;
    --highcharts-neutral-color-60: #adadad;
    --highcharts-neutral-color-40: #858585;
    --highcharts-neutral-color-20: #5c5c5c;
    --highcharts-neutral-color-10: #474747;
    --highcharts-neutral-color-5:  #3d3d3d;
    --highcharts-neutral-color-3:  #393939;

    /* Highlight color variations */
    --highcharts-highlight-color-100:#7aa7ff;
    --highcharts-highlight-color-80: #6c90d6;
    --highcharts-highlight-color-60: #5e79ad;
    --highcharts-highlight-color-20: #414a5c;
    --highcharts-highlight-color-10: #3a3f47;

    --highcharts-color-td: #00B4FF;
    --highcharts-color-ts: #1E90FF;

    --highcharts-color-cat1: #3CB371;
    --highcharts-color-cat2: #FFD700;
    --highcharts-color-cat3: #FF8C00;
    --highcharts-color-cat4: #DC143C;
    --highcharts-color-cat5: #B22222;

    /** CUSTTOM VARIABLES */
    --highcharts-title-color: hsl(0, 0%, 30%);
    --highcharts-subtitle-color: #ffffff;
    --highcharts-axis-label-color: hsl(0, 0%, 30%);
    --highcharts-border-radius-color: hsl(0, 0%, 80%);
  }

.highcharts-dark {
  /* Colors for data series and points */
  --highcharts-color-0: #4ca683; /*#b3597c; Line colour */
  --highcharts-color-1: #82842b; /*Background  */
  --highcharts-color-2: #87572e;
  --highcharts-color-3: #866e2d;
  --highcharts-color-4: #3b9773;
  --highcharts-color-5: #68822a;
  --highcharts-color-6: #4ca683;
  --highcharts-color-7: #4d8029;

  /* UI colors */
  --highcharts-background-color: #27272a;  /* Transparent background #3f3f46  #27272a #18181b*/   

  /* Neutral color variations */
  --highcharts-neutral-color-100:#ffffff;
  --highcharts-neutral-color-80: #d6d6d6;
  --highcharts-neutral-color-60: #adadad;
  --highcharts-neutral-color-40: #858585;
  --highcharts-neutral-color-20: #5c5c5c;
  --highcharts-neutral-color-10: #474747;
  --highcharts-neutral-color-5:  #3d3d3d;
  --highcharts-neutral-color-3:  #393939;

  /* Highlight color variations */
  --highcharts-highlight-color-100:#7aa7ff;
  --highcharts-highlight-color-80: #6c90d6;
  --highcharts-highlight-color-60: #5e79ad;
  --highcharts-highlight-color-20: #414a5c;
  --highcharts-highlight-color-10: #3a3f47;

  --highcharts-color-td: #00C8FF; /*#b3597c; Line colour */
  --highcharts-color-ts: #3A9AFF;

  --highcharts-color-cat1: #4CAF50;
  --highcharts-color-cat2: #FFC107;
  --highcharts-color-cat3: #FF7043;
  --highcharts-color-cat4: #F44336;
  --highcharts-color-cat5: #D32F2F;

  /** CUSTTOM VARIABLES */
--highcharts-title-color: hsl(0, 0%, 70%);
--highcharts-subtitle-color: #ffffff;
--highcharts-axis-label-color: hsl(0, 0%, 70%);
--highcharts-border-radius-color: hsl(0, 0%, 30%);
}


.highcharts-series-inactive { /** Prevent graying out of chart when hovering */
    opacity: 1 !important;
}


.highcharts-background { 
  transition: all 250ms;
}

.highcharts-description {
  margin: 10px;
}

.controls {
  margin: 10px;
}

.highcharts-yaxis-grid .highcharts-grid-line {
    stroke-width: 1px;
    stroke: var(--highcharts-line-color-0);
}

.highcharts-yaxis .highcharts-tick {
    stroke-width: 1px;
    stroke: var(--highcharts-line-color-0);
}

/* .highcharts-xaxis-grid .highcharts-grid-line {
    stroke-width: 2px;
    stroke: #d8d8d8;
}

.highcharts-xaxis .highcharts-tick {
    stroke-width: 2px;
    stroke: #d8d8d8;
} */

.highcharts-tooltip-box {
    fill: black;
    fill-opacity: 0.8;
    stroke-width: 0;
}

.highcharts-tooltip text {
    fill: white;
    text-shadow: 0 0 3px black;
}


  /*
  ::-webkit-scrollbar { width: 5px; height: 5px; }  SCROLLBAR SETTING 
  ::-webkit-scrollbar-track { box-shadow: inset 0 0 5px grey; border-radius: 10px; }    Track 
  ::-webkit-scrollbar-thumb { background: rgb(var(--v-theme-primary)) ; border-radius: 10px; }     Handle 
  ::-webkit-scrollbar-thumb:hover { background: rgb(var(--v-theme-secondary)); }    Handle on hover 
  */

  ::-webkit-scrollbar { width: 5px; height: 5px; } /* SCROLLBAR SETTING */
  ::-webkit-scrollbar-track { box-shadow: inset 0 0 5px grey; border-radius: 10px; }   /* Track */
  ::-webkit-scrollbar-thumb { background: var(--highcharts-color-0) ; border-radius: 10px; }    /* Handle */ 
  ::-webkit-scrollbar-thumb:hover { background: var(--highcharts-color-0); }   /* Handle on hover */


  .scrolleffect{
    overflow-y: scroll;
}

/* Hide scrollbar for Chrome, Safari and Opera */
.scrolleffect::-webkit-scrollbar {
    display: none;
}

/* Hide scrollbar for IE, Edge and Firefox */
.scrolleffect {
  -ms-overflow-style: none;  /* IE and Edge */
  scrollbar-width: none;  /* Firefox */
}

/* Remove autofill background/ box shadow color on Input fields */
::v-deep input:-webkit-autofill { 
  box-shadow: 0 0 0 0 rgba(168, 6, 44, 0) inset !important; /* Shadow effect */
  -webkit-box-shadow: 0 0 0 0 rgba(185, 19, 19, 0) inset !important; /* Ensure it works on Safari too */  
  border-top-left-radius: 25px;  /* border-radius: 25px; */
  border-bottom-left-radius: 25px;
}
 
 /* ADD ALL GLOBAL STYLES HERE */ 
  /* SLIDE RIGHT */
  .slide-enter-active,
  .slide-leave-active {
  transition: opacity 0.5s, transform 0.5s;
  }

  .slide-enter-from,.slide-leave-to {
  opacity: 0; 
  }

  .slide-enter-to,.slide-leave-from {
  opacity: 1;
  transform: translateX(10px);
 
  }

  /* FADE */
  .fade-enter-active{
    transition: opacity 0.2s ease-in-out 200ms;
  }

  .fade-leave-active {
    transition: opacity  ease-in-out 200ms;
  }

  .fade-enter-from ,
  .fade-leave-to {
  opacity: 0; 
  }

   /* FADEFAST */
   .fadefast-enter-active{
    transition: opacity ease-in-out 20ms;
  }

  .fadefast-leave-active {
    transition: opacity  ease-in-out 20ms;
  }

  .fadefast-enter-from ,
  .fadefast-leave-to {
  opacity: 0; 
  }


  /* BOUNCE */
  .bounce-enter-active {
    animation: bounce-in 0.5s;
  }
  .bounce-leave-active {
    animation: bounce-in 0.5s reverse;
  }
  @keyframes bounce-in {
    0% {
      transform: scale(0);
    }
    50% {
      transform: scale(1.025);
    }
    100% {
      transform: scale(1);
    }
  }

  /* SLIDE FADE */
  .slide-fade-enter-active {
  transition: all .2s ease-out 100ms;
}

.slide-fade-leave-active {
  transition: all cubic-bezier(1, 0.5, 0.8, 1) 100ms;
}

.slide-fade-enter-from,
.slide-fade-leave-to {
  transform: translateY(-20px);
  opacity: 0;
  /* position: absolute; */
}

/*  SLIDE UP */
.slide-up-enter-active{
  transition: all 0.4s ease-out 400ms;
}
.slide-up-leave-active {
  transition: all  ease-out 400ms;
}

.slide-up-enter-from {
  opacity: 0;
  transform: translateX(20px);
}

.slide-up-leave-to {
  opacity: 0;
  transform: translateX(-20px);
}

/*  SLIDE RIGHT */
.slide-right-enter-active{
  transition: all 0.2s ease-out 200ms;
}
.slide-right-leave-active {
  transition: all  ease-out 200ms;
}

.slide-right-enter-from {
  opacity: 0;
  transform: translateX(-20px);
}

.slide-right-leave-to {
  opacity: 0;
  transform: translateX(-20px);
}

/* LIST */
.lists-enter-active {
  transition: all 0.3s ease 300ms;
}
.lists-leave-active {
  transition: all  ease 300ms;
}
.lists-enter-from,
.lists-leave-to {
  opacity: 0;
  transform: translateX(30px);
  /* position: absolute; */
}


  .roboto-thin {
  font-family: "Roboto", sans-serif;
  font-weight: 100;
  font-style: normal;
}

.roboto-light {
  font-family: "Roboto", sans-serif;
  font-weight: 300;
  font-style: normal;
}

.roboto-regular {
  font-family: "Roboto", sans-serif;
  font-weight: 400;
  font-style: normal;
}

.roboto-medium {
  font-family: "Roboto", sans-serif;
  font-weight: 500;
  font-style: normal;
}

.roboto-bold {
  font-family: "Roboto", sans-serif;
  font-weight: 700;
  font-style: normal;
}

.roboto-black {
  font-family: "Roboto", sans-serif;
  font-weight: 900;
  font-style: normal;
}

.roboto-thin-italic {
  font-family: "Roboto", sans-serif;
  font-weight: 100;
  font-style: italic;
}

.roboto-light-italic {
  font-family: "Roboto", sans-serif;
  font-weight: 300;
  font-style: italic;
}

.roboto-regular-italic {
  font-family: "Roboto", sans-serif;
  font-weight: 400;
  font-style: italic;
}

.roboto-medium-italic {
  font-family: "Roboto", sans-serif;
  font-weight: 500;
  font-style: italic;
}

.roboto-bold-italic {
  font-family: "Roboto", sans-serif;
  font-weight: 700;
  font-style: italic;
}

.roboto-black-italic {
  font-family: "Roboto", sans-serif;
  font-weight: 900;
  font-style: italic;
}

/*
// <uniquifier>: Use a unique and descriptive class name
// <weight>: Use a value from 100 to 900

.roboto-condensed-<uniquifier> {
  font-family: "Roboto Condensed", sans-serif;
  font-optical-sizing: auto;
  font-weight: <weight>;
  font-style: normal;
}

// <uniquifier>: Use a unique and descriptive class name
// <weight>: Use a value from 100 to 1000

.roboto-flex-<uniquifier> {
  font-family: "Roboto Flex", sans-serif;
  font-optical-sizing: auto;
  font-weight: <weight>;
  font-style: normal;
  font-variation-settings:
    "slnt" 0,
    "wdth" 100,
    "GRAD" 0,
    "XOPQ" 96,
    "XTRA" 468,
    "YOPQ" 79,
    "YTAS" 750,
    "YTDE" -203,
    "YTFI" 738,
    "YTLC" 514,
    "YTUC" 712;
}

// <uniquifier>: Use a unique and descriptive class name
// <weight>: Use a value from 200 to 1000

.nunito-sans-<uniquifier> {
  font-family: "Nunito Sans", sans-serif;
  font-optical-sizing: auto;
  font-weight: <weight>;
  font-style: normal;
  font-variation-settings:
    "wdth" 100,
    "YTLC" 500;
}

// <uniquifier>: Use a unique and descriptive class name
// <weight>: Use a value from 200 to 1000

.nunito-<uniquifier> {
  font-family: "Nunito", sans-serif;
  font-optical-sizing: auto;
  font-weight: <weight>;
  font-style: normal;
}

*/

.roboto-header {
  font-family: "Roboto", sans-serif;
  font-weight: 500;
  font-style: normal;
  font-size: xx-large;
}

.roboto-title {
  font-family: "Roboto", sans-serif;
  font-weight: 300;
  font-style: normal;
  font-size: 97px;
}

.nunito-title {
  font-family: "Nunito", sans-serif;
  font-optical-sizing: auto;
  font-weight: 700;
  font-style: normal;
  /* line-height: 4vw;  */
}

.nunito-sans-title {
  font-family: "Nunito Sans", sans-serif;
  font-optical-sizing: auto;
  font-weight: 900;
  font-style: normal;
  font-size: 57px;
  line-height: 56px; 
  font-variation-settings:
    "wdth" 200,
    "YTLC" 500;
}

.roboto-subtitle-bold {
  font-family: "Roboto", sans-serif;
  font-weight: 500;
  font-style: normal;
  font-size: xx-large;
  font-size: 57px;
  line-height: 66px; 
}

.nunito-text {
  font-family: "Nunito", sans-serif;
  font-optical-sizing: auto;
  font-weight: 500;
  font-style: normal;
  font-size: x-large;
}

.nunito-black {
  font-family: "Nunito", sans-serif;
  font-optical-sizing: auto;
  font-weight: 400;
  font-style: italic;
}

.nunito-route {
  font-family: "Nunito", sans-serif;
  font-optical-sizing: auto;
  font-weight: 600;
  font-style: normal;  
}

.nunito-sans-route {
  font-family: "Nunito Sans", sans-serif;
  font-optical-sizing: auto;
  font-weight: 400;
  font-style: normal; 
  font-variation-settings:
    "wdth" 100,
    "YTLC" 500;
}

.roboto-condensed-route {
  font-family: "Roboto Condensed", sans-serif;
  font-optical-sizing: auto;
  font-weight: 400;
  font-style: normal;
}

.roboto-condensed-200 {
  font-family: "Roboto Condensed", sans-serif;
  font-optical-sizing: auto;
  font-weight: 900;
  font-style: italic;
}

.roboto-flex-200 {
  font-family: "Roboto Flex", sans-serif;
  font-optical-sizing: auto;
  font-weight: 200;
  font-style: normal;
  font-variation-settings:
    "slnt" 0,
    "wdth" 100,
    "GRAD" 0,
    "XOPQ" 96,
    "XTRA" 468,
    "YOPQ" 79,
    "YTAS" 750,
    "YTDE" -203,
    "YTFI" 738,
    "YTLC" 514,
    "YTUC" 712;
}

.heading{
	/* color: rgba(0, 0, 0, 0.505);
	-webkit-text-stroke: 1px #0000006f; */
	text-shadow: 0px 4px 8px rgba(0, 0, 0, 0.674);
}

.glass{ 
    /* From https://css.glass */
    background: rgb(var(--v-theme-inverseSurface),0.1); /* rgba(255, 255, 255, 0.29);*/
    /* border-radius: 16px; */
    box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
    backdrop-filter: blur(9.6px);
    -webkit-backdrop-filter: blur(9.6px);
    /* border: 1px solid rgba(255, 255, 255, 0.3); */
}


 /*
 .svgIcon {
    width: 25px;
    height: 25px;
    fill:none;
     
    stroke-width: 2;
    scale: 0.8;    
  }
   

  #moonIcon {
    fill:   rgb(var(--v-theme-onSurface));
  }
  
  .heroSVG{
    width: 90px;
    height: 150px;   
    
  }

  .heroSVG > path {  
    scale: 6;
    
    stroke:   rgb(0,0,0,0);
    fill:  rgb(var(--v-theme-primary));   
  } */

</style>