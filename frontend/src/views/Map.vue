  <template>  
    
    <div  class="w-screen h-screen  relative flex items-center justify-center" >
       
      <div id="map" class="w-[100%]  h-[100%]"  ></div> 

      <VBottomSheet :model-value="openLiveSheet" height="350" persistent content-class="bg-transparent"  >
        <VSheet rounded="t-lg" color="surface" >
      
          <VContainer class="h-full w-full pb-0 " fluid >
            <VRow class=" h-full pa-0 rounded-lg">
              <VCol  class="  border-r-2 border-neutral-300 rounded-lg overflow-hidden max-w-[230px] min-w-[200px] !bg-neutral-100 dark:!bg-purple-200"  >                
                    <VChip   v-for="param in params" size="large" :color="(darkmode)? 'surface': 'onSurface'" :variant="(graphToRender.selected == param)? 'flat': 'text' " class="text-caption ma-1 w-full max-w-[200px] rounded-lg border-b-[1px] border-neutral-600 "  @click="AppStore.resetGraphData(); graphToRender.selected = param; /*getData(param)*/" >
                      <template #prepend>
                        <Icon :icon="paramDetails[param].icon" width="24" height="24" class=""  />
                      </template>
                      <div class="flex flex-col py-1" >
                        <p  class="pl-3 font-bold text-xs" >{{ _.capitalize(param) }}</p>
                        <p class="pl-3 font-bold text-xs" > {{ _.round(sensordata[param], 2) }} {{ paramDetails[param].units }} </p>
                      </div>
                    </VChip>      
                   
              </VCol>
             
              <VCol   class="bg- red border-r-2 border-neutral-300 rounded-lg " >                
                <KeepAlive>
                  <component :is="renderGrapgh" class="tab"></component>
                </KeepAlive>   
                <VBtn icon="mdi:mdi-close" class="absolute top-8 right-12" color="onSurface" variant="tonal" density="compact" @click="UserStore.setSelectedStation(null)" />             
              </VCol>
            </VRow>
          </VContainer>
        </VSheet>
      </VBottomSheet>      
   </div>
  
  </template>
  
  <script setup>
    import { storeToRefs } from 'pinia';
    import { useMqttStore } from '@/stores/mqttStore'; 
    import { ref,reactive, watch, onMounted, onBeforeUnmount, shallowRef, resolveComponent, computed } from 'vue';  
    import { useRoute ,useRouter } from "vue-router";
    import _ from 'lodash';
    import { useToast } from 'primevue/usetoast';
    import { useUserStore } from '@/stores/userStore'; 
    import { useAppStore } from '@/stores/appStore';
    import { Icon } from '@iconify/vue';

    import { MaptilerLayer, MaptilerStyle } from "@maptiler/leaflet-maptilersdk";
    import { useDisplay } from 'vuetify';
    import 'leaflet/dist/leaflet.css';
    import 'leaflet.markercluster'   // https://github.com/leaflet/Leaflet.markercluster
    import 'leaflet.markercluster/dist/MarkerCluster.css'
    import 'leaflet.markercluster/dist/MarkerCluster.Default.css'
    import Temperature from '@/components/graphs/Temperature.vue';
    import Humidity from '@/components/graphs/Humidity.vue';
    import Pressure from '@/components/graphs/Pressure.vue';
    import Voc from '@/components/graphs/Voc.vue';
    import Vocindex from '@/components/graphs/Vocindex.vue';

    import { map, tileLayer, marker, DomEvent,  Popup } from 'leaflet';
    import L from 'leaflet';
    

  
  // VARIABLES
  
  const Mqtt                      = useMqttStore();
  const UserStore                 = useUserStore(); 
  const AppStore                  = useAppStore();
  const { xs,smAndDown,smAndUp, mdAndUp }   = useDisplay();
  const { payload, payloadTopic } = storeToRefs(Mqtt);
  const {
    id,
    loggedIn,
    image,     
    darkmode, 
    selectedStation, 
    mqtt_sub_credentials, 
    userSites}           = storeToRefs(UserStore);
  const {paramDetails,historyLoading}  = storeToRefs(AppStore);
  const router                    = useRouter();
  const route                     = useRoute(); 
  const toast                     = useToast();  
  const mymap                     = shallowRef(null);
  const markers                   = shallowRef(new L.markerClusterGroup({chunkedLoading: false}));
  const sensordata                = ref({});
  const params                    = ref([]);
  const stations                  = ref({});  
  const blueIcon                  = ref(null);
  const greenIcon                 = ref(null);
  const redIcon                   = ref(null);
  const goldIcon                  = ref(null);
  const blackIcon                 = ref(null);
  const graphToRender             = ref({"selected": "temperature","init":false, "list":[{"name":"temperature","component":"Temperature"}, {"name":"humidity","component":"Humidity"}]})

  const mtLayer                   = new MaptilerLayer( {
                                      apiKey: 'MacqP5qqahFSZdWB6tSq', // https://cloud.maptiler.com/maps/landscape/    https://docs.maptiler.com/leaflet/examples/vector-tiles-in-leaflet-js/
                                      style: MaptilerStyle.STREETS.DARK //https://docs.maptiler.com/sdk-js/examples/built-in-styles/
                                    } ); 
 
  /*
  Popup.prototype._animateZoom = (e) => {
      // SOLVE ERROR WHICH OCCURS WHEN ZOOMING AFTER OPENING A POPUP
      if (!this._map) { return }
      var pos = this._map._latLngToNewLayerPoint(this._latlng, e.zoom, e.center),
        anchor = this._getAnchor()
      DomUtil.setPosition(this._container, pos.add(anchor))
    }
 
    */

   // Computed properties 
   const openLiveSheet = computed(()=> !!selectedStation.value  );
    
  
  // WATCHERS
  watch(payload,(msg)=> {    
  
    if(msg.type == "station" ){      

      if (!!graphToRender.value.init){
        graphToRender.value.selected = params.value[0];
        graphToRender.value.init = true;
      }

      if(msg.id == selectedStation.value){      
        params.value = {...Object.keys(msg.data)}; 
        sensordata.value = {...msg['data']}
      }
    
      let lat = msg.lat;
      let lon = msg.lon;
      let date = new Date(msg.timestamp * 1000).toLocaleDateString('en-us', { /*weekday:"short",*/ year:"numeric", month:"short", day:"numeric"}) 
      let time = new Date(msg.timestamp * 1000).toLocaleTimeString('en-us')     
    
      let keys = Object.keys(stations.value); 

      if(keys.includes(msg.id)){
          // Marker already exist -  update marker    
          let params = Object.keys(msg.data);            
          let vals = ``
          params.forEach( param => vals += `<div class="tooltipMssg_items"><span class="itemNameParish">${_.capitalize(param)}</span> <span class="itemValueParish">${_.round(msg["data"][param], 2)} ${paramDetails.value[param].units}</span></div>`)

          const details = createElement(
                      `<div class="tooltipMssg">
                          <div class="tooltipMssg_items"><span class="itemNameStation">Station</span> <span class="itemValueStation"> ${msg.name.toUpperCase()}</span></div>
                          <div class="tooltipMssg_items"><span class="itemNameDate">Date</span> <span class="itemValueDate">${date}</span></div>
                          <div class="tooltipMssg_items"><span class="itemNameTime">Time</span> <span class="itemValueTime">${time}</span></div>
                          ${vals}                                             
                      </div>` 
                    );

          let myMarker = stations.value[msg.id]              
          myMarker.setPopupContent(details) 
          .on('mouseover', (ev) => { myMarker.openPopup(); })  
          .on('mouseout', (ev) => { myMarker.closePopup(); }) 
          .setIcon(greenIcon.value);             
      }  

    }
  
  });

  watch(userSites, (sites) => {

    if(!!sites){
      let keys = Object.keys(stations.value); 
      sites.forEach( site => {
          site.devices.forEach( device => {
            if(!keys.includes(device.id)) { 
              console.log("Creating Markers")
              // Create marker
              let myMarker = marker([device.lat, device.lon],{title: _.capitalize(device.name),opacity:1.0,riseOnHover:true })
                .bindPopup('Waiting for data') 
                .on('click', (e) => { UserStore.setSelectedStation(device.id); params.value = []})
                .setIcon(blackIcon.value)                       
            
                // Store marker
                stations.value[device.id] = myMarker ;
                markers.value.addLayer(myMarker);
                mymap.value.addLayer(markers.value);  

                      }
          })
      })
    }
  })
  
  const renderGrapgh = computed(() => {
      if(graphToRender.value.selected == 'temperature')
        return Temperature
      else if (graphToRender.value.selected == 'humidity')
        return Humidity
      else if (graphToRender.value.selected == 'pressure')
        return Pressure
      else if (graphToRender.value.selected == 'voc')
        return Voc
      else if (graphToRender.value.selected == 'vocindex')
        return Vocindex        
     } 
  ) 
  
  // FUNCTIONS
  onMounted(() => {

    L.Popup.prototype._animateZoom = (e) => {
      // SOLVE ERROR WHICH OCCURS WHEN ZOOMING AFTER OPENING A POPUP    
      if (!this) { return }
    
      var pos = this._map._latLngToNewLayerPoint(this._latlng, e.zoom, e.center),
        anchor = this._getAnchor()
      DomUtil.setPosition(this._container, pos.add(anchor))
    }

    UserStore.setSelectedStation(null); 

    blueIcon.value  = createIcon("bluestripe");
    redIcon.value   = createIcon("redstripe");
    greenIcon.value = createIcon("greenstripe");
    goldIcon.value  = createIcon("goldstripe");
    blackIcon.value = createIcon("blackstripe");

    mymap.value = map('map').setView([13.176257678629065, -59.54376034587126], 11);  
     
   
      
    tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}', {
                attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
                maxZoom: 18,
                id: 'tedwardsuwi/cl0d2e6io000t14qntylpu4j4',
                tileSize: 512,
                zoomOffset: -1,
                accessToken: 'pk.eyJ1IjoidGVkd2FyZHN1d2kiLCJhIjoiY2x3Y3RqMXY1MHpuNTJxcDA4emQ0ejQycCJ9.t-ENJ58Apo7e4gfhEidE8A'
            }).addTo(mymap.value);
      
    // mtLayer.addTo(mymap.value);

    UserStore.getAllSites();
  });
  
  onBeforeUnmount(()=>{ 
    // Mqtt.unsubTo("/references")
    // Mqtt.unsubTo("/devices")
    // Mqtt.subTo("/station")
  });
  
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


  </script>
  
  
  <style>
   /* #tooltipMssg{
     color: black;
   } */
  
   .tooltipMssg{
      display: flex;
      flex-direction: column; 
      min-width: 200px;
  }
  
  .tooltipMssg_items{
          display: grid;
          grid-template-columns: 1fr 1fr;
          padding: 2px;
          border-radius: 3px;
          
          }
  
  .tooltipMssg_items:nth-child(1){
              color: rgb(var(--v-theme-primary));
              font-size: 14px;
              font-weight: bolder;
              margin-bottom: 10px;
              
          }
  
  .tooltipMssg_items:nth-child(1):hover{
    color: rgb(var(--v-theme-onPrimaryContainer));
              }
  
              
  .tooltipMssg_items:hover{
              background-color: rgb(var(--v-theme-primaryContainer));
              color: rgb(var(--v-theme-onPrimaryContainer));
              font-weight: bold;
          }
  
  .popupBtn {
     border: 1px solid rgb(var(--v-theme-secondary));;
     border-radius: 8px; margin: 10px 0;
          }
  
  .popupBtn:hover {
      background-color: rgb(var(--v-theme-secondary));;
      color: rgb(var(--v-theme-onSecondary));;
      font-weight: bold;
       }
  </style>
  
  