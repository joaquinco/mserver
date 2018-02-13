import Vue from 'vue'
import Router from 'vue-router'
import Dispatcher from '@/components/Dispatcher'
import Vuex from 'vuex'

Vue.use(Router)
Vue.use(Vuex)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'Dispatcher',
      component: Dispatcher
    }
  ]
})
