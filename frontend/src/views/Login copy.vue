<template> 
<VCard variant="text"    rounded="0" >
  <template v-slot:image>
    <VImg src="@/assets/lawn.webp" cover style="filter: brightness(70%);" />
  </template>
  <VContainer class=" bg- black backg round d-flex align-center justify-center"    style="height: 100vh; width:100vw"   fluid   >

    <VRow  align="center" justify="center"  style="max-width:1500px; height:90%; overflow: hidden;"  class=" rounded-lg"  >
    <VCol v-if="!smAndDown" class="backgro und fill-height pa-0" align="center" style="height: 100%;" >
      <!-- LEFT IMAGES -->
      <VCard height="100%" width="100%" variant="text"   class="d-flex align-center justify-center"  flat> 
      <VCardItem class="text-white  " >
        <VImg  :src="logo"  max-height="200" height="100%">              
          <template v-slot:placeholder>
            <div class="d-flex align-center justify-center fill-height">
              <VProgressCircular color="grey-lighten-4" indeterminate ></VProgressCircular>
            </div>
          </template>
        </VImg> 
        
        <!-- <p class="nunito-sans-title my-5 "  >Welcome Back</p> -->
         <div>
          <span class="roboto-black-italic text-primary " style="font-size:xxx-large ; cursor: pointer" @click="router.push({name:'Home'})">Mars </span><span class="roboto-condensed-200  ">Air</span><span class="text-primary font-weight-bold text-h4">Q</span> 
         </div>
      </VCardItem>
      </VCard>
    
    </VCol>

    <VCol   align="center"  >
      <VSheet width="280" rounded="lg" color="surface" border  > 
        <!-- LOGIN FORM -->
      <VContainer>
        <VRow justify="center" style="max-width: 400px;">       

            <VCol cols="12" align="center" justify="center" style="min-width:200px; max-width: 275px" class="mt-10"  > 
            
                <VCard  rounded="sm"    flat color="transparent"  >
                  <template v-slot:title>
                    <div class=" nunito-title text-center    text-onInverseSurface" style="font-size: xx-large;">Login</div> 
                  </template>
                  <VCardItem  class="pt-7">
                    <form  @submit.prevent="onSubmit" id="loginForm" class=" bg-surfac eVariant " style="border-radius: 6px;"> 
                    
                          <VTextField
                          v-for="field in loginForm" :key="field.label"
                              clearable
                              flat                
                              class         = "text-caption py-1 "
                              density       = "compact"
                              :label        = "field.label"                           
                              :variant      = "field.variant"
                              :type         = "(field.name == 'Password' && showPasscode)? 'text':field.type"
                              :rules        = "rules(field.name)"  
                              :name         = "field.name"               
                              v-model       = "field.data" 
                              
                              >
                              <template v-slot:append-inner>
                                <VIcon v-if="field.name == 'Email'" :icon="field.icon" size="16"></VIcon>                                   
                                <VIcon v-else  @click="showPasscode = !showPasscode" :icon="(showPasscode) ? 'mdi:mdi-eye' : 'mdi:mdi-eye-off'" size="16"></VIcon>                                 
                              </template>
                              <template v-slot:clear>
                                <VIcon icon="mdi:mdi-close-circle" @click="field.data = ''" size="16"></VIcon>
                              </template>
                          </VTextField>
                  
                    </form>
                  </VCardItem>
                </VCard>        
                    
            
              <VTooltip text="login" >
                  <template v-slot:activator="{ props }"> 
                    <VHover  >
                      <template v-slot:default="{ isHovering, props }">           
                        <VBtn v-bind="props"   :variant="(isHovering)? 'flat':'flat'"    class="my-1" color="primary"  width="100%" max-width="215" :disabled="!enableSubmitButton" :loading="loading" type="submit" form="loginForm"   rounded="lg" justify-self="right">                     
                          <p class="text-caption font-weight-bold"> Continue </p>
                        </VBtn>
                      </template>            
                    </VHover>
                    
                  </template>
                </VTooltip>
            </VCol>
          
          <VCol cols="12" align="left"    class="pa-5" >          
            <VDivider class="mb-10" /> 
            <VBtn text="Signup" class="text-caption font-weight-regular" @click.prevent="router.push({name:'Signup'})" rounded="sm" flat density="compact" variant="plain" color="primary"  ></VBtn>   
            <span class="mx-1 nunito-text" style="font-size: small;">or</span>
            <VBtn text="Reset Password" class="text-caption font-weight-regular" @click.prevent="router.push({name:'PasswordReset'})" rounded="sm" flat density="compact" variant="plain" color="sencondary"></VBtn>   
          </VCol>
        </VRow>
      </VContainer>
      </VSheet>
    </VCol>
    </VRow>

  </VContainer>
