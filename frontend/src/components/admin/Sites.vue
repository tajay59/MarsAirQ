<template>
 <div class="w-full h-dvh flex flex-col" >

    <div class=" h-20 flex flex-col justify-center ml-16 relative" >
        <VSpeedDial location="left center" transition="slide-x-reverse-transition" >
            <template v-slot:activator="{ props: activatorProps }">                      
                <VFab v-bind="activatorProps" icon density="compact" color="transparent"  elevation="0" class="absolute top-0 right-24" size="large"  >
                    <Icon  v-if="activatorProps['aria-expanded'] == 'false'" icon="line-md:close-to-menu-alt-transition" width="24" height="24" />
                    <Icon v-else icon="line-md:menu-to-close-alt-transition" width="28" height="28" />
                </VFab>                     
            </template>

            <VBtn key="1" icon title="Search" color="onSurface"  variant="text" @click="openSearch = true" >
                <Icon icon="tdesign:map-search-filled" width="24" height="24" />
            </VBtn>

            <VBtn key="2" icon title="Create a Site" color="onSurface" variant="text" @click="openCreateSite = true"  >
                <Icon icon="line-md:map-marker-plus-filled" width="24" height="24" />
            </VBtn>           
        </VSpeedDial>

        <Toast />
    </div>

    <div class="bg-neutral-200 dark:bg-neutral-800 h-full ml-10 rounded-tl-3xl overflow-hidden  border border-neutral-800" >
        <VContainer class="min-h-screen" fluid >
            
            <VRow class=" w-full  bg-neutral-200 dark:bg-neutral-800 pa-7 pl-10"   >
                <!-- <VCol cols="12" > <p  class="text-xl font-medium">Site Details</p></VCol> -->
                <VCol class=""  :cols="(mdAndUp)? 5 : 12"  >
                    <VCard class="pa-3 bg-neutral-100 dark:bg-neutral-700/[0.5] " flat rounded="lg"  >
                        
                        <div id="listmap" class="size-full rounded-lg " :class="[(mdAndUp)? 'min-h-[600px]':'min-h-[200px]']"  ></div>
                        <VCardItem v-if="!!spss" class="px-0" > 
                            <VContainer fluid class="pa-0" >
                                <VRow align="center" class="pa-0 ma-0 mb-1"  >
                                    <VCol cols="4" class="pa-0"  ><p>Latitude</p></VCol>
                                    <VCol cols="8" class="pa-0"  ><p class=" bg-neutral-200 dark:bg-neutral-700 rounded-lg text-sm pa-1 pl-2 " >{{ spss.lat }}</p></VCol>
                                </VRow>
                                
                                <VRow align="center" class="pa-0 ma-0"  >
                                    <VCol cols="4"  class="pa-0" ><p>Longitude</p></VCol>
                                    <VCol cols="8"  class="pa-0" ><p class=" bg-neutral-200 dark:bg-neutral-700 rounded-lg text-sm pa-1 pl-2" >{{ spss.lon }}</p></VCol>
                                </VRow>
                            </VContainer>
                        
                        </VCardItem>
                    </VCard>
                </VCol>

                <VCol class="mt-" :cols="(mdAndUp)? 7 : 12" >            
                    <VCard class="pa-3  bg-neutral-100 dark:bg-neutral-700/[0.5] relative " flat rounded="lg"  min-height="712" >
                        <VList rounded="lg" density="compact"    variant="flat" class="relative mx-auto h-full bg-transparent"  >
                            <VListItem  variant="text" :active="(!!spss)? spss.id == site.id : false" class="bg-neutral-100 dark:bg-neutral-600/[0.9] mb-2"  v-for="site in sitePages.pages[sitePages.page - 1]" @click="setMarkerOnListMap(site.lat,site.lon); AppStore.setSPSS(site)" :key="site.id" :value="site.id"  border rounded="lg" >
                                <template #title >
                                    <div class="flex justify-start" >
                                        <span class="text-sm font-bold" >{{site.name}}</span>                            
                                    </div>    
                                </template>
                                
                                <template #prepend>        
                                    <VIcon v-if="site.enabled" icon="mdi:mdi-map-marker-multiple" class="text-green-700 dark:text-green-500" title="Enabled"  />
                                    <VIcon v-else icon="mdi:mdi-map-marker-multiple" class="text-red-700 dark:text-red-400" title="Disabled"  />
                                </template>
                                <template #append>        
                                    <VBtn  flat rounded="lg" title="View Details" variant="tonal" @click="router.push({name:'Site',params:{id: site.id}});" color="tertiary" icon="mdi:mdi-open-in-new" density="compact" class="text-none text-sm" />
                                </template>
                            </VListItem>
                        </VList>
                        <VSpacer />
                        <VCardItem  class="absolute bottom-4 mx-auto w-full"     >
                            <VPagination v-model="sitePages.page" v-if="sitePages.count > 0" :length="sitePages.count" density="compact" @click="AppStore.getPage(sitePages.page)"  :total-visible="7"></VPagination>
                        </VCardItem>
                    </VCard>
                </VCol>
            </VRow>
            

            <VRow  >
                <VDialog v-model="openSearch" transition="dialog-bottom-transition" width="500" persistent >
                    <template v-slot:default="{ isActive }">
                        <VCard >
                            <VToolbar >
                                <VTextField v-model="siteSearchPages.search" variant="solo-inverted" rounded="lg" placeholder="Search for a Site ..." class="text-caption mx-1" hide-details >
                                    <template #append-inner >
                                        <Icon icon="tdesign:map-search-filled" width="24" height="24" />
                                    </template>
                                </VTextField>
                            </VToolbar>

                            <VCardItem>
                                <VList rounded="lg" density="compact"   variant="flat" class="relative mx-auto"  >
                                    <VListItem  variant="text" :active="false" class="bg-neutral-100 dark:bg-neutral-600/[0.3] mb-2"  v-for="site in siteSearchPages.pages[siteSearchPages.page - 1]" :key="site.id" :value="site.id"  border rounded="lg" >
                                        <template #title >
                                            <div class="flex justify-start" >
                                                <span class="text-sm font-bold" >{{site.name}}</span>                            
                                            </div>    
                                        </template>
                                        
                                        <template #prepend>        
                                            <VIcon v-if="site.enabled" icon="mdi:mdi-map-marker-multiple" class="text-green-700 dark:text-green-500" title="Enabled"  />
                                            <VIcon v-else icon="mdi:mdi-map-marker-multiple" class="text-red-700 dark:text-red-400" title="Disabled"  />
                                        </template>
                                        <template #append>        
                                            <VBtn  flat rounded="lg" variant="tonal" color="tertiary" @click="router.push({name:'Site',params:{id: site.id}})" icon="mdi:mdi-open-in-new" density="compact" class="text-none text-sm" />
                                        </template>
                                    </VListItem>
                                </VList>
                            </VCardItem>
                            <VCardItem >
                                
                                <VPagination v-model="siteSearchPages.page"  v-if="siteSearchPages.count > 0" :length="siteSearchPages.count" density="compact" @click="AppStore.getPage(siteSearchPages.page)"  :total-visible="7"></VPagination>
                            </VCardItem>

                            <VCardActions class="justify-end">
                                <VBtn text="Close" @click="isActive.value = false" ></VBtn>
                            </VCardActions>
                        </VCard>
                    </template>
                </VDialog>

                <VDialog v-model="openCreateSite" class="mx-5" transition="dialog-bottom-transition" width="100%" max-width="400"  persistent >
                    <template v-slot:default="{ isActive }">
                        <VCard  > 
                            <VCardTitle class="h-[300px] pa-2 rounded-lg" >
                                <div id="sitemap" class="size-full rounded-lg"  ></div>
                            </VCardTitle>

                            <VCardSubtitle class=" px-2 pt-3">
                                <p class=" text-2xl font-light"  style="font-family: Nunito;" >Add a Site</p>
                            </VCardSubtitle>

                            <VCardText class="pb-0 px-2">
                                <VTextField v-model="createSite.name" label="Name" class="rounded-lg border border-neutral-600 dark:border-neutral-50 overflow-clip" density="compact" variant="solo-inverted"  flat hide-details clearable /> 
                                <VTextField v-model="createSite.lat" label="Latitude" step="0.000001"  type="number" class="my-2 rounded-lg border border-neutral-600 dark:border-neutral-50 overflow-clip" density="compact" variant="solo-inverted"  flat hide-details  clearable />
                                <VTextField v-model="createSite.lon" label="Longitude" step="0.000001" type="number"  class="rounded-lg border border-neutral-600 dark:border-neutral-50 overflow-clip" density="compact" variant="solo-inverted"  flat hide-details  clearable />
                            </VCardText>

                            <VCardActions class="justify-end pa-4">
                                <VBtn text="Submit" @click="addSite()" class="text-none font-bold"  :disabled="enableSiteCreateBtn" :loading="createSiteLoading"  ></VBtn>
                                <VBtn text="Cancel" @click="isActive.value = false"   class="text-none"></VBtn>                          
                            </VCardActions>
                        </VCard>
                    </template>
                </VDialog>
            </VRow>
            
        </VContainer>
    </div>      

