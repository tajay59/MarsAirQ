<template>  
 <div class="  w-full h-dvh flex flex-col" >

<div class=" h-20 flex flex-col justify-center ml-16 " >
    <!-- TOP BAR -->
</div>

<div class="bg-neutral-200 dark:bg-neutral-800 h-full ml-10 rounded-tl-3xl overflow-hidden  border border-neutral-800" >
    <VContainer  align="center" fluid>                           
        <VRow style="max-width: 1200px; width: 100%">
        <VCol>
            <VExpansionPanels flat border >
                
                <VExpansionPanel>
                    <!-- REGISTRATION -->
                    <VExpansionPanelTitle v-slot="{ expanded }">
                        <VRow no-gutters>
                        <VCol class="d-flex justify-start" cols="4">
                            <span>New Account(Ext)</span>
                        </VCol>
                        <VCol class="text--secondary" cols="8" >
                            <VFadeTransition leave-absolute> 
                            <VRow   style="width: 100%" no-gutters align="center" >
                                <VCol v-if="expanded" align="center">
                                    <VIcon icon="mdi:mdi-pencil-outline"></VIcon>
                                </VCol>
                                <VCol  v-else class="d-flex justify-center align-center ">
                                    <span>{{ emailList.registration.length }} person(s) in this list</span>
                                </VCol> 
                            </VRow> 
                            </VFadeTransition>
                        </VCol>
                        </VRow>
                    </VExpansionPanelTitle>
                    <VExpansionPanelText>
                        <VRow justify="space-around" no-gutters >
                        <VCol cols="12" class="my-5 text-left"><span>Whenever a new user account is created, an email will be dispatched to each individual in the list.</span></VCol>

                        <VCol align="center" :cols="(smAndDown)? 12: 6" class="pa-5"   >
                            <VCard title="Add to list" width="250" flat border>
                                <VCardItem>
                                    <VSelect
                                    label="Account"
                                    name = "Type"
                                    hide-details
                                    v-model="emailState.registration"
                                    :items="emailSelectedItem"
                                    item-title="name"
                                    item-value="value"
                                    variant="solo-inverted"
                                    flat
                                    density="compact"
                                    ></VSelect>
                                </VCardItem>
                                <VCardItem>
                                    <VBtn text="Submit" :disabled="!!!emailState.registration" class="text-caption ma-2" flat rounded="lg" @click="updateEmailList('registration')" append-icon="mdi:mdi-plus"></VBtn>
                                </VCardItem>
                            </VCard>
                            
                        </VCol>

                        <VCol align="center" :cols="(smAndDown)? 12: 6" class="pa-5"  >
                            
                            <VInfiniteScroll :height="300" :items="emailList.registration"  :onLoad="load" max-width="300"  class="d-flex align-center"   >
                                <span v-if="emailList.registration.length > 0">Recipient List</span>
                                <template v-for="(item, index) in emailList.registration" :key="item.account">
                                    <VSheet  color="inverseSurface" class="pa-4 my-1" border rounded="lg" max-width="250" width="100%">
                                        <VRow justify="space-between" align=center>
                                            <VCol align="left" class="pa-0">
                                                <p class="ml-3 font-weight-bold" >{{ _.capitalize(item.firstname) }} {{ _.capitalize(item.lastname) }}</p>
                                                <p class="ml-3 text-caption  " >{{ item.email }}</p>
                                            </VCol>                                                          
                                            <VBtn :text="item.email" icon="mdi:mdi-close-circle"   class=" text-caption"   @click="deleteEmail('registration',item.account)"   density="compact" variant="text" color="onPrimary" ></VBtn>                                                                
                                        </VRow> 
                                    </VSheet>
                                </template>

                                <template v-slot:empty>
                                    <VDivider />
                                    <!-- <span>really empty</span> -->
                                </template>
                            </VInfiniteScroll>
                        </VCol>
                        </VRow>
                    </VExpansionPanelText>
                </VExpansionPanel> 

                <VExpansionPanel>
                    <!-- ORDER CANCELLATION -->
                    <VExpansionPanelTitle v-slot="{ expanded }">
                        <VRow no-gutters>
                        <VCol class="d-flex justify-start" cols="4">
                            <span>Order Cancellation</span>
                        </VCol>
                        <VCol class="text--secondary" cols="8" >
                            <VFadeTransition leave-absolute> 
                            <VRow   style="width: 100%" no-gutters align="center" >
                                <VCol v-if="expanded" align="center">
                                    <VIcon icon="mdi:mdi-pencil-outline"></VIcon>
                                </VCol>
                                <VCol  v-else class="d-flex justify-center align-center ">
                                    <span>{{ emailList.cancellation.length }} person(s) in this list</span>
                                </VCol> 
                            </VRow> 
                            </VFadeTransition>
                        </VCol>
                        </VRow>
                    </VExpansionPanelTitle>
                    <VExpansionPanelText>
                        <VRow justify="space-around" no-gutters >
                        <VCol cols="12" class="my-5 text-left"><span>Whenever a customer submits an order cancellation request, an email will be dispatched to each individual in the list.</span></VCol>

                        <VCol align="center" :cols="(smAndDown)? 12: 6" class="pa-5"   >
                            <VCard title="Add to list" width="250" flat border>
                                <VCardItem>
                                    <VSelect
                                    label="Account"
                                    name = "Type"
                                    hide-details
                                    v-model="emailState.cancellation"
                                    :items="emailSelectedItem"
                                    item-title="name"
                                    item-value="value"
                                    variant="solo-inverted"
                                    flat
                                    density="compact"
                                    ></VSelect>
                                </VCardItem>
                                <VCardItem>
                                    <VBtn text="Submit" :disabled="!!!emailState.cancellation"  class="text-caption ma-2" flat rounded="lg" @click="updateEmailList('cancellation')" append-icon="mdi:mdi-plus"></VBtn>
                                </VCardItem>
                            </VCard>
                            
                        </VCol>

                        <VCol align="center" :cols="(smAndDown)? 12: 6" class="pa-5"  >
                            
                            <VInfiniteScroll :height="300" :items="emailList.cancellation"  :onLoad="load" max-width="300"  class="d-flex align-center"   >
                                <span v-if="emailList.cancellation.length > 0">Recipient List</span>
                                <template v-for="(item, index) in emailList.cancellation" :key="item.account">                                                        
                                    <VSheet  color="inverseSurface" class="pa-4 my-1" border rounded="lg" max-width="250" width="100%">
                                        <VRow justify="space-between" align=center>
                                            <VCol align="left" class="pa-0">
                                                <p class="ml-3 font-weight-bold" >{{ _.capitalize(item.firstname) }} {{ _.capitalize(item.lastname) }}</p>
                                                <p class="ml-3 text-caption  " >{{ item.email }}</p>
                                            </VCol>                                                          
                                            <VBtn :text="item.email" icon="mdi:mdi-close-circle"   class=" text-caption"   @click="deleteEmail('cancellation',item.account)"   density="compact" variant="text" color="onPrimary" ></VBtn>                                                                
                                        </VRow> 
                                    </VSheet>
                                </template>

                                <template v-slot:empty>
                                    <VDivider />
                                    <!-- <span>really empty</span> -->
                                </template>
                            </VInfiniteScroll>
                        </VCol>
                        </VRow>
                    </VExpansionPanelText>
                </VExpansionPanel> 

                
            </VExpansionPanels>
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



    // VARIABLES
    const AppStore        = useAppStore();
    const UserStore       = useUserStore();
    const { xs,smAndDown,smAndUp, mdAndUp }   = useDisplay();
    const { darkmode, layout}  = storeToRefs(UserStore);
    const { allStaffAccounts,emailSelectedItem, emailList }      = storeToRefs(AppStore);
    const variant         = "solo-inverted"; //   'outlined' | 'plain' | 'underlined' | 'filled' | 'solo' | 'solo-inverted' | 'solo-filled'
    const emailState      = reactive({registration:"",cancellation:""})

   
    const updateEmailList = (type) => {
        let account = null;

        if(type == "order"){
            account =  allStaffAccounts.value.filter( account => account.id == emailState.order );
        }
        else if(type == "registration"){
            account =  allStaffAccounts.value.filter( account => account.id == emailState.registration );
        }
        else if(type == "cancellation"){
            account =  allStaffAccounts.value.filter( account => account.id == emailState.cancellation );
        }
        else if(type == "invoice"){
            account =  allStaffAccounts.value.filter( account => account.id == emailState.invoice );
        }
        console.log("account",account)
       
        if(!!account){
            account = account[0]
            AppStore.updateEmailList(account.firstname,account.lastname,account.email,account.id,type);
        }
       
    }

    const deleteEmail = (type, acc) => {
       let account =  allStaffAccounts.value.filter( account => account.id == acc );
       console.log(account,acc)
       
       if(!!account){
           account = account[0]
           AppStore.deleteFromEmailList(account.id,type);
       }
  }

    // FUNCTIONS

    const   load =  async({ done }) => {
    // Perform API call
    // const res = await api()
    // items.value.push(...res)

    // 'ok':	Content was added succesfully
    // 'error':	Something went wrong when adding content. This will display the error slot
    // 'empty':	There is no more content to fetch. This will display the empty slot
    // 'loading':	Content is currently loading. This will display a message that content is loading. This status is only set internally by the component and should not be used with the done function

    done('empty')
  }

    onMounted(()=>{
   
        AppStore.getAllStaff(); 
        AppStore.getEmailList();
    })



</script>

<style>

</style>