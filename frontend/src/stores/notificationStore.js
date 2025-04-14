// Utilities
import { defineStore } from 'pinia'
import {ref,reactive,computed} from 'vue' 

export const useNotificationStore = defineStore('notification', ()=>{
  
  const snackbar    = reactive({"state": false,"color":"blue-darken-1","rounded":"rounded-lg","message":"one love","variant":"flat","icon":"fa fa-right-to-bracket","iconColor":"purple"});
  const State       = ref(false);
  const Color       = ref("blue-darken-1");
  const Rounded     = ref("rounded-lg");
  const Message     = ref("");
  const Variant     = ref("flat");
  const Icon        = ref("fa fa-right-to-bracket");
  const IconColor   = ref("purple");
  const TextColor   = ref("text-onSecondary");
  const Timeout     = ref(2000);
  const LoadingIcon = ref(false);


  const pushNotification = computed(()=>{
    // Since getters do not take arguments a dynamic getter should be used instead
    // This is a dynamic getter, which is a function that returns another function
    // The returned function takes an argument, which is the only way a getter can 
    // take an argument
    return (message,color,textColor, variant, icon, iconColor, state,timeout)=> { // rounded,
        // REQUIRED TO GET JWT CSRF COOKIE, OTHERWISE ACCESS TO PROTECTED ROUTES WILL FAIL
          Message.value      = message;                 
          Color.value        = color;
          TextColor.value    = textColor;
          Variant.value      = variant;
          Icon.value         = icon;
          IconColor.value    = iconColor;
          State.value        = state;
          Timeout.value      = timeout;   
          LoadingIcon.value  = false;       
        }
});

const LoadingNotification = computed(()=>{
  // Since getters do not take arguments a dynamic getter should be used instead
  // This is a dynamic getter, which is a function that returns another function
  // The returned function takes an argument, which is the only way a getter can 
  // take an argument
  return (message,color,textColor, variant, icon, iconColor, state,timeout)=> { // rounded,
      // REQUIRED TO GET JWT CSRF COOKIE, OTHERWISE ACCESS TO PROTECTED ROUTES WILL FAIL
        Message.value      = message;                 
        Color.value        = color;
        TextColor.value    = textColor;
        Variant.value      = variant;
        Icon.value         = icon;
        IconColor.value    = iconColor;
        State.value        = state;
        Timeout.value      = timeout;   
        LoadingIcon.value  = true;        
      }
});


  return { State,Color, TextColor,Rounded, Message, Variant, Icon, IconColor, Timeout, LoadingIcon, pushNotification, LoadingNotification}
},{persist: true})