</div>

    
     
</template>

<script setup>
// IMPORTS   
import { storeToRefs } from 'pinia';
import { useAppStore } from '@/stores/appStore';
import { useUserStore} from '@/stores/userStore';
import { ref,shallowRef,reactive,watch ,onMounted,computed } from "vue";  
import { useDisplay } from 'vuetify';
import { useToast } from 'primevue/usetoast';
import { RouterLink, useRouter } from "vue-router";
import NewAccounts from '@/components/admin/NewAccounts.vue';
import Accounts from '@/components/admin/Accounts.vue';
import { VListItem } from 'vuetify/lib/components/index.mjs';
import _ from 'lodash';
import { Icon } from '@iconify/vue';
import { MaptilerLayer, MaptilerStyle } from "@maptiler/leaflet-maptilersdk";
import { map, tileLayer, marker,circleMarker, DomEvent } from 'leaflet';
import 'leaflet/dist/leaflet.css';
import L from 'leaflet';

// VARIABLES 
const router            = useRouter(); 
const UserStore         = useUserStore(); 
const AppStore          = useAppStore();
const toast             = useToast(); 
const { xs,smAndDown,smAndUp, mdAndUp }   = useDisplay();
const {spss,sitePages,siteSearchPages, createSiteLoading}   = storeToRefs(AppStore);
const compToRender      = ref({"selected": "registering","init":false, "list":[{"text":"New Registrations","name":"registering","component":"NewAccounts"}, {"text":"Accounts","name":"accounts","component":"Accounts"}]})
const tab               = ref("");
const openSearch        = ref(false);
const openCreateSite    = ref(false);
const blueIcon          = ref(null);
const greenIcon         = ref(null);
const redIcon           = ref(null);
const goldIcon          = ref(null);
const blackIcon         = ref(null);
const createSiteMarker  = shallowRef(null);
const listSiteMarker    = shallowRef(null);
const mymap             = shallowRef(null);
const listmap           = shallowRef(null);
const mtLayer           = new MaptilerLayer( {
                                apiKey: 'MacqP5qqahFSZdWB6tSq', // https://cloud.maptiler.com/maps/landscape/    https://docs.maptiler.com/leaflet/examples/vector-tiles-in-leaflet-js/
                                style: MaptilerStyle.STREETS.DARK //https://docs.maptiler.com/sdk-js/examples/built-in-styles/
                            } ); 
