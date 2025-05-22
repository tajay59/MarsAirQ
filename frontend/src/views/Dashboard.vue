<template>
    <VContainer fluid class=" scrolleffect " align="center"  > 
        <VRow  :justify="(smAndDown)? 'center':'start'"  align="start" class="bg- red gap-3 mt-5" style="max-width: 1500px; min-width: 250px; width: 100%;" >
            <VBtn   :aria-controls="menuId" height="40" title="Select Station" density="compact" color="transparent" border  @click="toggle" class="text-none !bg-neutral-100 dark:!bg-neutral-700 !text-neutral-700 dark:!text-neutral-200  !border-lime-700 dark:!border-lime-500 border-l-4" flat rounded="lg" variant="text" >
                <template #prepend >
                  <Icon icon="heroicons-solid:device-mobile" width="24" height="24"  />
                </template>
                <p v-if="stationName.length > 0" class="text-none text-xl font-normal" >{{ stationName}}</p>
                <p v-else class="text-none text-md font-medium" >Select Station </p>
            </VBtn>
            <TieredMenu ref="deviceMenu" :id="menuId" :model="menuItems" popup class="mt-2" >
                <template #item="{ item, props, hasSubmenu }">
                    <div  class="!grid !grid-cols-8" v-bind="props.action"> 
                        <div class="col-span-1">
                            <Icon :icon="item.icon" width="24" height="24"  />
                        </div>
                        <div class="col-span-5">
                            <span class="ml-2">{{ item.label }}</span>
                        </div>
                        <div class="col-span-1  flex place-content-center">
                            <Badge v-if="item.badge" class="ml-auto" :value="item.badge" />
                        </div>
                        <div class="col-span-1 flex place-content-center">
                            <i v-if="hasSubmenu" class="pi pi-angle-right ml-auto"></i>
                        </div>
                    </div>
                </template>
            </TieredMenu>       
        </VRow>

            
        <VRow  :justify="(smAndDown)? 'center':'start'"  align="start" class="gap-3 min-h-screen mt-15" style="max-width: 1500px; min-width: 250px; width: 100%;" > 
            <VSheet border class="!rounded-xl pa-5 min-h-screen w-full !bg-neutral-100 dark:!bg-neutral-700" color="transparent" >
                <div v-if="layout.dashboard.length > 0" class="flex gap-2 flex-wrap justify-center" >
                    <TransitionGroup name="lists" >
                        <VSheet v-for="(component, index) in componentsToRender" :key="component.key" color="transparent"  >
                            <component :is="component.type" v-bind="component.props" @delete="deleteComponent(component.key)" ></component>
                        </VSheet>   
                    </TransitionGroup>                
                </div>   
                
                <div v-else class="flex flex-col align-center justify-center  h-[100dvh] "  >
                    <VImg v-if="!darkmode" src="@/assets/logo6_light.png" width="290" max-height="150" class="mx-15" style=" cursor: pointer;" @click="router.push({name:'Home'})"  >
                        <template v-slot:placeholder>
                            <div class="d-flex align-center justify-center fill-height">
                                <VProgressCircular color="grey-lighten-4" indeterminate ></VProgressCircular>
                            </div>
                        </template>
                    </VImg>
                    <VImg v-else src="@/assets/logo6_white.png" width="290"  max-height="150" class="mx-15" style=" cursor: pointer;" @click="router.push({name:'Home'})"  >
                        <template v-slot:placeholder>
                            <div class="d-flex align-center justify-center fill-height">
                                <VProgressCircular color="grey-lighten-4" indeterminate ></VProgressCircular>
                            </div>
                        </template>
                    </VImg>
                    <p v-if="stationName.length > 0" class="text-none text-4xl font-bold !text-lime-700 dark:!text-lime-500 " >{{ stationName}}'s</p>
                    <p class="font-light  my-5 text-xl " >Dashboard is empty. </p>
                    <div>
                        <VSheet class="flex gap-3 align-center justify-center  rounded-lg my-3 pa-5" border width="200"  >
                            <span class="flex place-content-center" >Click</span>
                            <Icon  icon="gg:menu-grid-o" width="24" height="24" :class="[(route.path == '/analytics/map')?'!text-neutral-100':'!text-neutral-500 dark:!text-neutral-300']" /> 
                            <Icon  icon="garden:chevron-right-fill-12" width="12" height="12" :class="[(route.path == '/analytics/map')?'!text-neutral-100':'!text-neutral-500 dark:!text-neutral-300']" /> 
                            <Icon  icon="si:dashboard-customize-fill" width="24" height="24" :class="[(route.path == '/analytics/map')?'!text-neutral-100':'!text-neutral-500 dark:!text-neutral-300']" />
                        </VSheet>
                        <p class="!max-w-[230px] text-pretty my-3" >to add graphs to your dashboard. Whenever your finish </p>
                        <VSheet class="flex gap-3 align-center justify-center rounded-lg my-3 pa-5" border width="200"   >
                            <span class="flex place-content-center" >Click</span>
                            <Icon  icon="gg:menu-grid-o" width="24" height="24" :class="[(route.path == '/analytics/map')?'!text-neutral-100':'!text-neutral-500 dark:!text-neutral-300']" /> 
                            <Icon  icon="garden:chevron-right-fill-12" width="12" height="12" :class="[(route.path == '/analytics/map')?'!text-neutral-100':'!text-neutral-500 dark:!text-neutral-300']" /> 
                            <Icon  icon="fluent:save-arrow-right-24-filled" width="24" height="24" :class="[(route.path == '/analytics/map')?'!text-neutral-100':'!text-neutral-500 dark:!text-neutral-300']" />
                        </VSheet>
                       
                        <span>to save your dashboard</span>
                    </div>

                </div>
            
                <Drawer v-model:visible="dashboardMenu" header="Graphs"  >
                    <div class="scrolleffect  overflow-y-scroll overflow-x-clip flex flex-col  gap-3"> 
                        <Gauge displaymode @add="addComponent('gauge')"  :width="250" />
                        <SingleKPIGauge displaymode @add="addComponent('singlekpigauge')"  :width="250" />
                        <Compass displaymode @add="addComponent('compass')" :width="250" />                                   
                        <Temperatures displaymode @add="addComponent('temperatures')"  :width="250" />
                        <SolidGauge displaymode @add="addComponent('solidgauge')"  :width="250"  />
                        <KPIGauge displaymode @add="addComponent('kpigauge')"  :width="250"  />
                    </div>
                </Drawer> 
            </VSheet>          
        </VRow>
          
    </VContainer> 
