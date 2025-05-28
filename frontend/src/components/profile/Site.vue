<template>
      
    <VContainer class="size-full" align="center"  fluid >
        
      <!-- TOP ROW -->
      <VRow class=" gap-3 mt-15"  style="max-width: 1200px;" >
        <VCol class=""> 
          <div id="sitemap" class="w-full min-w-[300px] max-w-[594px]  rounded-lg h-[300px]  min-[697px]:h-[826px]"  ></div>
        </VCol> 

        <VCol v-if="!!site" class="  flex flex-col justify-between min-w-[350px]">
          <VCard  class="bg-neutral-100 dark:bg-neutral-800" flat border  >
            <template #title >
              <div class="flex justify-between" > 
                <div class="flex justify-center align-center" >
                    <span class=" " >{{ entitySiteName.entity }} </span> 
                    <Icon icon="fa-solid:chevron-right" width="16" height="16" class="mx-1"  />
                    <span> {{ entitySiteName.site }}</span> 
                </div>
          
                <VBtn  density="comfortable" icon  @click="setSiteUpdate(); openUpdateSite = true"  class="text-none mr-6" title="Edit" variant="tonal" > 
                  <Icon icon="line-md:edit" width="24" height="24"   />
                </VBtn>
              </div>
            </template>


            <VCardItem >
              <VDivider :opacity="100" class="border-neutral-300 dark:border-neutral-600 mb-5"  />
              <VContainer >
                <VRow>
                  <VCol class="pa-0 flex gap-3 align-center" title="Latitude" > 
                    <VBtn  width="36" height="36" variant="text" :elevation="0"  icon  density="compact"    >
                      <Icon icon="mingcute:earth-latitude-fill" width="32" height="32"   /> 
                    </VBtn>   
                    <p>{{ site.lat }}</p>
                  </VCol>
                  <VCol  class="pa-0 flex align-center gap-3"  title="Longitude"> 
                    <VBtn      width="36" height="36" variant="text" :elevation="0"  icon  density="compact"    >
                      <Icon icon="mingcute:earth-longitude-fill" width="32" height="32"   /> 
                    </VBtn>   
                    <p>{{ site.lon }}</p>
                  </VCol>
                </VRow>

                <!-- <VRow class="mt-10">
                  ASSIGNED TO CARD
                  <VCol cols="12"  v-if="site.acc_owner.length > 0" >
                    <VCard :title="`${_.capitalize(site.acc_owner[0].firstname)} ${_.capitalize(site.acc_owner[0].lastname)}`" color="onSurface"   variant="tonal" width="100%" rounded="lg" border>
                    
                    <template #subtitle >
                      <div class="flex flex-col" >
                        <p class="text-xs" >{{ site.acc_owner[0].organization }}</p>
                        <p class="text-xs" >{{ site.acc_owner[0].country }}</p>
                      </div>
                    </template>
                    
                    
                      <template #prepend >
                      <div class="flex flex-col justify-center" >
                        <Icon icon="iconamoon:profile" width="48" height="48" class="!text-neutral-600 dark:!text-neutral-400 justify-center" />
                        <p class="text-xs" >Assigned to:</p>
                      </div>
                    </template>

                    <template #append >
                      <VBtn    density="comfortable" icon @click="openSearch = true" class="text-none" title="Assign/Reassign user" variant="tonal" > 
                        <Icon icon="line-md:edit" width="24" height="24"   />
                      </VBtn>

                      <VBtn    density="comfortable" icon @click="assignUser('')" class="text-none ml-1" title="Unassign" variant="text" > 
                        <Icon icon="ic:baseline-delete" width="24" height="24"   />
                      </VBtn>
                    </template>
                  </VCard>
                  </VCol>

                  <VCol v-else cols="12" >
                    <VCard   color="onSurface" variant="tonal" width="100%" rounded="lg" border>
                      <template #title >
                        <p>Site not assigned to a user</p>
                      </template>
                    <template #prepend >
                      <div class="flex flex-col justify-center" >
                        <Icon icon="mdi:account-alert" width="48" height="48" class="!text-rose-600 dark:!text-rose-400 justify-center" />                  
                      </div>
                    </template>


                    <template #append >
                      <VBtn    density="comfortable" icon @click="openSearch = true" class="text-none" title="Assign to user" variant="tonal" > 
                        <Icon icon="line-md:edit" width="24" height="24"   />
                      </VBtn>
                    </template>
                  </VCard>
                  </VCol>
                </VRow> -->
              
              </VContainer>

            </VCardItem>
          </VCard>

          <VCard  class="my-2 bg-neutral-100 dark:bg-neutral-800" flat border >
            <template #prepend >
              <p class="" >Status</p>
            </template>
            
            <template #title > <p>{{ (site.enabled)? 'Enabled' : 'Disabled' }}</p></template>
            
          </VCard>

          <VCard   class="bg-neutral-100 dark:bg-neutral-800" flat border  max-height="240" >
              <VToolbar >
                  <div class="flex align-center justify-between w-full pa-3">
                    <div v-if="!!site" >
                      <p class="text-xl"> Devices  ({{ site.devices.length }})</p>
                    </div>
                    <VBtn  class="text-none" icon title="Add a Device" variant="tonal"  @click="openCreateDevice = true" >
                      <Icon icon="line-md:map-marker-plus-filled" width="24" height="24" />
                    </VBtn>   
                  </div>
              </VToolbar> 
              
              <VCardItem>
                  <VList  v-if="!!site" rounded="lg" density="compact"   variant="flat" class="relative mx-auto" max-height="150"  >
                      <VListItem  variant="text" :active ="(!!device)? device.id == dev.id : false"  class="bg-neutral-100 dark:bg-neutral-600/[0.3] mb-2 mx-5"  v-for="dev in site.devices" :key="dev.id" :value="dev.id" @click="setMarkerOnListMap(dev.lat,dev.lon);AppStore.setDevice(dev)"  border rounded="lg" >
                          <template #title >
                              <div class="flex justify-start" >
                                  <span class="text-sm font-bold" >{{_.capitalize(dev.name)}}</span>                            
                              </div>    
                          </template>
                          
                          <template #prepend>        
                            <Icon icon="mdi:router-network-wireless" width="24" height="24" class="mr-5" />
                          </template>
                          <template #append>        
                              <VBtn  flat rounded="lg" variant="tonal" color="tertiary" @click="setDeviceUpdate({...dev})" icon density="compact" class="text-none text-sm" >
                                <VIcon  icon="mdi:mdi-dots-vertical" />
                                <VMenu activator="parent">
                                  <VList>
                                    <VListItem  key="update" value="update"  @click="openUpdateDevice = true" >
                                      <VListItemTitle>Update</VListItemTitle>
                                    </VListItem>
                                    <VListItem  key="delete" value="delete" @click="deleteDevice.siteid = site.id; deleteDevice.id = dev.id; deleteDevice.name = dev.name; openDeleteDevice = true" >
                                      <VListItemTitle>Delete</VListItemTitle>
                                    </VListItem>
                                  </VList>
                                </VMenu>
                              </VBtn>
                          </template>
                      </VListItem>
                  </VList>
              </VCardItem>                 
          </VCard>

          <VSheet  min-height="220" >
            <VCard  v-if="!!device"   class="my-2 bg-neutral-100 dark:bg-neutral-800" flat border >
                  <template #title ><p>{{ _.capitalize(device.name) }}</p></template>
                  <template #subtitle > 
                    <VContainer>
                      <VRow  class="gap-2" >
                        <VCol cols="5" class="pa-0 flex gap-3 align-center "  title="Latitude" >                  
                            <VBtn      width="36" height="36" variant="text" :elevation="0"  icon  density="compact"    >
                              <Icon icon="mingcute:earth-latitude-fill" width="32" height="32"   /> 
                            </VBtn>   
                            <p  >{{ device.lat }}</p>
                        
                        </VCol>
                        <VCol cols="5"  class="pa-0 flex align-center  gap-3"  title="Longitude"> 
                          <VBtn      width="36" height="36" variant="text" :elevation="0"  icon  density="compact"    >
                            <Icon icon="mingcute:earth-longitude-fill" width="32" height="32"   /> 
                          </VBtn>   
                        
                          <p class="text-center" >{{ device.lon }}</p>
                        </VCol>
                      </VRow>
                    </VContainer>
                  </template>
                  <VCardItem>
                    <VDivider :opacity="100" class="border-neutral-300 dark:border-neutral-600"  />
                    <VContainer >
                      <VRow>
                        <VCol cols="auto" >
                          <div class=" flex justify-start mb-2 font-medium opacity-60" ><p>Processor</p></div>
                            <div  class="flex flex-col justify-center" > 
                              <VBtn      width="36" height="36" variant="text" :elevation="0" :title="_.capitalize(device.processor)"  icon  density="compact"    >
                                <Icon :icon="getDeviceIcon" width="32" height="32"   /> 
                              </VBtn>  
                            </div>
                        </VCol>
                        <VCol align="start" class="ml-2" >
                          <div class=" flex justify-start mb-2 font-medium opacity-60" ><p>Params</p></div>
                          <VBtn   v-for="param in device.params"     width="36" height="36" variant="text" :elevation="0" :title="_.capitalize(param)"  icon  density="compact"    >
                              <Icon :icon="paramDetails[param].icon" width="32" height="32" class=""  /> 
                          </VBtn> 
                        </VCol>
                      </VRow>
                    </VContainer>
                    
                  </VCardItem>                    
            </VCard>
          </VSheet>
        

        </VCol> 

        <VDialog v-model="openUpdateSite" class="mx-5" transition="dialog-bottom-transition" width="100%" max-width="400"  persistent >
          <!-- UPDATE SITE -->
            <template v-slot:default="{ isActive }">
                <VCard  > 
                    <VCardTitle class="h-[300px] pa-2 rounded-lg" >
                        <div id="updatesitemap" class="size-full rounded-lg"  ></div>
                    </VCardTitle>

                    <VCardSubtitle class=" px-2 pt-3">
                        <p class=" text-2xl font-light"  style="font-family: Nunito;" >Update Site Request</p>
                    </VCardSubtitle>

                    <VCardText class="pb-0 px-2">
                        <VTextField v-model="updateSite.name" label="Name" class="rounded-lg border border-neutral-600 dark:border-neutral-50 overflow-clip" density="compact" variant="solo-inverted"  flat hide-details clearable /> 
                        <VTextField v-model="updateSite.lat" label="Latitude" step="0.000001"  type="number" class="my-2 rounded-lg border border-neutral-600 dark:border-neutral-50 overflow-clip" density="compact" variant="solo-inverted"  flat hide-details  clearable />
                        <VTextField v-model="updateSite.lon" label="Longitude" step="0.000001" type="number"  class="rounded-lg border border-neutral-600 dark:border-neutral-50 overflow-clip" density="compact" variant="solo-inverted"  flat hide-details  clearable />
                        
                        <!-- <VSelect v-model="updateSite.enabled" :items="[{'name':'Enable','value': true}, {'name':'Disable','value': false}]" item-title="name" item-value="value" label="Status" class="my-2 rounded-lg border border-neutral-600 dark:border-neutral-50 overflow-clip"  density="compact" variant="solo-inverted"   flat hide-details  clearable  >
                          <template v-slot:item="{ props, item }">
                            <VListItem v-bind="props" :title="_.capitalize(item.raw.name)"  class="ml-5">                                
                            </VListItem>
                          </template>
                        </VSelect> -->
                      </VCardText>

                    <VCardActions class="justify-end pa-4">
                        <VBtn text="Submit" @click="updateSingleSite()" class="text-none font-bold"   :loading="updateSiteLoading"  ></VBtn>
                        <VBtn text="Cancel" @click="isActive.value = false"   class="text-none"></VBtn>                          
                    </VCardActions>
                </VCard>
            </template>
        </VDialog>

        <VDialog v-model="openCreateDevice" class="mx-5" transition="dialog-bottom-transition" width="100%" max-width="400"  persistent >
          <!-- CREATE DEVICE -->
            <template v-slot:default="{ isActive }">
                <VCard  > 
                    <VCardTitle class="h-[300px] pa-2 rounded-lg" >
                        <div id="devicemap" class="size-full rounded-lg"  ></div>
                    </VCardTitle>

                    <VCardSubtitle class=" px-2 pt-3">
                        <p class=" text-2xl font-light"  style="font-family: Nunito;" >Add a Device</p>
                    </VCardSubtitle>

                    <VCardText class="pb-0 px-2">
                        <VTextField v-model="createDevice.name" label="Name" class="rounded-lg border border-neutral-600 dark:border-neutral-50 overflow-clip" density="compact" variant="solo-inverted"  flat hide-details clearable /> 
                        <VTextField v-model="createDevice.lat" label="Latitude" step="0.000001"  type="number" class="my-2 rounded-lg border border-neutral-600 dark:border-neutral-50 overflow-clip" density="compact" variant="solo-inverted"  flat hide-details  clearable />
                        <VTextField v-model="createDevice.lon" label="Longitude" step="0.000001" type="number"  class="rounded-lg border border-neutral-600 dark:border-neutral-50 overflow-clip" density="compact" variant="solo-inverted"  flat hide-details  clearable />
                        
                        <VSelect v-model="createDevice.processor" :items="processors" item-title="name" label="Processor" class="my-2 rounded-lg border border-neutral-600 dark:border-neutral-50 overflow-clip"  density="compact" variant="solo-inverted"   flat hide-details  clearable  >
                          <template v-slot:item="{ props, item }">
                            <VListItem v-bind="props" :title="_.capitalize(item.raw.name)"  class="ml-5">
                              <template #prepend >
                                <Icon :icon="item.raw.icon" width="24" height="24"  class="mr-5" />
                              </template>
                            </VListItem>
                          </template>
                        </VSelect>

                        <VSelect v-model="createDevice.params" :items="paramOptions" label="Device Sensor Params" multiple class="my-2 rounded-lg border border-neutral-600 dark:border-neutral-50 overflow-clip"  density="compact" variant="solo-inverted"   flat hide-details  clearable  >
                          <template v-slot:prepend-item>
                            <VListItem title="Select All" @click="toggle" >
                              <template v-slot:prepend>
                                <v-checkbox-btn
                                  :color="pickSomeParams ? 'indigo-darken-4' : undefined"
                                  :indeterminate="pickSomeParams && !pickAllParams"
                                  :model-value="pickAllParams"
                                ></v-checkbox-btn>
                              </template>
                            </VListItem>

                            <VDivider class="mt-2"></VDivider>
                          </template>

                        </VSelect>
                    
                      </VCardText>

                    <VCardActions class="justify-end pa-4">
                        <VBtn text="Submit" @click="addDevice()" class="text-none font-bold"  :disabled="enableDeviceCreateBtn" :loading="createDeviceLoading"  ></VBtn>
                        <VBtn text="Cancel" @click="isActive.value = false"   class="text-none"></VBtn>                          
                    </VCardActions>
                </VCard>
            </template>
        </VDialog>

        <VDialog v-model="openUpdateDevice" class="mx-5" transition="dialog-bottom-transition" width="100%" max-width="400"  persistent >
          <!-- UPDATE DEVICE -->
            <template v-slot:default="{ isActive }">
                <VCard  > 
                    <VCardTitle class="h-[300px] pa-2 rounded-lg" >
                        <div id="updatedevicemap" class="size-full rounded-lg"  ></div>
                    </VCardTitle>

                    <VCardSubtitle class=" px-2 pt-3">
                        <p class=" text-2xl font-light"  style="font-family: Nunito;" >Update Device Request</p>
                    </VCardSubtitle>

                    <VCardText class="pb-0 px-2">
                        <VTextField v-model="updateDevice.name" label="Name" class="rounded-lg border border-neutral-600 dark:border-neutral-50 overflow-clip" density="compact" variant="solo-inverted"  flat hide-details clearable /> 
                        <VTextField v-model="updateDevice.lat" label="Latitude" step="0.000001"  type="number" class="my-2 rounded-lg border border-neutral-600 dark:border-neutral-50 overflow-clip" density="compact" variant="solo-inverted"  flat hide-details  clearable />
                        <VTextField v-model="updateDevice.lon" label="Longitude" step="0.000001" type="number"  class="rounded-lg border border-neutral-600 dark:border-neutral-50 overflow-clip" density="compact" variant="solo-inverted"  flat hide-details  clearable />
                        
                        <VSelect v-model="updateDevice.processor" :items="processors" item-title="name" label="Processor" class="my-2 rounded-lg border border-neutral-600 dark:border-neutral-50 overflow-clip"  density="compact" variant="solo-inverted"   flat hide-details  clearable  >
                          <template v-slot:item="{ props, item }">
                            <VListItem v-bind="props" :title="_.capitalize(item.raw.name)"  class="ml-5">
                              <template #prepend >
                                <Icon :icon="item.raw.icon" width="24" height="24"  class="mr-5" />
                              </template>
                            </VListItem>
                          </template>
                        </VSelect>

                        <VSelect v-model="updateDevice.params" :items="paramOptions" label="Device Sensor Params" multiple class="my-2 rounded-lg border border-neutral-600 dark:border-neutral-50 overflow-clip"  density="compact" variant="solo-inverted"   flat hide-details  clearable  >
                          <template v-slot:prepend-item>
                            <VListItem title="Select All" @click="toggleUpdate" >
                              <template v-slot:prepend>
                                <v-checkbox-btn
                                  :color="pickSomeParamsUpdate ? 'indigo-darken-4' : undefined"
                                  :indeterminate="pickSomeParamsUpdate && !pickAllParamsUpdate"
                                  :model-value="pickAllParamsUpdate"
                                ></v-checkbox-btn>
                              </template>
                            </VListItem>

                            <VDivider class="mt-2"></VDivider>
                          </template>

                        </VSelect>
                    
                      </VCardText>

                    <VCardActions class="justify-end pa-4">
                        <VBtn text="Submit" @click="updateSingleDevice()" class="text-none font-bold"   :loading="updateDeviceLoading"  ></VBtn>
                        <VBtn text="Cancel" @click="isActive.value = false"   class="text-none"></VBtn>                          
                    </VCardActions>
                </VCard>
            </template>
        </VDialog>

        <VDialog v-model="openSearch" transition="dialog-bottom-transition" width="500" persistent >
          <!-- SEARCH FOR A USER TO ASSIGN -->
            <template v-slot:default="{ isActive }">
                <VCard >
                    <VToolbar >
                        <VTextField v-model="userSearch.text" variant="solo-inverted" rounded="lg" :loading="accSearchLoading" placeholder="Search for a Site ..." class="text-caption mx-1" hide-details >
                            <template #append-inner >
                                <Icon icon="tdesign:map-search-filled" width="24" height="24" />
                            </template>
                        </VTextField>
                    </VToolbar>

                    <VCardItem>
                        <VList rounded="lg" density="compact"   variant="flat" class="relative mx-auto"  >
                          
                              <div v-for="user in userSearch.result" >
                                <VHover>
                                  <template v-slot:default="{ isHovering, props }">
                                    <VListItem v-bind="props"  variant="text" :active="false" class="bg-neutral-100 dark:bg-neutral-600/[0.3] mb-2"   :key="user.id" :value="user.id"  border rounded="lg" >
                                        <template #title >
                                            <div class="flex justify-start" >
                                                <span class="text-sm font-bold" >{{`${user.firstname}  ${user.lastname}`}}</span>                            
                                            </div>    
                                        </template>
                                        <template #subtitle >
                                            <div class="flex justify-start" >
                                                <span class="text-xs" >{{`${user.organization}, ${user.country}`}}</span>                            
                                            </div>    
                                        </template>
                                        
                                        <template #prepend>        
                                            <!-- <VIcon v-if="site.enabled" icon="mdi:mdi-map-marker-multiple" class="text-green-700 dark:text-green-500" title="Enabled"  />
                                            <VIcon v-else icon="mdi:mdi-map-marker-multiple" class="text-red-700 dark:text-red-400" title="Disabled"  /> -->
                                        </template>
                                        <template #append>        
                                            <VBtn v-show="isHovering"  flat rounded="lg" text="Assign" variant="tonal" color="tertiary" @click="assignUser(user.id)" :loading="assignUserLoading"  density="compact" class="text-none text-sm" />
                                        </template>
                                    </VListItem>
                                  </template>
                                </VHover>
                              </div>
                              
                          
                           
                        </VList>
                    </VCardItem> 

                    <VCardActions class="justify-end">
                        <VBtn text="Close" @click="isActive.value = false" ></VBtn>
                    </VCardActions>
                </VCard>
            </template>
        </VDialog>

        <VDialog v-model="openDeleteDevice" max-width="400" persistent transition="dialog-bottom-transition" >
          <!-- DELETE DEVICE -->
            <VCard   class="border-t-4border-rose-600 dark:border-rose-300 " density="compact"  > 
          
              <template #title >
                <div class="text-center" >
                    <VIcon icon="mdi:mdi-router-network-wireless"    size="100" />
                </div>
              
              </template>
              <template #text >
                <p >You are about to  <strong class="font-bold text-rose-700" > Delete </strong> this device from the site. Are you sure you want to continue?</p>
              </template>

                <template v-slot:actions>
                  <VBtn text="Delete" class="text-subtitle-2" color="onSurface" width="100" :loading="deleteDeviceLoading" @click="deleteSingleDevice()" />
                  <VBtn text="Cancel" class="text-subtitle-2" color="onSurface" width="100"    @click="openDeleteDevice = false" />  
                </template>
            </VCard>
      </VDialog>

      </VRow>

      <!-- BOTTOM ROW --> 
   
   
    </VContainer>
     
  </template>
  
  <script setup> 
  import { ref,shallowRef,reactive, onMounted,onUnmounted,onBeforeMount,computed,watch} from 'vue';
  import { storeToRefs } from 'pinia'
  import { useAppStore} from '@/stores/appStore';  
  import { useUserStore} from '@/stores/userStore'; 
  import { useDisplay } from 'vuetify';
  import { useToast } from 'primevue/usetoast';
  import { useRoute } from "vue-router"; 
  import _ from 'lodash';
  import { Icon } from '@iconify/vue';
  import { MaptilerLayer, MaptilerStyle } from "@maptiler/leaflet-maptilersdk";
  import { map, tileLayer, marker,circleMarker, DomEvent, markerClusterGroup } from 'leaflet';
  import 'leaflet/dist/leaflet.css';
  import 'leaflet.markercluster'   // https://github.com/leaflet/Leaflet.markercluster
  import 'leaflet.markercluster/dist/MarkerCluster.css'
  import 'leaflet.markercluster/dist/MarkerCluster.Default.css'
 
  import L from 'leaflet';
  



