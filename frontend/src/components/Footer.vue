<template>
    <VContainer class="bg-background pa-3 mb-15 " fluid align="center"   >
        
        <VRow><VDivider thickness="1" /></VRow>
        <VRow style="max-width: 1300px; width: 100%;" :class="[(smAndDown)? 'pa-5':'','mb-15']"  >
            <VCol :cols="(smAndDown)?'12':'3'" align="left" > 
                <p class="roboto-bold mt-10">THE CARIBBEAN INSTITUTE FOR METEOROLOGY AND HYDROLOGY</p> 
                <address class="text-caption my-5 text-medium-emphasis">
                    Husbands <br>
                    St James <br>
                    Barbados BB23006 <br>
                </address>
                <p class="roboto-bold">CONTACT</p> 
                <p class=" text-medium-emphasis" style="font-size: 12px;">Tel :    +1 (246) 425 1362/63</p> 
                <p class=" text-medium-emphasis" style="font-size: 12px;">Fax:    +1 (246) 424 4733</p> 
                <p class=" text-medium-emphasis" style="font-size: 12px;">Email: info@cimh.edu.bb</p> 
                <p class=" text-medium-emphasis" style="font-size: 12px;">Website: <VBtn text="CIMH" href="https://cimh.edu.bb/" target="_blank" variant="plain" rounded="lg" class="text-caption my-2" density="compact" append-icon="mdi:mdi-open-in-new"> </VBtn></p> 
                  <!-- <a href="https://cimh.edu.bb/" target="_blank" class="bg-red" >Website</a> -->
                
            </VCol>

            <VCol :cols="(smAndDown)?'12':'2'"  align="left">
                <p class="text-subtitle-1  font-weight-bold mt-10">STAY CONNECTED</p> 
                <p class=" text-medium-emphasis" style="font-size: 12px;">Follow us on these networks:</p> 
                <VRow class="my-2 mx-0">
                    <VBtn variant="plain"    density="compact" icon="mdi:mdi-facebook" target="_blank" href="http://facebook.com/CIMHbb"></VBtn>
                    <VBtn variant="plain"    density="compact" icon="mdi:mdi-twitter"  target="_blank" href="http://twitter.com/CIMHbb"></VBtn>
                    <VBtn variant="plain"    density="compact" icon="mdi:mdi-linkedin" target="_blank" href="https://www.linkedin.com/pub/cimh-barbados/a5/104/15b/en"></VBtn>
                    <VBtn variant="plain"    density="compact" icon="mdi:mdi-vimeo"    target="_blank" href="http://vimeo.com/cimhtv"></VBtn>
                    <VBtn variant="plain"    density="compact" icon="mdi:mdi-youtube"  target="_blank" href="https://www.youtube.com/user/CIMHTV"></VBtn>
                    <VBtn variant="plain"    density="compact" icon="mdi:mdi-skype"    target="_blank" href="skype:cimhbb?chat"></VBtn>
                </VRow>
                 
                <p class="roboto-bold mt-10">WRITE TO US</p> 
                <p class=" text-medium-emphasis" style="font-size: 12px;">P.O. Box 130</p> 
                <p class=" text-medium-emphasis" style="font-size: 12px;">Bridgetown</p> 
                <p class=" text-medium-emphasis" style="font-size: 12px;">Barbados</p> 
            </VCol>

            <VCol :cols="(smAndDown)?'12':'3'"  align="left"  class="d-flex flex-column"> 
                <p class="roboto-bold mt-10 mb-5">HYDROLOGICAL & METEOROLOGICAL SERVICES</p> 
                 
                 
                <VChip variant="text" color="primary" class="text-caption pa-0" text="Antigua and Barbuda"   density="compact"     target="_blank" href="http://www.antiguamet.com/"  ></VChip>
                <VChip variant="text" color="primary" class="text-caption pa-0" text="Barbados"              density="compact"     target="_blank" href="http://www.barbadosweather.org/"   ></VChip>
                <VChip variant="text" color="primary" class="text-caption pa-0" text="Belize"                density="compact"     target="_blank" href="http://www.hydromet.gov.bz/"  ></VChip>
                <VChip variant="text" color="primary" class="text-caption pa-0" text="Cayman Islands"        density="compact"     target="_blank" href="http://www.weather.gov.ky/portal/page?_pageid=4421,1&_dad=portal&_schema=PORTAL"    ></VChip>
                <VChip variant="text" color="primary" class="text-caption pa-0" text="Dominica"              density="compact"     target="_blank" href="http://www.weather.gov.dm/"   ></VChip>
                <VChip variant="text" color="primary" class="text-caption pa-0" text="French Antilles"       density="compact"     target="_blank" href="http://www.meteofrance.gp/previsions-meteo-antilles-guyane/animation/radar/antilles"  ></VChip>
                <VChip variant="text" color="primary" class="text-caption pa-0" text="Guyana"                density="compact"     target="_blank" href="http://www.hydromet.gov.gy/"  ></VChip>
                <VChip variant="text" color="primary" class="text-caption pa-0" text="Jamaica: Hydro"        density="compact"     target="_blank" href="http://waterresourcesauthority.com/"  ></VChip>
                <VChip variant="text" color="primary" class="text-caption pa-0" text="Jamaica: Met"          density="compact"     target="_blank" href="http://www.metservice.gov.jm/"  ></VChip>
                <VChip variant="text" color="primary" class="text-caption pa-0" text="St. Kitts and Nevis"   density="compact"     target="_blank" href="http://www.weather.kn/"  ></VChip>
                <VChip variant="text" color="primary" class="text-caption pa-0" text="St. Lucia"             density="compact"     target="_blank" href="http://www.slumet.gov.lc/"  ></VChip>
                <VChip variant="text" color="primary" class="text-caption pa-0" text="Trinidad & Tobago"     density="compact"     target="_blank" href="http://www.metoffice.gov.tt/"  ></VChip>
                <!-- <VBtn variant="plain" class="text-caption" text=""   density="compact"     target="_blank" href=""></VBtn> -->
                            
            </VCol>

            <VCol :cols="(smAndDown)?'12':'4'"  align="left"  class="d-flex flex-column"> 
                <p class="roboto-bold mt-10 mb-5">OTHER RESOURCES</p> 
                 
                 <VChip  variant="text" color="primary" class="text-caption  pa-0"  density="compact" target="_blank" href="http://bb02.cimafoundation.org:8080/dewetra/" style="font-size: 5px;"> DEWETRA </VChip>
                 <VChip  variant="text" color="primary" class="text-caption pa-0"   density="compact" target="_blank" href="http://sigma.cptec.inpe.br/scope/"> SCOPE - Nowcasting  </VChip>
                 <VChip  variant="text" color="primary" class="text-caption pa-0"   density="compact" target="_blank" href="http://www.cdema.org/"> CDEMA  </VChip>
                 <VChip  variant="text" color="primary" class="text-caption pa-0"   density="compact" target="_blank" href="http://rammb.cira.colostate.edu/ramsdis/online/rmtc.asp#Sector"> RAMSDIS  </VChip>
                 <VChip  variant="text" color="primary" class="text-caption pa-0"   density="compact" target="_blank" href="http://www.star.nesdis.noaa.gov/smcd/emb/ff/HE_CA_3Hour.php"> Center for Satellite Applications and Research (STAR)  </VChip>
                 <VChip  variant="text" color="primary" class="text-caption pa-0"   density="compact" target="_blank" href="http://www.ncep.noaa.gov/"> National Centers for Environmental Prediction (NCEP)  </VChip>
                 <VChip  variant="text" color="primary" class="text-caption pa-0"   density="compact" target="_blank" href="http://www.hpc.ncep.noaa.gov/"> Hydrometeorological Prediction Center (HPC)  </VChip>  
                 <VChip  variant="text" color="primary" class="text-caption pa-0"   density="compact" target="_blank" href="http://www.nhc.noaa.gov/"> Tropical Prediction Center/National Hurricane Center (TPC/NHC)</VChip> 
                 <VChip  variant="text" color="primary" class="text-caption pa-0"   density="compact" target="_blank" href="http://weather.unisys.com/"> Unisys Weather  </VChip> 
            </VCol>
        </VRow>
    </VContainer>     
    </template>
    
    <script setup>
    // IMPORTS 
   
 
    import { useUserStore} from '@/stores/userStore';
    import { ref,watch ,onMounted,computed } from "vue";  
    import { RouterLink, useRouter } from "vue-router";
    import { useDisplay } from 'vuetify';
    
    // VARIABLES
    const { xs,smAndDown,smAndUp, mdAndUp }   = useDisplay(); 
    const route             = useRouter(); 
    const UserStore         = useUserStore();
    const firstname         = ref("John");
    const lastname          = ref("Doe");
    const text              = ref("");
    const changedText       = ref("");
    
    
    // PROPS
    const props = defineProps({
        item:{type:String,default:""},
    })
    
    // WATCHERS
    watch(text,  (newText, oldText) => {
      console.log(newText); 
      changedText.value = newText ;
    });
    
    // COMPUTED PROPERTIES
    const fullname = computed(()=>{    
        return `${firstname.value} ${lastname.value}`;
    });
    
    
    // FUNCTIONS
    onMounted(()=>{
        // console.log("TEMPLATE COMPONENT CREATED");
        
    })
    
    
    </script>
    
    <style>
    /*   Style */
    a{
        text-decoration: none;
    }
    
    a:hover{
        text-decoration:underline;
    }
     
    </style>