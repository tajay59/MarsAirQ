<template>  
<VContainer fluid class="fill-height pa-0">
  <VRow class="fill-height pa-0" >
    <VCol v-if="!smAndDown" cols="4" class="bg-neutral-800" >    
      
      
      <div class="my-10 h-[250px]" >
        <Transition name="fade" :duration="5000" >   
          <div class="" v-show="page >= 0 && page <= 1" >
            <VImg  src="@/assets/logo.png"  max-height="200" height="100%">              
              <template v-slot:placeholder>
                <div class="d-flex align-center justify-center fill-height">
                  <VProgressCircular color="grey-lighten-4" indeterminate ></VProgressCircular>
                </div>
              </template>
            </VImg> 
            <div class="mt-n2 text-center" >
              <span class="roboto-black-italic !text-purple-400 text-xl font-bold " style=" cursor: pointer" @click="router.push({name:'Home'})">KaleidoScope </span> <sub class="roboto-condensed-200 !text-gray-300">MARS</sub> 
            </div>
            <div class="  text-center" >
              <span class="roboto-black-italic text-neutral-200/[0.8] text-4xl " style=" cursor: pointer" @click="router.push({name:'Home'})">Registration </span> 
            </div>
          </div>    
        
        </Transition>
      </div>
      
   
      <VStepperVertical v-model="page" color="secondary" flat border theme="dark" hide-actions  >
        <template v-slot:default="{step}">
          <VStepperVerticalItem class="bg-transparent !text-gray-300" :complete="step > 0" subtitle="Personal details" title="User" value="0" >
            <p class="nunito !text-purple-400 text-xl font-light" > Please fill out the form with your user details.  </p>
          </VStepperVerticalItem>

          <VStepperVerticalItem class="bg-transparent !text-gray-300" :complete="step > 1" subtitle="Sent verification code" title="Verification" value="1" >
            <p class="nunito !text-purple-400 text-xl font-light" > Sent verification code.   </p>
          </VStepperVerticalItem>

          <VStepperVerticalItem class="bg-transparent !text-gray-300" subtitle="Account Request Sent" title="Confirmation" value="2" @click:next="onClickFinish" >
            <p class="nunito !text-purple-400 text-xl font-light" > Your verification was successful! Your request to create a new account has been submitted.  </p>
          </VStepperVerticalItem>          
        </template>
      </VStepperVertical>    
    </VCol>

    <VCol :cols="(smAndDown)? '12': '8'" class="bg-blue pa-0" >
      <VCarousel v-model="page" height="100%" hide-delimiter-background hide-delimiters :show-arrows="false">
        <VCarouselItem   key="0" >
          <VSheet height="100%" >
            <div class="d-flex flex-col fill-height justify-center align-center">
              <VCard    rounded="lg" flat width="300"  >
                  <template v-slot:title>
                    <div class="nunito-title text-center text-onInverseSurface text-3xl">Enter your Details</div>
                  </template>
                  <template v-slot:subtitle>
                    <div class="nunito text-center text-sm">All fields are required</div>
                  </template>
                  <VCardItem class="mt-15"  > 
                    <form  @submit.prevent="onSubmit" id="signupForm" class="mt-1">     
                      <div v-for="field in signupForm" :key="field.label"   >
                        <VSelect
                              v-if          = "field.label == 'Country'" 
                              v-model       = "field.data"  
                              :items        = "countries" 
                              border
                              clearable
                              flat 
                              class         = "text-caption py-1 "
                              rounded       = "xl"
                              density       = "compact"
                              :rules        = "rules(field.name)" 
                              :label        = "field.label"     
                              :variant      = "field.variant"                            
                              type          = "text"
                              :name         = "field.name"              
                              
                          >
                          <template v-slot:clear>
                            <VIcon icon="mdi:mdi-close-circle" @click="field.data = ''" size="16"></VIcon>
                          </template>                        
                        </VSelect>

                        <VSheet v-else-if= "field.label == 'Organization'" class=" mb-5"   >
                          <FloatLabel variant="on">
                            <AutoComplete   v-model="selectedOrganizations" optionLabel="organization" fluid dropdown placeholder="                        search" :suggestions="filteredOrganizations" @complete="search"  :pt="{root:'!text-purple-300 dark:!text-purple-200',dropdown: '!rounded-r-[50%]', chipItem: '!rounded-l-[50%] !text-purple-300 dark:!text-purple-200'}" style="width: 100%;" >
                              <template #option="slotProps">
                                  <div class="flex gap-2 place-content-center" @click="signupForm.country.data = slotProps.option.country">
                                    
                                    <Icon :icon="getCountryIcon(slotProps.option.code)"  with="24" height="24"></Icon>
                                    <span class="text-sm" >{{ slotProps.option.organization }}</span>
                                  </div>
                              </template>
                              <template #header>
                                  <div class="font-medium px-3 py-2">Available Companies</div>
                              </template>
                              <template #dropdownicon>         
                                    <Icon icon="stash:search-split"  with="24" height="24"></Icon>
                              </template>
                              <template #footer>
                                  <div class="px-3 py-3">
                                      <!-- <Button label="Add New" fluid severity="secondary" text size="small" icon="pi pi-plus" /> -->
                                  </div>
                              </template>
                          </AutoComplete>
                            <label for="on_label">Organization</label>
                        </FloatLabel>
                          
                        </VSheet>

                     

                        <VTextField   
                            v-else                    
                            border
                            clearable
                            flat 
                            class         = "text-caption py-1 "
                            rounded       = "xl"
                            density       = "compact"
                            :rules        = "rules(field.name)" 
                            :label        = "field.label"     
                            :variant      = "field.variant"                            
                            :type         = "((field.name == 'Password' && showPasscode) || (field.name == 'PasswordConfirm' && showPasscodeConfirm) )? 'text':field.type"
                            :name         = "field.name"              
                            v-model       = "field.data"  
                            >
                            <template v-slot:append-inner>
                              <VIcon v-if="['Password','PasswordConfirm'].includes(field.name)" @click="(field.name == 'Password')? showPasscode = !showPasscode : showPasscodeConfirm = !showPasscodeConfirm " :icon="((field.name == 'Password' && showPasscode) || (field.name == 'PasswordConfirm' && showPasscodeConfirm)) ? 'mdi:mdi-eye' : 'mdi:mdi-eye-off'" size="16"></VIcon>    
                              <VIcon v-else :icon="field.icon" size="16"></VIcon>
                            </template>
                            <template v-slot:clear>
                              <VIcon icon="mdi:mdi-close-circle" @click="field.data = ''" size="16"></VIcon>
                            </template>
                        </VTextField>   

                      </div>
                        

                        
              
                    </form>
                  </VCardItem>
                  
                </VCard>
                <VBtn text="Submit" class="text-sm font-bold my-4 !bg-purple-800 dark:!bg-purple-400 !text-gray-200 dark:!text-gray-700"   width="100" :disabled="( !enableSubmitButton  || signupForm.password.data != signupForm.passwordconfirm.data )"  :loading="loading" type="submit" form="signupForm"  variant="flat" rounded="xl"  justify-self="right" />  
                
            </div>
          </VSheet>
        </VCarouselItem>

        <VCarouselItem    key="1" >
          <VSheet height="100%" >
            <div class="d-flex fill-height justify-center align-center">
              <VCard :class="[(smAndDown)? 'px-0' :'px-6']"   class="text-center mx-auto ma-4 " max-width="500" width="100%" min-height="600" rounded="md"   flat >
                <template v-slot:title>
                    <div class="nunito-title text-center text-onInverseSurface text-3xl">Verification</div>
                  </template>
                  <template v-slot:subtitle>
                    <div class="nunito text-center text-sm">We sent a verification code to</div>
                  </template>

                  <!-- <h3 class="text-h5 mb-4"></h3> -->

                 <VCardItem  class="mt-15" >
                    <div class="text-body-2 mb-5 text-medium-emphasis">
                        <strong class="text-secondary">{{ signupForm.email.data }}</strong>                       
                    </div>

                    <p class="text-center nunito"  >
                      A verification code has been sent to your email. Please check your inbox (and spam folder, if necessary) for the code. Once you find it, enter the code in the provided field to complete the verification process. 
                    </p>

                    <div  v-if="!registered">
                      <div v-if="!registered && timerstate !== 'timedout'">
                        
                        <p class="nunito text-md mt-5 font-normal" >Time remaining </p>
                        <h4 class="text-error text-3xl">{{minutes}} : {{seconds}}</h4>
                      </div>        
                    </div>
                   
                    <VOtpInput v-model = "verification" type="text" class=" font-bold " :loading="verifying"  :length="8" variant="outlined" ></VOtpInput>                    
                    

                    <div class="  text-md mt-15">
                      Didn't receive the code? <VBtn text="Re-send" class="text-caption ml-5 font-bold !bg-purple-800 dark:!bg-purple-400  !text-neutral-200/[0.8] dark:!text-neutral-900"   variant="tonal" density="compact" @click.prevent="onSubmit" flat  />  
                    </div>
                 </VCardItem>
                </VCard>
            </div>
          </VSheet>
        </VCarouselItem>

        <VCarouselItem    key="2" >
          <VSheet height="100%" >
            <div class="d-flex fill-height justify-center align-center">
              <VCard   max-width="60%"  flat>
                <VCardItem>
                
                    <div class="mb-15" >
                      <VImg  src="@/assets/logo.png"  max-height="200" height="100%">              
                        <template v-slot:placeholder>
                          <div class="d-flex align-center justify-center fill-height">
                            <VProgressCircular color="grey-lighten-4" indeterminate ></VProgressCircular>
                          </div>
                        </template>
                      </VImg> 
                      <div class="mt-n5 text-center" >
                        <span class="roboto-black-italic !text-purple-800 dark:!text-purple-400 font-bold text-xl " style=" cursor: pointer" @click="router.push({name:'Home'})">Mars </span><span class="roboto-condensed-200  ">Air</span><span class="!text-purple-800 dark:!text-purple-400 font-weight-bold text-h4">Q</span> 
                      </div>
                  </div>               
                   
                </VCardItem>
                <VCardItem>
                  <div class="text-3xl text-center">New Account Request Submited</div>
                  <!-- <div class="text-caption  text-onInverseSurface">Your email <strong class="text-secondary"> {{ signupForm.email.data}} </strong> has been confirmed</div> -->
                  <p class="mt-10" >
                    We are now processing your request, and you will receive an email notification once it's been completed. Thank you for your patience, and feel free to reach out if you have any questions in the meantime.
                  </p>
                </VCardItem>

                <VCardItem>
                  <VBtn class="text-sm my-4 !bg-purple-800 dark:!bg-purple-400 !text-gray-200 dark:!text-gray-700" width="100" to="/login" variant="flat"  rounded="xl"  >Continue</VBtn>
                </VCardItem>

              </VCard>
            </div>
          </VSheet>
        </VCarouselItem>
      </VCarousel>
      
    </VCol>
  </VRow>
