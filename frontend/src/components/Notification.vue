<template>
  <VContainer  style="position: absolute;top: 0px; z-index: -2; width: 0px; height: 0px;">        
      <VRow class="d-flex align-center justify-center" >
        <VCol cols="auto">
          <VSnackbar class="pa-0 mb-15" v-model="State"  :timeout="Timeout" :color="Color" :variant="Variant" :rounded="Rounded"  >
      
            <VContainer class=" ma-0 pa-0">
              <VRow class="pa-0 ma-0 h-50" align="center" justify="start"    >
                
                <VCol class=" ma-0 pa-0"    cols="1">
                  <v-progress-circular indeterminate v-if="LoadingIcon" :size="20" :width="2"></v-progress-circular>
                  <VIcon v-else density="compact" size="16" class="mt-n1"   :icon = "Icon" :color="IconColor" ></VIcon>
                </VCol>
              
                <VCol  class="pa-0 ma-0 ml-1 "      cols="10"  ><div :class="TextColor" style="display: flex;"> {{ Message }}</div></VCol>
                
                
              </VRow>
            </VContainer>

            <template v-slot:actions>
              <VDivider class="mr-2"   vertical thickness="1" color="black"  style="height: 28px;" /> 
              <VBtn size="16" density="compact" color="grey-darken-1" border="left"  @click="close()"   >
                <template v-slot:default>
                  <VIcon icon="mdi:mdi-close-circle"  size="16"></VIcon>
                </template>
              </VBtn>
            </template>

            </VSnackbar>
        </VCol>    
      </VRow> 
  </VContainer>
</template>

<script setup>

  // IMPORTS
  import { storeToRefs } from 'pinia'
  import { useNotificationStore } from '@/stores/notificationStore';

  // VARIABLES
  const NotificationStore     = useNotificationStore();
  const { State,Color, Rounded, Message,TextColor, Variant, Icon, IconColor, Timeout, LoadingIcon }           = storeToRefs(NotificationStore);

  // FUNCTIONS
  const close = ()=> {
    State.value = false;
    // console.log("Closing snackbar");
  }

</script>
