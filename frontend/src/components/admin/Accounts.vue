<template>
<div class="relative" >
 <p class="text-none font-light text-4xl max-w-[1000px] w-full mx-auto" >Account Details</p>
  
 <VFab text="Edit"  @click="edit = !edit" variant="plain" color="onSurface" :ripple="false" class=" top-1 right-14"   size="large" absolute offset>
   <div class="flex flex-col justify-center" >
    <TransitionGroup name="slide-right" >
        <VIcon  v-if="!edit"  icon="mdi:mdi-account-edit" size="30" />
        <VIcon v-else icon="mdi:mdi-pencil" size="30" />
    </TransitionGroup>
     
    <TransitionGroup name="slide-right" >
        <p v-if="!edit" class="text-none" style="font-size: xx-small;" >EDIT</p>
        <p v-else class="text-none" style="font-size: xx-small;" >EDITING...</p>
    </TransitionGroup>   
   </div>
 </VFab>

 <VFab text="Edit" v-if="!!selectedAccount"  @click="dialog = true" variant="plain"  color="tertiary"  class="mr-15 top-1 right-20" :ripple="false"   size="large" absolute offset>
  <div class="flex flex-col justify-center" >
    <VIcon   icon="mdi:mdi-account-remove" size="30" />
    <p class="text-none" style="font-size: xx-small;" >DELETE</p>
  </div>
 </VFab>
 
 <VCard v-if="!!selectedAccount" border  class="pb-5 mt-15 bg-neutral-100 dark:bg-neutral-700/[0.5] mx-auto " flat width="100%" max-width="1000"  >
    <template #title> <p class="" >{{ _.capitalize(selectedAccount.firstname) }} {{ _.capitalize(selectedAccount.lastname) }}</p></template>
    <template #subtitle> <p class="" >{{ selectedAccount.email }}</p></template>
    <template #append > <Icon :icon="selectedAccount.icon" width="30" height="30"   /> </template>

    <Transition name="slide-right" >
      <VCardItem class="py-3 ml-2" v-if="edit" >
          <VContainer fluid  >
              <VRow justify="space-between" align="center" >
                <div class="flex " > <VBtn icon flat width="10" height="10" class="!bg-lime-600 dark:!bg-lime-400 mr-2"  />  <p class="text-xs font-bold nunito-text" > Changes made ...</p>    </div>  
                <VBtn text="Submit Changes" v-if="edit" @click="updateAccount()" :loading="updateAccLoading" color="tertiary" variant="tonal" class="text-subtitle-2"  rounded="lg"   />              
              </VRow>
          </VContainer>
      </VCardItem>            
    </Transition>  


    <VCardItem class="py-0">
        <VContainer fluid  >
            <VRow class="  bg-neutral-200 dark:bg-neutral-800/[0.5]  rounded-lg  border border-neutral-400"  >
                <VCol  > <p class="text-sm font-bold nunito-text" >Organization</p> </VCol>
                <VCol  :align="tableAlign"> <p class="Nunito-text" >{{ selectedAccount.organization  }}</p></VCol>
            </VRow>
        </VContainer>
    </VCardItem>

    <VCardItem class="py-0">
        <VContainer fluid  >
            <VRow class="  bg-neutral-200 dark:bg-neutral-800/[0.5] rounded-lg  border border-neutral-400" >
                <VCol  > <p class="text-sm font-bold nunito-text" >ID</p> </VCol>
                <VCol  :align="tableAlign"> <p class="Nunito-text" >{{ selectedAccount.id  }}</p></VCol>
            </VRow>
        </VContainer>
    </VCardItem>

    <VCardItem class="py-0">
        <VContainer fluid  >
            <VRow class="  bg-neutral-200 dark:bg-neutral-800/[0.5] rounded-lg  border border-neutral-400" >
                <VCol  > <p class="text-sm font-bold nunito-text" >Created</p> </VCol>
                <VCol  :align="tableAlign"> <p class="Nunito-text" >{{ new Date(selectedAccount.registered).toLocaleDateString('en-us', { weekday:'long', year:'numeric', month:'short', day:'numeric'})  }}</p></VCol>
            </VRow>
        </VContainer>
    </VCardItem>

    <VCardItem class="py-0">
        <VContainer fluid  >
            <VRow class="  bg-neutral-200 dark:bg-neutral-800/[0.5] rounded-lg  border border-neutral-400" >
                <VCol  > <p class="text-sm font-bold nunito-text" >Country</p> </VCol>
                <VCol  :align="tableAlign"> <p class="Nunito-text" >{{ selectedAccount.country }}</p></VCol>
            </VRow>
        </VContainer>
    </VCardItem>

    <VCardItem class="py-0">
        <VContainer fluid class=" "  >
            <VRow class="  bg-neutral-200 dark:bg-neutral-800/[0.5] rounded-lg  border border-neutral-400"  :class="[(selectedAccount.role != selectedAccEdited.role && edit)? 'border-x-4 border-lime-600 dark:border-lime-400' : '']" >
                <VCol  > <p class="text-sm font-bold nunito-text" >Role</p> </VCol>
                <VCol :align="tableAlign">    
                    <TransitionGroup name="slide-right" >
                        <VSelect v-if="edit" v-model="selectedAccEdited.role" variant="solo-filled" density="compact"  max-width="150" rounded="lg" flat border  :items="['admin','user','staff']" hide-details ></VSelect>
                        <p v-else class="Nunito-text" >{{  _.capitalize(selectedAccount.role) }}</p>
                    </TransitionGroup>             
                </VCol>
            </VRow>
        </VContainer>
    </VCardItem>

    <VCardItem class="py-0">
        <VContainer fluid class=" "  >
            <VRow class="bg-neutral-200 dark:bg-neutral-800/[0.5] rounded-lg  border border-neutral-400"  :class="[(selectedAccount.activated != selectedAccEdited.activated && edit)? 'border-x-4 border-lime-600 dark:border-lime-400' : '']" >
                <VCol  > <p class="text-sm font-bold nunito-text" >Activated</p> </VCol>
                <VCol :align="tableAlign">    
                    <TransitionGroup name="slide-right" >
                        <VSwitch v-if="edit" density="compact"  v-model="selectedAccEdited.activated" variant="tonal" max-width="70" inset  hide-details></VSwitch>                      
                        <p v-else class="Nunito-text" >{{  (selectedAccount.activated)? 'Yes' : 'No' }}</p>
                    </TransitionGroup>             
                </VCol>
            </VRow>
        </VContainer>
    </VCardItem>

    <VCardItem class="py-0">
        <VContainer fluid class=" "  >
            <VRow class="  bg-neutral-200 dark:bg-neutral-800/[0.5] rounded-lg  border border-neutral-400"  :class="[(selectedAccount.suball != selectedAccEdited.suball && edit)? 'border-x-4 border-lime-600 dark:border-lime-400' : '']" >
                <VCol  > <p class="text-sm font-bold nunito-text" >Subscribe to All</p> </VCol>
                <VCol :align="tableAlign">    
                    <TransitionGroup name="slide-right" >
                        <VSwitch v-if="edit" density="compact"  v-model="selectedAccEdited.suball" variant="tonal" max-width="70" inset  hide-details ></VSwitch>                      
                        <p v-else class="Nunito-text" >{{ (selectedAccount.suball)? 'Yes' : 'No' }}</p>
                    </TransitionGroup>             
                </VCol>
            </VRow>
        </VContainer>
    </VCardItem>