// VARIABLES
const AppStore          = useAppStore(); 
const UserStore         = useUserStore();
const { xs,sm,smAndDown,smAndUp, mdAndUp }   = useDisplay(); 
const {
  site, 
  device, 
  userSearch,
  siteLoading, 
  createDeviceLoading,
  updateDeviceLoading, 
  updateSiteLoading,
  accSearchLoading, 
  deleteDeviceLoading,
  assignUserLoading, 
  paramDetails}         = storeToRefs(AppStore);
const {darkmode}        = storeToRefs(UserStore);
const route             = useRoute(); 
const loading           = ref(true);   
const toast             = useToast(); 
const openSearch        = ref(false);
const openDeleteDevice  = ref(false);
const openUpdateSite    = ref(false);
const openCreateDevice  = ref(false);
const openUpdateDevice  = ref(false);
const blueIcon          = ref(null);
const greenIcon         = ref(null);
const redIcon           = ref(null);
const goldIcon          = ref(null);
const blackIcon         = ref(null);
const deleteDeviceID    = ref("");
var markers             = new L.markerClusterGroup();
const upateDeviceMarker = shallowRef(null); 
const updateSiteMarker  = shallowRef(null); 
const createDeviceMarker  = shallowRef(null); 
const createSiteMarker  = shallowRef(null);
const mymap             = shallowRef(null);
const updatesitemap     = shallowRef(null); 
const updatedevicemap   = shallowRef(null);  
const listmap           = shallowRef(null);
const search            = ref({"text":"","result":[]});
const mtLayer           = new MaptilerLayer( {
                                maxZoom: 18,
                                apiKey: 'MacqP5qqahFSZdWB6tSq', // https://cloud.maptiler.com/maps/landscape/    https://docs.maptiler.com/leaflet/examples/vector-tiles-in-leaflet-js/
                                style: MaptilerStyle.STREETS.DARK //https://docs.maptiler.com/sdk-js/examples/built-in-styles/
                            } ); 
