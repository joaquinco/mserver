<template>
  <div class="flex-d flex-column justify-content-center container-sm">
    <div class="d-flex flex-column">
      <h1>Quien sos wacho</h1>
      <ApiError :errorResponse='apiError'/>
      <input type=text placeholder="Nombre" v-model="username"/>
      <input v-if="!basicLogin" type=password placeholder="Contraseña" v-model="password"/>
      <div class="d-flex flex-row justify-content-end">
        <LoadingCircular :is-loading="isLoading" :in-place="true" :size="30"></LoadingCircular>
        <button class="button-primary ml-1" @click.prevent.stop="submit()" :disabled="isFormInvalid">Dale</button>
      </div>
    </div>
    <div class="position-fixed trigger-password" @click.stop="wantToTriggerPassword()">
      <h4 v-show="triggerPasswordCount > 3">{{triggerPassworClickLimit - triggerPasswordCount}}</h4>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import { mapActions } from 'vuex'
import { urls } from '@/api'
import LoadingCircular from '@/components/LoadingCircular'
import ApiError from './ApiError'

export default {
  name: 'Login',
  components: {
    LoadingCircular,
    ApiError
  },
  data () {
    return {
      username: '',
      password: '',
      basicLogin: true,
      triggerPassworClickLimit: 10,
      triggerPasswordCount: 0,
      timer: null,
      isLoading: false,
      apiError: null
    }
  },
  computed: {
    isFormInvalid () {
      return this.username.length < 5
    }
  },
  methods: {
    ...mapActions(['setUser']),
    wantToTriggerPassword () {
      if (this.timer) {
        clearTimeout(this.timer)
      }
      this.triggerPasswordCount += 1
      if (this.triggerPasswordCount >= this.triggerPassworClickLimit) {
        this.basicLogin = false
        this.clearPasswordCount()
      } else {
        this.timer = setTimeout(this.clearPasswordCount, 800)
      }
    },
    clearPasswordCount () {
      this.triggerPasswordCount = 0
    },
    submit () {
      this.isLoading = true

      let stopLoading = (fn) => (params) => {
        this.isLoading = false
        return fn(params)
      }

      axios.post(urls.auth, {
        username: this.username,
        password: this.password
      }).then(stopLoading(this.onLoginSuccess), stopLoading((error) => { this.apiError = error }))
    },
    onLoginSuccess (response) {
      this.setUser(response.data)
      this.$router.push('/')
    }
  }
}
</script>

<style scoped>
.trigger-password {
  width: 50px;
  height: 50px;
  right: 0;
  bottom: 0;
}
</style>
