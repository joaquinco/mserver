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
  mounted () {
    this.connectToServer()
  },
  methods: {
    ...mapActions(['updateServerStatus']),
    connectToServer () {
      axios.get(urls.rpc.system_status).then((response) => {
        this.loading = false
        this.message = '...'
        this.updateServerStatus({success: true, data: response.data})
        this.onConnected()
      }, (error) => {
        console.log(error)
        this.loading = false
        this.errorMessage = 'No se pudo conectar con el servidor'
        this.updateServerStatus({success: false})
      })
    },
    onConnected () {
      
    }

  }
}
</script>
