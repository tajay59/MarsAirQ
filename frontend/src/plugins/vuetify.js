/**
 * plugins/vuetify.js
 *
 * Framework documentation: https://vuetifyjs.com`
 */



// Styles 
import '@mdi/font/css/materialdesignicons.css' // Ensure you are using css-loader
import 'material-design-icons-iconfont/dist/material-design-icons.css' // Ensure your project 
import '@fortawesome/fontawesome-free/css/all.css' // Ensure your project is capable of 
import 'primeicons/primeicons.css'
import 'vuetify/styles' 
import { VStepperVertical, VStepperVerticalItem  } from 'vuetify/labs/VStepperVertical'

// SCSS Styles
// import '@/styles/main.scss'

import { md3 } from 'vuetify/blueprints' 
import { fa } from 'vuetify/iconsets/fa'
// import { mdi } from 'vuetify/iconsets/mdi'
import { aliases, mdi } from 'vuetify/iconsets/mdi-svg'
import {  md } from 'vuetify/iconsets/md' 


// Composables
import { createVuetify } from 'vuetify'

const lightMode = {
  dark: false,
  colors: {
    primary : "#335CA8",
    onPrimary : "#FFFFFF",
    primaryContainer : "#D8E2FF",
    onPrimaryContainer : "#001A42",
    secondary : "#0060AC",
    onSecondary : "#FFFFFF",
    secondaryContainer : "#D4E3FF",
    onSecondaryContainer : "#001C39",
    tertiary : "#715573",
    onTertiary : "#FFFFFF",
    tertiaryContainer : "#FCD7FB",
    onTertiaryContainer : "#2A132D",
    error : "#BA1A1A",
    errorContainer : "#FFDAD6",
    onError : "#FFFFFF",
    onErrorContainer : "#410002",
    background : "#FFFFFF", // "#FEFBFF"
    onBackground : "#1B1B1F",
    surface : "#FFFFFF", // #FEFBFF
    onSurface : "#1B1B1F",
    surfaceVariant : "#E1E2EC",
    onSurfaceVariant : "#44474F",
    outline : "#75777F",
    inverseOnSurface : "#F2F0F4",
    inverseSurface : "#303034",
    inversePrimary : "#AEC6FF",
    shadow : "#000000",
    surfaceTint : "#335CA8",
    outlineVariant : "#C5C6D0",
    scrim : "#000000"
  },
}

const darkMode = {
  dark: true,
  colors: {
    primary : "#AEC6FF",
    onPrimary : "#002E6B",
    primaryContainer : "#12448F",
    onPrimaryContainer : "#D8E2FF",
    secondary : "#A4C9FF",
    onSecondary : "#00315D",
    secondaryContainer : "#004883",
    onSecondaryContainer : "#D4E3FF",
    tertiary : "#DFBBDE",
    onTertiary : "#402843",
    tertiaryContainer : "#583E5A",
    onTertiaryContainer : "#FCD7FB",
    error : "#FFB4AB",
    errorContainer : "#93000A",
    onError : "#690005",
    onErrorContainer : "#FFDAD6",
    background : "#212121", //"#1B1B1F"
    onBackground : "#E3E2E6",
    surface : "#333333", // "#1B1B1F"
    onSurface : "#E3E2E6",
    surfaceVariant : "#44474F",
    onSurfaceVariant : "#C5C6D0",
    outline : "#8E9099",
    inverseOnSurface : "#1B1B1F",
    inverseSurface : "#E3E2E6",
    inversePrimary : "#335CA8",
    shadow : "#000000",
    surfaceTint : "#AEC6FF",
    outlineVariant : "#44474F",
    scrim : "#000000"
  },
}


