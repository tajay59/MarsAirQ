<template>
    <VContainer fluid class=" scrolleffect  " align="center"  >
        <VRow class="pa-0 gap-3"     justify="center">
            <VCard    density="compact" rounded="lg" width="200" border flat >
                <template #subtitle > <p class="font-medium" >PTB330</p> </template> 
                <VCardItem  class="py-1"   >                       
                    <VChip class="pa-4 w-100 bg-sky-900/[0.8] dark:bg-sky-300/[0.9]"   variant="flat" >
                        <span class="text-lg font-medium ml-1 " >{{ PTB330.pressure.toFixed(2) }} hPa</span>
                        <template #prepend>
                            <VIcon icon="mdi:mdi-gauge" size="24" />
                        </template>
                    </VChip> 
                </VCardItem>
            </VCard>

            <VCard   class="pb-3"  density="compact" rounded="lg" width="200" border flat  >  
                <template #subtitle > <p class="font-medium" >BMP390</p> </template>                
                <VCardItem  class="py-1"   >     
                    <VChip class="pa-4 w-100 " >
                        <span class="text-lg font-medium ml-1 " >{{ BMP390.pressure.toFixed(2) }} hPa</span>
                        <template #prepend>
                            <VIcon icon="mdi:mdi-gauge" size="24" />
                        </template>
                    </VChip> 
                </VCardItem>
                <VCardItem class="py-1"  >     
                    <VChip class="pa-4  w-100 " >
                        <p class="text-lg font-medium ml-1" >{{ BMP390.temperature.toFixed(2) }} °C</p>
                        <template #prepend>
                            <VIcon icon="mdi:mdi-thermometer" size="24" />
                        </template>
                    </VChip> 
                </VCardItem>
                <VCardItem  class="py-1"   >     
                    <VChip class="pa-4 w-100 " >
                        <span class="text-lg font-medium ml-1 " >{{ BMP390.altitude.toFixed(2) }} ft</span>
                        <template #prepend>
                            <VIcon icon="mdi:mdi-altitude" size="24" />
                        </template>
                    </VChip> 
                </VCardItem>

            </VCard>

            <VDivider vertical thickness="2" class="mx-2" /> 

            <VCard  density="compact" rounded="lg" width="200" border flat  >    
                <template #subtitle > <p class="font-medium" >HMP75</p> </template>         
                <VCardItem class="py-1"  >     
                    <VChip class="pa-4  w-100  bg-sky-900/[0.8] dark:bg-sky-300/[0.9]"  variant="flat"  >
                        <p class="text-lg font-medium ml-1" >{{ HMP75.temperature.toFixed(2) }} °C</p>
                        <template #prepend>
                            <VIcon icon="mdi:mdi-thermometer" size="24" />
                        </template>
                    </VChip> 
                </VCardItem>
                <VCardItem  class="py-1"   >     
                    <VChip class="pa-4 w-100  bg-sky-900/[0.8] dark:bg-sky-300/[0.9]"  variant="flat"  >
                        <span class="text-lg font-medium ml-1 " >{{ HMP75.humidity.toFixed(2) }} %</span>
                        <template #prepend>
                            <VIcon icon="mdi:mdi-water-percent" size="24" />
                        </template>
                    </VChip> 
                </VCardItem>
            </VCard>

            <VCard density="compact" rounded="lg" width="200" border flat  >   
                <template #subtitle > <p class="font-medium" >SHT45</p> </template>    
                <VCardItem class="py-1"  >     
                    <VChip class="pa-4  w-100 " >
                        <p class="text-lg font-medium ml-1" >{{ SHT45.temperature.toFixed(2) }} °C</p>
                        <template #prepend>
                            <VIcon icon="mdi:mdi-thermometer" size="24" />
                        </template>
                    </VChip> 
                </VCardItem>
                <VCardItem  class="py-1"   >     
                    <VChip class="pa-4 w-100 " >
                        <span class="text-lg font-medium ml-1 " >{{ SHT45.humidity.toFixed(2) }} %</span>
                        <template #prepend>
                            <VIcon icon="mdi:mdi-water-percent" size="24" />
                        </template>
                    </VChip> 
                </VCardItem>
            </VCard>
            
            <VCard  density="compact" rounded="lg" width="200" border flat  >  
                <template #subtitle > <p class="font-medium" >MCP9808 </p> </template>     
                <VCardItem class="py-1"  >     
                    <VChip class="pa-4  w-100 " >
                        <p class="text-lg font-medium ml-1" >{{ MCP9808.temperature.toFixed(2) }} °C</p>
                        <template #prepend>
                            <VIcon icon="mdi:mdi-thermometer" size="24" />
                        </template>
                    </VChip> 
                </VCardItem> 
            </VCard>            
        </VRow>

        <VRow class="pa-0 gap-3 mt-15"     justify="center">
            <VCard class="pb-3"   density="compact" rounded="lg" width="220" border flat >
                <template #subtitle ><span class="font-medium" > </span>  <VIcon icon="mdi:mdi-gauge" size="32" /></template> 
                <VCardItem  class="py-1"   >                     
                    <VChip class="pa-4 w-100 bg-sky-900/[0.8] dark:bg-sky-300/[0.9]"   variant="flat"  >
                        <span class="text-lg font-medium ml-1 " >{{ PTB330.pressure.toFixed(2) }} hPa</span>
                        <template #prepend> 
                            <p class="text-xs text-left font-bold mr-3" >PTB330</p>  
                        </template>
                    </VChip> 
                </VCardItem>
                <VCardItem  class="py-1"   >                     
                    <VChip class="pa-4 w-100 "      >
                        <span class="text-md font-medium ml-1 " >{{ BMP390.pressure.toFixed(2) }} hPa</span>
                        <template #prepend> 
                            <p class="text-xs text-left font-bold mr-3" >BMP390</p>  
                        </template>
                    </VChip> 
                </VCardItem>

                <VDivider class="my-1" />

                <VCardItem  class="py-1"   >                     
                    <VChip class="pa-4 w-100 bg-rose-800/[0.8] dark:bg-rose-300/[0.9]"   variant="flat"   >
                        <span class="text-lg font-medium ml-1 " >{{ pressureDifference.toFixed(2) }} hPa</span>
                        <template #prepend> 
                            <p class="text-xs text-left font-bold mr-3" >Diff</p>  
                        </template>
                    </VChip> 
                </VCardItem>
            </VCard>

            <VCard   class="pb-3"  density="compact" rounded="lg" width="200" border flat  >  
                <template #subtitle > <span class="font-medium" ></span>  <VIcon icon="mdi:mdi-thermometer" size="32" /></template>     
                <VCardItem  class="py-1"   >                     
                    <VChip class="pa-4 w-100 bg-sky-900/[0.8] dark:bg-sky-300/[0.9]"   variant="flat"  >
                        <span class="text-lg font-medium ml-1 " >{{ HMP75.temperature.toFixed(2) }} °C</span>
                        <template #prepend> 
                            <p class="text-xs text-left font-bold mr-3" >HMP75</p>  
                        </template>
                    </VChip> 
                </VCardItem>   
                <VCardItem  class="py-1"   >                     
                    <VChip class="pa-4 w-100 "     >
                        <span class="text-md font-medium ml-1 " >{{ MCP9808.temperature.toFixed(2) }} °C</span>
                        <template #prepend> 
                            <p class="text-xs text-left font-bold mr-1" >MCP9808</p>  
                        </template>
                    </VChip> 
                </VCardItem>  
                <VCardItem  class="py-1"   >                     
                    <VChip class="pa-4 w-100 "     >
                        <span class="text-md font-medium ml-1 " >{{ SHT45.temperature.toFixed(2) }} °C</span>
                        <template #prepend> 
                            <p class="text-xs text-left font-bold mr-3" >SHT45</p>  
                        </template>
                    </VChip> 
                </VCardItem>   
                <VCardItem  class="py-1"   >                     
                    <VChip class="pa-4 w-100 "    >
                        <span class="text-md font-medium ml-1 " >{{ BMP390.temperature.toFixed(2) }} °C</span>
                        <template #prepend> 
                            <p class="text-xs text-left font-bold mr-3" >BMP390</p>  
                        </template>
                    </VChip> 
                </VCardItem> 

                <VDivider class="my-1" />

                <VCardItem  class="py-1"   >                     
                    <VChip class="pa-4 w-100 bg-rose-800/[0.8] dark:bg-rose-300/[0.9]"   variant="flat"   >
                        <span class="text-lg font-medium ml-1 " >{{ temperatureDifference.toFixed(2) }} °C</span>
                        <template #prepend> 
                            <p class="text-xs text-left font-bold mr-3" >Diff</p>  
                        </template>
                    </VChip> 
                </VCardItem>

            </VCard>

            <VCard   class="pb-3"  density="compact" rounded="lg" width="200" border flat  >  
                <template #subtitle > <span class="font-medium" ></span> <VIcon icon="mdi:mdi-water-percent" size="32" /></template>     
                <VCardItem  class="py-1"   >                     
                    <VChip class="pa-4 w-100 bg-sky-900/[0.8] dark:bg-sky-300/[0.9]"   variant="flat"  >
                        <span class="text-lg font-medium ml-1 " >{{ HMP75.humidity.toFixed(2) }} %</span>
                        <template #prepend> 
                            <p class="text-xs text-left font-bold mr-3" >HMP75</p>  
                        </template>
                    </VChip> 
                </VCardItem>   
                <VCardItem  class="py-1"   >                     
                    <VChip class="pa-4 w-100 "    >
                        <span class="text-md font-medium ml-1 " >{{ SHT45.humidity.toFixed(2) }} %</span>
                        <template #prepend> 
                            <p class="text-xs text-left font-bold mr-1" >SHT45</p>  
                        </template>
                    </VChip> 
                </VCardItem>  

                <VDivider class="my-1" />

                <VCardItem  class="py-1"   >                     
                    <VChip class="pa-4 w-100 bg-rose-800/[0.8] dark:bg-rose-300/[0.9]"   variant="flat"   >
                        <span class="text-lg font-medium ml-1 " >{{ humidityDifference.toFixed(2) }} %</span>
                        <template #prepend> 
                            <p class="text-xs text-left font-bold mr-3" >Diff</p>  
                        </template>
                    </VChip> 
                </VCardItem>

            </VCard>

                     
        </VRow>
       
    </VContainer> 
