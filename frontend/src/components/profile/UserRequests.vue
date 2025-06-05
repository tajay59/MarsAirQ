<template>  
    <div class="w-full flex flex-col" >
   
   <div class="h-20 flex flex-col justify-center ml-16 " >
       <!-- TOP BAR -->
   </div>
   
   <div class="bg-neutral-200 dark:bg-neutral-800 h-full ml-10 rounded-tl-3xl overflow-hidden  border border-neutral-800" >
       <VContainer  align="center" fluid>                           
           <VRow style="max-width: 1200px; width: 100%">
                <VCol> 
                    <VList rounded="lg" density="compact" variant="flat" class="relative mx-auto w-full"  >
                        <div  v-for="request in requests" @click="selectedRequest = request.id" class="max-w-[700px]"   >
                            <VListItem v-if="['createentity','updateentity','deleteentity'].includes(request.reqtype)"  variant="text" :active="false" class="bg-neutral-100 dark:bg-neutral-600/[0.3] mb-2"   :title="`${_.capitalize(request.reqtype)}`" :subtitle="''" :key="request.id" :value="request.id"  border rounded="lg" >
                                <!-- CREATE / UPDATE ENTITY REQUEST -->
                                <template #title ><span class="text-lg font-bold" >{{`${ request.data.name}`}}</span></template>
                                <template #subtitle >
                                    <div class="flex flex-col justify-start align-start" >
                                        <div v-if="request.reqtype == 'createentity'" class="text-xs font-bold" >Entity Request </div>
                                        <div v-else-if="request.reqtype == 'updateentity'" class="text-xs font-bold" >Update Entity Request </div>
                                        <div v-else-if="request.reqtype == 'deleteentity'" class="text-xs font-bold" >Delete Entity Request </div>
                                    <div class="text-xs mt-3" >{{ request.data.organization }} </div>
                                    </div>
                                </template>
                                <template #append>        
                                    <Icon :icon="AppStore.getCountryIcon(request.data.country)" width="30" height="30" class="absolute top-2 right-3"  />     
                                </template>
                            </VListItem>


                            <VListItem v-if="['deletesite','createsite','updatesite'].includes(request.reqtype)"  variant="text" :active="false" class="bg-neutral-100 dark:bg-neutral-600/[0.3] mb-2"   :title="`${_.capitalize(request.reqtype)}`" :subtitle="''" :key="request.id" :value="request.id"  border rounded="lg" >
                                <!-- CREATE/UPDATE/DELETE SITE REQUEST -->
                                <template #title ><span class="text-lg font-bold" >{{`${ request.data.name}`}}</span></template>
                                <template #subtitle >
                                    <div class="flex flex-col justify-start align-start" > 
                                        <div v-if="request.reqtype == 'createsite'" class="text-xs font-bold" >Create Site Request </div>
                                        <div v-else-if="request.reqtype == 'updatesite'" class="text-xs font-bold" >Update Site Request </div>
                                        <div v-else-if="request.reqtype == 'deletesite'" class="text-xs font-bold" >Delete Site Request </div>
                                        <div class="text-sm font-bold mt-3" >Latitude: <span>{{ request.data.lat }}</span>  Longitude: <span>{{ request.data.lon }}</span>  </div>
                                    
                                    </div>
                                </template>
                                <template #append>        
                                    <Icon :icon="AppStore.getCountryIcon(request.data.country)" width="30" height="30" class="absolute top-2 right-3"  />     
                                </template>
                            </VListItem>

                            <VListItem v-if="['deletedevice','createdevice','updatedevice'].includes(request.reqtype)"  variant="text" :active="false" class="bg-neutral-100 dark:bg-neutral-600/[0.3] mb-2"   :title="`${_.capitalize(request.reqtype)}`" :subtitle="''" :key="request.id" :value="request.id"  border rounded="lg" >
                                <!-- CREATE/UPDATE/DELETE SITE REQUEST -->
                                <template #title ><span class="text-lg font-bold" >{{`${ request.data.name}`}}</span></template>
                                <template #subtitle >
                                    <div class="flex flex-col justify-start align-start" > 
                                        <div v-if="request.reqtype == 'createdevice'" class="text-xs font-bold" >Create Device Request </div>
                                        <div v-else-if="request.reqtype == 'updatedevice'" class="text-xs font-bold" >Update Device Request </div>
                                        <div v-else-if="request.reqtype == 'deletedevice'" class="text-xs font-bold" >Delete Device Request </div>
                                        <div class="text-sm font-bold  mt-3" >Site: <span>{{ request.site.name }}</span>    </div>
                                        <div class="text-sm font-bold" >Latitude: <span>{{ request.data.lat }}</span>  Longitude: <span>{{ request.data.lon }}</span>  </div>                                
                                    </div>
                                </template>
                                <template #append>        
                                    <Icon :icon="AppStore.getCountryIcon(request.data.country)" width="30" height="30" class="absolute top-2 right-3"  />     
                                </template>
                            </VListItem>
                        </div>
                    
                    </VList>
                </VCol>
           </VRow>
       </VContainer> 
   </div>      
   
   </div>
    
   </template>
   
   <script   setup>
       import { ref,reactive, onMounted,computed, watch} from 'vue';
       import { useAppStore} from '@/stores/appStore'; 
       import { useUserStore } from '@/stores/userStore';
       import { storeToRefs } from 'pinia';
       import { useDisplay } from 'vuetify';
       import _ from 'lodash';
       import { Icon } from '@iconify/vue';
       import { useToast } from 'primevue/usetoast';
   
   
   
       // VARIABLES
       const AppStore        = useAppStore();
       const UserStore       = useUserStore();
       const toast           = useToast(); 
       const { xs,smAndDown,smAndUp, mdAndUp }   = useDisplay();
       const dialog            = ref(false);
       const denyOrApprove     = reactive({"id":"","decision":""})
       const { darkmode, layout}  = storeToRefs(UserStore);
       const { allStaffAccounts,emailSelectedItem, emailList, requests,aodLoading }      = storeToRefs(AppStore);
       const variant         = "solo-inverted"; //   'outlined' | 'plain' | 'underlined' | 'filled' | 'solo' | 'solo-inverted' | 'solo-filled'
       const emailState      = reactive({registration:"",cancellation:""});
       const requestLoading  = ref(false);
       const selectedRequest = ref(""); 
   
         
       // FUNCTIONS   
       onMounted(()=>{  
           AppStore.getRequests(requestLoading);
       })
   
   
   
   </script>
   
   <style>
   
   </style>