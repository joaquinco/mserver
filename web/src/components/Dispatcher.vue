<template>
<div class="row">
  <div class="column">
    <Loading :is-loading="loading"></Loading>
    <h4 v-if="!errorMessage" class="center-text">{{message}}</h4>
    <h4 v-if="errorMessage" class="error center-text">{{errorMessage}}</h4>
  </div>
</div>
</template>

<script>
import Loading from './Loading'
import { mapActions } from 'vuex'
import axios from 'axios'
import { urls } from '@/api'

export default {
  name: 'Dispatcher',
  components: { Loading },
  data () {
    return {
      loading: true,
      message: 'Conectando',
      errorMessage: ''
    }
  },
  mounted: function () {
    this.connectToServer()
  },
  methods: {
    connectToServer: function () {
      var self = this
      axios.get(urls.rpc.system_status).then((response) => {
        self.loading = false
        self.updateServerStatus(true, response.data)
      }, (error) => {
        console.log(error)
        self.loading = false
        self.errorMessage = 'No se pudo conectar con el servidor'
        self.updateServerStatus(false)
      })
    },
    ...mapActions(['updateServerStatus'])
  }
}
</script>