let USDollar = new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' });
const updateSite          = reactive({id:"",name:"", lat:"0",lon:"0", enabled: true});
const createDevice        = reactive({name:"", lat:"0",lon:"0", processor:"", params :[]});
const updateDevice        = reactive({siteid:"",deviceid:"", name:"", lat:"0",lon:"0", processor:"", params:[]});
const deleteDevice        = reactive({siteid:"",id:"", name:""});
const paramOptions        = ref(["temperature","humidity","pressure","co2","voc","vocindex","pm25","pm10","radiation","uva","uvb","uvc","voltage","current","bat","oxidised","reduced","nh3","lux"]);
let searchTextID, timeoutVal = 1000; 

const processors = ref([{"name":"esp32", "icon":"simple-icons:espressif"},{"name":"zero", "icon":"cib:raspberry-pi"},{"name":"pimoroni", "icon":"cib:raspberry-pi"}])
 

// WATCHERS
watch(openCreateDevice,  (state) => {
    if(state){

        setTimeout(()=> {
          listmap.value = map('devicemap',{ zoomControl: false}).setView([14.5255555556, -75.8183333333], 4);     
            
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
        //    mtLayer.addTo(mymap.value) 
        listmap.value.whenReady(()=> {
          createDeviceMarker.value = marker([14.5255555556, -75.8183333333],{title: "Site",opacity:1.0,riseOnHover:true })
          .on('click', (e) => { 
          console.log("Clicked marker");
              })   

          .bindPopup('Device location')  
          .setIcon(greenIcon.value)   
          createDeviceMarker.value.addTo(listmap.value)
          
            })   
             
        },500) 
    } 
     
});

