<template>
 <div class="w-full h-dvh flex flex-col " >

    <div class=" h-20 flex flex-col justify-center ml-16 relative" >
       <!-- TOP BAR -->          
    </div>

    <div class="bg-neutral-200 dark:bg-neutral-800 h-full ml-10 rounded-tl-3xl overflow-hidden  border border-neutral-800" >
        <VContainer class="min-h-screen" fluid >
            
            <VRow class=" w-full  bg-neutral-200 dark:bg-neutral-800 pa-7 pl-10"   >
                <!-- <VCol cols="12" > <p  class="text-xl font-medium">Site Details</p></VCol> -->
                <VCol class=""  :cols="(mdAndUp)? 5 : 12"  >
                    <VCard class="pa-3 bg-neutral-100 dark:bg-neutral-700/[0.5] " flat rounded="lg"  >
                        
                        <div :id="mapcontainer" class="size-full rounded-lg " :class="[(mdAndUp)? 'min-h-[600px]':'min-h-[200px]']"  ></div>
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
                    <VCard class="pa-3  bg-neutral-100 dark:bg-neutral-700/[0.5] relative !overflow-y-scroll" flat rounded="lg"  min-height="712" max-height="713"  >
                       
                          <PanelMenu :model="menuItems" multiple class="w-full md:w-96">
                             <template #item="{ item }">
                                <a v-if="item.type == 'main'" v-ripple class="flex justify-between align-center px-4 py-2 cursor-pointer group">
                                    <div class="ml-2 flex gap-3 place-content-center">
                                        <Icon :icon="item.icon" class="!text-neutral-600 dark:!text-neutral-400" width="24" height="24"  />
                                        <span :class="[{ 'font-semibold': item.items }]">{{ item.label }}</span>  
                                    </div>                              
                                  
                                    
                                    <div class="flex gap-3 place-content-center">
                                        <span v-if="item.shortcut" class="ml-auto border border-surface rounded bg-emphasis text-muted-color text-xs p-1">{{ item.shortcut }}</span>
                                        <Badge v-if="item.badge" class="ml-auto" :value="item.badge" />
                                        <VBtn @click="openDeleteEntity = true; deleteEntityReq.name = _.toUpper(item.label);  deleteEntityReq.id = item.id" icon flat density="compact" variant="text"> 
                                            <Icon icon="ic:baseline-delete" class="!text-neutral-600 dark:!text-neutral-400" width="24" height="24"  />
                                        </VBtn>
                                    </div>                     
                                    
                                </a>
                                <a v-else-if="item.type == 'mainitems'" v-ripple class="flex items-center px-4 py-2 cursor-pointer group">                 
                                       
                                    <Icon :icon="item.icon" class="!text-neutral-600 dark:!text-neutral-400" width="24" height="24"  />
                                    <span :class="['ml-2', { 'font-semibold': item.items }]">{{ item.label }}</span>                                
                                    <Badge v-if="item.badge" class="ml-auto" :value="item.badge" />
                                    <span v-if="item.shortcut" class="ml-auto border border-surface rounded bg-emphasis text-muted-color text-xs p-1">{{ item.shortcut }}</span>
                                </a>
                                <!-- AppStore.setSPSS(site) -->
                                <a v-else v-ripple class="flex items-center px-4 py-2 cursor-pointer group" @click="setMarkerOnListMap(item.lat,item.lon)">
                                     <div class="flex justify-between  w-full" >
                                        <span :class="['ml-2', { 'font-semibold': item.items }]">{{ item.label }}</span>
                                        <div class="flex gap-3">
                                            <VBtn @click="router.push({name:'Site',params:{id: item.site}})" icon flat density="compact" variant="text"> 
                                                <Icon :icon="item.icon" class="!text-neutral-600 dark:!text-neutral-400" width="24" height="24"  />
                                            </VBtn>
                                            <VBtn @click="openDeleteSite = true; deleteSiteReq.name = _.toUpper(item.label); deleteSiteReq.entity = _.toUpper(item.name); deleteSiteReq.id = item.site" icon flat density="compact" variant="text"> 
                                                <Icon icon="ic:baseline-delete" class="!text-neutral-600 dark:!text-neutral-400" width="24" height="24"  />
                                            </VBtn>
                                        </div>
                                     </div>
                                    
                                
                                    <Badge v-if="item.badge" class="ml-auto" :value="item.badge" />
                                    <span v-if="item.shortcut" class="ml-auto border border-surface rounded bg-emphasis text-muted-color text-xs p-1">{{ item.shortcut }}</span>
                                </a>
                            </template>
                        </PanelMenu>

                        <VSpacer />
                        <VCardItem  class=" mx-auto w-full mt-10"     >
                            <VPagination v-model="sitePages.page" v-if="sitePages.count > 0" :length="sitePages.count" density="compact" @click="AppStore.getPage(sitePages.page)"  :total-visible="7"></VPagination>
                        </VCardItem>
                    </VCard>
                </VCol>
            </VRow>
            

            <VRow  >
                <VDialog v-model="openSiteSearch" transition="dialog-bottom-transition" width="500" persistent >
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
                                <div :id="sitemapcontainer" class="size-full rounded-lg"  ></div>
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

                <VDialog v-model="openCreateEntity" class="mx-5" transition="dialog-bottom-transition" width="100%" max-width="400"  persistent >
                    <template v-slot:default="{ isActive }">
                        <VCard  > 

                            <VCardSubtitle class=" px-2 pt-3">
                                <p class=" text-2xl font-light"  style="font-family: Nunito;" >Create Entity</p>
                            </VCardSubtitle>

                            <VCardText class="pb-0 px-2 flex flex-col gap-2">
                                <VTextField v-model="createEntity.name" label="Name" class="rounded-lg border border-neutral-600 dark:border-neutral-50 overflow-clip" density="compact" variant="solo-inverted"  flat hide-details clearable />                               
                                <Select v-model="createEntity.country" :options="caribbeanCountries" optionLabel="name" optionValue="code"  checkmark :highlightOnSelect="false" placeholder="Select a Country" class="w-full" pt:overlay="!z-[5000]" />
                            </VCardText>

                            <VCardActions class="justify-end pa-4">
                                <VBtn text="Submit" @click="addEntity()" class="text-none font-bold"  :disabled="enableEntityCreateBtn" :loading="createEntityLoading"  ></VBtn>
                                <VBtn text="Cancel" @click="isActive.value = false"   class="text-none"></VBtn>                          
                            </VCardActions>
                        </VCard>
                    </template>
                </VDialog>

                <VDialog v-model="openDeleteSite" class="mx-5" transition="dialog-bottom-transition" width="100%" max-width="400"  persistent  >
                <!-- DELETE SITE -->
                    <VCard   class="border-t-4border-rose-600 dark:border-rose-300 " density="compact"  > 
                
                    <template #title >
                        <div class="flex place-content-center" >
                            <Icon icon="mdi:delete-empty" class="!text-neutral-600 dark:!text-neutral-400" width="64" height="64"  />
                        </div>
                    
                    </template>
                    <template #text >
                        <p >You are about to  <strong class="font-bold text-rose-700" > Delete </strong> {{ _.toUpper(deleteSiteReq.name) }} from {{ _.toUpper(deleteSiteReq.entity) }}. Are you sure you want to continue?</p>
                    </template>

                        <template v-slot:actions>
                        <VBtn text="Delete" class="text-subtitle-2" color="onSurface" width="100" :loading="deleteSiteLoading" @click="deleteSite()" />
                        <VBtn text="Cancel" class="text-subtitle-2" color="onSurface" width="100"    @click="openDeleteSite = false" />  
                        </template>
                    </VCard>
            </VDialog>

            <VDialog v-model="openDeleteEntity" class="mx-5" transition="dialog-bottom-transition" width="100%" max-width="400"  persistent  >
                <!-- DELETE ENTITY -->
                    <VCard   class="border-t-4border-rose-600 dark:border-rose-300 " density="compact"  > 
                
                    <template #title >
                        <div class="flex place-content-center  " >
                            <Icon icon="mdi:delete-empty" class="!text-neutral-600 dark:!text-neutral-400" width="64" height="64"  />
                        </div>
                    
                    </template>
                    <template #text >
                        <p >You are about to  <strong class="font-bold text-rose-700" > Delete </strong> {{ _.toUpper(deleteEntityReq.name) }} along with all associated Sites. Are you sure you want to continue?</p>
                    </template>

                        <template v-slot:actions>
                        <VBtn text="Delete" class="text-subtitle-2" color="onSurface" width="100" :loading="deleteEntityLoading" @click="deleteEntity()" />
                        <VBtn text="Cancel" class="text-subtitle-2" color="onSurface" width="100"    @click="openDeleteEntity = false" />  
                        </template>
                    </VCard>
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
import { ref,shallowRef,reactive,watch ,onMounted,computed, onBeforeMount } from "vue";  
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
const {
    spss,
    sitePages,
    siteSearchPages,
    createSiteLoading,
    createEntityLoading,
    openCreateEntity,
    openSiteSearch,
    openCreateSite,
    entities,
    caribbeanCountries}   = storeToRefs(AppStore);
