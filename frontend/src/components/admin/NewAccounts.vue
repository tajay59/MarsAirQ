<template>
<div class="Page">
<VDivider class="my-15" />
 <VList rounded="lg" density="compact" max-width="700" variant="flat" class="relative mx-auto"  >
    <VListItem  variant="text" :active="false" class="bg-neutral-100 dark:bg-neutral-600/[0.3] mb-2"  v-for="account in newRegistrations"  :title="`${account.user.firstname} ${account.user.lastname}`" :subtitle="account.user.email" :key="account.user.id" :value="account.user.id"  border rounded="lg" >
        <template #title ><span class="text-sm font-bold" >{{`${ _.capitalize(account.user.firstname)} ${ _.capitalize(account.user.lastname)}`}}</span></template>
        <template #subtitle ><span class="text-xs" >{{ account.user.email }}</span></template>
        <template #append>        
            <Icon :icon="account.user.icon" width="30" height="30" class="absolute top-2 right-3"  />     
        </template>
        <!-- <VDivider  :thickness="1"  class="my-5 border-opacity-100 border-neutral-600  dark:border-neutral-400" /> -->
        <VListItemAction class="justify-between pb-2" >
            <p class="" >{{ account.user.organization }}</p>
            <div    >
                <VBtn text="Approve" variant="text" density="compact" color="onSurface"  class="self-end text-subtitle-2 mx-1" @click="dialog = true; denyOrApprove.id = account.id; denyOrApprove.decision = 'approve'" />
                <VBtn text="Deny" variant="text" density="compact" color="onSurface" class="self-end text-subtitle-2 mx-1" @click="dialog = true; denyOrApprove.id = account.id; denyOrApprove.decision = 'deny'" />
            </div>           
        </VListItemAction>
    </VListItem>
</VList>

  

<VDialog v-model="dialog" max-width="400" persistent transition="dialog-bottom-transition" >
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
</div>       
</template>

<script setup>
// IMPORTS   
import { storeToRefs } from 'pinia';
import { useAppStore } from '@/stores/appStore';
import { useUserStore} from '@/stores/userStore';
import { ref,reactive,watch ,onMounted,computed } from "vue";  
import { RouterLink, useRouter } from "vue-router";
import { Icon } from '@iconify/vue';
import { useToast } from 'primevue/usetoast';
import _ from 'lodash';


// VARIABLES 
const route             = useRouter(); 
const UserStore         = useUserStore();
const AppStore          = useAppStore();
const {newRegistrations, aodLoading} = storeToRefs(AppStore);
const dialog            = ref(false);
const toast             = useToast();
const denyOrApprove     = reactive({"id":"","decision":""})
const firstname         = ref("John");
const lastname          = ref("Doe");
const text              = ref("");
const changedText       = ref("");
const myWorker          = ref(null);




// PROPS
const props = defineProps({
    item:{type:String,default:""},
})

// WATCHERS
watch(text,  (newText, oldText) => {
  console.log(newText); 
  changedText.value = newText ;
});

// COMPUTED PROPERTIES
const fullname = computed(()=>{    
    return `${firstname.value} ${lastname.value}`;
});


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

// FUNCTIONS
const getAccounts = () => {
    if (!!window.SharedWorker) {
        if(!!myWorker.value){
            const cookie        = UserStore.getCookie("csrf_access_token"); 
            myWorker.value.port.postMessage({"user": UserStore.getID, "cookie": cookie});      
        }
    }
}

onMounted(()=>{
    console.log("TEMPLATE COMPONENT CREATED");
    if (!!window.SharedWorker) {
        myWorker.value = new SharedWorker("/src/assets/js/adminAccountsWorker.js");
    
        myWorker.value.port.onmessage = (e) => { 
            let {newRegistrations, staffs, users} = e.data;
            console.log(e.data);
            AppStore.setAdminAccountVariables("newRegistrations",newRegistrations);
            AppStore.setAdminAccountVariables("staffs",staffs);
            AppStore.setAdminAccountVariables("users",users);
            // console.log(e.lastEventId);
        };

        myWorker.value.onerror = (error) => {
        console.log(`New Registrations Worker error: ${error.message}`);
        throw error;
      };        
    }
    

})

 
 
</script>

<style>
/*   Style */

 
</style>