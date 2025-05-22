<template>
    <div class="mt-10  size-full relative" >
        <div :id="mapcontainer" class="w-[100%]  h-[100%]  rounded-lg"  ></div> 

       
        <VBottomSheet :model-value="openLiveSheet"  height="290" width="300" inset persistent content-class="bg-transparent mx-auto" class="flex place-content-center "  >
            <VSheet rounded="t-lg" color="transparent"  class="pa-0" >
        
            <VContainer class="h-full w-full pa-10 bg-neutral-50 dark:bg-neutral-950 rounded-t-lg" fluid >
                <VRow class="" justify="space-between" >
                    <div class=" " v-if="!!selectedDevice"> 
                        <p   class="text-none text-xl font-bold" >{{ _.capitalize(selectedDevice.name)}}</p>
                    </div>               
                    <VBtn icon="mdi:mdi-close" @click="openLiveSheet = false; selected = null"  title="Close" color="onSurface" size="24" variant="flat" density="compact"  />
                    <VDivider :opacity="100" class="border-neutral-300 dark:border-neutral-600 my-3"  />
                </VRow>
                
                <VRow class=" pa-0 rounded-lg">               
                <VCol   class=" rounded-lg pa-0 flex flex-col gap-1" >                     
                    <VBtn v-for="name in Object.keys(dataDetails)" @click="copyToClipboard(name)" width="200" title="copy"   color="transparent" class="flex justify-between text-none border-b  !text-neutral-700 dark:!text-neutral-200" flat rounded="lg" variant="text" >                               
                        <template #append >
                            <Icon icon="solar:copy-bold" width="24" height="24"  />   
                        </template>      
                        <p class="text-none text-xl font-normal flex-1" >{{ _.capitalize(name) }}</p>                    
                    </VBtn>                    
                </VCol>
                </VRow>
            </VContainer>
            </VSheet>
        </VBottomSheet>
       
    </div>
    </template>
    
    <script setup>
    // IMPORTS   
    import { storeToRefs } from 'pinia';
    import { useUserStore} from '@/stores/userStore';
    import { ref,watch ,onMounted,computed, shallowRef } from "vue";  
    import { RouterLink, useRouter } from "vue-router";
    import { useAppStore } from '@/stores/appStore';
    import { useToast } from 'primevue/usetoast';
    import _ from 'lodash';
    import { Icon } from '@iconify/vue';

    import { MaptilerLayer, MaptilerStyle } from "@maptiler/leaflet-maptilersdk";
    import 'leaflet/dist/leaflet.css';
    import 'leaflet.markercluster'   // https://github.com/leaflet/Leaflet.markercluster
    import 'leaflet.markercluster/dist/MarkerCluster.css'
    import 'leaflet.markercluster/dist/MarkerCluster.Default.css'

    import { map, tileLayer, marker, DomEvent,  Popup } from 'leaflet';
    import L from 'leaflet';
        
    // VARIABLES 
    const route                     = useRouter(); 
    const UserStore                 = useUserStore();
    const AppStore                  = useAppStore();
    const mymap                     = shallowRef(null);
    const markers                   = shallowRef(L.markerClusterGroup({chunkedLoading: false,showCoverageOnHover:false,animateAddingMarkers:true})); 
    const {userSites,mqtt_sub_credentials}  = storeToRefs(UserStore);
    const toast                     = useToast();
    const blueIcon                  = ref(null);
    const greenIcon                 = ref(null);
    const redIcon                   = ref(null);
    const goldIcon                  = ref(null);
    const blackIcon                 = ref(null);
    const stations                  = ref({});  
    const sitesLoading              = ref(false);
    const mapcontainer              = ref(`container${_.random(0,100000)}`);
    const selectedDevice            = ref(null);
    const selected                  = ref(null);
    const dataDetails               = ref({"id":"","username":"","passkey":"","owner":""})


    const mtLayer                   = new MaptilerLayer( {
                                        apiKey: 'MacqP5qqahFSZdWB6tSq', // https://cloud.maptiler.com/maps/landscape/    https://docs.maptiler.com/leaflet/examples/vector-tiles-in-leaflet-js/
                                        style: MaptilerStyle.STREETS.DARK //https://docs.maptiler.com/sdk-js/examples/built-in-styles/
                                        } ); 
    
    
    
    // PROPS
    const props = defineProps({
        item:{type:String,default:""},
    })
    
    // WATCHERS
    watch(() => userSites, (sites) => {
        
        if(!!sites){
        let keys = Object.keys(stations.value); 
        setSiteMarkers(sites);
        /*
        sites.forEach( site => {
            site.devices.forEach( device => {
                if(!keys.includes(device.id)) { 
                
                    // Create marker
                    let myMarker = marker([device.lat, device.lon],{title: _.capitalize(device.name),opacity:1.0,riseOnHover:true })
                        .bindPopup(`${_.capitalize(device.name)}`) 
                        .on('click', (e) => { selected.value =  device.id })
                        .setIcon(goldIcon.value)                       
                    
                        // Store marker
                        stations.value[device.id] = myMarker ;
                        markers.value.addLayer(myMarker);
                        mymap.value.addLayer(markers.value);  

                        }
            })
        })*/
        }
})
    
    // COMPUTED PROPERTIES
    const openLiveSheet = computed(()=> !!selected.value );
    
    watch(selected, (device)=>{
            if(!!userSites.value){ 
                
            userSites.value.forEach( site => {
                site.devices.forEach( dev => {
                    if(dev.id == device){
                        selectedDevice.value = {...dev};
                        dataDetails.value.id = dev.id
                        dataDetails.value.owner = mqtt_sub_credentials.value.username
                        dataDetails.value.username = site.username
                        dataDetails.value.passkey = site.id
                    }
                    
                });
            })
        }
    })
    
    // FUNCTIONS

    const copyToClipboard = (name) => { 
        navigator.clipboard.writeText(dataDetails.value[name]);
        toast.add({ severity: 'contrast', summary: 'COPIED', detail: `${_.toUpper(name)} successfully COPIED to clipboard`, life: 3000 });  
    }

    onMounted(() => { 
        // AppStore.getSites();
        L.Popup.prototype._animateZoom = (e) => {
        // SOLVE ERROR WHICH OCCURS WHEN ZOOMING AFTER OPENING A POPUP    
        if (!this) { return }
        
        var pos = this._map._latLngToNewLayerPoint(this._latlng, e.zoom, e.center),
            anchor = this._getAnchor()
        DomUtil.setPosition(this._container, pos.add(anchor))
        }

       

        blueIcon.value  = createIcon("bluestripe");
        redIcon.value   = createIcon("redstripe");
        greenIcon.value = createIcon("greenstripe");
        goldIcon.value  = createIcon("goldstripe");
        blackIcon.value = createIcon("blackstripe");

        mymap.value = map(mapcontainer.value).setView([13.176257678629065, -59.54376034587126], 11);  
        
    
        
        tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}', {
                    attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
                    maxZoom: 18,
                    id: 'tedwardsuwi/cl0d2e6io000t14qntylpu4j4',
                    tileSize: 512,
                    zoomOffset: -1,
                    accessToken: 'pk.eyJ1IjoidGVkd2FyZHN1d2kiLCJhIjoiY2x3Y3RqMXY1MHpuNTJxcDA4emQ0ejQycCJ9.t-ENJ58Apo7e4gfhEidE8A'
                }).addTo(mymap.value);
        
        // mtLayer.addTo(mymap.value);

        // getUserSites();
        setSiteMarkers(userSites.value)
    })
    
    
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
  
  const createElement = str => {
    const el = document.createElement('div');
    el.innerHTML = str;
    return el.firstElementChild;
  };

  const setSiteMarkers = (sites) => {
    if(!!sites){
        let keys = Object.keys(stations.value); 
        // markers.value.bindPopup('Name') 

        markers.value.on('clustermouseover', function (e) {
            // var latLngBounds = a.layer.getBounds();
            console.log("Hovering")
        });

        sites.forEach( site => {
            site.devices.forEach( device => {
                if(!keys.includes(device.id)) { 
                // Create marker
                let myMarker = marker([device.lat, device.lon],{title: _.capitalize(device.name),opacity:1.0,riseOnHover:true })
                    .bindPopup(`${_.capitalize(device.name)}`) 
                    .on('click', (e) => { selected.value =  device.id })
                    .setIcon(goldIcon.value)                       
                
                    // Store marker
                    stations.value[device.id] = myMarker ;
                    markers.value.addLayer(myMarker);
                    mymap.value.addLayer(markers.value);  

                        }
            })
        })
        }
  }

  const getUserSites = async () => {
        let [status, result] = await AppStore.getSites(sitesLoading.value);

   
        switch (status) {
            case "found":
                setSiteMarkers(result)
                // toast.add({ severity: 'success', summary: 'UPDATED', detail: 'Station successfully RESET!', life: 3000 });  
                break;
            
            case "failed":                
                toast.add({ severity: 'error', summary: 'FAILED', detail: 'Unable to RESET Station', life: 3000 });  
                break;  

            default:
                toast.add({ severity: 'error', summary: 'Request Failed', detail: 'Station RESET request failed!', life: 3000 });  
                break;
        }
        }
     
    </script>
    
    <style>
    /*   Style */
    
     
    </style>