watch(openUpdateSite,  (state) => {
    if(state){

        setTimeout(()=> {
          updatesitemap.value = map('updatesitemap',{ zoomControl: false}).setView([updateSite.lat, updateSite.lon], 11);     
            
            // /*
            tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}', {
                        attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
                        maxZoom: 18,
                        id: 'tedwardsuwi/cl0d2e6io000t14qntylpu4j4',
                        tileSize: 512,
                        zoomOffset: -1,
                        accessToken: 'pk.eyJ1IjoidGVkd2FyZHN1d2kiLCJhIjoiY2x3Y3RqMXY1MHpuNTJxcDA4emQ0ejQycCJ9.t-ENJ58Apo7e4gfhEidE8A'
                    }).addTo(updatesitemap.value);
            // */    
        //    mtLayer.addTo(mymap.value) 
        updatesitemap.value.whenReady(()=> {     
          updateSiteMarker.value = marker([updateSite.lat, updateSite.lon],{title: "Site",opacity:1.0,riseOnHover:true })
          .on('click', (e) => { 
          console.log("Clicked marker");
              })   

          .bindPopup('Site location')  
          .setIcon(greenIcon.value)             
          updateSiteMarker.value.addTo(updatesitemap.value);   
               
            })   
             
        },500) 
    } 
     
});

