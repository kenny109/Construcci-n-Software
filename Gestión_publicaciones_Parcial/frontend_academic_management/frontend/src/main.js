import Vue from 'vue'
import App from './App.vue'
import router from './router'
import { createPinia, PiniaVuePlugin } from 'pinia'
import './assets/main.css'

// Crear instancia de Vue 2
Vue.use(PiniaVuePlugin)

const pinia = createPinia()

new Vue({
  render: h => h(App),
  router,
  pinia
}).$mount('#app')
