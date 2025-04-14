<template>
<div class="Page">
   <h1>Profile</h1>
</div>       
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


const pingPong = async ()=>{
        // FETCH REQUEST WILL TIMEOUT AFTER 20 SECONDS 
        // const UserStore     = useUserStore(); 
        const controller    = new AbortController();
        const signal        = controller.signal;
        const id            = setTimeout(()=>{controller.abort()},10000);
        const request       = {"message":"ping"}
        const token         = UserStore.GetCSRFToken;
        const cookie        = UserStore.getCookie("csrf_access_token"); 
    
        try {
            const response  = await fetch('/api/ping',{ method: 'POST',body:JSON.stringify(request), signal: signal ,headers: { 'Accept': 'application/json', 'Content-Type': 'application/json','X-CSRFToken': token,"X-CSRF-TOKEN": cookie } });
            const data      = await response.json(); 
            let keys        = Object.keys(data);
            
            console.log(data);
    
            if (keys.includes("status")){
    
                if (data["status"] === "pong"){
                  //User is already logged in                
                  console.log("GOT PONG FROM PING") ;    
                } 
               
                
            }
            
    
        }
        catch(err){
          if( err.message === "The user aborted a request."){
            console.log("REQUEST TIMEDOUT"); 
          }
          console.error('PING PONG error: ', err.message);   
    
        }    
      
    
    }
 
</script>

<style>
/*   Style */

 
</style>