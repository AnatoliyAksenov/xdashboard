// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'

import Vuex from 'vuex'
import store from './state'

import VueMaterial from 'vue-material'
import 'vue-material/dist/vue-material.min.css'
//import 'vue-material/dist/theme/default-dark.css'
import 'vue-material/dist/theme/default.css'

Vue.config.productionTip = false

Vue.use(Vuex)
Vue.use(VueMaterial)

/* eslint-disable no-new */
new Vue({
    store,
    el: '#app',
    router,
    components: { App },
    template: '<App/>'
})