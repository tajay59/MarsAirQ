    <template>
    <div class=" flex flex-col gap-3 [&>*]:max-w-[500px] [&>*]:w-full  justify-between align-center" >
        <p class="text-lg font-bold mb-10" >Edit Profile</p>  
        <div class="flex justify-between mb-15"  >
            <div class="bg-[url('@/assets/default.png')]  size-[150px] rounded-full relative border border-neutral-500 dark:border-neutral-400" >
                <VTooltip text="Edit Profile Data">
                    <template v-slot:activator="{ props }">                        
                        <VBtn v-bind="props"flat icon name="Edit Profile Data" class="absolute right-0 bottom-0 border-4 border-neutral-100 dark:border-neutral-800" @click="enableForm = !enableForm" >
                            <template #default >
                                <Icon icon="fluent:edit-12-filled" width="24" height="24" class=" z-[20000]"  />   
                            </template>
                        </VBtn>  
                    </template>
                </VTooltip>
                        
            </div> 

            <div class="flex gap-3 place-content-center ">
                <div class="flex flex-col place-content-end " >
                <VBtn  flat icon variant="text" width="40" height="40" class=" border-4 border-neutral-100 dark:border-neutral-800 size-[36px]" density="compact" >
                    <template #default >
                        <Icon v-if="userAccount.activated" icon="nrk:check-active" width="32" height="32" class=" z-[20000]"  />   
                        <Icon v-else icon="nrk:close-active" width="32" height="32" class=" z-[20000]"  />   
                    </template>
                </VBtn> 
                <span class="text-xs font-bold" >Active</span>
            </div>

            <div class="flex flex-col  place-content-end" >
                <VBtn flat icon variant="text" width="40" height="40" class=" border-4 border-neutral-100 dark:border-neutral-800" density="compact">
                    <template #default >
                        <Icon v-if="userAccount.suball" icon="fluent:plug-connected-16-filled" width="32" height="32" class=" z-[20000]"  />   
                        <Icon v-else icon="fluent:plug-disconnected-20-regular" width="32" height="32" class=" z-[20000]"  />   
                    </template>
                </VBtn> 
            
                <span class="text-xs  font-bold" >Sub-All</span>
               
            </div>
            </div>
        </div>
       
        <div class="my-5 text-lg font-semibold nunito" > Registered: {{ registered }}</div>

        <div class="flex gap-2" >
            <VTextField v-model="userAccount.firstname" label="First Name" :disabled="enableForm" class="!h-[50px] pa-0 ma-0  rounded-xl border border-neutral-600 dark:border-neutral-50 overflow-clip" density="compact" variant="solo-inverted"  flat hide-details clearable /> 
            <VTextField v-model="userAccount.lastname" label="Last Name"  :disabled="enableForm" class="!h-[50px]   rounded-xl border border-neutral-600 dark:border-neutral-50 overflow-clip" density="compact" variant="solo-inverted"  flat hide-details clearable />        
        </div>
        <VTextField v-model="userAccount.email" label="Email"   :disabled="enableForm" class="!h-[50px] rounded-xl border border-neutral-600 dark:border-neutral-50 overflow-clip" density="compact" variant="solo-inverted"  flat hide-details clearable /> 
        <VTextField v-model="userAccount.organization" label="Organization"  :disabled="enableForm" class="!h-[50px] rounded-xl border border-neutral-600 dark:border-neutral-50 overflow-clip" density="compact" variant="solo-inverted"  flat hide-details clearable /> 
        <VSelect
             
            border
            flat 
            :items        = "countries"
            class         = "text-caption rounded-xl border border-neutral-600 dark:border-neutral-50 overflow-clip !h-[50px] "
            hide-details
            density       = "compact"
            label         = "Country"     
            variant       = "solo-inverted"                           
            type          = "text"             
            v-model       = "userAccount.country"  
            :disabled     = "enableForm" 
        >
        <template v-slot:clear>
            <VIcon icon="mdi:mdi-close-circle" @click="field.data = ''" size="16"></VIcon>
        </template>
        <template #append-inner >
            <Icon  :icon="userAccount.icon" width="32" height="32" class=" z-[20000]"  /> 
        </template>
        
        </VSelect>
        
        <!-- <VTextField v-model="userAccount.username" label="Mqtt Username" class="rounded-lg border border-neutral-600 dark:border-neutral-50 overflow-clip" density="compact" variant="solo-inverted"  flat hide-details clearable /> 
        <VTextField v-model="userAccount.passkey" label="Mqtt Key" class="my-2  text-xs rounded-lg border border-neutral-600 dark:border-neutral-50 overflow-clip" density="compact" variant="solo-inverted"  flat hide-details clearable /> 
        <VTextField v-model="userAccount.owner" label="Owner" class="rounded-lg border border-neutral-600 dark:border-neutral-50 overflow-clip" density="compact" variant="solo-inverted"  flat hide-details clearable /> 
        <VTextField v-model="userAccount.lat" label="Latitude" step="0.000001"  type="number" class="my-2 rounded-lg border border-neutral-600 dark:border-neutral-50 overflow-clip" density="compact" variant="solo-inverted"  flat hide-details  clearable />
        <VTextField v-model="userAccount.lon" label="Longitude" step="0.000001" type="number"  class="rounded-lg border border-neutral-600 dark:border-neutral-50 overflow-clip" density="compact" variant="solo-inverted"  flat hide-details  clearable /> -->
        
        <!-- <VImg  src="@/assets/default.png" width="130" height="130" cover class="relative mx-15 rounded-[50%] border-2 border-neutral-500 dark:border-neutral-400"  /> 
        <Icon icon="fluent:edit-12-filled" width="24" height="24" class="absolute z-[20000]"  />     -->
        <VBtn text="Submit" color="transparent" width="100"  class="mt-5 text-none !bg-neutral-700 dark:!bg-neutral-100  !text-neutral-100 dark:!text-neutral-900 !border " />
    </div>   
    </template>
    
    <script setup>
    // IMPORTS   
    import { storeToRefs } from 'pinia';
    import { useUserStore} from '@/stores/userStore';
    import { ref,watch ,onMounted,onBeforeMount,computed, reactive } from "vue";  
    import { RouterLink, useRouter } from "vue-router";
    import { useAppStore } from '@/stores/appStore';
    import { Icon } from '@iconify/vue';
    
    // VARIABLES 
    const route             = useRouter(); 
    const UserStore         = useUserStore();
    const AppStore          = useAppStore();
    const {userAccount, caribbeanCountries}     = storeToRefs(AppStore);
    const accountLoading    = ref(false);
    const enableForm        =  ref(true);
    const registrationDate  = ref(null); 
    const registrationTime  = ref(null)

    
    // PROPS
    const props = defineProps({
        item:{type:String,default:""},
    })

    const countries = computed(() => {
        let list = [];
        caribbeanCountries.value.forEach((country) => list.push(country.name));
        return list
        })
    
    // WATCHERS
    // watch(text,  (newText, oldText) => {
    //   console.log(newText); 
    //   changedText.value = newText ;
    // });
    
    // COMPUTED PROPERTIES
    const registered = computed(()=>{  
           /* 
        day:
            The representation of the day.
            Possible values are "numeric", "2-digit".
        weekday:
            The representation of the weekday.
            Possible values are "narrow", "short", "long".
        year:
            The representation of the year.
            Possible values are "numeric", "2-digit".
        month:
            The representation of the month.
            Possible values are "numeric", "2-digit", "narrow", "short", "long".
        hour:
            The representation of the hour.
            Possible values are "numeric", "2-digit".
        minute: The representation of the minute.
            Possible values are "numeric", "2-digit".
        second:
            The representation of the second.
            Possible values are "numeric", 2-digit".
        hour12:
            The representation of time format.
            Accepts boolean true or false
        */  
        
        console.log(userAccount.value.timestamp)
        if(!!userAccount.value.timestamp){ 
            let date = new Date(userAccount.value.timestamp * 1000);
            // registrationTime.value = date.toLocaleTimeString("en-US",{hour: 'numeric', minute: 'numeric'});
            return date.toLocaleDateString("en-US", { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric',hour12: true });  
            
        }         
            
        return null;
    });
    
    
    // FUNCTIONS
    onBeforeMount(()=>{ 
        AppStore.getAccount(accountLoading.value);
    })

    onMounted(()=>{
        console.log("TEMPLATE COMPONENT CREATED"); 
    })
    
    
    
     
    </script>
    
    <style>
    /*   Style */
    
     
    </style>