watch(openUpdateDevice,  (state) => {
    if(state){

        setTimeout(()=> {
          updatedevicemap.value = map('updatedevicemap',{ zoomControl: false}).setView([updateDevice.lat, updateDevice.lon], 11);     
            
            // /*
          tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}', {
                        attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
                        maxZoom: 18,
                        id: 'tedwardsuwi/cl0d2e6io000t14qntylpu4j4',
                        tileSize: 512,
                        zoomOffset: -1,
                        accessToken: 'pk.eyJ1IjoidGVkd2FyZHN1d2kiLCJhIjoiY2x3Y3RqMXY1MHpuNTJxcDA4emQ0ejQycCJ9.t-ENJ58Apo7e4gfhEidE8A'
                    }).addTo(updatedevicemap.value);
            // */    
        //    mtLayer.addTo(mymap.value) 
          updatedevicemap.value.whenReady(() => {     
             upateDeviceMarker.value = marker([updateDevice.lat, updateDevice.lon],{title: "Device",opacity:1.0,riseOnHover:true })
              .on('click', (e) => { 
              console.log("Clicked marker");
                  })   
              .bindPopup('Device location')  
              .setIcon(greenIcon.value) 
 
              upateDeviceMarker.value.addTo(updatedevicemap.value);    
            })   
             
        },500) 
    } 
   
});

