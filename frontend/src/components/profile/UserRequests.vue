<template>
    <p>REQUESTS</p>     
    </template>
    
    <script setup>
    // IMPORTS   
    import { useUserStore} from '@/stores/userStore';
    import { ref,watch ,onMounted,computed } from "vue";  
    import { RouterLink, useRouter } from "vue-router";
    
    // VARIABLES 
    const route             = useRouter(); 
    const UserStore         = useUserStore();
    const firstname         = ref("John");
    const lastname          = ref("Doe");
    const text              = ref("");
    const changedText       = ref("");
    
    
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
    
    
    // FUNCTIONS
    onMounted(()=>{
        console.log("TEMPLATE COMPONENT CREATED");
        // pingPong();
    })
    
    
    
     
    </script>
    
    <style>
    /*   Style */
    
     
    </style>