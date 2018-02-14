import Vue from 'vue'
import Router from 'vue-router'
import Dispatcher from '@/components/Dispatcher'
import Login from '@/components/Login'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'dispatch',
      component: Dispatcher
    },
    {
      path: '/who',
      name: 'login',
      component: Login
    }
  ]
})
