  <template>     
    <div  :class="[(smAndDown)?'h-[calc(100dvh-57px)] mb-n3':'h-screen']"   class="w-screen   relative flex items-center justify-center" >
       
      <div :id="mapcontainer" class="w-[100%]  h-[100%]"  ></div> 

      <VBottomSheet :model-value="openLiveSheet"  persistent content-class="bg-transparent relative pa-0"  >
        <VBtn  icon align="end"   variant="text" class="!text-red-500 dark:!text-red-300 !text-small   absolute -top-12 right-0"   @click="selectedStation = null">                  
                <Icon icon="solar:close-square-bold" width="32" height="32" class=""  />          
            </VBtn>
        <VSheet rounded="t-lg" color="surface" > 
           
          <VContainer class=" bg-[hsl(0,0%,93%)] dark:bg-[hsl(0,0%,20%)] " fluid >
            <VRow  justify="center" align="center" class="pa-2" >
                <VCol   class="" style=" width: 100%;"   >
                    <div class="[&>*]:rounded-lg  grid grid-cols-[200px,_minmax(460px,_1fr)] grid-rows-[1fr]  max-[560px]:grid-cols-1 max-[560px]:grid-rows-[100px,fr1]  gap-5 max-h-[370px]    max-[560px]:hidden">
                       <VCol  class="  border-r-2 border-neutral-300 rounded-lg overflow-hidden max-w-[230px] min-w-[200px] max-h-[370px] overflow-y-scroll scrolleffect !bg-neutral-100 dark:!bg-purple-100"  >                
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
                                                  
                        <TransitionGroup name="lists">
                            <div v-if="graphToRender.selected.length <= 0" class="col-span-1 max-h-[390px] flex justify-center align-center">
                                <p class="text-lg "  >Select a <strong>'Parameter'</strong> from the left to graph</p>
                            </div>
                            <div v-else class="col-span-1 max-h-[390px] ">
                                <KeepAlive>       
                                    <AllGraphs :param="graphToRender.selected" />                            
                                </KeepAlive>   
                            </div>
                        </TransitionGroup>

                    </div> 
                    <VTabs v-model="tabs" color="primary" grow  class="!hidden max-[560px]:!block mt-3"  >
                        <VTab :value="1" class="mx-1" density="compact" hide-slider variant="flat"> <p class="text-none font-bold" >Live</p> </VTab>
                        <VTab :value="2" class="mx-1"  density="compact" hide-slider variant="flat"> <p class="text-none font-bold" >Graph</p> </VTab>                        
                    </VTabs>

                    <VTabsWindow v-model="tabs"  class="!hidden max-[560px]:!block py-5" >
                        <VTabsWindowItem   :key="1" :value="1" >
                            <div class="max-h-[350px] py-5 grid grid-rows-[repeat(auto-fit,_minmax(50px,60px))] grid-cols-[1fr] gap-2 overflow-y-scroll place-content-start border-y [&>*]:w-full  ">                     
                                <div   v-for="param in params"  class="grid grid-cols-3 gap-2 cursor-pointer rounded-md hover:bg-neutral-100 hover:dark:bg-neutral-600" :class="[(graphToRender.selected == param)? 'bg-neutral-200  dark:bg-neutral-600 ':'']"   @click="AppStore.resetGraphData(); graphToRender.selected = param; /*getData(param)*/" >                        
                                    <div class="col-span-1 flex justify-center align-center" >
                                        <VSheet width="40" height="40" rounded="pill" class="flex justify-center align-center" :class="[(graphToRender.selected ==  param)?'bg-neutral-800 dark:bg-neutral-600':'']"   >
                                            <Icon :icon="paramDetails[param].icon" width="32" height="32"  :class="[(graphToRender.selected == param)?'text-sky-300/[0.8] dark:text-rose-300/[0.9]':'text-neutral-800 dark:text-neutral-100']"  />                                    
                                        </VSheet>
                                    </div>
                                    <div class="col-span-2 flex flex-col justify-center align-start " > 
                                        <p  class="pl-3 font-bold text-xs" >{{ _.capitalize(param) }}</p>
                                        <p class="pl-3 font-bold text-xs" > {{ _.round(sensordata[param], 2) }} {{ paramDetails[param].units }} </p>
                                    </div>                     
                                </div>                        
                            </div>
                        </VTabsWindowItem>

                        <VTabsWindowItem   :key="2" :value="2" >
                          <TransitionGroup name="lists">
                            <div v-if="graphToRender.selected.length <= 0" class="min-h-[560px] flex justify-center align-center">
                                <p class="text-lg "  >Select a Parameter under the <strong>'Live Data'</strong> tab first</p>
                            </div>
                            <div v-else class="max-h-[350px]">
                                <KeepAlive>       
                                    <AllGraphs :param="graphToRender.selected" />                            
                                </KeepAlive>                     
                            </div>
                          </TransitionGroup>                    
                        </VTabsWindowItem>
                    </VTabsWindow>
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
    import { ref,reactive, watch, onMounted, onBeforeUnmount, shallowRef, resolveComponent, computed, onBeforeMount } from 'vue';  
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

    import { map, tileLayer, marker, DomEvent,  Popup } from 'leaflet';
    import L from 'leaflet';

    import AllGraphs from '@/components/graphs/AllGraphs.vue';
    

  
  // VARIABLES
  
  const Mqtt         = useMqttStore();
  const UserStore    = useUserStore(); 
  const AppStore     = useAppStore();
  const { xs,smAndDown,smAndUp, mdAndUp }   = useDisplay();
  const { connected, payload, payloadTopic } = storeToRefs(Mqtt);

  const {
    id,
    loggedIn,
    image,  
    suball,   
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
  const mapcontainer              = ref(`container${_.random(0,100000)}`);
  
  const sensordata                = ref({});
  const params                    = ref([]);
  const stations                  = ref({});  
  const blueIcon                  = ref(null);
  const greenIcon                 = ref(null);
  const redIcon                   = ref(null);
  const goldIcon                  = ref(null);
  const blackIcon                 = ref(null);
  const tabs                      = ref(1);
  const sectors                   = ref(["N","NNE","NE","ENE","E","ESE","SE","SSE","S","SSW","SW","WSW","W","WNW","NW","NNW","N"]);
  const directionName             = ref(""); 
  const graphToRender             = ref({"selected": "temperature","init":false, "list":[]})

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
  
  
  // FUNCTIONS
  onBeforeMount(() => {
    connected.value = false;
 
    if(userSites.value.length <= 0){ 
      UserStore.getAllSites();
    }
  })


  onMounted(() => {

    if(!Mqtt.isConnected) { 
      if(suball.value){
        Mqtt.subTo("/station/data/#");
      }
      else {
        if(!!mqtt_sub_credentials.value)
          Mqtt.subTo(mqtt_sub_credentials.value.topic);
      }
        Mqtt.connect();
    } 

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

    UserStore.getAllSites();
  });
  
  onBeforeUnmount(() =>{ 
    // Mqtt.unsubTo("/references")
    // Mqtt.unsubTo("/devices")
    // Mqtt.subTo("/station")
    
  });
  
  const createIcon = (name) => {      
    return new L.Icon({
        iconUrl: `/src/assets/markers/${name}.png`,
        shadowUrl: '/src/assets/markers/marker-shadow.png',
        // iconUrl: `../src/assets/${name}.png`,
        // shadowUrl: '../src/assets/marker-shadow.png',
        iconSize:     [50, 50],
        iconAnchor:   [25.5, 49.5],
        popupAnchor:  [1, -34],
        shadowSize:   [41, 41],
        shadowAnchor: [13,40]
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
  
  