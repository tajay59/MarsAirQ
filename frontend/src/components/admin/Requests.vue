<template>  
    <div class="  w-full h-dvh flex flex-col" >
   
   <div class=" h-20 flex flex-col justify-center ml-16 " >
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
                        
                        <VListItemAction class="justify-between py-2  mt-5" >
                            <div >
                                <VBtn  variant="text" density="compact" color="onSurface" icon  class="self-end text-subtitle-2 mx-1"  @click="toggle($event)" >
                                    <Icon icon="iconamoon:profile-fill" width="24" height="24" />
                                </VBtn>
                                <VBtn v-if="['updateentity'].includes(request.reqtype)" variant="text" density="compact" color="onSurface" icon  class="self-end text-subtitle-2 mx-1"  @click="toggleEntity($event)" >
                                    <Icon icon="fluent:organization-48-filled" width="24" height="24" />
                                </VBtn>
                            </div>
                            <div    >
                                <VBtn text="Approve" variant="text" density="compact" color="onSurface"  class="self-end text-subtitle-2 mx-1" @click="dialog = true; denyOrApprove.id = request.id; denyOrApprove.decision = 'approve'" />
                                <VBtn text="Deny" variant="text" density="compact" color="error" class="self-end text-subtitle-2 mx-1" @click="dialog = true; denyOrApprove.id = request.id; denyOrApprove.decision = 'deny'" />
                            </div>           
                        </VListItemAction>
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
                        <!-- <VDivider  :thickness="1"  class="my-5 border-opacity-100 border-neutral-600  dark:border-neutral-400" /> -->
                        <VListItemAction class="justify-between py-2 mt-5" >
                            <div >
                                <VBtn  variant="text" density="compact" color="onSurface" icon  class="self-end text-subtitle-2 mx-1"  @click="toggle($event)" >
                                    <Icon icon="iconamoon:profile-fill" width="24" height="24" />
                                </VBtn>
                                <VBtn  variant="text" density="compact" color="onSurface" icon  class="self-end text-subtitle-2 mx-1"  @click="toggleEntity($event)" >
                                    <Icon icon="fluent:organization-48-filled" width="24" height="24" />
                                </VBtn>
                            </div>
                            
                            <div    >
                                <VBtn text="Approve" variant="text" density="compact" color="onSurface"  class="self-end text-subtitle-2 mx-1" @click="dialog = true; denyOrApprove.id = request.id; denyOrApprove.decision = 'approve'" />
                                <VBtn text="Deny" variant="text" density="compact" color="error" class="self-end text-subtitle-2 mx-1" @click="dialog = true; denyOrApprove.id = request.id; denyOrApprove.decision = 'deny'" />
                            </div>           
                        </VListItemAction>
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
                        <!-- <VDivider  :thickness="1"  class="my-5 border-opacity-100 border-neutral-600  dark:border-neutral-400" /> -->
                        <VListItemAction class="justify-between py-2 mt-5" >
                            <div >
                                <VBtn  variant="text" density="compact" color="onSurface" icon  class="self-end text-subtitle-2 mx-1"  @click="toggle($event)" >
                                    <Icon icon="iconamoon:profile-fill" width="24" height="24" />
                                </VBtn>
                                <VBtn  variant="text" density="compact" color="onSurface" icon  class="self-end text-subtitle-2 mx-1"  @click="toggleEntity($event)" >
                                    <Icon icon="fluent:organization-48-filled" width="24" height="24" />
                                </VBtn>
                            </div>
                            
                            <div    >
                                <VBtn text="Approve" variant="text" density="compact" color="onSurface"  class="self-end text-subtitle-2 mx-1" @click="dialog = true; denyOrApprove.id = request.id; denyOrApprove.decision = 'approve'" />
                                <VBtn text="Deny" variant="text" density="compact" color="error" class="self-end text-subtitle-2 mx-1" @click="dialog = true; denyOrApprove.id = request.id; denyOrApprove.decision = 'deny'" />
                            </div>           
                        </VListItemAction>
                    </VListItem>
                </div>
              

                <Popover ref="op">
                    <div class="flex flex-col gap-4">
                        <div>
                            <span class="font-medium block mb-2">Requested by: </span>
                            <ul v-if="!!member" class="list-none p-0 m-0 flex flex-col">
                                <li  class="flex items-center gap-2 px-2 py-3 hover:bg-emphasis cursor-pointer rounded-border" >
                                    <Icon :icon="member.icon" width="48" height="48" />
                                    <div>
                                        <span class="font-medium">{{ member.firstname }} {{ member.lastname }}</span>
                                        <div class="text-sm text-surface-500 dark:text-surface-400">{{ member.email }}</div>
                                        <div class="text-sm text-surface-500 dark:text-surface-400">{{ member.organization }}</div>
                                    </div>
                                </li>
                            </ul>
                        </div>
                    </div>
                </Popover>

                <Popover ref="opEntity">
                    <div class="flex flex-col gap-4">
                        <div>
                            <span class="font-medium block mb-2">Entity: </span>
                            <ul v-if="!!requestEntity" class="list-none p-0 m-0 flex flex-col">
                                <li  class="flex items-center gap-2 px-2 py-3 hover:bg-emphasis cursor-pointer rounded-border" >
                                    <Icon :icon="requestEntity.icon" width="48" height="48" />
                                    <div>
                                        <span class="font-medium">{{ requestEntity.name }}</span>
                                        <div class="text-sm text-surface-500 dark:text-surface-400">{{ requestEntity.country }}</div>
                                        <div class="text-sm text-surface-500 dark:text-surface-400">{{ requestEntity.organization }}</div>
                                    </div>
                                </li>
                            </ul>
                        </div>
                    </div>
                </Popover>
            </VList>
         
            
           </VCol>
           </VRow>
           <VRow>
                <VDialog v-model="dialog" max-width="400" persistent transition="dialog-bottom-transition" >
                    <!-- APPROVE OR DENY -->
                    <VCard   class="border-t-4 " :class="[(denyOrApprove.decision == 'approve')? 'border-green-500':'border-rose-500']" density="compact"  > 
                    
                    <template #title >
                        <div class="text-center" >
                            <VIcon icon="mdi:mdi-account-check" v-if="denyOrApprove.decision == 'approve'" size="100" />
                            <VIcon icon="mdi:mdi-account-remove"  v-if="denyOrApprove.decision == 'deny'"  size="100" />
                        </div>
                    
                    </template>
                    <template #text >
                        <p  v-if="denyOrApprove.decision == 'approve'" >You are about to approve this Account. Are you sure?</p>
                        <p v-if="denyOrApprove.decision == 'deny'" >You are about to deny this Account. An E-mail will be sent to notify the user. Are you sure?  </p>
                    </template>

                        <template v-slot:actions>
                        <v-spacer></v-spacer>

                        <VBtn :text="_.capitalize(denyOrApprove.decision)"  class="text-subtitle-2" color="onSurface" width="100" :loading="aodLoading" @click="sendAODRequest()" />
                        <VBtn text="Cancel"  class="text-subtitle-2" color="onSurface" width="100"   @click="dialog = false" />  
                        </template>
                    </VCard>
                </VDialog>
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
   
       const op         = ref();
       const opEntity   = ref();

       const member = computed(() => {            
            let res = requests.value.filter(req => req.id == selectedRequest.value);  
            if (!!res[0])
                return res[0].account
        });
        const requestEntity = computed(() => {     
            let entity = null;       
            let res = requests.value.filter(req => req.id == selectedRequest.value);              

            if (!!res[0]){
                let icon = AppStore.getCountryIcon(res[0].entity.code);
                entity = {"icon": icon, ...res[0].entity }
            }                        
            return entity
        });
        
        const toggle = (event) => { op.value.toggle(event); };
        const toggleEntity = (event) => { opEntity.value.toggle(event); };
    
       // FUNCTIONS
       
   
     const sendAODRequest = async () => {
            let result = await AppStore.approveOrDenyRequest(denyOrApprove.id, denyOrApprove.decision);
        
            switch (result) {
                case "approved": 
                    AppStore.getRequests(requestLoading);
                    dialog.value = false;
                    toast.add({ severity: 'success', summary: 'APPROVED', detail: 'Request successfully APPROVED!', life: 7000 });                     
                    break;

                case "exist":  
                    dialog.value = false;
                    toast.add({ severity: 'warn', summary: 'NOTE', detail: 'Entity/Site/Device already exist', life: 7000 });         
                    break;   
                
                case "denied": 
                    AppStore.getRequests(requestLoading);
                    dialog.value = false;
                    toast.add({ severity: 'success', summary: 'DENIED', detail: 'Request successfully DENIED', life: 7000 });         
                    break;  

                default:
                    toast.add({ severity: 'error', summary: 'Request Failed', detail: 'Aprrove/Deny request failed!', life: 7000 });  
                    break;
            }
        }
   
       onMounted(()=>{
      
           AppStore.getAllStaff(); 
           AppStore.getEmailList(); 
           AppStore.getRequests(requestLoading);
       })
   
   
   
   </script>
   
   <style>
   
   </style>