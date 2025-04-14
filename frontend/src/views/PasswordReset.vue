<template>
  <VContainer fluid class="fill-height pa-0">
  <VRow class="fill-height pa-0" >
    <VCol cols="4" class="bg-slate-900 pa-0" >    
      
      <Toast  position="bottom-right" />
      <div class="h-[400px]" >
        <Transition name="fade" :duration="5000" >   
          <div class="" v-show="resetPasswordPage >= 0 && resetPasswordPage <= 2" >
            <VCard width="100%" height="250">
              <template #image>
                <VImg  src="@/assets/digitallock.png" cover  max-height="250" height="100%">              
                  <template v-slot:placeholder>
                    <div class="d-flex align-center justify-center fill-height">
                      <VProgressCircular color="grey-lighten-4" indeterminate ></VProgressCircular>
                    </div>
                  </template>
                </VImg> 
              </template>
           
            </VCard>
            <div class=" mt-2 text-center" >
              <span class="roboto-black-italic text-slate-200 font-bold text-xl " style=" cursor: pointer" @click="router.push({name:'Home'})">Mars </span><span class="roboto-condensed-200 !text-sky-400">Air</span><span class="text-slate-200 font-weight-bold text-h4">Q</span> 
            </div>
            <div class="  text-center" >
              <span class="roboto-black-italic text-slate-200 text-4xl " style=" cursor: pointer" @click="router.push({name:'Home'})">Password Reset </span> 
            </div>
          </div>    
        
        </Transition>
      </div>
      
   
       
            
        
      <VStepperVertical v-model="resetPasswordPage" color="secondary" flat border theme="dark" hide-actions class="mx-5 "  >
        <template v-slot:default="{step}">
          <VStepperVerticalItem class="bg-transparent !text-gray-300" :complete="step > 0" subtitle="Personal details" title="Email" value="0" >
            <p class="nunito text-sky-400 text-xl  font-medium" > Submit E-mail address  </p>
          </VStepperVerticalItem>

          <VStepperVerticalItem class="bg-transparent !text-gray-300" :complete="step > 1" subtitle="Sent verification code" title="Verification" value="1" >
            <p class="nunito text-sky-400 text-xl font-medium" > Sent verification code.   </p>
          </VStepperVerticalItem>

          <VStepperVerticalItem class="bg-transparent !text-gray-300" :complete="step > 2" subtitle="Submit new password" title="Password" value="2"   >
            <p class="nunito text-sky-400 text-xl font-medium" > Please provide your new password  </p>
          </VStepperVerticalItem>   
          
          <VStepperVerticalItem class="bg-transparent !text-gray-300" subtitle="Password reset complete" title="Confirmation" value="3"   >
            <p class="nunito text-sky-400 text-xl font-medium" > Password reset was successful! Your new password have been saved.  </p>
          </VStepperVerticalItem>  
        </template>
      </VStepperVertical>    
    </VCol>

    <VCol cols="8" class="bg-blue pa-0" >
      <VCarousel v-model="resetPasswordPage" height="100%" hide-delimiter-background :show-arrows="false">
        <VCarouselItem   key="0" >
          <VSheet height="100%" >
            <div class="d-flex flex-col fill-height justify-center align-center">
              <VCard     width="300"  flat justify="center"  > 

                  <template v-slot:title>
                    <div class="nunito-title text-center text-onInverseSurface text-3xl">E-mail Address</div>
                  </template>
                  <template v-slot:subtitle>
                    <div class="nunito text-center text-sm">Please provide your E-mail address</div>
                  </template> 

                  <VCardItem   >
                    <form  @submit.prevent="sendVerificationCode" id="resetForm"  >  
                      <VResponsive v-for="field in resetForm" :key="field.label">
                            <VTextField
                                v-if="field.name == 'Email'"
                                  :error        = "(!!password(field.name))"
                                  clearable
                                  flat
                                  class         = "text-caption mt-2"
                                  rounded       = "lg"
                                  density       = "compact"
                                  :label        = "`${(!!errors[field.name.toLocaleLowerCase()])? errors[field.name.toLocaleLowerCase()] : field.label }`" 
                                  :variant      = "field.variant" 
                                  :type         = "field.type"
                                  :name         = "field.name"              
                                  v-model       = "field.data" 
                                  >
                            </VTextField> 
                      </VResponsive> 
                    </form>
                  
                  </VCardItem> 

                 
                </VCard>     
            
                <VBtn  class="text-subtitle-2 my-4 !bg-sky-400 !text-gray-200" :disabled="emailBtn" width="270"  :loading="emailLoading" type="submit" form="resetForm" variant="tonal" rounded = "lg">Submit</VBtn>
               
                 
            </div>
          </VSheet>
        </VCarouselItem>

        <VCarouselItem    key="1" >
          <VSheet height="100%" >
            <div class="d-flex fill-height justify-center align-center">
              <VCard :class="[(smAndDown)? 'px-0' :'px-6']"   class="text-center mx-auto ma-4 " max-width="600" width="100%" min-height="600" rounded="md"   flat >
                <template v-slot:title>
                    <div class="nunito-title text-center text-onInverseSurface text-3xl">Verification</div>
                  </template>
                  <template v-slot:subtitle>
                    <div class="nunito text-center text-sm">We sent a verification code to</div>
                  </template>

                  <!-- <h3 class="text-h5 mb-4"></h3> -->

                 <VCardItem  class="my-1" >
                   
                    <p class="text-sky-400 text-lg font-bold my-2">{{ resetForm.email.data }}</p>

                    <p class="text-center"  >
                      A verification code has been sent to your email. Please check your inbox (and spam folder, if necessary) for the code. Once you find it, enter the code in the provided field to complete the verification process. 
                    </p>

                  
                      <div  >                        
                        <p class="nunito text-md mt-5 font-normal" >Time remaining </p>
                        <h4 class="text-error text-3xl">{{minutes}} : {{seconds}}</h4>
                      </div>        
                   

                    <VSheet  >
                      <VOtpInput v-model = "verification" type="text" class="!text-gray-200 font-bold" :loading="verifying" color="sky-400"  :length="8" variant="outlined" ></VOtpInput>
                    </VSheet>
                    

                    <div class="  text-md mt-15">
                      Didn't receive the code? <VBtn text="Re-send" class="text-caption ml-5 font-bold " color="secondary" variant="tonal" density="compact" @click.prevent="sendVerificationCode" flat  />  
                    </div>
                 </VCardItem>
                </VCard>
            </div>
          </VSheet>
        </VCarouselItem>

        <VCarouselItem    key="2" >
          <VSheet height="100%" >
            <div class="d-flex flex-col fill-height justify-center align-center">
              <VCard      subtitle="New Password" max-width="60%" flat   >                     
                      

                     <template v-slot:title>
                      <div class="nunito-title text-center text-onInverseSurface text-3xl">New Password</div>
                    </template>
                    <template v-slot:subtitle>
                      <div class="nunito text-center text-sm">Please provide your new password</div>
                    </template> 

                       <VCardItem>
                         <form  @submit.prevent="resetPassword" id="resetForm1"  >
                             <VResponsive v-for="field in resetForm" :key="field.label">
                                 <VTextField
                                     v-if="field.name != 'Email'"
                                       :error        = "(!!password(field.name))"
                                       clearable
                                       flat
                                       hide-details
                                       class         = "text-caption  py-1 "
                                       rounded       = "lg"
                                       density       = "compact"   
                                       :label        = "`${(!!errors[field.name.toLocaleLowerCase()])? errors[field.name.toLocaleLowerCase()] : field.label }`"                           
                                       :variant      = "field.variant"                                
                                       :type         = "((field.name == 'Password' && showPasscode) || (field.name == 'PasswordConfirm' && showPasscodeConfirm) )? 'text':field.type"
                                       :name         = "field.name"            
                                       v-model       = "field.data" 
                                       >
                                       <template v-slot:append-inner>                                
                                         <VIcon  @click="(field.name == 'Password')? showPasscode = !showPasscode : showPasscodeConfirm = !showPasscodeConfirm " :icon="((field.name == 'Password' && showPasscode) || (field.name == 'PasswordConfirm' && showPasscodeConfirm)) ? 'mdi:mdi-eye' : 'mdi:mdi-eye-off'" size="16"></VIcon>                                 
                                       </template>
                                       <template v-slot:clear>
                                         <VIcon icon="mdi:mdi-close-circle" @click="field.data = ''" size="16"></VIcon>
                                       </template>
                                 </VTextField> 
                           </VResponsive> 
                         </form>
                       </VCardItem> 
              </VCard>  
              <VBtn text="Submit" class="text-subtitle-2 my-4 !bg-sky-400 !text-gray-200"   width="220" :disabled="passwordBtn"  :loading="passwordLoading" type="submit" form="resetForm1"  variant="flat" rounded="lg"  justify-self="right" />   
              
            </div>
          </VSheet>
        </VCarouselItem>

        <VCarouselItem    key="3" >
          <VSheet height="100%" >
            <div class="d-flex fill-height justify-center align-center">
              <VCard   max-width="60%"  flat>
                <VCardItem>                
                    <div class="mb-15" >
                      <VImg  src="@/assets/digitallock.png"  width="300" height="100%" rounded="lg" >              
                        <template v-slot:placeholder>
                          <div class="d-flex align-center justify-center fill-height">
                            <VProgressCircular color="grey-lighten-4" indeterminate ></VProgressCircular>
                          </div>
                        </template>
                      </VImg> 
                      <div class=" text-center mt-5" >
                        <span class="roboto-black-italic text-sky-400 text-2xl " style=" cursor: pointer" @click="router.push({name:'Home'})">Mars </span><span class="roboto-condensed-200  ">Air</span><span class="text-sky-400 font-weight-bold text-h4">Q</span> 
                      </div>
                  </div>                  
                </VCardItem>

                <VCardItem>
                  <div class="nunito-title text-3xl text-center">You're all set!</div> 
                  <div class="nunito mt-1 text-center" > Password reset complete </div>
                </VCardItem>

                <VCardItem align="center" >
                  <VBtn class="text-caption my-5 !bg-sky-400 !text-gray-200" to="/login" variant="flat"  rounded="lg"  >Continue</VBtn>
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