</template>

<script setup>
/** JAVASCRIPT HERE */

// IMPORTS
import { ref,reactive, markRaw ,watch ,onMounted,onBeforeUnmount,computed, resolveComponent, shallowRef, onBeforeMount } from "vue";  
import { useRoute ,useRouter } from "vue-router";
import { useMqttStore } from "@/stores/mqttStore";
import { useAppStore } from "@/stores/appStore";
import { storeToRefs } from "pinia";
import { useUserStore } from "@/stores/userStore";
import { useDisplay } from 'vuetify';
import { useToast } from 'primevue/usetoast';

import { Icon } from "@iconify/vue";
import _ from "lodash";

import Gauge from "@/components/graphs/Gauge.vue";
import KPIGauge from "@/components/graphs/KPIGauge.vue";
import SingleKPIGauge from "@/components/graphs/SingleKPIGauge.vue";
import AllDailyGraphs from "@/components/graphs/AllDailyGraphs.vue";
import AllGraphs from "@/components/graphs/AllGraphs.vue";
import AllHourlyGraphs from "@/components/graphs/AllHourlyGraphs.vue";
import Compass from "@/components/graphs/Compass.vue";
import Windrose from "@/components/graphs/Windrose.vue";
import Temperatures from "@/components/graphs/Temperatures.vue";
import SolidGauge from "@/components/graphs/SolidGauge.vue";


markRaw(Gauge)
markRaw(SingleKPIGauge)
markRaw(Compass)
markRaw(Windrose)
markRaw(AllGraphs)
markRaw(Temperatures)
markRaw(SolidGauge) 
markRaw(KPIGauge)
// markRaw()


 
 
// VARIABLES
const { smAndDown }   = useDisplay();
const router          = useRouter();
const route           = useRoute();  
const Mqtt            = useMqttStore();
const AppStore        = useAppStore();
const UserStore       = useUserStore();
const toast           = useToast(); 
const {connected, payload, payloadTopic } = storeToRefs(Mqtt);  
const {dashboardMenu}  = storeToRefs(AppStore);
const {darkmode,userSites, selectedStation, layout} = storeToRefs(UserStore);
const deviceMenu = ref();
const menuId = ref(`container${_.random(0,100000)}`);

 