</VCard>

<VDialog v-model="dialog" max-width="400" persistent transition="dialog-bottom-transition" >
      <VCard   class="border-t-4border-rose-600 dark:border-rose-300 " density="compact"  > 
     
        <template #title >
          <div class="text-center" >
              <VIcon icon="mdi:mdi-account-remove"    size="100" />
          </div>
        
        </template>
        <template #text >
          <p >You are about to  <strong class="font-bold text-rose-700" > Delete </strong> this Account. Are you sure you want to continue?</p>
        </template>

          <template v-slot:actions>
            <VBtn text="Delete" class="text-subtitle-2" color="onSurface" width="100" :loading="removeAccLoading" @click="deleteAccount()" />
            <VBtn text="Cancel" class="text-subtitle-2" color="onSurface" width="100"    @click="dialog = false" />  
          </template>
      </VCard>
</VDialog>
 
      

</div>       
</template>

<script setup>
// IMPORTS   
import { storeToRefs } from 'pinia';
import { useUserStore} from '@/stores/userStore';
import { ref,watch ,onMounted,computed } from "vue";  
import { RouterLink, useRouter } from "vue-router";
import { useAppStore } from '@/stores/appStore';
import { useToast } from 'primevue/usetoast';
import _ from 'lodash';
import { Icon } from '@iconify/vue';


// VARIABLES 
const route             = useRouter(); 
const UserStore         = useUserStore();
const AppStore          = useAppStore();
const {
  staffs,
   users,
   removeAccLoading,
   updateAccLoading,
   selectedAccount,
   selectedAccEdited,
   edit}   = storeToRefs(AppStore);
const toast             = useToast();
const firstname         = ref("John");
const lastname          = ref("Doe");
const text              = ref("");
const changedText       = ref("");
const myWorker          = ref(null);
const tableAlign        = ref("start");
const dialog            = ref(false);