const openDeleteSite    = ref(false);
const compToRender      = ref({"selected": "registering","init":false, "list":[{"text":"New Registrations","name":"registering","component":"NewAccounts"}, {"text":"Accounts","name":"accounts","component":"Accounts"}]})
const tab               = ref(""); 
const blueIcon          = ref(null);
const greenIcon         = ref(null);
const redIcon           = ref(null);
const goldIcon          = ref(null);
const blackIcon         = ref(null);
const createSiteMarker  = shallowRef(null);
const listSiteMarker    = shallowRef(null);
const mymap             = shallowRef(null);
const listmap           = shallowRef(null);
const deleteSiteReq     = ref({"id":"","name":"","entity":""});
const deleteEntityReq   = ref({"id":"","name":""});
const deleteSiteLoading = ref(false);
const deleteEntityLoading = ref(false);
const mapcontainer      = ref(`container${_.random(0,100000)}`);
const sitemapcontainer  = ref(`container${_.random(0,100000)}`);
const mtLayer           = new MaptilerLayer( {
                                apiKey: 'MacqP5qqahFSZdWB6tSq', // https://cloud.maptiler.com/maps/landscape/    https://docs.maptiler.com/leaflet/examples/vector-tiles-in-leaflet-js/
                                style: MaptilerStyle.STREETS.DARK //https://docs.maptiler.com/sdk-js/examples/built-in-styles/
                            } ); 
