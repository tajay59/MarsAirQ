<template>

      <div class=" w-full h-dvh flex flex-col" >

        <div class=" h-20 flex flex-col justify-center ml-16 " >
            <VBtnGroup  variant="outlined" divided density="compact" rounded="lg" class=""   >
                <VBtn v-for="comp in compToRender.list" :text="comp.text"    :active="(compToRender.selected == comp.name)"    :class="[(compToRender.selected == comp.name)?   'font-bold': 'font-regular']"   color="onSurface"   class="text-caption " @click="compToRender.selected = comp.name; (comp.name == 'accounts')? drawer = true: drawer = false"   size="x-small" ></VBtn>
            
            </VBtnGroup>  
            <VNavigationDrawer v-model="drawer"   class="z-[50000000]" width="370" >
                <VList nav  width="370"  >                
                    <VListItem>
                        <p class="text-subtitle-1" >Accounts</p>
                    </VListItem>      
                    <VDivider :opacity="100" class="border-neutral-300 dark:border-neutral-600 mb-5"  />
                    <VListItem  class="" style="text-decoration: none;"   :title="route.title" :value="route.name" :to="route.route">
                    <VCard  rounded="0" flat  height="100%"   color="surface"   >
                        <VTabs v-model="tab" bg-color="surface"  fixed-tabs :show-arrows="false" align-tabs="start"  slider-color="!text-purple-600 dark:!text-purple-300"   selected-class="!text-purple-600 dark:!text-purple-300 font-bold" >
                            <VTab text="Staff" value="staff" color="surface" density="compact" variant="text"  fixed rounded="0"  class="text-none text-sm" ></VTab>
                            <VTab text="Users" value="users" color="surface" density="compact" variant="text" fixed rounded="0"   class="text-none text-sm" ></VTab> 
                        </VTabs>
                        
                        <VDivider />

                        <VCardItem class="my-2"  >
                            <VTextField variant="solo-inverted" flat class="border border-neutral-200 rounded-md" hide-details density="compact" width="100%" clearable placeholder="Search..." >
                                <template #append-inner >
                                    <VIcon icon="mdi:mdi-magnify"  />
                                </template>
                            </VTextField>
                        </VCardItem>

                        <VCardItem class="pa-0">
                            <VTabsWindow v-model="tab">
                                <VTabsWindowItem value="staff">                          
                                    <VList nav >
                                        <VListItem v-for="(staff, index) in staffs" :class="[(index != (staffs.length - 1) && staffs.length > 1) ? 'border-b border-neutral-700 dark:border-neutral-100':'','pb-2',(activeState(staff.id))? 'border-l-4 border-purple-600 dark:border-purple-300':'']"     :key="staff.id" :value="staff.id" @click="AppStore.setSelectedAccount(staff)" :active="activeState(staff.id)"   > 
                                            <template #title ><span class="text-sm font-bold" >{{`${ _.capitalize(staff.firstname)} ${ _.capitalize(staff.lastname)}`}}</span></template>
                                            <template #subtitle ><span class="text-xs" >{{ staff.email }}</span></template>
                                            <template #append ><div class="min-h-[40px]" > <span class="text-xs" >{{ _.capitalize(staff.role)}}</span></div></template>
                                        </VListItem>
                                    </VList>                            
                                </VTabsWindowItem>

                                <VTabsWindowItem value="users">                            
                                    <VList nav  >
                                        <VListItem v-for="(user, index) in users" :class="[(index != (users.length - 1) && users.length > 1) ? 'border-b border-neutral-700 dark:border-neutral-100':'','pb-2',(activeState(user.id))? 'border-l-4 border-purple-600 dark:border-purple-300':'']"   :title="`${user.firstname} ${user.lastname}`" :subtitle="user.email" :key="user.id" :value="user.id" @click="AppStore.setSelectedAccount(user)" :active="activeState(user.id)"  >
                                            <template #title ><span class="text-sm font-bold" >{{`${ _.capitalize(user.firstname)} ${ _.capitalize(user.lastname)}`}}</span></template>
                                            <template #subtitle ><span class="text-xs" >{{ user.email }}</span></template>
                                            <template #append ><div class="min-h-[40px]" > <span class="text-xs" >{{ _.capitalize(user.country)}}</span></div></template>
                                        </VListItem>
                                    </VList>                           
                                </VTabsWindowItem>
                            </VTabsWindow>
                        </VCardItem>

                    
                    </VCard>  
                    </VListItem>  
                </VList>
                <template #append >
                    <div class="w-full" >
                        <VBtn prepend-icon="mdi:mdi-arrow-left-bold" rounded="lg" text="Back" @click="compToRender.selected = 'registering'" variant="text" class="text-caption font-bold !text-neutral-600 dark:!text-neutral-400"  />
                    </div>
                </template>
            </VNavigationDrawer>

            
        </div>

        <div class="bg-neutral-200 dark:bg-neutral-800 h-full ml-10 rounded-tl-3xl overflow-hidden  border border-neutral-800" >
           <VContainer class=" size-full  relative"  fluid >              

                <VRow   >
                    <VCol style="height: 100%;" >
                        <Transition name="slide-right"  >
                            <KeepAlive>
                                <component :is="renderComp" class="tab"></component>
                            </KeepAlive>  
                        </Transition>
                    
                    </VCol>
                </VRow>                
                
            </VContainer>
    

        </div>      

      </div>

</template>

<script setup>
// IMPORTS   
import { storeToRefs } from 'pinia';
import { useAppStore } from '@/stores/appStore';
import { useUserStore} from '@/stores/userStore';
import { ref,watch ,onMounted,computed } from "vue";  
import { RouterLink, useRouter } from "vue-router";
import NewAccounts from '@/components/admin/NewAccounts.vue';
import Accounts from '@/components/admin/Accounts.vue';
import { VListItem } from 'vuetify/lib/components/index.mjs';
import _ from 'lodash';

// VARIABLES 
const route             = useRouter(); 
const UserStore         = useUserStore(); 
const AppStore          = useAppStore();
const {id,loggedIn,image, darkmode}       = storeToRefs(UserStore);
const {staffs, users, selectedAccount}   = storeToRefs(AppStore);
const text              = ref("");
const changedText       = ref(""); 
const compToRender      = ref({"selected": "registering","init":false, "list":[{"text":"New Registrations","name":"registering","component":"NewAccounts"}, {"text":"Accounts","name":"accounts","component":"Accounts"}]})
const tab               = ref("");
const drawer            = ref(false);


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
const renderComp = computed(() => 
     {
      if(compToRender.value.selected == 'registering')
        return NewAccounts
      else if (compToRender.value.selected == 'accounts')
        return Accounts
     }     

  ) 

  const accountsDrawer = computed(()=> {
    return compToRender.value.selected == 'accounts';
  });

  const activeState = computed(() => {
      // THIS IS A DYNAMIC GETTER
      return (id) => {
        if (!!selectedAccount.value){
            if(selectedAccount.value.id == id){
                return true
            }
        }
        
        return false
      }
  }); 


// FUNCTIONS

onMounted(() => {

 
})

 
 
</script>

<style>
/*   Style */

 
</style>