const caribbeanCountries = [
  {
    name: "Antigua and Barbuda",
    icon:"emojione-v1:flag-for-antigua-and-barbuda",
    center: {
      latitude: 17.0608,
      longitude: -61.7964
    }
  },
  {
    name: "Bahamas",
    icon:"emojione-v1:flag-for-bahamas",
    center: {
      latitude: 25.0239,
      longitude: -77.3963
    }
  },
  {
    name: "Barbados",
    icon:"emojione-v1:flag-for-barbados",
    center: {
      latitude: 13.1939,
      longitude: -59.5431
    }
  },
  {
    name: "Belize",
    icon:"emojione-v1:flag-for-belize",
    center: {
      latitude: 17.2510,
      longitude: -88.7719
    }
  },
  {
    name: "Cuba",
    icon:"emojione-v1:flag-for-cuba",
    center: {
      latitude: 21.5217,
      longitude: -77.7812
    }
  },
  {
    name: "Dominica",
    icon:"emojione-v1:flag-for-dominica",
    center: {
      latitude: 15.4150,
      longitude: -61.3710
    }
  },
  {
    name: "Dominican Republic",
    icon:"emojione-v1:flag-for-dominican-republic",
    center: {
      latitude: 19.1940,
      longitude: -70.6667
    }
  },
  {
    name: "Grenada",
    icon:"emojione-v1:flag-for-grenada",
    center: {
      latitude: 12.1165,
      longitude: -61.6790
    }
  },
  {
    name: "Guyana",
    icon:"emojione-v1:flag-for-guyana",
    center: {
      latitude: 4.9387,
      longitude: -58.9310
    }
  },
  {
    name: "Haiti",
    icon:"emojione-v1:flag-for-haiti",
    center: {
      latitude: 18.9712,
      longitude: -72.2852
    }
  },
  {
    name: "Jamaica",
    icon:"emojione-v1:flag-for-jamaica",
    center: {
      latitude: 18.1096,
      longitude: -77.2975
    }
  },
  {
    name: "Saint Kitts and Nevis",
    icon:"emojione-v1:flag-for-st-kitts-and-nevis",
    center: {
      latitude: 17.3571,
      longitude: -62.7829
    }
  },
  {
    name: "Saint Lucia",
    icon:"emojione-v1:flag-for-st-lucia",
    center: {
      latitude: 13.9094,
      longitude: -60.9789
    }
  },
  {
    name: "Saint Vincent and the Grenadines",
    icon:"emojione-v1:flag-for-st-vincent-and-grenadines",
    center: {
      latitude: 13.2541,
      longitude: -61.2072
    }
  },
  {
    name: "Suriname",
    icon:"emojione-v1:flag-for-suriname",
    center: {
      latitude: 3.9190,
      longitude: -56.0278
    }
  },
  {
    name: "Trinidad and Tobago",
    icon:"emojione-v1:flag-for-trinidad-and-tobago",
    center: {
      latitude: 10.6918,
      longitude: -61.2225
    }
  }
];



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

const getCountryIcon = (country) => {
        let found = caribbeanCountries.filter((name)=> name == country)
        let result = "";
        if(found.length > 0){
            result = found[0].icon
        }
        
    return result
    }


// FUNCTIONS
const getAccounts = () => {
    if (!!window.SharedWorker) {
        if(!!myWorker.value){
            const cookie        = UserStore.getCookie("csrf_access_token");         
            myWorker.value.port.postMessage({"user": UserStore.getID, "cookie": cookie, "selected": (!!selectedAccount.value)? selectedAccount.value.id : null, "role": (!!selectedAccount.value)? selectedAccount.value.role : null });      
        }
    }
}

const updateAccount = async () => {
  let result = await AppStore.updateAccount();

  switch (result) {
      case "updated":
          // AppStore.setSelectedAccount(null);
          edit.value = false;
          getAccounts();
          toast.add({ severity: 'success', summary: 'UPDATED', detail: 'Account successfully UPDATED!', life: 3000 });  
          break;
      
      case "failed":
          getAccounts();
          edit.value = false;
          toast.add({ severity: 'error', summary: 'FAILED', detail: 'Unable to update selected account', life: 3000 });  
          break;  

      default:
          toast.add({ severity: 'error', summary: 'Request Failed', detail: 'Account update request failed!', life: 3000 });  
          break;
  }
}

const deleteAccount = async () => {
    let result = await AppStore.removeAccount();

    switch (result) {
        case "deleted":
            AppStore.setSelectedAccount(null);
            dialog.value = false;
            getAccounts();
            toast.add({ severity: 'success', summary: 'DELETED', detail: 'Account successfully DELETED!', life: 3000 });  
            break;
        
        case "failed":
            getAccounts();
            dialog.value = false;
            toast.add({ severity: 'error', summary: 'FAILED', detail: 'Unable to delete selected account', life: 3000 });  
            break;  

        default:
            toast.add({ severity: 'error', summary: 'Request Failed', detail: 'Aprrove/Deny request failed!', life: 3000 });  
            break;
    }
  }

onMounted(()=>{
    // console.log("TEMPLATE COMPONENT CREATED");

    if (!!window.SharedWorker) {
        myWorker.value = new SharedWorker("/src/assets/js/adminAccountsWorker.js");
    
        myWorker.value.port.onmessage = (e) => { 
            let {newRegistrations, staffs, users, selected} = e.data;
            console.log(e.data);
            AppStore.setAdminAccountVariables("newRegistrations",newRegistrations);
            AppStore.setAdminAccountVariables("staffs",staffs);
            AppStore.setAdminAccountVariables("users",users);
            
            if(!!selected)
              AppStore.setSelectedAccount(selected);
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