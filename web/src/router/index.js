import Vue from 'vue'
import Router from 'vue-router'
import Dispatcher from '@/components/Dispatcher'
import Login from '@/components/Login'
import PageNotFound from '@/components/PageNotFound'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      redirect: { name: 'dispatch' }
    },
    {
      path: '/mmm',
      name: 'dispatch',
      component: Dispatcher
    },
    {
      path: '/who',
      name: 'login',
      component: Login
    },
    {
      path: '*',
      component: PageNotFound
    }
  ]
})