<script setup> 
  // IMPORTS
  import { useNotificationStore } from '@/stores/notificationStore';
  import { useDisplay } from 'vuetify'
  import { useTheme } from 'vuetify'
  import { useForm } from 'vee-validate';  
  import * as yup from 'yup';
  import { useRoute, useRouter } from "vue-router";
  import { ref,reactive, onMounted,onBeforeMount,onBeforeUnmount,computed, watch} from 'vue';
  import { useToast } from 'primevue/usetoast';

  // PINIA STORES
  import { storeToRefs } from 'pinia';
  import { useAppStore} from '@/stores/appStore';
  import { useUserStore} from '@/stores/userStore';
 



  // VARIABLES 
  const { smAndDown,smAndUp, xs }   = useDisplay();
  const NotificationStore = useNotificationStore(); 
  const UserStore         = useUserStore(); 
  const AppStore          = useAppStore()
  const router            = useRouter();
  const route             = useRoute(); 
  const theme             = useTheme();
  const toast             = useToast();  
  const {darkmode,resetPasswordPage,resetTimer}        = storeToRefs(UserStore); 
  const verification      = ref("");
  const page              = ref(0);
  let prTimerID;
  const variant           = "outlined"; //   'outlined' | 'plain' | 'underlined' | 'filled' | 'solo' | 'solo-inverted' | 'solo-filled'
  const complete          = reactive({ "account": ref(false), "verification": ref(false), "password": ref(false), "complete": ref(false) });
  const resetForm         = reactive({ 
                                  "email": ref({"icon":"mdi:mdi-email-variant","label":"E-mail","hint":"Enter your account E-mail address ", "type":"email","name":"Email","data":"","variant":variant}),
                                  "password": ref({ "label":"Password", "type":"password","name":"Password","data":"","variant":variant}),
                                  "passwordConfirm": ref({ "label":"Confirm Password", "type":"password","name":"PasswordConfirm","data":"","variant":variant })
                              });
 
  const snackbar              = reactive({"show":ref(false),"text":ref(""),"timeout": ref(3000),"color": ref("success")});
  const emailLoading          = ref(false);      
  const verifying             = ref(false);
  const passwordLoading       = ref(false);  
  const showPasscode          = ref(false);  
  const showPasscodeConfirm   = ref(false);  
  

    // VALIDATION CONFIG 

    const schema =   yup.object({        
      email: yup.string().email('Please enter a valid E-mail').required("E-mail required!").matches(/^[\w-\.]+@([\w-]+\.)+[\w-]{2,4}$/, 'Enter a valid E-mail address').test('staff email', 'Enter a valid E-mail address', (value) => { return value && !value.includes("cimh.edu.bb"); }),
          password: yup.string().required('No password provided.').min(8, 'Minimum 8 characters').matches(/[~`!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?]/, 'Minimum 1 special character').matches(/.*[A-Z].*/, 'Minimum 1 capitalized letter'),
          passwordConfirm: yup.string().required('Confirm password required!').min(8, 'Minimum 8 characters').matches(/[~`!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?]/, 'Minimum 1 special character').matches(/.*[A-Z].*/, 'Minimum 1 capitalized letter'),
        });
        
  const { useFieldModel, errors, handleSubmit } = useForm({validationSchema: schema } );
  [resetForm.email.data,resetForm.password.data,resetForm.passwordConfirm.data ] = useFieldModel(['email','password','passwordConfirm']);

 


