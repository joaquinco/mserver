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
        ({ data }) => {
          this.updateServerStatus({
            success: true,
            data
          })
          this.onServerUp()
        },
        error => {
          this.loading = false
          this.updateServerStatus({
            success: false
          })
          self.onConnectionError(error)
        }
      )
    },
    onConnectionError(error) {
      let response = error && error.response
      if (response && response.status === 401) {
        storage.set('token', null)
        this.redirectLogin()
      }

      this.error = error
      this.loading = false
    },
    onServerUp() {
      let token = storage.get('token')
      if (!token) {
        this.redirectLogin()
      } else {
        var api = getEndpoints(token)
        api.auth.self.get().then(response => {
          this.setUser({ ...response.data })
          this.setToken(token)

          getSocket(token).then(socket => {
            this.initComm({ api, socket })
            this.$router.push({ name: 'player' })
          }, this.onConnectionError)
        }, this.onConnectionError)
      }
    },
    redirectLogin() {
      this.$router.push({ name: 'login' })
    },
    reconnect() {
      this.socket.on('connect', params => this.$router.push({ name: 'player' }))
    }
  }
}
</script>
