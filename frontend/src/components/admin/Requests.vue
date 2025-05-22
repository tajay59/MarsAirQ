<template>  
    <div class="  w-full h-dvh flex flex-col" >
   
   <div class=" h-20 flex flex-col justify-center ml-16 " >
       <!-- TOP BAR -->
   </div>
   
   <div class="bg-neutral-200 dark:bg-neutral-800 h-full ml-10 rounded-tl-3xl overflow-hidden  border border-neutral-800" >
       <VContainer  align="center" fluid>                           
           <VRow style="max-width: 1200px; width: 100%">
           <VCol>
            <p>REQUESTS</p>
            <VList rounded="lg" density="compact" max-width="700" variant="flat" class="relative mx-auto"  >
                <VListItem  variant="text" :active="false" class="bg-neutral-100 dark:bg-neutral-600/[0.3] mb-2"  v-for="request in requests"  :title="`${_.capitalize(request.reqtype)}`" :subtitle="''" :key="request.id" :value="request.id"  border rounded="lg" >
                    <template #title ><span class="text-sm font-bold" >{{`${ request.data.name}`}}</span></template>
                    <template #subtitle ><span class="text-xs" >{{ request.data.lat }}  {{ request.data.lon }}</span></template>
                    <template #append>        
                        <!-- <Icon :icon="account.user.icon" width="30" height="30" class="absolute top-2 right-3"  />      -->
                    </template>
                    <!-- <VDivider  :thickness="1"  class="my-5 border-opacity-100 border-neutral-600  dark:border-neutral-400" /> -->
                    <VListItemAction class="justify-between pb-2" >
                        <!-- <p class="" >{{ account.user.organization }}</p> -->
                        <div    >
                            <VBtn text="Approve" variant="text" density="compact" color="onSurface"  class="self-end text-subtitle-2 mx-1" @click="dialog = true; denyOrApprove.id = request.id; denyOrApprove.decision = 'approve'" />
                            <VBtn text="Deny" variant="text" density="compact" color="onSurface" class="self-end text-subtitle-2 mx-1" @click="dialog = true; denyOrApprove.id = request.id; denyOrApprove.decision = 'deny'" />
                        </div>           
                    </VListItemAction>
                </VListItem>
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
   
   
   
       // VARIABLES
       const AppStore        = useAppStore();
       const UserStore       = useUserStore();
       const { xs,smAndDown,smAndUp, mdAndUp }   = useDisplay();
       const dialog            = ref(false);
       const denyOrApprove     = reactive({"id":"","decision":""})
       const { darkmode, layout}  = storeToRefs(UserStore);
       const { allStaffAccounts,emailSelectedItem, emailList, requests }      = storeToRefs(AppStore);
       const variant         = "solo-inverted"; //   'outlined' | 'plain' | 'underlined' | 'filled' | 'solo' | 'solo-inverted' | 'solo-filled'
       const emailState      = reactive({registration:"",cancellation:""});
       const requestLoading  = ref(false);
   
      
    
       // FUNCTIONS
   
     const sendAODRequest = async () => {
            let result = await AppStore.approveOrDenyRequest(denyOrApprove.id, denyOrApprove.decision);
        
            switch (result) {
                case "approved":
                    getAccounts();
                    dialog.value = false;
                    toast.add({ severity: 'success', summary: 'APPROVED', detail: 'Account successfully APPROVED!', life: 3000 }); 
                    
                    break;
                
                case "denied":
                    getAccounts();
                    dialog.value = false;
                    toast.add({ severity: 'success', summary: 'DENIED', detail: 'Account successfully DENIED', life: 3000 });         
                    break;  

                default:
                    toast.add({ severity: 'error', summary: 'Request Failed', detail: 'Aprrove/Deny request failed!', life: 3000 });  
                    break;
            }
        }
   
       onMounted(()=>{
      
           AppStore.getAllStaff(); 
           AppStore.getEmailList();
           console.log("ready-set learn")
           AppStore.getRequests(requestLoading);
       })
   
   
   
   </script>
   
   <style>
   
   </style>