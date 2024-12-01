import { createApp } from 'vue'
import App from './App.vue'
import './assets/style.css'
import 'bootstrap'
import 'bootstrap/dist/css/bootstrap.min.css'
import router from './router'
import store from './store.js'

createApp(App).use(router).use(store).mount('#app') 
