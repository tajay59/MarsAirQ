<template> 
    <VBottomNavigation v-model="value" bg-color="surface" mode="shift" :active="active"   height="90" border   > 
      
      <VBtn class="text-caption" :class="[(smAndDown)?'px-0':'px-3']" width="20px"   >
        <VIcon v-if="menu" icon="mdi:mdi-menu-open"></VIcon>
        <VIcon v-else icon="mdi:mdi-menu"></VIcon>

        <VMenu v-model="menu" :close-on-content-click="false" location="end" activator="parent" >   
          <VCard :min-width="(UserStore.loggedIn)? '300':'100' ">
            <VList v-if="UserStore.loggedIn">
              <VListItem  align="start" style="cursor: pointer;" @click="menu = false; router.push({name: 'Profile'});toTop()">
              <template v-slot:title>
                {{ `${account.firstname} ${account.lastname}` }} 
              </template>

              <template v-slot:subtitle>
              {{ account.email }}
              </template>

              <template v-slot:prepend>
                <VImg style="border-radius: 50%; border: 2px solid grey;" class="mx-2" cover src="@/assets/default.jpg" width="50" height="50" >
                  <template v-slot:placeholder>
                    <div class="d-flex align-center justify-center fill-height">
                      <VProgressCircular color="grey-lighten-4" indeterminate ></VProgressCircular>
                    </div>
                  </template>
                </VImg> 
              </template>

              <template v-slot:append>
                <VBtn icon="mdi:mdi-account" variant="text" color="inverseSurface" ></VBtn>
              </template>
              </VListItem>
            </VList>

            <VDivider></VDivider>

            <VList>
              <VListItem>
                <VBtn class="text-caption" text="Home" variant="text" @click="menu = false; router.push({name: 'Home'});toTop()" width="100%" rounded="lg" >
                  <template v-slot:prepend>
                    <svg class="svgIcon" >
                    <path d="M15 18H9"  stroke-linecap="round"/>
                    <path d="M21.6359 12.9579L21.3572 14.8952C20.8697 18.2827 20.626 19.9764 19.451 20.9882C18.2759 22 16.5526 22 13.1061 22H10.8939C7.44737 22 5.72409 22 4.54903 20.9882C3.37396 19.9764 3.13025 18.2827 2.64284 14.8952L2.36407 12.9579C1.98463 10.3208 1.79491 9.00229 2.33537 7.87495C2.87583 6.7476 4.02619 6.06234 6.32691 4.69181L7.71175 3.86687C9.80104 2.62229 10.8457 2 12 2C13.1543 2 14.199 2.62229 16.2882 3.86687L17.6731 4.69181C19.9738 6.06234 21.1242 6.7476 21.6646 7.87495"  stroke-linecap="round"/>
                    </svg>
                  </template>
                </VBtn>
              </VListItem>
              <VListItem>
                <VBtn class="text-caption"  text="Theme"  variant="text"    @click="darkmode = !darkmode"  width="100%" rounded="lg">                             
                  <template v-slot:prepend>
                    <svg v-if="darkmode" class="svgIcon"  >
                                <path d="M13.5 8H16.5L13.5 11H16.5"  stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                                <path d="M18 2H22L18 6H22"  stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                                <path stroke-width="0.5" id="moonIcon" d="M21.0672 11.8568L20.4253 11.469L21.0672 11.8568ZM12.1432 2.93276L11.7553 2.29085V2.29085L12.1432 2.93276ZM7.37554 20.013C7.017 19.8056 6.5582 19.9281 6.3508 20.2866C6.14339 20.6452 6.26591 21.104 6.62446 21.3114L7.37554 20.013ZM2.68862 17.3755C2.89602 17.7341 3.35482 17.8566 3.71337 17.6492C4.07191 17.4418 4.19443 16.983 3.98703 16.6245L2.68862 17.3755ZM21.25 12C21.25 17.1086 17.1086 21.25 12 21.25V22.75C17.9371 22.75 22.75 17.9371 22.75 12H21.25ZM2.75 12C2.75 6.89137 6.89137 2.75 12 2.75V1.25C6.06294 1.25 1.25 6.06294 1.25 12H2.75ZM15.5 14.25C12.3244 14.25 9.75 11.6756 9.75 8.5H8.25C8.25 12.5041 11.4959 15.75 15.5 15.75V14.25ZM20.4253 11.469C19.4172 13.1373 17.5882 14.25 15.5 14.25V15.75C18.1349 15.75 20.4407 14.3439 21.7092 12.2447L20.4253 11.469ZM9.75 8.5C9.75 6.41182 10.8627 4.5828 12.531 3.57467L11.7553 2.29085C9.65609 3.5593 8.25 5.86509 8.25 8.5H9.75ZM12 2.75C11.9115 2.75 11.8077 2.71008 11.7324 2.63168C11.6686 2.56527 11.6538 2.50244 11.6503 2.47703C11.6461 2.44587 11.6482 2.35557 11.7553 2.29085L12.531 3.57467C13.0342 3.27065 13.196 2.71398 13.1368 2.27627C13.0754 1.82126 12.7166 1.25 12 1.25V2.75ZM21.7092 12.2447C21.6444 12.3518 21.5541 12.3539 21.523 12.3497C21.4976 12.3462 21.4347 12.3314 21.3683 12.2676C21.2899 12.1923 21.25 12.0885 21.25 12H22.75C22.75 11.2834 22.1787 10.9246 21.7237 10.8632C21.286 10.804 20.7293 10.9658 20.4253 11.469L21.7092 12.2447ZM12 21.25C10.3139 21.25 8.73533 20.7996 7.37554 20.013L6.62446 21.3114C8.2064 22.2265 10.0432 22.75 12 22.75V21.25ZM3.98703 16.6245C3.20043 15.2647 2.75 13.6861 2.75 12H1.25C1.25 13.9568 1.77351 15.7936 2.68862 17.3755L3.98703 16.6245Z"/>
                            </svg>
                            <svg v-else  class="svgIcon"   >
                                <path d="M7.28451 10.3333C7.10026 10.8546 7 11.4156 7 12C7 14.7614 9.23858 17 12 17C14.7614 17 17 14.7614 17 12C17 9.23858 14.7614 7 12 7C11.4156 7 10.8546 7.10026 10.3333 7.28451"  stroke-linecap="round"/>
                                <path d="M12 2V4"  stroke-linecap="round"/>
                                <path d="M12 20V22"  stroke-linecap="round"/>
                                <path d="M4 12L2 12"  stroke-linecap="round"/>
                                <path d="M22 12L20 12"  stroke-linecap="round"/>
                                <path d="M19.7778 4.22266L17.5558 6.25424"  stroke-linecap="round"/>
                                <path d="M4.22217 4.22266L6.44418 6.25424"  stroke-linecap="round"/>
                                <path d="M6.44434 17.5557L4.22211 19.7779"  stroke-linecap="round"/>
                                <path d="M19.7778 19.7773L17.5558 17.5551"  stroke-linecap="round"/>
                            </svg>
                  </template>
                        </VBtn>
              </VListItem>
            </VList>

            <VCard-actions>
              <VSpacer></VSpacer> 
              <VBtn class="text-caption"  width="100" rounded="lg" @click="loginLogout" >
                <template v-slot:prepend>
                  <svg v-if="UserStore.loggedIn" class="svgIcon"  >
                      <path d="M15 12L6 12M6 12L8 14M6 12L8 10"   stroke-linecap="round" stroke-linejoin="round"/>
                      <path d="M12 21.9827C10.4465 21.9359 9.51995 21.7626 8.87865 21.1213C8.11027 20.3529 8.01382 19.175 8.00171 17M16 21.9983C18.175 21.9862 19.3529 21.8897 20.1213 21.1213C21 20.2426 21 18.8284 21 16V14V10V8C21 5.17157 21 3.75736 20.1213 2.87868C19.2426 2 17.8284 2 15 2H14C11.1715 2 9.75733 2 8.87865 2.87868C8.11027 3.64706 8.01382 4.82497 8.00171 7"  stroke-linecap="round"/>
                      <path d="M3 9.5V14.5C3 16.857 3 18.0355 3.73223 18.7678C4.46447 19.5 5.64298 19.5 8 19.5M3.73223 5.23223C4.46447 4.5 5.64298 4.5 8 4.5"  stroke-linecap="round"/>
                  </svg>
                  <svg v-else class="svgIcon"  >
                      <path d="M8 16C8 18.8284 8 20.2426 8.87868 21.1213C9.51998 21.7626 10.4466 21.9359 12 21.9827M8 8C8 5.17157 8 3.75736 8.87868 2.87868C9.75736 2 11.1716 2 14 2H15C17.8284 2 19.2426 2 20.1213 2.87868C21 3.75736 21 5.17157 21 8V10V14V16C21 18.8284 21 20.2426 20.1213 21.1213C19.3529 21.8897 18.175 21.9862 16 21.9983" stroke-linecap="round"/>
                      <path d="M3 9.5V14.5C3 16.857 3 18.0355 3.73223 18.7678C4.46447 19.5 5.64298 19.5 8 19.5M3.73223 5.23223C4.46447 4.5 5.64298 4.5 8 4.5" stroke-linecap="round"/>
                      <path d="M6 12L15 12M15 12L12.5 14.5M15 12L12.5 9.5" stroke-linecap="round" stroke-linejoin="round"/>
                  </svg>
                </template>
                
                <span v-if="UserStore.loggedIn">Logout</span>
                <span v-else>Login</span>
              </VBtn>
            </VCard-actions>
          </VCard>
        </VMenu>
        <span >Menu</span>
      </VBtn>

      <VBtn class="text-caption"  @click="router.push({name: 'Protected'});toTop()"  >
        <svg  class="svgIcon"  >
          <path d="M21.4825 19C21.4436 19.9362 21.3183 20.5101 20.9142 20.9142C20.3284 21.5 19.3856 21.5 17.5 21.5C15.6144 21.5 14.6716 21.5 14.0858 20.9142C13.5 20.3284 13.5 19.3856 13.5 17.5V15.5C13.5 13.6144 13.5 12.6716 14.0858 12.0858C14.6716 11.5 15.6144 11.5 17.5 11.5C19.3856 11.5 20.3284 11.5 20.9142 12.0858C21.4458 12.6173 21.495 13.4428 21.4995 15"  stroke-linecap="round"/>
          <path d="M2 8.5C2 10.3856 2 11.3284 2.58579 11.9142C3.17157 12.5 4.11438 12.5 6 12.5C7.88562 12.5 8.82843 12.5 9.41421 11.9142C10 11.3284 10 10.3856 10 8.5V6.5C10 4.61438 10 3.67157 9.41421 3.08579C8.82843 2.5 7.88562 2.5 6 2.5C4.11438 2.5 3.17157 2.5 2.58579 3.08579C2 3.67157 2 4.61438 2 6.5V8.5Z" />
          <path d="M15.5 2.51343C15.1727 2.53017 14.9385 2.56777 14.7346 2.65224C14.2446 2.85522 13.8552 3.24457 13.6522 3.73463C13.5 4.10217 13.5 4.56811 13.5 5.49999C13.5 6.43188 13.5 6.89782 13.6522 7.26536C13.8552 7.75542 14.2446 8.14477 14.7346 8.34775C15.1022 8.49999 15.5681 8.49999 16.5 8.49999H18.5C19.4319 8.49999 19.8978 8.49999 20.2654 8.34775C20.7554 8.14477 21.1448 7.75542 21.3478 7.26536C21.5 6.89782 21.5 6.43188 21.5 5.49999C21.5 4.56811 21.5 4.10217 21.3478 3.73463C21.1448 3.24457 20.7554 2.85522 20.2654 2.65224C20.0615 2.56777 19.8273 2.53017 19.5 2.51343"  stroke-linecap="round"/>
          <path d="M2 18.5C2 19.4319 2 19.8978 2.15224 20.2654C2.35523 20.7554 2.74458 21.1448 3.23463 21.3478C3.60218 21.5 4.06812 21.5 5 21.5H7C7.93188 21.5 8.39782 21.5 8.76537 21.3478C9.25542 21.1448 9.64477 20.7554 9.84776 20.2654C10 19.8978 10 19.4319 10 18.5C10 17.5681 10 17.1022 9.84776 16.7346C9.64477 16.2446 9.25542 15.8552 8.76537 15.6522C8.39782 15.5 7.93188 15.5 7 15.5H5C4.06812 15.5 3.60218 15.5 3.23463 15.6522C2.74458 15.8552 2.35523 16.2446 2.15224 16.7346C2 17.1022 2 17.5681 2 18.5Z" />
        </svg>
        <span>Protected</span>
      </VBtn>

      <VBtn class="text-caption"  @click="router.push({name: 'Map'});toTop()"  >
        <svg  class="svgIcon" viewBox="0 0 24 24"><defs><mask id="letsIconsMapDuotoneLine0"><g fill="none"><path stroke="silver" stroke-opacity="0.25" d="m18.5 21.5l-6-15m9-2l-19 4"/><path stroke="#fff" stroke-linecap="round" d="M2.5 5.7c0-1.12 0-1.68.218-2.108a2 2 0 0 1 .874-.874C4.02 2.5 4.58 2.5 5.7 2.5h12.6c1.12 0 1.68 0 2.108.218a2 2 0 0 1 .874.874c.218.428.218.988.218 2.108v12.6c0 1.12 0 1.68-.218 2.108a2 2 0 0 1-.874.874c-.428.218-.988.218-2.108.218H5.7c-1.12 0-1.68 0-2.108-.218a2 2 0 0 1-.874-.874C2.5 19.98 2.5 19.42 2.5 18.3z"/><path stroke="#fff" d="M12.5 15.03c0 2.158-2.14 3.674-3.073 4.233a.83.83 0 0 1-.854 0C7.64 18.704 5.5 17.188 5.5 15.029C5.5 12.912 7.196 11.5 9 11.5c1.867 0 3.5 1.412 3.5 3.53Z"/><circle cx="9" cy="15" r="1" fill="#fff"/></g></mask></defs><path fill="currentColor" d="M0 0h24v24H0z" mask="url(#letsIconsMapDuotoneLine0)"/></svg>
        <span>Map</span>
      </VBtn>
      
    </VBottomNavigation>

    <!-- <Notification/> -->
    <Modal />

