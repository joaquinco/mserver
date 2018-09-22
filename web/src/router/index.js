import Vue from 'vue'
import Router from 'vue-router'
import Dispatcher from '@/components/Dispatcher'
import Login from '@/components/Login'
import PageNotFound from '@/components/PageNotFound'
import Player from '@/components/Player'
import SearchPage from '@/components/SearchPage'

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
      component: SearchPage
    },
    {
      path: '*',
      component: PageNotFound
    }
  ]
})