/*
const darkMode  = {
  dark: true,
  colors : {}
}
*/
const light  = {
  dark: false,
  colors : {
    "primary": "#405F91",
    "surfaceTint": "#405F91",
    "onPrimary": "#FFFFFF",
    "primaryContainer": "#D6E3FF",
    "onPrimaryContainer": "#001B3E",
    "secondary": "#565F71",
    "onSecondary": "#FFFFFF",
    "secondaryContainer": "#DAE2F9",  
    "onSecondaryContainer": "#131C2B",
    "tertiary": "#6F5575",
    "onTertiary": "#FFFFFF",
    "tertiaryContainer": "#F9D8FD",
    "onTertiaryContainer": "#28132E",
    "error": "#BA1A1A",
    "onError": "#FFFFFF",
    "errorContainer": "#FFDAD6",
    "onErrorContainer": "#410002",
    "background": "#FFFFFF",
    "onBackground": "#191C20",
    "surface": "#FFFFFF",
    "onSurface": "#191C20",
    "surfaceVariant": "#E0E2EC",
    "onSurfaceVariant": "#44474E",
    "outline": "#74777F",
    "outlineVariant": "#C4C6D0",
    "shadow": "#000000",
    "scrim": "#000000",
    "inverseSurface": "#2E3036",
    "inverseOnSurface": "#F0F0F7",
    "inversePrimary": "#AAC7FF",
    "primaryFixed": "#D6E3FF",
    "onPrimaryFixed": "#001B3E",
    "primaryFixedDim": "#AAC7FF",
    "onPrimaryFixedVariant": "#274777",
    "secondaryFixed": "#DAE2F9",
    "onSecondaryFixed": "#131C2B",
    "secondaryFixedDim": "#BEC6DC",
    "onSecondaryFixedVariant": "#3E4759",
    "tertiaryFixed": "#F9D8FD",
    "onTertiaryFixed": "#28132E",
    "tertiaryFixedDim": "#DCBCE0",
    "onTertiaryFixedVariant": "#573E5C",
    "surfaceDim": "#D9D9E0",
    "surfaceBright": "#FFFFFF",
    "surfaceContainerLowest": "#FFFFFF",
    "surfaceContainerLow": "#F3F3FA",
    "surfaceContainer": "#EDEDF4",
    "surfaceContainerHigh": "#E7E8EE",
    "surfaceContainerHighest": "#E2E2E9"
  }
}

const lightMediumContrast  = {
  dark: false,
  colors : {
    "primary": "#234373",
    "surfaceTint": "#405F91",
    "onPrimary": "#FFFFFF",
    "primaryContainer": "#5775A8",
    "onPrimaryContainer": "#FFFFFF",
    "secondary": "#3A4354",
    "onSecondary": "#FFFFFF",
    "secondaryContainer": "#6C7588",
    "onSecondaryContainer": "#FFFFFF",
    "tertiary": "#523A58",
    "onTertiary": "#FFFFFF",
    "tertiaryContainer": "#876B8C",
    "onTertiaryContainer": "#FFFFFF",
    "error": "#8C0009",
    "onError": "#FFFFFF",
    "errorContainer": "#DA342E",
    "onErrorContainer": "#FFFFFF",
    "background": "#FFFFFF",
    "onBackground": "#191C20",
    "surface": "#FFFFFF",
    "onSurface": "#191C20",
    "surfaceVariant": "#E0E2EC",
    "onSurfaceVariant": "#40434A",
    "outline": "#5C5F67",
    "outlineVariant": "#787A83",
    "shadow": "#000000",
    "scrim": "#000000",
    "inverseSurface": "#2E3036",
    "inverseOnSurface": "#F0F0F7",
    "inversePrimary": "#AAC7FF",
    "primaryFixed": "#5775A8",
    "onPrimaryFixed": "#FFFFFF",
    "primaryFixedDim": "#3E5C8E",
    "onPrimaryFixedVariant": "#FFFFFF",
    "secondaryFixed": "#6C7588",
    "onSecondaryFixed": "#FFFFFF",
    "secondaryFixedDim": "#535C6F",
    "onSecondaryFixedVariant": "#FFFFFF",
    "tertiaryFixed": "#876B8C",
    "onTertiaryFixed": "#FFFFFF",
    "tertiaryFixedDim": "#6D5372",
    "onTertiaryFixedVariant": "#FFFFFF",
    "surfaceDim": "#D9D9E0",
    "surfaceBright": "#FFFFFF",
    "surfaceContainerLowest": "#FFFFFF",
    "surfaceContainerLow": "#F3F3FA",
    "surfaceContainer": "#EDEDF4",
    "surfaceContainerHigh": "#E7E8EE",
    "surfaceContainerHighest": "#E2E2E9"
  }
}

