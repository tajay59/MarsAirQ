/**
 * plugins/index.js
 *
 * Automatically included in `./src/main.js`
 */

// Plugins

import { loadFonts } from './webfontloader'
import vuetify from './vuetify'
// import pinia from '../store'
import { createPinia } from 'pinia'
import piniaPluginPersistedstate from "pinia-plugin-persistedstate";
import router from '../router'

const pinia = createPinia();
pinia.use(piniaPluginPersistedstate);


export function registerPlugins (app) {
  loadFonts()
  app
    .use(vuetify)
    .use(pinia)
    .use(router)
}
