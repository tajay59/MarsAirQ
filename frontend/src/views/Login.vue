  <template> 
 
    
      <VContainer class=" pa-0"    style="height: 100vh; width:100vw"   fluid   >
        <VRow  align="center" justify="center"  style=" overflow: hidden;"  class="fill-height pa-0 ma-0 rounded-lg"  >
          <VCol v-if="!smAndDown" class=" fill-height pa-0" align="center" style="height: 100%;" >
            <!-- LEFT IMAGES -->
            <VCard height="100%" width="100%" variant="flat" border   class="bg-[url('@/assets/sky1.png')] bg-no-repeat bg-cover bg-rose-950 d-flex align-center justify-center rounded-e-xl"  flat> 
              <template v-slot:image>
                  <!-- <VImg  src="@/assets/landing.png" cover   height="100%">              
                    <template v-slot:placeholder>
                      <div class="d-flex align-center justify-center fill-height">
                        <VProgressCircular color="grey-lighten-4" indeterminate ></VProgressCircular>
                      </div>
                    </template>
                  </VImg>  -->
                  <ImageCompare class="shadow-lg rounded-2xl">
                      <template #left> <img src="@/assets/mars1.png" style="background-size: contain;" /> </template>
                      <template #right> <img src="@/assets/earth1.png" style="background-size: contain;"  /> </template>
                  </ImageCompare>
              </template>
            </VCard>
          
          </VCol>

          <VCol   align="center" class="fill-height  " >
        
              <!-- LOGIN FORM -->
              <VContainer fluid class="fill-height  pa-0" align="center" >

                <VRow class=" fill-height"  justify="center" >
                  <VCol cols="12" class=" "  align-self="start" justify="space-between" style="max-width: 500px;">
                    <VImg  src="@/assets/logo.png"  max-height="200" height="100%">              
                      <template v-slot:placeholder>
                        <div class="d-flex align-center justify-center fill-height">
                          <VProgressCircular color="grey-lighten-4" indeterminate ></VProgressCircular>
                        </div>
                      </template>
                    </VImg> 
                    <div class="mt-n5" >
                      <span class="roboto-black-italic text-primary font-bold text-xl " style=" cursor: pointer" @click="router.push({name:'Home'})">Mars </span><span class="roboto-condensed-200  ">Air</span><span class="text-primary font-weight-bold text-h4">Q</span> 
                    </div>
                  </VCol>

                  <VCol  cols="12" align-self="center" class=" " justify="center" >
                    <VCard  rounded="sm"    flat color="transparent" min-width="200" max-width="275"  >
                        <template v-slot:title>
                          <div class=" nunito-title text-center text-3xl text-neutral-900  dark:text-neutral-200/[0.8]"  >Welcome Back</div> 
                          
                        </template>
                        <template v-slot:subtitle>
                          <div class=" nunito text-center text-sm text-neutral-900  dark:text-neutral-200/[0.8]"  >Please enter your details</div> 
                        </template>
                        <VCardItem class="bg- green" >
                          <!-- <SelectButton v-model="selectedOption" :options="options" class="rounded-lg" :pt="{root:'w-[300px] bg-red', pcToggleButton:'w-[300px] bg-green'}" /> -->
                        </VCardItem>
                        <VCardItem  class="pt-1 pb-0">
                          <form  @submit.prevent="onSubmit" id="loginForm" class="pt-2" style="border-radius: 6px;"> 
                          
                                <VTextField
                                    v-for="field in loginForm" :key="field.label"
                                    clearable                                   
                                    rounded       = "xl"            
                                    class         = "text-xs mt-3"
                                    density       = "compact"
                                    :label        = "field.label"                           
                                    :variant      = "field.variant"
                                    :type         = "(field.name == 'Password' && showPasscode)? 'text':field.type"
                                    :rules        = "rules(field.name)"  
                                    :name         = "field.name"               
                                    v-model       = "field.data" 
                                    
                                    >
                                    <template v-slot:append-inner>
                                      <VIcon v-if="field.name == 'Email'" :icon="field.icon" size="24"></VIcon>                                   
                                      <VIcon v-else  @click="showPasscode = !showPasscode" :icon="(showPasscode) ? 'mdi:mdi-eye' : 'mdi:mdi-eye-off'" size="24"></VIcon>                                 
                                    </template>
                                    <template v-slot:clear>
                                      <VIcon icon="mdi:mdi-close-circle" @click="field.data = ''" size="24"></VIcon>
                                    </template>
                                </VTextField>
                        
                          </form>
                        </VCardItem>
                        <VCardItem class="pt-0">
                          <VTooltip text="login" >
                            <template v-slot:activator="{ props }"> 
                              <VHover  >
                                <template v-slot:default="{ isHovering, props }">           
                                  <VBtn v-bind="props"   :variant="(isHovering)? 'flat':'flat'"    class="my-1 !bg-purple-800 dark:!bg-purple-400"    width="100%" max-width="240" :disabled="!enableSubmitButton" :loading="loading" type="submit" form="loginForm"   rounded="xl"  >                     
                                    <p class="nunito text-sm font-weight-bold "> Continue </p>
                                  </VBtn>
                                </template>            
                              </VHover>
                              
                            </template>
                          </VTooltip>
                        </VCardItem>
                      </VCard>        
                          
                
                    <VDivider class="my-3 w-[240px]" color="#ff0000" theme="light"  thickness="3"   />
                    <VBtn text="Signup" class="text-caption font-weight-regular" @click.prevent="router.push({name:'Signup'})" rounded="sm" flat density="compact" variant="plain" color="primary"  ></VBtn>   
                    <span class="mx-1 nunito-text" style="font-size: small;">or</span>
                    <VBtn text="Reset Password" class="text-caption font-weight-regular" @click.prevent="router.push({name:'PasswordReset'})" rounded="sm" flat density="compact" variant="plain" color="sencondary"></VBtn>   
                  
                  </VCol> 
                  <VCol  cols="12" align-self="end" >
                    <p class="nunito text-xs text-center text-neutral-900  dark:text-neutral-200/[0.8] mb-10 " style="max-width: 500px;">Join the growing community that relies on Mars AirQ to monitor and improve air quality. Log in to access your personalized dashboard, track real-time air quality data, and make informed decisions to create a healthier environment.</p>
                  </VCol>
                </VRow>
            
              </VContainer>
        
          </VCol>
        </VRow>
        <VRow>
            
        </VRow>

      </VContainer>
 
  </template>
  
  <script setup lang="ts"> 
  // IMPORTS
  import { useDisplay } from 'vuetify'
  import { useTheme } from 'vuetify'
  import { object, string, number, date, ObjectSchema  } from 'yup';
  import  type { InferType } from 'yup';
  import { useRoute, useRouter } from "vue-router";
  import { ref,reactive, onMounted,onBeforeMount,computed, watch } from 'vue';
  import { Icon } from '@iconify/vue';
  import { useToast } from 'primevue/usetoast';
  

  // PINIA STORES
  import { storeToRefs } from 'pinia';
  import { useAppStore} from '@/stores/appStore';
  import { useUserStore} from '@/stores/userStore'; 
  import { useMqttStore} from '@/stores/mqttStore';
  import { useNotificationStore } from '@/stores/notificationStore';
 
  
  
  // VARIABLES 
  const NotificationStore       = useNotificationStore(); 
  const { xs,smAndDown,smAndUp, mdAndUp }   = useDisplay();
  const UserStore   = useUserStore(); 
  const AppStore    = useAppStore();
  const Mqtt        = useMqttStore();
  const toast       = useToast();
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
                      "email": ref({"icon":"mdi:mdi-email","label":"E-mail","hint":"Account E-mail address ", "type":"email","name":"Email","data":"","variant":variant}),
                      "password": ref({"icon":"mdi:mdi-form-textbox-password","label":"Password","hint":"Super secret password", "type":"password","name":"Password","data":"","variant":variant})
                      });


  // VALIDATION CONFIG
  interface Person { email: string; password: string; }


  const schema: ObjectSchema<Person> = object({
    password: string().required(' required!').min(8, 'Minimum 8 characters').matches(/[~`!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?]/, 'Minimum 1 special character').matches(/.*[A-Z].*/, 'Minimum 1 capitalized letter'),
    email: string().email('Please enter a valid E-mail').required("required!").matches(/^[\w-\.]+@([\w-]+\.)+[\w-]{2,4}$/, 'Enter a valid E-mail address'), //.test('staff email', 'Enter a valid E-mail address', (value) => { return value && !value.includes("cimh.edu.bb"); }),
    
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
                    UserStore.suball    = data['suball'];
                    UserStore.image     = data['image'];
                    UserStore.mqtt_sub_credentials = data['web'];
                    Mqtt.username = data['web']['username'];
                    Mqtt.password = data['web']['password'];
                    // Mqtt.connect();
                    UserStore.getAllSites();
                  

                    // PUSH NOTIFICATION  
                    toast.add({ severity: 'success', summary: 'Logged in!', detail: '', life: 3000 });    
                  

                    // REDIRECT TO EXPLORE PAGE SINCE LOGIN IS SUCCESSFUL 
                    // setTimeout(()=>{router.replace(route.query.redirect || {name:"Home"});}, 1000);
                    
                }
                
                else if(data['status'] === "failed" ){    
                  // PUSH NOTIFICATION  
                  toast.add({ severity: 'error', summary: 'Signin Failed', detail: '', life: 3000 });    
                  
                    
                } 
                else if(data['status'] === "accountDoesNotExist"  ){   
                  // PUSH NOTIFICATION    
                  toast.add({ severity: 'warn', summary: 'Signin Failed', detail: 'Account Does Not Exist', life: 3000 });                       
                } 
                else if(data['status'] === "Invalid credentials"  ){     
                  // PUSH NOTIFICATION 
                  toast.add({ severity: 'error', summary: 'Signin Failed', detail: 'Invalid credentials', life: 3000 });                         
                }                              
                else{                           
                    console.log(`Login failed Unable to process request `);     
                    // PUSH NOTIFICATION 
                    toast.add({ severity: 'error', summary: 'Signin Failed', detail: 'Unable To Process Request', life: 3000 }); 
                }
                    }
            else{
                    // console.warn(data);  
                    console.log(`Login failed Unable to process request `); 
                    toast.add({ severity: 'error', summary: 'Signin Failed', detail: 'Unable To Process Request', life: 3000 });                  
            }
          }
          else{
            loading.value = false;             
            const data    = await response.text();
            console.warn(data);  
              // PUSH NOTIFICATION 
              toast.add({ severity: 'error', summary: 'Signin Failed', detail: 'Unable To Process Request', life: 3000 }); 
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
          toast.add({ severity: 'error', summary: 'Signin Failed', detail: 'Request timed out', life: 3000 });  
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
 
::v-deep input:-webkit-autofill { 
  box-shadow: 0 0 0 0 rgba(168, 6, 44, 0) inset !important; /* Shadow effect */
  -webkit-box-shadow: 0 0 0 0 rgba(185, 19, 19, 0) inset !important; /* Ensure it works on Safari too */  
  border-top-left-radius: 25px;  /* border-radius: 25px; */
  border-bottom-left-radius: 25px;
}

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