const createSite        = reactive({name:"", lat:"0",lon:"0"}); 
let searchTextID, timeoutVal = 1000; 


// PROPS
const props = defineProps({
    item:{type:String,default:""},
})


// WATCHERS
watch(openCreateSite,  (state) => {
    if(state){

        setTimeout(()=> {
            mymap.value = map('sitemap',{ zoomControl: false}).setView([14.5255555556, -75.8183333333], 4);     
            
            // /*
            tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}', {
                        attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
                        maxZoom: 18,
                        id: 'tedwardsuwi/cl0d2e6io000t14qntylpu4j4',
                        tileSize: 512,
                        zoomOffset: -1,
                        accessToken: 'pk.eyJ1IjoidGVkd2FyZHN1d2kiLCJhIjoiY2x3Y3RqMXY1MHpuNTJxcDA4emQ0ejQycCJ9.t-ENJ58Apo7e4gfhEidE8A'
                    }).addTo(mymap.value);
            // */    
        //    mtLayer.addTo(mymap.value) 
            mymap.value.whenReady(()=> {
                
                createSiteMarker.value.addTo(mymap.value) 
            })   
             
        },500) 
    } 
    else {
        mymap.value.remove();
    }
});

watch(createSite,  (site) => { 

    const lat = parseFloat(site.lat);
    const lon = parseFloat(site.lon);
 
    if(typeof(lat)  == "number" && typeof(lon) == "number"){
        if(!!lat && !!lon){                  
            mymap.value.flyTo([lat, lon], 13);
            createSiteMarker.value.setLatLng([lat, lon]);             
        } 
    }
});