const createSite        = reactive({name:"", lat:"0",lon:"0", entity:""}); 
const createEntity      = reactive({name:"", country:""}); 
const openDeleteEntity  = ref(false);
let searchTextID, timeoutVal = 1000; 

const items = ref([
    {
        label: 'cimh',
        icon: 'pi pi-file',
        items: [
            { label: 'Add Site', icon:"fluent:slide-add-32-filled", command: () => { openCreateSite.value = true; createSite.entity = "one"} },
            {
                label: 'Debbles',
                icon: 'pi pi-file',
            },
            {
                label: 'Ragged',
                icon: 'pi pi-image',
            }
        ]
    },
    {
        label: 'Massey Distr',
        icon: 'pi pi-cloud',
        items: [
            {
                label: 'Warrens',
                icon: 'pi pi-cloud-upload'
            },
            {
                label: 'Bridgetown',
                icon: 'pi pi-cloud-download'
            },
            {
                label: 'Holetown',
                icon: 'pi pi-refresh'
            }
        ]
    },
    {
        label: 'Caves',
        icon: 'pi pi-desktop',
        items: [
            {
                label: 'Harrisons',
                icon: 'pi pi-mobile'
            },
            {
                label: 'Chukka',
                icon: 'pi pi-desktop'
            },
            {
                label: 'YS Falls',
                icon: 'pi pi-tablet'
            }
        ]
    }
]);

// PROPS
const props = defineProps({
    item:{type:String,default:""},
})


