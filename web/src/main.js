// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import { store } from './store'
import VueMoment from 'vue-moment'
import moment from 'moment'
import './assets/skeleton.css'
import './assets/site.css'
// import './assets/normalize.css'
// import '@/assets/bootstrap.css'
import '@/assets/bootstrap-grid.css'

Vue.config.productionTip = false

router.beforeEach((to, from, next) => {
  // hooks must be set before mounting the app
  if (!store.state.server.checked && to.name !== 'dispatch') {
    next({name: 'dispatch'})
  } else {
    next()
  }
})

moment.locale('es')

Vue.use(VueMoment)

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  store,
  components: { App },
  template: '<App/>'
})
