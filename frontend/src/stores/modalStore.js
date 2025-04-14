// Utilities
import { defineStore } from 'pinia'
import {ref,reactive,computed} from 'vue' 

export const useModalStore = defineStore('modal', ()=>{
  
 
  const State       = ref(false); 
  const Message     = ref("");
  const Variant     = ref("flat"); 


  const pushNotification = computed(()=>{
    // Since getters do not take arguments a dynamic getter should be used instead
    // This is a dynamic getter, which is a function that returns another function
    // The returned function takes an argument, which is the only way a getter can 
    // take an argument
    return (message, variant, state)=> { // rounded,
        // REQUIRED TO GET JWT CSRF COOKIE, OTHERWISE ACCESS TO PROTECTED ROUTES WILL FAIL
          Message.value      = message;    
          Variant.value      = variant; 
          State.value        = state;    
        }
});

 

  return { State, Message, Variant, pushNotification}
},{persist: true})