const items = ref([
    {
        label: 'File',
        icon: 'pi pi-file',
        items: [
            {
                label: 'New',
                icon: 'pi pi-plus',
                items: [ { label: 'Document', icon: 'pi pi-file' }, { label: 'Image', icon: 'pi pi-image' }, { label: 'Video', icon: 'pi pi-video' } ]
            },
            {
                label: 'Open',
                icon: 'pi pi-folder-open'
            },
            {
                label: 'Print',
                icon: 'pi pi-print'
            }
        ]
    },
    {
        label: 'Edit',
        icon: 'pi pi-file-edit',
        items: [
            {
                label: 'Copy',
                icon: 'pi pi-copy'
            },
            {
                label: 'Delete',
                icon: 'pi pi-times'
            }
        ]
    },
    {
        label: 'Search',
        icon: 'pi pi-search'
    },
    {
        separator: true
    },
    {
        label: 'Share',
        icon: 'pi pi-share-alt',
        items: [ { label: 'Slack', icon: 'pi pi-slack' }, { label: 'Whatsapp', icon: 'pi pi-whatsapp' } ]
    }
]);

 

const componentsToRender = ref([]) 


    // VERY IMPORTANT!!
    // graphs.value.forEach(graph => markRaw(graph))


// COMPUTED PROPERTIES 
const menuItems = computed(()=>{
    let list = [];
    userSites.value.forEach((site)=> {
        let devices = []
        let item = {"label": _.capitalize(site.name),"icon":"iconamoon:location-pin-duotone"}
        site.devices.forEach( device => devices.push({"icon": "heroicons-solid:device-mobile","label": device.name,command: ()=> {updateDash(site,device)}}));
        
        if(devices.length > 0){
            item["items"] = devices
        }
        item["badge"] = devices.length
        list.push(item);
    });

    return list
})

const stationName = computed(()=>{    
    let name = ""
    userSites.value.forEach((site)=> {
        site.devices.forEach( device => { 
            if(device.id == selectedStation.value){
                name = _.capitalize(device.name)
            }
        })
    })
    return name;
});


// WATCHERS
  
watch(payload, (data)=>{ 
  

}) 

// FUNCTIONS

const updateDash = (site,device) => {
    //site and device comes from UserStore.userSites
    selectedStation.value   = device.id; 
    layout.value.site       = site.id; 
    layout.value.device     = device.id, 
    layout.value.dashboard  = device.dashboard;   
    componentsToRender.value = [];  
    layout.value.dashboard.forEach( graph => { addComponentFromDashboard(graph.type,graph.param,graph.id)});    
}
 
const toggle = (event) => {
    deviceMenu.value.toggle(event);
};

const deleteComponent = (key) => { 
    componentsToRender.value = componentsToRender.value.filter( item => item.key !== key); 
}

/*
const addComponent = (name) => { 
    switch(name){
        case "gauge":
            componentsToRender.value.push({ type: Gauge, props: { param: 'default' }, key: `container${_.random(0,100000)}` });
            break; 
        case "singlekpigauge":
            componentsToRender.value.push({ type: SingleKPIGauge, props: { param: 'default' }, key: `container${_.random(0,100000)}` });
            break; 
        case "compass":
            componentsToRender.value.push({ type: Compass, props: { param: '' }, key: `container${_.random(0,100000)}` });
            break; 
        case "temperatures":
            componentsToRender.value.push({ type: Temperatures, props: { param: '' }, key: `container${_.random(0,100000)}` });
            break; 
        case "solidgauge":
            componentsToRender.value.push({ type: SolidGauge, props: { param: 'default' }, key: `container${_.random(0,100000)}` });
            break; 
        case "kpigauge":
            componentsToRender.value.push({ type: KPIGauge, props: { params: ['uva','uvb','uvc'] }, key: `container${_.random(0,100000)}` });
            break; 
        default:
            // Statements executed when none of the cases match the expression Temperatures
            break; 
    } 
}
*/

