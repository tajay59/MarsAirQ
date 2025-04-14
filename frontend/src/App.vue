<template>
  <VApp class="bg-surface"   > 

    <!-- <Transition name="fade"  >       -->
      <!-- <TopAppBar v-if="!['Signup','PasswordReset', 'Login'].includes(route.name) && !smAndDown"  /> -->
    <!-- </Transition> -->
   

    <!-- v-if="!['Login','Signup','PasswordReset'].includes(route.name) ||" -->
    <!-- <NavDrawer  v-if="['Map','Live','Dashboard','Analysis'].includes(route.name)"  /> -->
    <Notification/>
   
    <VMain  > 
      <RouterView v-slot="{ Component, route}"> 
        <transition :name="route.meta.transition || 'fade'" mode="out-in" >
          <component :is="Component" />
        </transition>
      </RouterView>
    </VMain>

    <!-- <Footer v-if="route.name !== 'Tour'"  />    -->
    <BottomNavBar v-if="!['Login','Signup','PasswordReset'].includes(route.name)"  :active="smAndDown" />       
  
  </VApp>
</template>

<script setup>
  // IMPORTS
  import { ref,reactive, onMounted,computed, watch,onBeforeMount, onBeforeUnmount, toRaw} from 'vue';
  import TopAppBar from '@/components/TopAppBar.vue';
  import BottomNavBar from '@/components/BottomNavBar.vue';
  import Footer from '@/components/Footer.vue';
  import { RouterLink, RouterView } from 'vue-router'
  import { useRoute, useRouter } from "vue-router";
  import { useUserStore } from '@/stores/userStore';
  import { useMqttStore } from '@/stores/mqttStore'; // Import Mqtt Store
  import { storeToRefs } from "pinia";
  import { useTheme } from 'vuetify';
  import { useDisplay } from 'vuetify';
  import NavDrawer from './components/NavDrawer.vue';

  

// VARIABLES
const { xs,smAndDown,smAndUp, mdAndUp }   = useDisplay();
const UserStore         = useUserStore();
const {id,loggedIn,image,suball, darkmode, mqtt_sub_credentials} = storeToRefs(UserStore); 
const route             = useRoute(); 
const theme             = useTheme();
const Mqtt              = useMqttStore();
const {
  username,
  password,
   subs,
   unsubs,
   subTopics,
   connected,
   payload,
   payloadTopic } = storeToRefs(Mqtt);
let subsID = "";
let unsubsID = "";
// theme.global.current.value.colors.onSurfaceVariant

// Watchers
watch(darkmode,  (mode) => {
    // appDarkMode.value = mode;

    theme.global.name.value = mode ?  'dark' : 'light';
    localStorage.setItem("theme",mode ? 'dark' : 'light');  

    if(theme.global.current.value.dark)
          document.documentElement.classList.replace('light','dark');            
    else 
        document.documentElement.classList.replace('dark','light'); 
});




watch(suball, async (sub)=> { 
    Mqtt.clearSubs();

   setTimeout(() => { 
      if(sub){ Mqtt.subTo("/station/data/#"); }
      else {  Mqtt.subTo(mqtt_sub_credentials.value.topic); } 
    }, 1000)
  })
 

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
onBeforeMount(()=> {
  // SAVE THEME TO LOCALSTORAGE MAKING IT PERSIST BROWSER REFRESH
  Mqtt.clearSubs();
  UserStore.getAllSites();

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
    clearInterval(subsID)
});
 
</script>

<style >
*,
*::before,
*::after {
  box-sizing: border-box;
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

  
  ::-webkit-scrollbar { width: 5px; height: 5px; } /* SCROLLBAR SETTING */
  ::-webkit-scrollbar-track { box-shadow: inset 0 0 5px grey; border-radius: 10px; }   /* Track */
  ::-webkit-scrollbar-thumb { background: rgb(var(--v-theme-primary)) ; border-radius: 10px; }    /* Handle */ 
  ::-webkit-scrollbar-thumb:hover { background: rgb(var(--v-theme-secondary)); }   /* Handle on hover */

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