</template>

<script setup>
// IMPORTS 
 
 
import { useUserStore} from '@/stores/userStore';
import { ref,watch ,onMounted, onBeforeMount, computed } from "vue";  
import { useRoute, useRouter } from "vue-router";
import { storeToRefs } from "pinia"; 
import { useDisplay } from 'vuetify';
import { useTheme } from 'vuetify'
import Notification from "./Notification.vue"; 
import Modal from "./Modal.vue";
 

// VARIABLES
const { xs,smAndDown,smAndUp, mdAndUp }   = useDisplay(); 
const theme             = useTheme();
const router            = useRouter();
const route             = useRoute(); 
const UserStore         = useUserStore(); 
const {account, darkmode, loggedIn}         = storeToRefs(UserStore);
const firstname         = ref("John");
const lastname          = ref("Doe");
const text              = ref("");
const value             = ref(1);
const menu              = ref(false);


// PROPS
const props = defineProps({
    active:{type:Boolean,default:false},
})

// WATCHERS
watch(darkmode,  (mode) => {
  theme.global.name.value = mode ?  'darkMode' : 'lightMode';
  localStorage.setItem("theme",mode ? 'darkMode' : 'lightMode');  
});


watch(()=> route.name,  (routename) => { 
  if(routename === "Home"){ value.value = 0 }
  if(routename === "Protected"){ value.value = 1 }
  if(routename === "Profile"){ value.value = 2 }  
});