</VCard>
   
 
  </template>
  
  <script setup lang="ts"> 
  // IMPORTS
  import { useDisplay } from 'vuetify'
  import { useTheme } from 'vuetify'
  import { object, string, number, date, ObjectSchema  } from 'yup';
  import  type { InferType } from 'yup';
  import { useRoute, useRouter } from "vue-router";
  import { ref,reactive, onMounted,onBeforeMount,computed, watch} from 'vue';
  

  // PINIA STORES
  import { storeToRefs } from 'pinia';
  import { useAppStore} from '@/stores/appStore';
  import { useUserStore} from '@/stores/userStore'; 
  import { useNotificationStore } from '@/stores/notificationStore';
 
  
  
  // VARIABLES 
  const NotificationStore       = useNotificationStore(); 
  const { xs,smAndDown,smAndUp, mdAndUp }   = useDisplay();
  const UserStore   = useUserStore(); 
  const AppStore    = useAppStore();
  
  const router      = useRouter();
  const route       = useRoute(); 
  const theme       = useTheme();
  const {darkmode}  = storeToRefs(UserStore);
  const loading     = ref(false);
  const showPasscode = ref(false);  
  const errors      = reactive({name:"", errors: []}); 
  const enableSubmitButton  = ref(false); 
  const variant     = "outlined"; //   'outlined' | 'plain' | 'underlined' | 'filled' | 'solo' | 'solo-inverted' | 'solo-filled'
  const loginForm   = reactive({
                      "email": ref({"icon":"mdi:mdi-email-variant","label":"E-mail","hint":"Account E-mail address ", "type":"email","name":"Email","data":"","variant":variant}),
                      "password": ref({"icon":"mdi:mdi-form-textbox-password","label":"Password","hint":"Super secret password", "type":"password","name":"Password","data":"","variant":variant})
                      });


  // VALIDATION CONFIG
  interface Person { 
    email: string;
    password: string; 
  }

  const schema: ObjectSchema<Person> = object({
    password: string().required(' required!').min(8, 'Minimum 8 characters').matches(/[~`!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?]/, 'Minimum 1 special character').matches(/.*[A-Z].*/, 'Minimum 1 capitalized letter'),
    email: string().email('Please enter a valid E-mail').required("required!").matches(/^[\w-\.]+@([\w-]+\.)+[\w-]{2,4}$/, 'Enter a valid E-mail address').test('staff email', 'Enter a valid E-mail address', (value) => { return value && !value.includes("cimh.edu.bb"); }),
    
                      });


  onBeforeMount(()=>{
  theme.global.name.value = darkmode.value ?  'darkMode' : 'lightMode';
  localStorage.setItem("theme",darkmode.value ? 'darkMode' : 'lightMode');  
 });

// WATCHERS
watch(darkmode,  (mode) => {
  theme.global.name.value = mode ?  'darkMode' : 'lightMode';
  localStorage.setItem("theme",mode ? 'darkMode' : 'lightMode');  
});

watch(loginForm,  async (form) => {
  // VERIFY CODE EMAILED TO USER
   const person: Person = { email:form.email.data, password:form.password.data}

   try {
    const user = await schema.validate(person, { strict: true });
    enableSubmitButton.value = true;
    errors.errors = []
  } catch (err) {   
    enableSubmitButton.value = false;
    //  console.log(  err.name, err.type, err.value, err.params.path, err.inner  )
    errors.name = err.params.path;
    errors.errors = err.errors 
  }
});

// COMPUTED PROPERTIES


const logo = computed( () => {
  if (smAndDown.value){ 
    // if(theme.global.current.value.dark)
      return '/api/images/cimh-logo-white.webp'
    // return 'src/assets/cimh-logo-blue.webp'
  }
  else {
    // if(theme.global.current.value.dark)
      return '/api/images/cimh-logo-colour-white.webp'
    // return 'src/assets/cimh-logo-colour-black.webp'etting
  } 
})

  
  // FUNCTIONS
 onMounted(()=>{
    AppStore.currentRoute = "LOGIN";
    toTop();
  })

 

const onSubmit = () => {
  // alert(JSON.stringify(values, null, 2));
  userLogin();
} ;


const userLogin = async ()=>{
    // COLLECT USER INPUT FROM LOGIN FORM THEN POST TO FLASK API
    
    let Form            = document.querySelector<HTMLFormElement>("#loginForm");
    let form_data       = new FormData(Form);     
    const URL           = '/api/login';

    // FETCH REQUEST WILL TIMEOUT AFTER 20 SECONDS 
    const controller    = new AbortController();
    const signal        = controller.signal;
    const id            = setTimeout(()=>{controller.abort()},10000);

    const cookie        = UserStore.getCookie("csrf_access_token"); 
    
    loading.value = true;
    
    try {
          const response  = await fetch(URL,{ method: 'POST',body: form_data, signal: signal ,headers: { "X-CSRF-TOKEN": cookie ,"X-User":UserStore.userType } });
          
          if(response.ok){
            const data      = await response.json(); 
            let keys        = Object.keys(data);

            loading.value = false;
            if(keys.includes("status")){
           
                if( data['status'] === "loggedIn"  ){ 
                    
                  router.replace(route.query.redirect || {name:"Home"});                       
                    // UPDATE PINIA STOREs
                    UserStore.loggedIn  = true;
                    UserStore.user      = data['username'];
                    UserStore.email     = data['email'];
                    UserStore.role      = data['role'];
                    UserStore.id        = data['id'];
                    UserStore.image     = data['image'];
                  

                    // PUSH NOTIFICATION 
                    NotificationStore.pushNotification("Logged in!","secondary","text-onSecondary","flat","fas fa-circle-check","onSecondary",true,2000);
                  

                    // REDIRECT TO EXPLORE PAGE SINCE LOGIN IS SUCCESSFUL 
                    // setTimeout(()=>{router.replace(route.query.redirect || {name:"Home"});}, 1000);
                    
                }
                
                else if(data['status'] === "failed" ){    
                  // PUSH NOTIFICATION 
                  NotificationStore.pushNotification("Login failed"  ,"error","text-onError","flat","fas fa-triangle-exclamation","onError",true,2000);
                    
                } 
                else if(data['status'] === "accountDoesNotExist"  ){   
                  // PUSH NOTIFICATION 
                  NotificationStore.pushNotification("Account Does Not Exist"  ,"error","text-onError","flat","fas fa-triangle-exclamation","onError",true,2000);                        
                } 
                else if(data['status'] === "Invalid credentials"  ){     
                  // PUSH NOTIFICATION 
                  NotificationStore.pushNotification("Invalid credentials"  ,"error","text-onError","flat","fas fa-triangle-exclamation","onError",true,2000);                         
                }                              
                else{                           
                    console.log(`Login failed Unable to process request `);     
                    // PUSH NOTIFICATION 
                  NotificationStore.pushNotification("Unable To Process Request"  ,"error","text-onError","flat","fas fa-triangle-exclamation","onError",true,2000);
                }
                    }
            else{
                    // console.warn(data);  
                    console.log(`Login failed Unable to process request `); 
                  NotificationStore.pushNotification("Unable To Process Request"  ,"error","text-onError","flat","fas fa-triangle-exclamation","onError",true,2000);                   
            }
          }
          else{
            loading.value = false;             
            const data    = await response.text();
            console.warn(data);  
              // PUSH NOTIFICATION 
              NotificationStore.pushNotification("Unable To Process Request"  ,"error","text-onError","flat","fas fa-triangle-exclamation","onError",true,2000);
          }
         
    
        }
        catch(error){
          // Loader.style.visibility = "hidden"; 
          loading.value = false;
          console.error('Error:', error); 
          if( error.message === "The user aborted a request."){
                console.log("REQUEST ABORTED");             
              } 
           
          // PUSH NOTIFICATION 
          NotificationStore.pushNotification("Request timed out"  ,"error","text-onError","flat","fas fa-triangle-exclamation","onError",true,2000);
        } 

 }

 const toTop =()=> {
        window.scrollTo({
          top: 0,
          behavior: "smooth"
        });
      }

  const rules =  (name: string) => {   
    if(name == "Email"){     
          if(errors.name == "email"){
            return errors.errors
          }   
          return [true]
        }

    if(name == "Password"){     
      if(errors.name == "password"){
        return errors.errors
      }   
      return [true]
    } 
};
  </script>  

<style scoped>
.background{
   /* background-image: url('https://images.unsplash.com/photo-1634176866089-b633f4aec882?q=80&w=2080&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D'); */
   background-image: url('src/assets/lawn.webp');
   background-repeat: no-repeat;
   background-position: center;
   background-size: cover;
  
   /* filter: brightness(10%); */
}

/* 
.v-text-field ::v-deep label {
    font-size: 0.7em;
}
.v-text-field ::v-deep input {
    font-size: 0.8em;  
} */



.loo { 
  filter: blur(0px);
  filter: brightness(70%);
  transition: filter 700ms;
}

.loo:hover {
  filter: blur(5px);
  /* filter: brightness(50%); */
}

</style>