watch(createDevice,  (device) => {
    const lat = parseFloat(device.lat);
    const lon = parseFloat(device.lon);
 
    if(typeof(lat)  == "number" && typeof(lon) == "number"){
        if(!!lat && !!lon){                  
          listmap.value.flyTo([lat, lon], 13);
          createDeviceMarker.value.setLatLng([lat, lon]);             
        } 
    }

});


watch(()=> site.value, (site) => {
    if(!!site && !!mymap.value) {
      mymap.value.setZoom(11);
      mymap.value.setView([site.lat, site.lon]);
      // createSiteMarker.value.setLatLng([site.lat, site.lon]);
    }    
  })

  watch(updateSite, (site) => {
    if( !!updatesitemap.value) {
      updatesitemap.value.setZoom(11);
      updatesitemap.value.setView([site.lat, site.lon]);
      updateSiteMarker.value.setLatLng([site.lat, site.lon]);
    }    
  })

  watch(updateDevice, (site) => {
    if(!!updatedevicemap.value) { 
      updatedevicemap.value.setZoom(11);
      updatedevicemap.value.setView([site.lat, site.lon]);
      upateDeviceMarker.value.setLatLng([site.lat, site.lon]);
    }    
  })

watch(siteLoading, (loading) => {
  console.log("LOADING CHANGED", loading)
  if(!!site.value){
    if(!!mymap.value){
   
      console.log("SITE IS READY")
      mymap.value.setZoom(11);
      mymap.value.panTo([site.value.lat, site.value.lon]);

      // Add markers to Cluster
      site.value.devices.forEach(dev => {
        markers.addLayer(
          marker([dev.lat, dev.lon],{title: "Site",opacity:1.0,riseOnHover:true })
          .on('click', (e) => { 
          console.log("Clicked marker");
              })   

          .bindPopup(`${_.capitalize(dev.name)}`)  
          .setIcon(greenIcon.value)   
      );
      });

      mymap.value.addLayer(markers); 
      // console.log(markers)

      /*

      createSiteMarker.value = circleMarker([site.value.lat, site.value.lon],{radius: 20, color:"#00ff00"})
    .on('click', (e) => { 
    console.log("Clicked marker");
    //  dashboardTopic.value["dashboard"] = `/sensors/${msg.id}`;
    //  UserStore.setSelectedStation(msg.id);
        })   

    .bindPopup('Waiting for data')      
  .addTo(mymap.value)
*/
      // HERE
      // mymap.value.setZoom(11);
      // mymap.value.setView([site.value.lat, site.value.lon]);
      // createSiteMarker.value.setLatLng([site.value.lat, site.value.lon]);
    }
  }    
})