const lightHighContrast  = {
  dark: false,
  colors : {
    "primary": "#00214A",
    "surfaceTint": "#405F91",
    "onPrimary": "#FFFFFF",
    "primaryContainer": "#234373",
    "onPrimaryContainer": "#FFFFFF",
    "secondary": "#192232",
    "onSecondary": "#FFFFFF",
    "secondaryContainer": "#3A4354",
    "onSecondaryContainer": "#FFFFFF",
    "tertiary": "#2F1A35",
    "onTertiary": "#FFFFFF",
    "tertiaryContainer": "#523A58",
    "onTertiaryContainer": "#FFFFFF",
    "error": "#4E0002",
    "onError": "#FFFFFF",
    "errorContainer": "#8C0009",
    "onErrorContainer": "#FFFFFF",
    "background": "#FFFFFF",
    "onBackground": "#191C20",
    "surface": "#FFFFFF",
    "onSurface": "#000000",
    "surfaceVariant": "#E0E2EC",
    "onSurfaceVariant": "#21242B",
    "outline": "#40434A",
    "outlineVariant": "#40434A",
    "shadow": "#000000",
    "scrim": "#000000",
    "inverseSurface": "#2E3036",
    "inverseOnSurface": "#FFFFFF",
    "inversePrimary": "#E5ECFF",
    "primaryFixed": "#234373",
    "onPrimaryFixed": "#FFFFFF",
    "primaryFixedDim": "#032C5B",
    "onPrimaryFixedVariant": "#FFFFFF",
    "secondaryFixed": "#3A4354",
    "onSecondaryFixed": "#FFFFFF",
    "secondaryFixedDim": "#242D3D",
    "onSecondaryFixedVariant": "#FFFFFF",
    "tertiaryFixed": "#523A58",
    "onTertiaryFixed": "#FFFFFF",
    "tertiaryFixedDim": "#3B2441",
    "onTertiaryFixedVariant": "#FFFFFF",
    "surfaceDim": "#D9D9E0",
    "surfaceBright": "#FFFFFF",
    "surfaceContainerLowest": "#FFFFFF",
    "surfaceContainerLow": "#F3F3FA",
    "surfaceContainer": "#EDEDF4",
    "surfaceContainerHigh": "#E7E8EE",
    "surfaceContainerHighest": "#E2E2E9"
  }
}

const dark  = {
  dark: true,
  colors : {
    "primary": "#AAC7FF",
    "surfaceTint": "#AAC7FF",
    "onPrimary": "#0A305F",
    "primaryContainer": "#274777",
    "onPrimaryContainer": "#D6E3FF",
    "secondary": "#BEC6DC",
    "onSecondary": "#283141",
    "secondaryContainer": "#3E4759",  
    "onSecondaryContainer": "#DAE2F9",
    "tertiary": "#DCBCE0",
    "onTertiary": "#3F2844",
    "tertiaryContainer": "#573E5C",
    "onTertiaryContainer": "#F9D8FD",
    "error": "#FFB4AB",
    "onError": "#690005",
    "errorContainer": "#93000A",
    "onErrorContainer": "#FFDAD6",
    "background": "#111318",
    "onBackground": "#E2E2E9",
    "surface": "#111318",
    "onSurface": "#E2E2E9",
    "surfaceVariant": "#44474E",
    "onSurfaceVariant": "#C4C6D0",
    "outline": "#8E9099",
    "outlineVariant": "#44474E",
    "shadow": "#000000",
    "scrim": "#000000",
    "inverseSurface": "#E2E2E9",
    "inverseOnSurface": "#2E3036",
    "inversePrimary": "#405F91",
    "primaryFixed": "#D6E3FF",
    "onPrimaryFixed": "#001B3E",
    "primaryFixedDim": "#AAC7FF",
    "onPrimaryFixedVariant": "#274777",
    "secondaryFixed": "#DAE2F9",
    "onSecondaryFixed": "#131C2B",
    "secondaryFixedDim": "#BEC6DC",
    "onSecondaryFixedVariant": "#3E4759",
    "tertiaryFixed": "#F9D8FD",
    "onTertiaryFixed": "#28132E",
    "tertiaryFixedDim": "#DCBCE0",
    "onTertiaryFixedVariant": "#573E5C",
    "surfaceDim": "#111318",
    "surfaceBright": "#37393E",
    "surfaceContainerLowest": "#0C0E13",
    "surfaceContainerLow": "#191C20",
    "surfaceContainer": "#1D2024",
    "surfaceContainerHigh": "#282A2F",
    "surfaceContainerHighest": "#33353A"
  }
}