</template>

<script setup>
/** JAVASCRIPT HERE */

// IMPORTS
import { ref,reactive,watch ,onMounted,onBeforeUnmount,computed } from "vue";  
import { useRoute ,useRouter } from "vue-router";
import { useMqttStore } from "@/stores/mqttStore";
import { storeToRefs } from "pinia";
import { useDisplay } from 'vuetify'
 
 
// VARIABLES
const { smAndDown }   = useDisplay();
const router                    = useRouter();
const route                     = useRoute();  
const Mqtt                      = useMqttStore();
const {connected, payload, payloadTopic } = storeToRefs(Mqtt);

const frontdoor                 = ref(1);
const sidedoor                  = ref(1);
const burglarBar                = ref(1);
const brightness                = ref(50);

const selectedColor             = reactive({"color":{"r":0,"g":0,"b":0,"a":0}}); 
const temperature               = ref(0);
const humidity                  = ref(0);

const laundryroom               = ref(0);
const miniroom                  = ref(0);
const kitchen                   = ref(0);
const minibathroom              = ref(0);
const masterbathroom            = ref(0);

// Sensors
const BMP390             = reactive({"temperature": 0, "pressure": 0, "altitude": 0}); 
const PTB330             = reactive({"temperature": 0, "pressure": 0}); 
const HMP75              = reactive({"temperature": 0, "humidity": 0}); 
const SHT45              = reactive({"temperature": 0, "humidity": 0}); 
const MCP9808            = reactive({"temperature": 0}); 



