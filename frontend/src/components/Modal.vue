<template>
  <VContainer  style="position: absolute;top: 0px; z-index: -1; width: 0px; height: 0px;">        
    <VRow justify="space-around">        
          <VCol cols="auto">
            <VDialog transition="dialog-top-transition" width="auto"  v-model="State"> 
              <template v-slot:default="{ isActive }">
                <VCard   align="center" class="" width="300"  >
                  <VCardItem>
                      <VIcon icon="mdi:mdi-alert-circle-outline" size="70" color="error"></VIcon>
                  </VCardItem>
                  <VCardItem>
                    <div class="text-h6  py-5">{{ Message }}</div>
                  </VCardItem>
                   
                  <VCardActions class="justify-end">
                    <VBtn variant="text" @click="isActive.value = false" >Close</VBtn>
                  </VCardActions>
                </VCard>
              </template>
            </VDialog>
          </VCol>
    </VRow>
  </VContainer>
</template>

<script setup>

  // IMPORTS
  import { storeToRefs } from 'pinia'
  import { useModalStore } from '@/stores/modalStore';

  // VARIABLES
  const ModalStore     = useModalStore();
  const { State, Message, Variant }           = storeToRefs(ModalStore);

 

</script>