// COMPUTED PROPERTIES
const fullname = computed(()=>{    
    return `${firstname.value} ${lastname.value}`;
});


// FUNCTIONS
onMounted(()=>{
    // console.log("TEMPLATE COMPONENT CREATED"); 
   
});

onBeforeMount(()=>{
  // SAVE THEME TO LOCALSTORAGE MAKING IT PERSIST BROWSER REFRESH

  if(!!account.value == false){
    UserStore.getAccount();
  }

  if(localStorage.getItem("theme") != null){
    theme.global.name.value = localStorage.getItem("theme");
    darkmode.value = theme.global.current.value.dark;
  }
  else{
    // localStorage.setItem("theme",theme.global.current.value.dark ? 'dark' : 'light');
    // darkmode.value = theme.global.current.value.dark;
    localStorage.setItem("theme",theme.global.current.value.dark ? 'darkMode' : 'lightMode');
    darkmode.value = theme.global.current.value.dark;    
  }  
});

const toTop =()=> {
        window.scrollTo({
          top: 0,
          behavior: "smooth"
        });
      }

const loginLogout = () => {
  if(loggedIn.value){
    menu.value = false; 
    UserStore.userLogout();
    toTop();
  }

  else{
    router.push({name:'Login'})
  }
}

</script>

<style>
/*   Style */

 
</style>