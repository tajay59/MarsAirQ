<template>
  
    <VContainer   fluid>
      <VRow justify="center"  >      
        
            <VPagination 
              class="my-4"
              :length="props.length"
              :model-value="props.value"
              :total-visible="windowSize/80"
              @update:model-value="$emit('update',$event)"
              color="secondary"
              density="compact"
              variant="text"
              :show-first-last-page="true"               
            ></VPagination>      
      
      </VRow>
       
    </VContainer>
   
</template>

<script setup>
// IMPORTS
import { ref, reactive, onMounted, computed, watch} from 'vue';
 
const windowSize =  ref(window.innerWidth); 


window.onresize = ()=>{
  windowSize.value = window.innerWidth;
};

// PROPS
const props = defineProps({
    length:{type: Number,default: 0},
    value :{type: Number,default: 0},
});


// COMPUTED PROPERTIES
// const winWidth = computed(()=>{    
//     return  window.innerWidth;
// });

// WATCHERS
// watch( s,  (newType , oldType) => {
//   console.log(`OLD : ${oldType}, NEW : ${newType}`);    
// });

// FUNCTIONS
onMounted(()=>{
  // console.log(`PAGINATION TYPE : ${productType}`); 
  // console.log(`PAGINATION VALUE : ${props.value} LENGTH: ${props.length} `); 
});

 
  

</script>
