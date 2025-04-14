/**
 * main.js
 *
 * Bootstraps Vuetify and other plugins then mounts the App`
 */

// Components
import App from './App.vue'; 
import ToastService from 'primevue/toastservice';
import Tooltip from 'primevue/tooltip';



// Composables
import { createApp } from 'vue'

// Plugins
import { registerPlugins } from '@/plugins';
import PrimeVue from 'primevue/config';
import Aura from '@primevue/themes/aura';

const app = createApp(App);
app.directive('tooltip', Tooltip);
app.use(ToastService);
app.use(PrimeVue, {
    // Default theme configuration
    theme: {
        preset: Aura,
        options: {
            darkModeSelector: '.dark', 
        }
    }
 });

registerPlugins(app);

app.mount('#app')