</VContainer>
 
  </template>
  
  <script setup lang="ts"> 
  // IMPORTS
  import { useNotificationStore } from '@/stores/notificationStore';
  import { useDisplay } from 'vuetify'
  import { useTheme } from 'vuetify'
  import { useForm } from 'vee-validate';  
  import { object, string, number, date, ObjectSchema  } from 'yup'; 
  import { useRoute, useRouter } from "vue-router";
  import { ref,reactive, onMounted,onBeforeMount,computed, watch} from 'vue'; 
  import { Icon } from '@iconify/vue';

  // PINIA STORES
  import { storeToRefs } from 'pinia';
  import { useAppStore} from '@/stores/appStore';
  import { useUserStore} from '@/stores/userStore'; 
  import { useToast } from 'primevue/usetoast'; 
  
  
  // VARIABLES 
  const { smAndDown,smAndUp, xs }   = useDisplay();
  const NotificationStore = useNotificationStore();  
  const UserStore         = useUserStore(); 
  const AppStore          = useAppStore()
  const router            = useRouter();
  const route             = useRoute(); 
  const theme             = useTheme();
  const loading           = ref(false);
  const toast             = useToast();  
  const timeout           = 2000
  const timer             = ref(0);
  const variant           = "outlined"; //   'outlined' | 'plain' | 'underlined' | 'filled' | 'solo' | 'solo-inverted' | 'solo-filled'
  const registered        = ref(false); 
  const timerstate        = ref("start"); 
  const verification      = ref("");
  const page              = ref(0); 
  const department        = ref("");  
  const verifying         = ref(false);
  const {darkmode}        = storeToRefs(UserStore);
  const {caribbeanCountries, signupEntities} = storeToRefs(AppStore);
  const snackbar           = reactive({"show":ref(false),"text":ref(""),"timeout": ref(3000),"color": ref("success")});
  const showPasscode          = ref(false);  
  const showPasscodeConfirm   = ref(false);  
  const enableSubmitButton  = ref(false); 
  const errors        = reactive({name:"", errors: []}); 
  const finished    = ref(false); 
  // const organizations = ref();
  const selectedOrganizations = ref();
  const filteredOrganizations = ref();


  
    
  const signupForm = reactive({
      "firstname": ref({"icon":"fa:fas fa-user","label":"First Name","hint":"Enter your first name", "type":"text","name":"Firstname","data":"","variant":variant}),
      "lastname": ref({"icon":"mdi","label":"Last Name","hint":"Enter your last name", "type":"text","name":"Lastname","data":"","variant":variant}),
      "email": ref({"icon":"mdi:mdi-email-variant","label":"E-mail","hint":"Enter your account E-mail address ", "type":"email","name":"Email","data":"","variant":variant}),
      "organization": ref({"icon":"mdi mdi-office-building","label":"Organization","hint":"Enter the name of your Organization", "type":"text","name":"Organization","data":"","variant":variant}),
      "country": ref({"icon":"mdi:mdi-earth","label":"Country","hint":"Select your Country", "type":"text","name":"Country","data":"","variant":variant}),
      "password": ref({"icon":"mdi:mdi","label":"Password","hint":"Enter your super secret password", "type":"password","name":"Password","data":"","variant":variant}),
      "passwordconfirm": ref({"icon":"mdi:mdi","label":"Confirm Password","hint":"Re-Enter your super secret password", "type":"password","name":"PasswordConfirm","data":"","variant":variant})
  });

  const complete          = reactive({
                                "account": ref(false),
                                "verification": ref(false),
                                "complete": ref(false)
                              });

 
  // VALIDATION CONFIG 
  interface Person {
    firstname:  string;
    lastname: string;
    email: string;
    // organization: string; 
    country: string;
    password: string;
    passwordconfirm:  string;
  }

  const schema: ObjectSchema<Person> =   object({    
    passwordconfirm: string().required('Confirm password required!').min(8, 'Minimum 8 characters').matches(/[~`!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?]/, 'Minimum 1 special character').matches(/.*[A-Z].*/, 'Minimum 1 capitalized letter'),
    password: string().required('No password provided.').min(8, 'Minimum 8 characters').matches(/[~`!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?]/, 'Minimum 1 special character').matches(/.*[A-Z].*/, 'Minimum 1 capitalized letter'),
    country: string().min(2, 'Minimum 2 characters').optional().required("Country required!"),
    // organization: string().optional(), 
    email: string().email('Please enter a valid E-mail').required("E-mail required!").matches(/^[\w-\.]+@([\w-]+\.)+[\w-]{2,4}$/, 'Enter a valid E-mail address'), //.test('staff email', 'Enter a valid E-mail address', (value) => { return value && !value.includes("cimh.edu.bb"); }),
    lastname: string().min(2, 'Minimum 2 characters').required("Lastname required!"),        
    firstname: string().min(2, 'Minimum 2 characters').required("Firstname required!")

        });
    
 
  // PROPS
  // const props = defineProps({
  //     item:{type:String,default:""},
  // })
  
  
 onBeforeMount(()=>{
    theme.global.name.value = darkmode.value ?  'darkMode' : 'lightMode';
    localStorage.setItem("theme",darkmode.value ? 'darkMode' : 'lightMode');  
    AppStore.getEntitiesForSignup(); 
 });
  
  onMounted(() => {  
    page.value = 0; 
    setInterval(()=>{       
      timer.value--;
      if(timer.value <= 0){
        timer.value = 0;        
      }
    },1000);

  });

