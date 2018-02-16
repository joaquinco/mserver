<template>
  <div class="flex-d flex-column justify-content-center">
    <div class="d-flex flex-column">
      <h1>Quien sos wacho</h1>
      <input type=text placeholder="Nombre"/>
      <input v-if="!basicLogin" type=password placeholder="Contraseña"/>
      <div class="d-flex flex-row justify-content-center mt-10">
        <button>Dale</button>
      </div>
    </div>
    <div class="position-fixed trigger-password" @click.stop="wantToTriggerPassword()">
      <h4 v-show="triggerPasswordCount > 3">{{triggerPassworClickLimit - triggerPasswordCount}}</h4>
    </div>
  </div>
</template>

<script>
import { mapState } from 'vuex'

export default {
  name: 'Login',
  data () {
    return {
      basicLogin: true,
      username: '',
      password: '',
      triggerPassworClickLimit: 10,
      triggerPasswordCount: 0,
      timer: null
    }
  },
  computed: {
    ...mapState({
      auth: state => state.auth
    })
  },
  methods: {
    wantToTriggerPassword () {
      if (this.timer) {
        clearTimeout(this.timer)
      }
      this.triggerPasswordCount += 1;
      if (this.triggerPasswordCount >= this.triggerPassworClickLimit) {
        this.basicLogin = false;
        this.clearPasswordCount();
      } else {
        this.timer = setTimeout(this.clearPasswordCount, 1000);
      }
    },
    clearPasswordCount () {
      this.triggerPasswordCount = 0;
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