// WATCHERS
watch(openCreateSite,  (state) => {
    if(state){

        setTimeout(()=> {
            mymap.value = map(sitemapcontainer.value,{ zoomControl: false}).setView([14.5255555556, -75.8183333333], 4);     
            
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
const menuItems = computed(() =>{
    let list = [];
    entities.value.forEach((entity) => {
        let item = {"label": _.capitalize(entity.name),"type":"main","icon":"iconamoon:location-pin-duotone","id": entity.id,"items":[{ label: 'Add Site',"type":"mainitems", icon:"fluent:slide-add-32-filled", command: () => { openCreateSite.value = true; createSite.entity = entity.id} }]}
        
        entity.sites.forEach( site => item.items.push({"label": site.name, "icon": "eva:external-link-outline","type":"site", "site": site.id,"name": entity.name, "lat": site.lat,"lon": site.lon}));  // command: ()=> {router.push({name:'Site',params:{id: site.id}}) }
        
        item["badge"] = (item.items.length > 1)? item.items.length -1 : 0
        list.push(item);
    });

    return list
})

const enableSiteCreateBtn = computed(() => 
     {
       
      if(!!createSite.lat && !!createSite.lon  && !!createSite.name){
        if(createSite.name.length > 3 && createSite.lat.length > 3  && createSite.lon.length > 3 )
            return false
      }
      return true        
     } 
  ) 

const enableEntityCreateBtn = computed(() => 
     {
       
      if(!!createEntity.name && !!createEntity.country ){
        if(createEntity.name.length >= 3 && createEntity.country.length == 2 )
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
const deleteSite = async () => {
    let result = await AppStore.removeSite(deleteSiteReq.value.id,deleteSiteLoading);
 
    switch (result) {
        case "deleted":   
            AppStore.getEntities();                    
            openDeleteSite.value = false;
            deleteSiteReq.value.entity = "";
            deleteSiteReq.value.id = "";
            deleteSiteReq.value.name = "";
            
            toast.add({ severity: 'success', summary: 'DELETED', detail: 'Successfully deleted SITE!', life: 3000 });             
            break;
        
        case "failed":             
            openDeleteSite.value = false;
            toast.add({ severity: 'error', summary: 'FAILED', detail: 'Unable to delete SITE!', life: 3000 });         
            break;  

        default:
            toast.add({ severity: 'error', summary: 'Request Failed', detail: 'Request failed!', life: 3000 });  
            break;
    }
}

const deleteEntity = async () => {
    let result = await AppStore.removeEntity(deleteEntityReq.value.id,deleteEntityLoading);
 
    switch (result) {
        case "deleted":   
            AppStore.getEntities();                    
            openDeleteEntity.value = false; 
            deleteEntityReq.value.id = "";
            deleteEntityReq.value.name = "";
            
            toast.add({ severity: 'success', summary: 'DELETED', detail: 'Successfully deleted ENTITY!', life: 3000 });             
            break;
        
        case "failed":             
            openDeleteEntity.value = false;
            toast.add({ severity: 'error', summary: 'FAILED', detail: 'Unable to delete ENTITY!', life: 3000 });         
            break;  

        default:
            toast.add({ severity: 'error', summary: 'Request Failed', detail: 'Request failed!', life: 3000 });  
            break;
    }
}

const addSite = async () => {
    let result = await AppStore.createSite(createSite.name, createSite.lat, createSite.lon, createSite.entity);

    switch (result) {
        case "added":
            AppStore.getEntities();
            openCreateSite.value = false;
            createSite.name  = "";
            createSite.lat  = "0";
            createSite.lon  = "0";
            createSite.entity = "";
            toast.add({ severity: 'success', summary: 'CREATED', detail: 'Successfully created new SITE!', life: 3000 });             
            break;
        
        case "failed":
            openCreateSite.value = false;
            toast.add({ severity: 'error', summary: 'FAILED', detail: 'Unable to create new SITE!', life: 3000 });         
            break;  

        default:
            toast.add({ severity: 'error', summary: 'Request Failed', detail: 'Request failed!', life: 3000 });  
            break;
    }
}


const addEntity = async () => {
    let result = await AppStore.createEntity(createEntity.name, createEntity.country);
 
    switch (result) {
        case "created":
            openCreateEntity.value = false;
            createEntity.name  = "";
            createEntity.country  = ""; 
            toast.add({ severity: 'success', summary: 'CREATED', detail: 'Successfully created new Entity!', life: 3000 });             
            break;
        
        case "exist":
            openCreateSite.value = false;
            createSite.name  = "";
            createSite.lat  = "0";
            createSite.lon  = "0";
            toast.add({ severity: 'success', summary: 'EXIST', detail: 'ENTITY already exist!', life: 3000 });             
            break;

        case "failed":
            openCreateEntity.value = false;
            toast.add({ severity: 'success', summary: 'FAILED', detail: 'Unable to create new Entity!', life: 3000 });         
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

onBeforeMount(()=>{
    AppStore.getEntities();
})

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
    
    listmap.value =  map(mapcontainer.value,{ zoomControl: false}).setView([14.5255555556, -75.8183333333], 4);     
    
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