watch( () => siteSearchPages.value.search, async (text) => {   
   
    clearTimeout(searchTextID); // prevent errant multiple timeouts from being generated
    if(!!text || text == ''){   
        if(text.length > 0){
            searchTextID = setTimeout(async () => {
            // SEND QUERY ONLY IF TEXT PASSES REGEX. THIS FILTERS OUT INVALID TEXT QUERIES
            if(/^[A-Za-z0-9]*$/.test(text) ){
                siteSearchPages.page = 0
                await AppStore.getPageCount(true);
                await AppStore.getPage(1,true);
            }
                }, timeoutVal);
        }     
    }
});

// COMPUTED PROPERTIES 
const enableSiteCreateBtn = computed(() => 
     {
       
      if(!!createSite.lat && !!createSite.lon  && !!createSite.name){
        if(createSite.name.length > 3 && createSite.lat.length > 3  && createSite.lon.length > 3 )
            return false
      }
      return true        
     } 
  ) 

const renderComp = computed(() => 
     {
      if(compToRender.value.selected == 'registering')
        return NewAccounts
      else if (compToRender.value.selected == 'accounts')
        return Accounts
     }     

  ) 

const activeState = computed(() => {
    // THIS IS A DYNAMIC GETTER
    return (id) => {
    if (!!selectedAccount.value){
        if(selectedAccount.value.id == id){
            return true
        }
    }
    
    return false
    }
}); 


// FUNCTIONS
const addSite = async () => {
    let result = await AppStore.createSite(createSite.name, createSite.lat, createSite.lon);
 
    switch (result) {
        case "added":
            AppStore.getPageCount();
            AppStore.getPage(1);
            openCreateSite.value = false;
            createSite.name  = "";
            createSite.lat  = "0";
            createSite.lon  = "0";
            toast.add({ severity: 'success', summary: 'CREATED', detail: 'Successfully created new SITE!', life: 3000 });             
            break;
        
        case "failed":
            AppStore.getPageCount();
            AppStore.getPage(1);
            openCreateSite.value = false;
            toast.add({ severity: 'success', summary: 'FAILED', detail: 'Unable to create new SITE!', life: 3000 });         
            break;  

        default:
            toast.add({ severity: 'error', summary: 'Request Failed', detail: 'Request failed!', life: 3000 });  
            break;
    }
}

 

const createIcon = (name) => {      
    return new L.Icon({
        iconUrl: `/src/assets/${name}.png`,
        shadowUrl: '/src/assets/marker-shadow.png',
        // iconUrl: `../src/assets/${name}.png`,
        // shadowUrl: '../src/assets/marker-shadow.png',
        iconSize: [50, 50],
        iconAnchor: [25.5, 49.5],
        popupAnchor: [1, -34],
        shadowSize: [41, 41],
        shadowAnchor : [13,40]
    });  
  }

const setMarkerOnListMap = (lat, lon) => {   
    listmap.value.setZoom(11);
    listmap.value.setView([lat, lon]);

    if(listSiteMarker.value) {        
        listSiteMarker.value.setLatLng([lat, lon]);  
    }
    else {
        listSiteMarker.value  = circleMarker([lat, lon],{radius: 50, color:"#00ff00"})  
        .on('click', (e) => { 
            console.log("Clicked marker");
            })
        .bindPopup('Site location')    
        .addTo(listmap.value)
    }
       
}

onMounted(() => {

    blueIcon.value  = createIcon("bluestripe");
    redIcon.value   = createIcon("redstripe");
    greenIcon.value = createIcon("greenstripe");
    goldIcon.value  = createIcon("goldstripe");
    blackIcon.value = createIcon("blackstripe");

    createSiteMarker.value = marker([14.5255555556, -75.8183333333],{title: "Site",opacity:1.0,riseOnHover:true })
        .on('click', (e) => { 
            console.log("Clicked marker");
            })  
        .bindPopup('Prospective site location')  
        .setIcon(greenIcon.value)      
    
    listmap.value =  map('listmap',{ zoomControl: false}).setView([14.5255555556, -75.8183333333], 4);     
    
    // /*
    tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}', {
                attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
                maxZoom: 18,
                id: 'tedwardsuwi/cl0d2e6io000t14qntylpu4j4',
                tileSize: 512,
                zoomOffset: -1,
                accessToken: 'pk.eyJ1IjoidGVkd2FyZHN1d2kiLCJhIjoiY2x3Y3RqMXY1MHpuNTJxcDA4emQ0ejQycCJ9.t-ENJ58Apo7e4gfhEidE8A'
            }).addTo(listmap.value);
    // */    
    // mtLayer.addTo(mymap.value) 

 
})

 
 
</script>

<style>
/*   Style */

body {
    font-family: Nunito;
}

 
</style>