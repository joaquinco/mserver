<template>
  <div class="d-flex flex-column container align-items-center">
      <LoadingLine :is-loading="loading"></LoadingLine>
      <h4 v-if="!error" class="center-text">{{message}}</h4>
      <ApiError :errorResponse="error"/>
  </div>
</template>

<script>
import axios from 'axios'
import { mapActions, mapMutations, mapState } from 'vuex'

import { urls, getEndpoints, getSocket } from '@/api'
import storage from '@/storage'
import LoadingLine from '@/components/LoadingLine'
import ApiError from '@/components/ApiError'

export default {
  name: 'Dispatcher',
  components: {
    LoadingLine,
    ApiError
  },
  computed: {
    ...mapState({
      serverChecked: state => state.server.checked,
      socket: state => state.comm.socket
    })
  },
  data() {
    return {
      loading: true,
      message: 'Conectando',
      error: ''
    }
  },
  mounted() {
    if (!this.serverChecked) {
      this.connectToServer()
    } else if (this.socket && this.socket.disconnected) {
      this.reconnect()
    } else {
      this.onServerUp()
    }
  },
  methods: {
    ...mapActions(['updateServerStatus', 'initComm', 'setUser']),
    ...mapMutations(['setToken']),
    connectToServer() {
      var self = this
      axios.get(urls.rpc.system_status).then(
        response => {
          this.updateServerStatus({
            success: true,
            data: response.data
          })
          this.onServerUp()
        },
        error => {
          console.log(error)
          this.loading = false
          this.updateServerStatus({
            success: false
          })
          self.onConnectionError(error)
        }
      )
    },
    onConnectionError(error) {
      if (!error) {
        error = 'No se pudo conectar con el servidor'
      }
      this.error = error
      this.loading = false
    },
    onServerUp() {
      let token = storage.get('token')
      if (!token) {
        this.$router.push({ name: 'login' })
      } else {
        this.setToken(token)
        var api = getEndpoints(token)
        api.auth.self.get().then(response => {
          this.setUser({ ...response.data })
          getSocket(token).then(socket => {
            this.initComm({ api, socket })
            this.$router.push({ name: 'player' })
          }, this.onConnectionError)
        }, this.onConnectionError)
      }
    },
    reconnect() {
      this.socket.on('connect', params => this.$router.push({ name: 'player' }))
    }
  }
}
</script>