const onSubmit = handleSubmit(values => {
  //alert(JSON.stringify(values, null, 2));
  // preRegister();
} );
  // PROPS
  const props = defineProps({
      item:{type:String,default:""},
  })

  // COMPUTED
  const minutes = computed(()=>{
    let min = parseInt(resetTimer.value / 60);
    return (min < 10)? `0${min}`: min;
  });

  const emailBtn = computed(()=>{    
    return (Object.keys(errors.value).length > 0 || !!resetForm.email.data == false) ? true : false
  });

  const passwordBtn = computed(()=>{    
    return (Object.keys(errors.value).length > 0 || !!resetForm.password.data == false || !!resetForm.passwordConfirm.data == false || resetForm.password.data != resetForm.passwordConfirm.data ) ? true : false
  });

  const seconds = computed(()=>{
    let sec = parseInt(resetTimer.value % 60);
    
    return (sec < 10)? `0${sec}` : sec;
  });

  const password = computed(()=>{
    // DYNAMIC COMPUTED PROPERTY
    return (name)=>{
          const keys = Object.keys(errors.value);
          if(name == "Password"){
              if(keys.includes("password")){
                return errors.value["password"]
              }
              return ""
          }
          if(name == "PasswordConfirm"){
              if(keys.includes("passwordConfirm")){
                return errors.value["passwordConfirm"]
              }
              return ""
          } 

          if(name == "Email"){     
            if(keys.includes("email")){
              return errors["email"]
            }   
            return ""
           }
        }
    
  });


  // EMITTERS
  // const emit = defineEmits(["currentRoute"]);

  // WATCHERS
  watch(resetTimer,  (state) => { 
    // CLOSE MODAL AND NOTIFY USER SINCE VERIFICATION TIMEDOUT
    if(state === 0){
      snackbar.color  = "info";
      snackbar.text   = "Canceling password reset " ;
      snackbar.show   = true ; 
      setTimeout(()=>{cancel();},4000);
    }
  });

  watch(verification,  (code) => {
    // VERIFY CODE EMAILED TO USER
    if(code.length === 8){ 
      verifyCode();    
    }
  });

  watch(darkmode,  (mode) => {
    theme.global.name.value = mode ?  'darkMode' : 'lightMode';
    localStorage.setItem("theme",mode ? 'darkMode' : 'lightMode');  
  });

  // FUNCTIONS
  const cancel = ()=>{
    resetTimer.value = 0;
    router.replace({name:"Login"});
  }

  onBeforeMount(()=>{
    theme.global.name.value = darkmode.value ?  'darkMode' : 'lightMode';
    localStorage.setItem("theme",darkmode.value ? 'darkMode' : 'lightMode');  
  }); 

  onBeforeUnmount(()=>{
    // console.log("PASSWORD RESET UNMOUNTING");
    clearTimeout(prTimerID);
  });

  onMounted(()=>{
    // console.log("PASSWORD RESET MOUNTED")
    resetPasswordPage.value = 0;
    clearTimeout(prTimerID); // prevent errant multiple timeouts from being generated
    prTimerID = setInterval(()=>{       
      resetTimer.value--;
      
      if(resetTimer.value <= 0){
        resetTimer.value = 0;        
      }
    },1000);
  });

  const sendVerificationCode = async ()=>{
    // COLLECT USER INPUT FROM LOGIN FORM THEN POST TO FLASK API
     
    let lForm           = document.querySelector("#resetForm") ;
    let form            = new FormData(lForm);     
 
    const URL           = '/api/verification/sendemail' ;
    

    // FETCH REQUEST WILL TIMEOUT AFTER 60 SECONDS 
    const controller    = new AbortController();
    const signal        = controller.signal;
    const id            = setTimeout(()=>{controller.abort()}, 60000);

    const cookie        = UserStore.getCookie("csrf_access_token"); 

    emailLoading.value = true;
    
    try {
            const response  = await fetch(URL,{ method: 'POST',body:form, signal: signal ,headers: {"X-CSRF-TOKEN": cookie ,'X-USER':'internal'} });
            
            if(response.ok){
              const data              = await response.json(); 
              let keys                = Object.keys(data);              
              
              emailLoading.value = false;

              if(keys.includes("message")){
                    // console.log(data);
                    if(  data['message'] === "emailSent" || data['message'] === "alreadySent"){  
                        resetPasswordPage.value   = 1 ; 
                        resetTimer.value          = (data['message'] === "alreadySent")? parseInt(data['timestamp']) : 300;
                        complete.account          = true;   
                        toast.add({ severity: 'info', summary: 'Notification', detail: 'Email Sent!', life: 3000 });                 
                    }
                    else if(  data['message'] === "Account Does Not Exist" ){   
                          // PUSH NOTIFICATION   
                          toast.add({ severity: 'error', summary: 'Error', detail: 'Account Does Not Exist!', life: 3000 });                                  
                      }   
                      else if(  data['message'] === "failed" ){   
                          // PUSH NOTIFICATION    
                          toast.add({ severity: 'error', summary: 'Error', detail: 'Unable to send an email to that account!', life: 3000 });                         
                      }                                                                    
                          
                      }
              else{     
                      // PUSH NOTIFICATION    
                      toast.add({ severity: 'error', summary: 'Error', detail: 'Unable To Process', life: 3000 });
              }
            }
            else{
              // REQUEST FAILED OR RETURNED ERRORS
              emailLoading.value = false;
              const data      = await response.text();
              console.warn(data);
              setTimeout( ()=>{ sendVerificationCode() } ,2000);   
            }
        }
        catch(error){
          emailLoading.value = false;
          console.error('Error:', error); 
          if( error.message === "The user aborted a request."){
                console.log("REQUEST TIMEDOUT"); 
                // PUSH NOTIFICATION     
                toast.add({ severity: 'error', summary: 'Error', detail: 'Request Timed Out', life: 3000 });  
              }    
        }   
 }

 const verifyCode = async ()=>{
    // COLLECT USER INPUT FROM LOGIN FORM THEN POST TO FLASK API
     
    let form            = new FormData();    
    form.append("Email", resetForm.email.data) 
    form.append("Code", verification.value)
    const URL           = '/api/verification/verifycode' ;
    

    // FETCH REQUEST WILL TIMEOUT AFTER 60 SECONDS 
    const controller    = new AbortController();
    const signal        = controller.signal;
    const id            = setTimeout(()=>{controller.abort()}, 60000);

    const cookie        = UserStore.getCookie("csrf_access_token"); 

    verifying.value = true;
    
    try {
            const response  = await fetch(URL,{ method: 'POST',body:form, signal: signal ,headers: {"X-CSRF-TOKEN": cookie ,'X-USER':'internal'} });
            
            if(response.ok){
              const data              = await response.json(); 
              let keys                = Object.keys(data);              
              
              verifying.value = false;

              if(keys.includes("message")){
                    // console.log(data);
                    if(  data['message'] === "verified"  ){  
                        resetPasswordPage.value    = 2 ;  
                        complete.verification      = true;
                           
                    }
                    else if(  data['message'] === "failed" ){   
                          // PUSH NOTIFICATION       
                          toast.add({ severity: 'error', summary: 'Error', detail: 'Verification Failed!. Check that the code entered is correct', life: 3000 });                        
                      }                                                                      
                          
                      }
              else{     
                      // PUSH NOTIFICATION   
                      toast.add({ severity: 'error', summary: 'Error', detail: 'Unable To Process', life: 3000 });  
              }
            }
            else{
              // REQUEST FAILED OR RETURNED ERRORS
              verifying.value = false;
              const data      = await response.text();
              console.warn(data);
              setTimeout( ()=>{ verifyCode() } ,2000);   
            }
        }
        catch(error){
          verifying.value = false;
          console.error('Error:', error); 
          if( error.message === "The user aborted a request."){
                console.log("REQUEST TIMEDOUT"); 
                // PUSH NOTIFICATION       
                toast.add({ severity: 'error', summary: 'Error', detail: 'Request Timed Out', life: 3000 });  
              }    
        }   
 }

 const resetPassword = async ()=> {
    // COLLECT USER INPUT FROM LOGIN FORM THEN POST TO FLASK API
    let lForm           = document.querySelector("#resetForm1") ;
    let form            = new FormData(lForm);  
    const URL           = '/api/verification/rp';

    
    form.append("Email", resetForm.email.data) 
    form.append("Code", verification.value)
    

    // FETCH REQUEST WILL TIMEOUT AFTER 60 SECONDS 
    const controller    = new AbortController();
    const signal        = controller.signal;
    const id            = setTimeout(()=>{controller.abort()}, 60000);

    const cookie        = UserStore.getCookie("csrf_access_token"); 

    passwordLoading.value = true;
    
    try {
            const response  = await fetch(URL,{ method: 'POST',body:form, signal: signal ,headers: {"X-CSRF-TOKEN": cookie ,'X-USER':'internal'} });
            
            if(response.ok){
              const data              = await response.json(); 
              let keys                = Object.keys(data);              
              
              passwordLoading.value = false;

              if(keys.includes("message")){
                    // console.log(data);
                    if(  data['message'] === "updated"  ){  
                        resetPasswordPage.value    = 3 ;  
                        complete.password      = true;
                        complete.complete      = true;
                           
                    }
                    else if(  data['message'] === "Mismatched passwords" ){   
                          // PUSH NOTIFICATION      
                          toast.add({ severity: 'error', summary: 'Error', detail: 'Mismatched passwords', life: 3000 });  

                          // REDIRECT TO LOGIN PAGE SINCE ACCOUNT ALREADY EXIST
                          //setTimeout(()=>{router.push({name:"Login"});},2000);                            
                      } 
                      else if(  data['message'] === "failed" ){   
                          // PUSH NOTIFICATION  
                          toast.add({ severity: 'error', summary: 'Error', detail: 'Reset failed. Check that the password entered is correct', life: 3000 });                              
                      }                                                                        
                          
                      }
              else{     
                      // PUSH NOTIFICATION   
                      toast.add({ severity: 'error', summary: 'Error', detail: 'Unable To Process', life: 3000 });  
              }
            }
            else{
              // REQUEST FAILED OR RETURNED ERRORS
              passwordLoading.value = false;
              const data      = await response.text();
              console.warn(data);
              setTimeout( ()=>{ resetPassword() } ,2000);   
            }
        }
        catch(error){
          passwordLoading.value = false;
          console.error('Error:', error); 
          if( error.message === "The user aborted a request."){
                console.log("REQUEST TIMEDOUT"); 
                // PUSH NOTIFICATION  
                toast.add({ severity: 'error', summary: 'Error', detail: 'Request Timed Out', life: 3000 });    
              }    
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

 