// COMPUTED PROPERTIES
const entitySiteName = computed(()=>{
  let entity = "";
  let sitename = "";

  if (!!route.params.entity)
      entity = route.params.entity
  if(!!site.value)
    sitename = site.value.name
  return {"entity": entity, "site": sitename}
})


const enableSiteUpdateBtn  = computed(() => 
     {       
      if(!!updateSite.lat && !!updateSite.lon  && !!updateSite.name){
        if(updateSite.name.length > 3 && updateSite.lat > 0  && updateSite.lon > 0 )
            return false
      }
      return true        
     } 
  ) 

const enableDeviceCreateBtn = computed(() => 
     {       
      if(!!createDevice.lat && !!createDevice.lon  && !!createDevice.name){
        if(createDevice.name.length > 3 && createDevice.lat.length > 3  && createDevice.lon.length > 3 )
            return false
      }
      return true        
     } 
  ) 

const enableDeviceUpdateBtn = computed(() => 
     {       
      if(!!updateDevice.lat && !!updateDevice.lon  && !!updateDevice.name){
        if(updateDevice.name.length > 3 && updateDevice.lat.length > 3  && updateDevice.lon.length > 3 )
            return false
      }
      return true        
     } 
  ) 

const getDeviceIcon = computed(() => {
  let found = processors.value.filter( dev => dev.name == device.value.processor );
  if(found.length > 0)
    return found[0].icon

  return ""
}) 

const  pickAllParams = computed(() => {
        return createDevice.params.length === paramOptions.value.length
      })

const  pickAllParamsUpdate = computed(() => {
  return updateDevice.params.length === paramOptions.value.length
})

const  pickSomeParams = computed(() => {
    return createDevice.params.length > 0
      })

const  pickSomeParamsUpdate = computed(() => {
    return updateDevice.params.length > 0
      })

//FUNCTIONSs
watch( () => userSearch.value.text, async (text) => {   
    console.log(text)
    clearTimeout(searchTextID); // prevent errant multiple timeouts from being generated
    if(!!text || text == ''){   
        if(text.length > 0){
            searchTextID = setTimeout( async () => {
            // SEND QUERY ONLY IF TEXT PASSES REGEX. THIS FILTERS OUT INVALID TEXT QUERIES
            if(/^[A-Za-z0-9]*$/.test(text) ){               
                await AppStore.searchUser(text);                
            }
                }, timeoutVal);
        }     
    }
});


const  toggle = () => {
        if (pickAllParams.value) {
          createDevice.params = []
        } else {
          createDevice.params = paramOptions.value.slice()
        }
      }

const  toggleUpdate = () => {
      if (pickAllParamsUpdate.value) {
        updateDevice.params = []
      } else {
        updateDevice.params = paramOptions.value.slice()
      }
    }

const addDevice = async () => {
    // let result = await AppStore.createDevice(createDevice, site.value.id);
    let result = await AppStore.submitRequest("createdevice" , {"siteid": site.value.id, ...createDevice} , createDeviceLoading);
 
    switch (result) {
        case "submitted":
            // AppStore.getSite(route.params.id);
            openCreateDevice.value = false;
            createDevice.name  = "";
            createDevice.lat  = "0";
            createDevice.lon  = "0";
            createDevice.params  = [];
            createDevice.processor  = "";

            toast.add({ severity: 'success', summary: 'CREATED', detail: 'Successfully sent new DEVICE! request', life: 3000 });             
            break;
        
        case "failed": 
            openCreateDevice.value = false;
            toast.add({ severity: 'error', summary: 'FAILED', detail: 'Unable to send new DEVICE! request', life: 3000 });         
            break;  

        default:
            toast.add({ severity: 'error', summary: 'Request Failed', detail: 'Request failed!', life: 3000 });  
            break;
    }
}