// Computed Properties
const countries = computed(() => {
  let list = [];
  caribbeanCountries.value.forEach((country) => list.push(country.name));
  return list
})

const getCountryIcon = computed(() => {
  return (code)=> {
    let icon = "";
    caribbeanCountries.value.forEach((country) => {
      if(country.code == code)
        icon = country.icon
    });
    return icon
  }
})

// WATCHERS 

watch(verification,  (code) => {
  // VERIFY CODE EMAILED TO USER
  if(code.length === 8){
    register();    
  }
});



watch(signupForm,  async (form) => {
  // VERIFY CODE EMAILED TO USER

   const person: Person = {firstname: form.firstname.data, lastname:form.lastname.data, email:form.email.data, country: form.country.data, password:form.password.data,  passwordconfirm: form.passwordconfirm.data}
    
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
 

watch(darkmode,  (mode) => {
  theme.global.name.value = mode ?  'darkMode' : 'lightMode';
  localStorage.setItem("theme",mode ? 'darkMode' : 'lightMode');  
});

watch(timer,  (state) => { 
  // CLOSE MODAL AND NOTIFY USER SINCE VERIFICATION TIMEDOUT
  if(state === 0){
    snackbar.color  = "info";
    snackbar.text   = "Canceling registration" ;
    snackbar.show   = true ; 
    setTimeout(()=>{cancel();},4000);
  }
});


const rules =  ( name: string) => {    
  
  if(name == "Firstname"){     
        if(errors.name == "firstname"){
          return errors.errors
        }   
        return [true] 
      }

  if(name == "Lastname"){     
    if(errors.name == "lastname"){
      return errors.errors
    }   
    return [true]
  }

  if(name == "Email"){     
    if(errors.name == "email"){
      return errors.errors
    }   
    return [true]
  }

  if(name == "Organization"){     
    if(errors.name == "organization"){
      return errors.errors
    }   
    return [true]
  }

  if(name == "Country"){     
    if(errors.name == "country"){
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

  if(name == "PasswordConfirm"){     
    if(errors.name == "passwordconfirm"){
      return errors.errors
    }   
    return [true]
  }
};


const minutes = computed(()=>{
  let min = Math.floor(timer.value / 60);
  return (min < 10)? `0${min}`: min;
});

const seconds = computed(()=>{
  let sec =  timer.value % 60;
  
  return (sec < 10)? `0${sec}` : sec;
});

  
// FUNCTIONS
const search = (event) => {
    setTimeout(() => { 
        if (!event.query.trim().length) {
            filteredOrganizations.value = [...signupEntities.value];
        } else {
            filteredOrganizations.value = signupEntities.value.filter((entity) => {
                return entity.organization.toLowerCase().startsWith(event.query.toLowerCase());
            });
        }
    }, 250);
}

const onClickFinish = ()=> {
        finished.value = true
    }

  const cancel = ()=>{
    timer.value = 0;
    page.value = 0;
    router.replace({name:"Login"});
  }

 

const onSubmit =  ()=> {
  //alert(JSON.stringify(values, null, 2));
  preRegister();
} ;


 
 
 const preRegister = async ()=>{
    // COLLECT USER INPUT FROM LOGIN FORM THEN POST TO FLASK API
     
    let lForm           = document.querySelector<HTMLFormElement>("#signupForm") ;
    let form            = new FormData(lForm);  
  
    let entity          = (!!selectedOrganizations.value)? selectedOrganizations.value.id : ""
    let organization    = (!!selectedOrganizations.value)? selectedOrganizations.value.organization : ""

    form.set("Entity", entity);
    form.set("Organization", organization);

    const URL           = '/api/verification' ; 

    // FETCH REQUEST WILL TIMEOUT AFTER 60 SECONDS 
    const controller    = new AbortController();
    const signal        = controller.signal;
    const id            = setTimeout(()=>{controller.abort()}, 60000);

    const cookie        = UserStore.getCookie("csrf_access_token"); 

    loading.value = true;
    
    try {
            const response  = await fetch(URL,{ method: 'POST',body:form, signal: signal ,headers: {"X-CSRF-TOKEN": cookie ,'X-USER':'internal'} });
            
            if(response.ok){
              const data              = await response.json(); 
              let keys                = Object.keys(data);              
              
              loading.value = false;

              if(keys.includes("message")){
                    // console.log(data);
                    if(  data['message'] === "emailSent" || data['message'] === "alreadySent"){ 
                    
                        page.value            = 1 ;
                        timerstate.value      = "running";
                        timer.value           = (data['message'] === "alreadySent")? parseInt(data['timestamp']) : 300;
                        complete.account      = true;

                        // PUSH NOTIFICATION 
                        toast.add({ severity: 'info', summary: 'Notification', detail: 'Email Sent!', life: 3000 });
                          
                    }
                    else if(  data['message'] === "Account Already Exist" ){       
                      
                          // PUSH NOTIFICATION   
                          toast.add({ severity: 'error', summary: 'Warning', detail: 'Account Already Exist. You will be redirecteed to the Login page', life: 3000 });
 
                          // REDIRECT TO LOGIN PAGE SINCE ACCOUNT ALREADY EXIST
                          setTimeout(()=>{router.push({name:"Login"});},4000);
                            
                      }
                    else if(  data['message'] === "Mismatched Passwords" ){       
                      
                      // PUSH NOTIFICATION   
                      toast.add({ severity: 'error', summary: 'Error', detail: 'Mismatched Passwords', life: 3000 });                        
                      }
                    else {  
                          // PUSH NOTIFICATION   
                          toast.add({ severity: 'error', summary: 'Error', detail: 'Registration Failed', life: 3000 }); 
                    }                                                                          
                          
                      }
              else{                                           
                      // PUSH NOTIFICATION   
                      toast.add({ severity: 'error', summary: 'Error', detail: 'Unable send an Email to that account', life: 3000 }); 
              }
            }
            else{
              // REQUEST FAILED OR RETURNED ERRORS
              loading.value = false;

              const data      = await response.text();
              // console.warn(data);
              setTimeout( ()=>{ preRegister() } ,1000);              

            }
    
        }
        catch(error){
          loading.value = false;
          if( error.message === "The user aborted a request."){
                console.log("REQUEST TIMEDOUT"); 
              } 

          console.error('Error:', error);
          // PUSH NOTIFICATION  
          toast.add({ severity: 'warn', summary: 'Notification', detail: 'Request Timed Out', life: 3000 });    
        }   
 }

 const register = async ()=>{
    // COLLECT USER INPUT FROM LOGIN FORM THEN POST TO FLASK API
   
    let lForm           = document.querySelector<HTMLFormElement>("#signupForm") ;
    let form            = new FormData(lForm);     
    const URL           = '/api/register' ; 

    let entity          = (!!selectedOrganizations.value)? selectedOrganizations.value.id : ""
    let organization    = (!!selectedOrganizations.value)? selectedOrganizations.value.organization : ""


    form.set("Entity", entity);
    form.set("Organization", organization);
    form.set("Code", verification.value)

    // FETCH REQUEST WILL TIMEOUT AFTER 20 SECONDS 
    const controller    = new AbortController();
    const signal        = controller.signal;
    const id            = setTimeout(()=>{controller.abort()},60000);
 
    const cookie        = UserStore.getCookie("csrf_access_token"); 

    loading.value       = true;
    verifying.value     = true;
    try {
            const response  = await fetch( URL, { method: 'POST',body: form, signal: signal ,headers: { "X-CSRF-TOKEN": cookie, "X-USER": "internal" } });
            
            if(response.ok){
              loading.value   = false;
              verifying.value = false;
              const data      = await response.json(); 
              let keys        = Object.keys(data);
              
              // console.log(data);
              if(keys.includes("message")){
                    // console.log(data);
                    if(  data['message'] === "Registered"){                         
                        page.value            = 2 ;        
                        toast.add({ severity: 'success', summary: 'Notification', detail: 'New account request received', life: 3000 });
                        // REDIRECT TO LOGIN PAGE SINCE REGISTRATION WAS SUCCESSFUL
                        // setTimeout(()=>{router.push({name:"Login"});},15000);                         
                    }
                    else if(data['message'] === "formErrors"){                       
                        // PUSH NOTIFICATION 
                        snackbar.color  = "errorContainer";
                        snackbar.text   = "Form Errors" ; 
                        snackbar.show   = true ;                      
                    } 
                    
                    else if(  data['message'] === "Verification Failed!. Check that the code entered is correct" ){       
                      
                      // PUSH NOTIFICATION      
                      toast.add({ severity: 'error', summary: 'Error', detail: 'Verification failed. Retry', life: 3000 });                       
                      }
                    else{             
                          // PUSH NOTIFICATION    
                          toast.add({ severity: 'error', summary: 'Error', detail: 'New account request failed', life: 3000 });   
                    }
                                                                            
                          
                      }
              
              else { 
                    // PUSH NOTIFICATION   
                    toast.add({ severity: 'error', summary: 'Error', detail: 'Unable To Process Request', life: 3000 });   
              }

            }
            else {
              loading.value   = false;
              verifying.value = false;
              const data      = await response.text();
              console.warn(data);
               setTimeout( ()=>{ register()} ,1000);
            }
        }
        catch(error){
          loading.value = false;
          verifying.value = false;
          if( error.message === "The user aborted a request."){ 
            console.log("REQUEST ABORTED");       
          }  
          console.error('Error:', error);  
          // PUSH NOTIFICATION    
          toast.add({ severity: 'error', summary: 'Error', detail: 'Request Aborted', life: 3000 });   
     }

    }

    
  </script>

  <style scoped >
  
  ::v-deep input:-webkit-autofill { 
  box-shadow: 0 0 0 0 rgba(168, 6, 44, 0) inset !important; /* Shadow effect */
  -webkit-box-shadow: 0 0 0 0 rgba(185, 19, 19, 0) inset !important; /* Ensure it works on Safari too */  
  border-top-left-radius: 25px;  /* border-radius: 25px; */
  border-bottom-left-radius: 25px;
}

  </style>
  
 