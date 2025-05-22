<template>
    <div  >                
        <RouterView />   
        
    </div>       
</template>

<script setup>
// IMPORTS   

import { ref,watch ,onMounted,computed, reactive } from "vue";   

import { useUserStore } from '@/stores/userStore'; 
import { useAppStore } from '@/stores/appStore';
import { useRoute ,useRouter } from "vue-router";
import { useDisplay } from 'vuetify';
import _ from 'lodash';
import { storeToRefs } from 'pinia';
import { Icon } from '@iconify/vue';

// VARIABLES 
const router            = useRouter();
const route             = useRoute(); 
const UserStore         = useUserStore(); 
const AppStore          = useAppStore();
const { xs,smAndDown,smAndUp, mdAndUp }   = useDisplay();
const {id,loggedIn,image, darkmode, selectedStation, userSites, layout} = storeToRefs(UserStore);
const {dashboardMenu}   = storeToRefs(AppStore);


// PROPS
const props = defineProps({
    item:{type:String,default:""},
})

// WATCHERS

 
// COMPUTED PROPERTIES


// FUNCTIONS

onMounted(()=>{ 
    
})

 
</script>

<style>
/*   Style */

 
</style>