const updateSingleDevice = async () => {
    // let result = await AppStore.updateDevice(updateDevice);
    let result = await AppStore.submitRequest("updatedevice" , updateDevice , updateDeviceLoading);
 
    switch (result) {
        case "submitted":
            openUpdateDevice.value = false;
            toast.add({ severity: 'success', summary: 'UPDATED', detail: 'Successfully sent update DEVICE! request', life: 3000 });             
            break;
        
        case "failed": 
            openUpdateDevice.value = false;
            toast.add({ severity: 'error', summary: 'FAILED', detail: 'Unable to update DEVICE!', life: 3000 });         
            break;  

        default:
            toast.add({ severity: 'error', summary: 'Request Failed', detail: 'Request failed!', life: 3000 });  
            break;
    }
}

const deleteSingleDevice = async () => {
    // let result = await AppStore.deleteDevice(site.value.id,deleteDeviceID.value);
    let result = await AppStore.submitRequest("deletedevice" , deleteDevice , deleteDeviceLoading);
 
    switch (result) {
        case "submitted":                       
            openDeleteDevice.value = false;
            toast.add({ severity: 'success', summary: 'DELETED', detail: 'Successfully sent DEVICE! deletion request', life: 3000 });             
            break;
        
        case "failed":             
            openDeleteDevice.value = false;
            toast.add({ severity: 'error', summary: 'FAILED', detail: 'Unable to send DEVICE! deletion request', life: 3000 });         
            break;  

        default:
            toast.add({ severity: 'error', summary: 'Request Failed', detail: 'Request failed!', life: 3000 });  
            break;
    }
}

const updateSingleSite = async () => { 
    let result = await AppStore.submitRequest("updatesite" , updateSite , updateSiteLoading);
 
    switch (result) {
        case "submitted":                        
            openUpdateSite.value = false;
            toast.add({ severity: 'success', summary: 'UPDATED', detail: 'Successfully sent update SITE! request', life: 3000 });             
            break;
        
        case "failed": 
            openUpdateSite.value = false;
            toast.add({ severity: 'error', summary: 'FAILED', detail: 'Unable to send update SITE! request', life: 3000 });         
            break;  

        default:
            toast.add({ severity: 'error', summary: 'Request Failed', detail: 'Request failed!', life: 3000 });  
            break;
    }
}

const assignUser = async (id) => {
    let result = await AppStore.assignUser(site.value.id,id);
 
    switch (result) {
        case "assigned":                       
            openSearch.value = false;
            toast.add({ severity: 'success', summary: 'COMPLETED', detail: 'Successfully ASSIGNED/UNASSIGNED user account', life: 3000 });             
            break;
        
        case "failed":             
            openSearch.value = false;
            toast.add({ severity: 'error', summary: 'FAILED', detail: 'Unable to ASSIGN/UNASSIGN user account', life: 3000 });         
            break;  

        default:
            toast.add({ severity: 'error', summary: 'Request Failed', detail: 'Request failed!', life: 3000 });  
            break;
    }
}



const setDeviceUpdate = (dev) => {  
    updateDevice.siteid = site.value.id;
    updateDevice.deviceid = dev.id;
    updateDevice.lat = dev.lat;
    updateDevice.lon = dev.lon;
    updateDevice.name = dev.name;
    updateDevice.params = dev.params;
    updateDevice.processor = dev.processor;
}

const setSiteUpdate = () => { 
    updateSite.id = site.value.id;
    updateSite.lat = site.value.lat;
    updateSite.lon = site.value.lon;
    updateSite.name = site.value.name; 
    updateSite.enabled = site.value.enabled
}

const setMarkerOnListMap = (lat, lon) => {    
    mymap.value.setZoom(16);
    mymap.value.panTo([lat, lon]);
    // createDeviceMarker.value.setLatLng([lat, lon]);     
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



onBeforeMount(()=>{  
    AppStore.getSite(route.params.id);
})


onMounted(() => {

blueIcon.value  = createIcon("bluestripe");
redIcon.value   = createIcon("redstripe");
greenIcon.value = createIcon("greenstripe");
goldIcon.value  = createIcon("goldstripe");
blackIcon.value = createIcon("blackstripe");


mymap.value =  map('sitemap',{ zoomControl: false}).setView([14.5255555556, -75.8183333333], 4);     


tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}', {
            attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
            maxZoom: 18,
            id: 'tedwardsuwi/cl0d2e6io000t14qntylpu4j4',
            tileSize: 512,
            zoomOffset: -1,
            accessToken: 'pk.eyJ1IjoidGVkd2FyZHN1d2kiLCJhIjoiY2x3Y3RqMXY1MHpuNTJxcDA4emQ0ejQycCJ9.t-ENJ58Apo7e4gfhEidE8A'
        }).addTo(mymap.value);
 
  //  mtLayer.addTo(mymap.value) 

})



onUnmounted(()=>{
  AppStore.resetSite();
  AppStore.resetDevice();  

  if(!!listmap.value)
    listmap.value.remove();

  if(!!updatesitemap.value)
    updatesitemap.value.remove();

  if(!!updatedevicemap.value)
    updatedevicemap.value.remove();
})

 
 
  </script>
  
  <style>

</style>