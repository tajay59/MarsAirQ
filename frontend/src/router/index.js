// Composables
import { createRouter, createWebHistory } from 'vue-router';
import { useUserStore } from '@/stores/userStore';
import { useModalStore } from '@/stores/modalStore';

//FUNCTIONS

// Analytics.vue

const routes = [
  { path: '/', name: 'Home', component: () => import('@/views/Home.vue'), meta:{ resquiresAuth: false, transition: 'fade'} },
  { path: '/research', name: 'Research', component: () => import('@/components/Research.vue'), meta:{ resquiresAuth: true, transition: 'fade'} }, 
  { path: '/admin', name: 'Admin', component: () => import('@/views/Admin.vue'), 
    meta:{ resquiresAuth: true, transition: 'fade'},
    children: [
      { path: 'accounts', name: 'Accounts', component: () => import('@/components/admin/AccountsMain.vue'), meta:{ resquiresAuth: true, transition: 'fade'} },
      { path: 'sites', name: 'Sites', component: () => import('@/components/admin/Sites.vue'), meta:{ resquiresAuth: true, transition: 'fade'} },
      { path: 'emails', name: 'Emails', component: () => import('@/components/admin/Emails.vue'), meta:{ resquiresAuth: true, transition: 'fade'} }
     ] },
  { path: '/admin/sites/:id', name: "Site", component: () => import('@/components/admin/Site.vue'), meta:{ resquiresAuth: true, transition: 'fade'} },
  { path: '/analytics', name: 'Analytics',
     component: () => import('@/components/Analytics.vue'), 
     meta:{ resquiresAuth: true, transition: 'fade'},
     children: [
      { path: 'map', name: 'Map', component: () => import('@/views/Map.vue'), meta:{ resquiresAuth: true, transition: 'fade'} },
      { path: 'live', name: 'Live', component: () => import('@/views/Live.vue'), meta:{resquiresAuth: true,  transition: 'fade'} }, 
      { path: 'dashboard', name: 'Dashboard', component: () => import('@/views/Dashboard.vue'), meta:{ resquiresAuth: true, transition: 'fade'} }, 
      { path: 'analysis', name: 'Analysis', component: () => import('@/views/Analysis.vue'), meta:{resquiresAuth: true,  transition: 'fade'} }, 
     ]
     },
  
  { path: '/login', name: 'Login', component: () => import('@/views/Login.vue'), },
  { path: '/signup', name: 'Signup', component: () => import('@/views/Signup.vue'), }, 
  { path: '/pr', name: 'PasswordReset', component: () => import('@/views/PasswordReset.vue'), meta:{ transition: 'fade'} },  
  { path: '/profile', name: 'Profile', component: () => import('@/components/Profile.vue'), meta:{ resquiresAuth: true, transition: 'fade'} },  
  /*
  {
    path: '/',
    component: () => import('@/layouts/default/Default.vue'),
    children: [
      {
        path: '',
        name: 'Home',
        // route level code-splitting
        // this generates a separate chunk (about.[hash].js) for this route
        // which is lazy-loaded when the route is visited.
        component: () => import( '@/views/Home.vue'), // webpackChunkName: "home" 
      },
    ],
  },*/
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
})

// ROUTE GUARD
router.beforeEach( async (to, from)=>{
  // Global navigation guard. This code will run each time a user try to access a route
  // Every time a route changes in the application , this function is fired
  // console.log("from ",from)
  const UserStore         = useUserStore(); 
  // csrf_access_token=eede34a2-6188-4299-8ddc-c1d599f58cbb; csrf_refresh_token=e388423a-7310-4103-8afd-1a7710a2df45
  if(to.meta.resquiresAuth ) {
    // Need to loggin if not already logged in 
    //[UserStore.loggedIn,UserStore.role,UserStore.user,UserStore.id] = await Auth();     
    
    const cookies = document.cookie
    UserStore.loggedIn = (cookies.includes("csrf_access_token=") && cookies.includes("csrf_refresh_token=")) ? true : false;
    // console.log(`AUTH : ${UserStore.loggedIn}  ROLE : ${UserStore.role}`)

    if(to.name !== 'Login' && !UserStore.loggedIn){ 
      // console.log(" USER NOT LOGGED IN "); 
      UserStore.loggedIn  = false;
      UserStore.user      = "";
      UserStore.role      = "user";
      UserStore.email     = "";
      UserStore.id        = ""; 
      return { name:"Login", query: { redirect: to.fullPath } }; 
    }
   if(to.name === 'Orderplaced' && from.name !== 'Cart'){ 
      // console.log(" Orderplaced must only be accessed from Cart route ");  
      return {path: from.fullPath , query: { redirect: from.fullPath } }; 
    }
    
      
      /*
      {
      // console.log("USER ALREADY LOGGEDIN");
      let restrictedRoutes = ['/stow','/pick','/inventory','/orders'];
      // console.log("FULL PATH ",to.fullPath);
      if(restrictedRoutes.includes(to.fullPath) && UserStore.role !== 'staff'){
         console.log("RESTRICTED ACCESS");
        router.push( from.fullPath);
      } 
    }*/
        
  }
  else {
    //  AUTH NOT REQUIRED FOR THESE ROUTES
   if (to.name == 'Login' && UserStore.loggedIn){
      console.log("ALREADY LOGGED IN")
      return  {name:"Home", query: { redirect: to.fullPath }, replace: true }; 
    } 
  }
 

});

export default router
