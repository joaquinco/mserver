<template>
  <div class="flex-d flex-column justify-content-center container-sm">
    <form class="d-flex flex-column">
      <h1>Quien sos?</h1>
      <ApiError :errorResponse='apiError'/>
      <input type=text placeholder="Nombre" v-model="username"/>
      <span class="input-help">(mínimo {{usernameMinimunLength}} letras)</span>
      <input v-if="!basicLogin" type=password placeholder="Contraseña" v-model="password"/>
      <div class="d-flex flex-row justify-content-end">
        <LoadingCircular :is-loading="isLoading" :in-place="true" :size="30"></LoadingCircular>
        <button class="button-primary ml-1" @click.prevent.stop="submit()" :disabled="isFormInvalid">Dale</button>
      </div>
    </form>
    <div class="position-fixed trigger-password noselect" @click.stop="wantToTriggerPassword()">
      <h4 v-show="triggerPasswordCount > 3">{{triggerPassworClickLimit - triggerPasswordCount}}</h4>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import { urls } from '@/api'
import LoadingCircular from '@/components/LoadingCircular'
import ApiError from '@/components/ApiError'
import storage from '@/storage'

export default {
  name: 'Login',
  components: {
    LoadingCircular,
    ApiError
  },
  data() {
    return {
      username: '',
      password: '',
      basicLogin: true,
      triggerPassworClickLimit: 10,
      triggerPasswordCount: 0,
      timer: null,
      isLoading: false,
      apiError: null,
      usernameMinimunLength: 4
    }
  },
  computed: {
    isFormInvalid() {
      return this.username.length < this.usernameMinimunLength
    }
  },
  methods: {
    wantToTriggerPassword() {
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
    clearPasswordCount() {
      this.triggerPasswordCount = 0
    },
    submit() {
      this.isLoading = true

      let stopLoading = fn => params => {
        this.isLoading = false
        return fn(params)
      }

      axios
        .post(urls.auth.login, {
          username: this.username,
          password: this.password
        })
        .then(
          stopLoading(this.onLoginSuccess),
          stopLoading(error => {
            this.apiError = error
          })
        )
    },
    onLoginSuccess(response) {
      storage.set('token', response.data.access_token)
      this.$router.push({ name: 'dispatch' })
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
.input-help {
  margin-bottom: 10px;
  font-size: 0.7em;
}

input {
  margin: 0;
}
</style>