const darkMediumContrast  = {
  dark: true,
  colors : {
    "primary": "#B1CBFF",
    "surfaceTint": "#AAC7FF",
    "onPrimary": "#001634",
    "primaryContainer": "#7491C6",
    "onPrimaryContainer": "#000000",
    "secondary": "#C2CBE0",
    "onSecondary": "#0D1626",
    "secondaryContainer": "#8891A5",
    "onSecondaryContainer": "#000000",
    "tertiary": "#E1C0E5",
    "onTertiary": "#230E29",
    "tertiaryContainer": "#A487A9",
    "onTertiaryContainer": "#000000",
    "error": "#FFBAB1",
    "onError": "#370001",
    "errorContainer": "#FF5449",
    "onErrorContainer": "#000000",
    "background": "#111318",
    "onBackground": "#E2E2E9",
    "surface": "#111318",
    "onSurface": "#FBFAFF",
    "surfaceVariant": "#44474E",
    "onSurfaceVariant": "#C8CAD4",
    "outline": "#A0A3AC",
    "outlineVariant": "#80838C",
    "shadow": "#000000",
    "scrim": "#000000",
    "inverseSurface": "#E2E2E9",
    "inverseOnSurface": "#282A2F",
    "inversePrimary": "#284878",
    "primaryFixed": "#D6E3FF",
    "onPrimaryFixed": "#00112B",
    "primaryFixedDim": "#AAC7FF",
    "onPrimaryFixedVariant": "#133665",
    "secondaryFixed": "#DAE2F9",
    "onSecondaryFixed": "#081121",
    "secondaryFixedDim": "#BEC6DC",
    "onSecondaryFixedVariant": "#2D3647",
    "tertiaryFixed": "#F9D8FD",
    "onTertiaryFixed": "#1D0823",
    "tertiaryFixedDim": "#DCBCE0",
    "onTertiaryFixedVariant": "#452E4B",
    "surfaceDim": "#111318",
    "surfaceBright": "#37393E",
    "surfaceContainerLowest": "#0C0E13",
    "surfaceContainerLow": "#191C20",
    "surfaceContainer": "#1D2024",
    "surfaceContainerHigh": "#282A2F",
    "surfaceContainerHighest": "#33353A"
  }
}

const darkHighContrast  = {
  dark: true,
  colors : {
    "primary": "#FBFAFF",
    "surfaceTint": "#AAC7FF",
    "onPrimary": "#000000",
    "primaryContainer": "#B1CBFF",
    "onPrimaryContainer": "#000000",
    "secondary": "#FBFAFF",
    "onSecondary": "#000000",
    "secondaryContainer": "#C2CBE0",
    "onSecondaryContainer": "#000000",
    "tertiary": "#FFF9FA",
    "onTertiary": "#000000",
    "tertiaryContainer": "#E1C0E5",
    "onTertiaryContainer": "#000000",
    "error": "#FFF9F9",
    "onError": "#000000",
    "errorContainer": "#FFBAB1",
    "onErrorContainer": "#000000",
    "background": "#111318",
    "onBackground": "#E2E2E9",
    "surface": "#111318",
    "onSurface": "#FFFFFF",
    "surfaceVariant": "#44474E",
    "onSurfaceVariant": "#FBFAFF",
    "outline": "#C8CAD4",
    "outlineVariant": "#C8CAD4",
    "shadow": "#000000",
    "scrim": "#000000",
    "inverseSurface": "#E2E2E9",
    "inverseOnSurface": "#000000",
    "inversePrimary": "#002958",
    "primaryFixed": "#DDE7FF",
    "onPrimaryFixed": "#000000",
    "primaryFixedDim": "#B1CBFF",
    "onPrimaryFixedVariant": "#001634",
    "secondaryFixed": "#DEE7FD",
    "onSecondaryFixed": "#000000",
    "secondaryFixedDim": "#C2CBE0",
    "onSecondaryFixedVariant": "#0D1626",
    "tertiaryFixed": "#FCDDFF",
    "onTertiaryFixed": "#000000",
    "tertiaryFixedDim": "#E1C0E5",
    "onTertiaryFixedVariant": "#230E29",
    "surfaceDim": "#111318",
    "surfaceBright": "#37393E",
    "surfaceContainerLowest": "#0C0E13",
    "surfaceContainerLow": "#191C20",
    "surfaceContainer": "#1D2024",
    "surfaceContainerHigh": "#282A2F",
    "surfaceContainerHighest": "#33353A"
  }
}

// https://vuetifyjs.com/en/introduction/why-vuetify/#feature-guides
export default createVuetify({
  components: {
    VStepperVertical,VStepperVerticalItem
  },
  icons: {
    defaultSet: 'fa',
    aliases,
    sets: {
      fa,
      md,
      // mdi,
    },
  },
  blueprint: md3,
  theme: {
    defaultTheme: 'light',
    themes: {
      lightMode,
      light,
      lightMediumContrast,
      lightHighContrast,
      darkMode,
      dark,
      darkMediumContrast,
      darkHighContrast
    },
  } 
})
 

