<template>
  <div class="column" v-if="basic_login">
    <div class="row"></div>
  </div>
</template>

<script>
import { mapState } from 'vuex'

export default {
  name: 'Login',
  data () {
    basic_login: true
  },
  computed: {
    ...mapState({
      auth: state => state.auth
    })
  },
  methods: {
  }
}
</script>

<style>
</style>
