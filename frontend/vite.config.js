// Plugins
import vue from '@vitejs/plugin-vue'
import vuetify, { transformAssetUrls } from 'vite-plugin-vuetify'
import ViteFonts from 'unplugin-fonts/vite'
import Components from 'unplugin-vue-components/vite';
import {PrimeVueResolver} from '@primevue/auto-import-resolver';
import basicSsl from '@vitejs/plugin-basic-ssl'



// Utilities
import { defineConfig } from 'vite'
import { fileURLToPath, URL } from 'node:url'

// https://vitejs.dev/config/
export default defineConfig({ 

  plugins: [
    vue({ template: { transformAssetUrls } }), // https://github.com/vuetifyjs/vuetify-loader/tree/next/packages/vite-plugin
    vuetify({ autoImport: true, styles: { configFile: 'src/styles/settings.scss'}, }),   
    // basicSsl(),
    ViteFonts({
      google: {
        families: [{
          name: 'Roboto',
          styles: 'wght@100;300;400;500;700;900',
        }],
      },
    }),
    Components({
      resolvers: [ PrimeVueResolver() ]
    })
  ],
  define: { 'process.env': {} },
  resolve: {
    alias: { '@': fileURLToPath(new URL('./src', import.meta.url)) },
    extensions: [ '.js', '.json', '.jsx', '.mjs', '.ts', '.tsx', '.vue', ],
  },
 
  build: { outDir: '../dist' },
  server: {
    port: 3000,
    host:true, 
    headers:{'X-User':'internal'},
     proxy: {
    '^/api*': { 
      // target: 'http://192.168.1.28:8080/', 
      target: 'http://localhost:8080/',
     changeOrigin: false,
  },  // 'http://localhost:8080/'  http://192.168.0.203:443/
    
    }
    },
    base:"/"
  
})