const addComponent = (name) => {  
    let id = `container${_.random(0,100000)}`;
    switch(name){
        case "gauge":            
            componentsToRender.value.push({ type: Gauge, props: { param: 'default', id: id }, key: id });
            toast.add({ severity: 'success', summary: 'Added', detail: 'Gauge added to Dashboard', life: 3000 }); 
            layout.value.dashboard.push({"type":"gauge", "param": "","id": id});
            break; 
        case "singlekpigauge":
            componentsToRender.value.push({ type: SingleKPIGauge, props: { param: 'default', id: id }, key: id });
            toast.add({ severity: 'success', summary: 'Added', detail: 'KPI Gauge added to Dashboard', life: 3000 }); 
            layout.value.dashboard.push({"type":"singlekpigauge", "param": "","id": id});
            break; 
        case "compass":
            componentsToRender.value.push({ type: Compass, props: { param: '', id: id }, key: id });
            toast.add({ severity: 'success', summary: 'Added', detail: 'compass added to Dashboard', life: 3000 }); 
            layout.value.dashboard.push({"type":"compass", "param": "","id": id});
            break; 
        case "temperatures":
            componentsToRender.value.push({ type: Temperatures, props: { param: '', id: id }, key: id });
            toast.add({ severity: 'success', summary: 'Added', detail: 'Graph added to Dashboard', life: 3000 });
            layout.value.dashboard.push({"type":"temperatures", "param": "","id": id});
            break; 
        case "solidgauge":
            componentsToRender.value.push({ type: SolidGauge, props: { param: 'default', id: id }, key: id });
            toast.add({ severity: 'success', summary: 'Added', detail: 'Solid Gauge added to Dashboard', life: 3000 }); 
            layout.value.dashboard.push({"type":"solidgauge", "param": "","id": id});
            break; 
        case "kpigauge":
            componentsToRender.value.push({ type: KPIGauge, props: { params: ['uva','uvb','uvc'], id: id }, key: id });
            toast.add({ severity: 'success', summary: 'Added', detail: 'Multi KPI Gauge added to Dashboard', life: 3000 }); 
            layout.value.dashboard.push({"type":"kpigauge", "param": "","id": id});
            break; 
        default:
            // Statements executed when none of the cases match the expression Temperatures
            toast.add({ severity: 'error', summary: 'Failed', detail: 'Unable to add Graph', life: 3000 });  
            break; 
    } 
}

const addComponentFromDashboard = (name,param,id) => {   
    switch(name){
        case "gauge":            
            componentsToRender.value.push({ type: Gauge, props: { param: param, id: id }, key: id });  
            break; 
        case "singlekpigauge":
            componentsToRender.value.push({ type: SingleKPIGauge, props: { param: param , id: id }, key: id }); 
            break; 
        case "compass":
            componentsToRender.value.push({ type: Compass, props: { param: '', id: id }, key: id }); 
            break; 
        case "temperatures":
            componentsToRender.value.push({ type: Temperatures, props: { param: '', id: id }, key: id }); 
            break; 
        case "solidgauge":
            componentsToRender.value.push({ type: SolidGauge, props: { param: param , id: id }, key: id }); 
            break; 
        case "kpigauge":
            componentsToRender.value.push({ type: KPIGauge, props: { params: ['uva','uvb','uvc'], id: id }, key: id }); 
            break; 
        default:
            // Statements executed when none of the cases match the expression Temperatures
            toast.add({ severity: 'error', summary: 'Failed', detail: 'Unable to add Graph', life: 3000 });  
            break; 
    } 
}

onBeforeMount(()=>{
    layout.value.dashboard.forEach( graph => { addComponentFromDashboard(graph.type,graph.param,graph.id)});
})


onMounted(()=>{
    // THIS FUNCTION IS CALLED AFTER THIS COMPONENT HAS BEEN MOUNTED    

    if(!Mqtt.isConnected) { 
      if(suball.value){
        Mqtt.subTo("/station/data/#");
      }
      else {
        if(!!mqtt_sub_credentials.value)
          Mqtt.subTo(mqtt_sub_credentials.value.topic);
      }
        Mqtt.connect();
    } 

});


onBeforeUnmount(()=>{
    // THIS FUNCTION IS CALLED RIGHT BEFORE THIS COMPONENT IS UNMOUNTED
    // Mqtt.unsubscribeAll();
});


</script>


<style >
/** CSS STYLE HERE */

.scrolleffect{
    overflow-y: scroll;
}

/* Hide scrollbar for Chrome, Safari and Opera */
.scrolleffect::-webkit-scrollbar {
    display: none;
}

/* Hide scrollbar for IE, Edge and Firefox */
.scrolleffect {
  -ms-overflow-style: none;  /* IE and Edge */
  scrollbar-width: none;  /* Firefox */
}

</style>
  