// COMPUTED PROPERTIES
const pressureDifference = computed(()=>{
    return BMP390.pressure - PTB330.pressure;   
});

const temperatureDifference = computed(()=>{
    return MCP9808.temperature - HMP75.temperature;   
});

const humidityDifference = computed(()=>{
    return HMP75.humidity - SHT45.humidity;   
});

// WATCHERS
 watch(selectedColor,(data)=>{ 
    let message = JSON.stringify({"type":"led","color": data.color}); // Create message and convert to a json string
  Mqtt.publish("620085969_sub",message);  // Publish message to appropriate topic  
})
 

 
watch(payload,(data)=>{ 
  
    if(data.model == "PTB330"){   
        PTB330.pressure  = data.pressure;
        }

    if(data.model == "BMP390"){     
        BMP390.pressure = data.pressure;
        BMP390.temperature = data.temperature;  
        BMP390.altitude = data.alt;
    }

    if(data.model == "HMP75"){        
        HMP75.temperature = data.temperature;  
        HMP75.humidity = data.humidity;       
    }

    if(data.model == "SHT45"){        
        SHT45.temperature = data.temperature;  
        SHT45.humidity = data.humidity;       
    }

    if(data.model == "MCP9808"){        
        MCP9808.temperature = data.temperature;       
    }
    
    

}) 

// FUNCTIONS
onMounted(()=>{
    // THIS FUNCTION IS CALLED AFTER THIS COMPONENT HAS BEEN MOUNTED
    /*
    Mqtt.connect(); // Connect to Broker located on the backend
    setTimeout( ()=>{
    // Subscribe to each topic
    Mqtt.subscribe("/devices");
    Mqtt.subscribe("/references");
    },3000);
*/

});


onBeforeUnmount(()=>{
    // THIS FUNCTION IS CALLED RIGHT BEFORE THIS COMPONENT IS UNMOUNTED
    // Mqtt.unsubscribeAll();
});



const toggle = (name) => {
  let message = JSON.stringify({"type":"toggle","device": name}); // Create message and convert to a json string
  Mqtt.publish("620085969_sub",message);  // Publish message to appropriate topic  
}

</script>


<style scoped>
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
  