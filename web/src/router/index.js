import Vue from 'vue'
import Router from 'vue-router'
import Dispatcher from '@/components/Dispatcher'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'dispatch',
      component: Dispatcher
    }
  ]
})
