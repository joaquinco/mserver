<template>
  <div class="d-flex flex-column container">
      <LoadingLine :is-loading="loading"></LoadingLine>
      <h4 v-if="!errorMessage" class="center-text">{{message}}</h4>
      <h4 v-if="errorMessage" class="error center-text">{{errorMessage}}</h4>
  </div>
</template>

<script>
import LoadingLine from './LoadingLine'
import { mapActions, mapMutations } from 'vuex'
import axios from 'axios'
import { urls, getEndpoints, getSocket } from '@/api'
import storage from '@/storage'

export default {
  name: 'Dispatcher',
  components: {
    LoadingLine
  },
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
    ...mapMutations(['setComm']),
    connectToServer () {
      axios.get(urls.rpc.system_status).then((response) => {
        this.updateServerStatus({
          success: true,
          data: response.data
        })
        this.onServerUp()
      }, (error) => {
        console.log(error)
        this.loading = false
        this.updateServerStatus({
          success: false
        })
      })
    },
    onConnectionError () {
      this.errorMessage = 'No se pudo conectar con el servidor'
    },
    onServerUp () {
      let token = storage.get('token')
      if (!token) {
        this.$router.push('who')
      } else {
        var api = getEndpoints(token)
        getSocket(token).then((socket) => {
          this.setComm({api, socket})
        }, this.onConnectionError)
      }
    }
  }
}
</script>
