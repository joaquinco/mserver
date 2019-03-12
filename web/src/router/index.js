import Vue from 'vue'
import Router from 'vue-router'
import Dispatcher from '@/pages/Dispatcher'
import Login from '@/pages/Login'
import PageNotFound from '@/pages/PageNotFound'
import Player from '@/pages/Player'
import Search from '@/pages/Search'
import Configuration from '@/pages/Configuration'

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
      path: '/player',
      name: 'player',
      component: Player
    },
    {
      path: '/search',
      name: 'search',
      component: Search
    },
    {
      path: '/config',
      name: 'configuration',
      component: Configuration
    },
    {
      path: '*',
      component: PageNotFound
    }
  ]
})
