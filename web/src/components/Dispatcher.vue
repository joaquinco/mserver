<template>
<div class="row">
  <div class="column">
    <Loading v-if="loading"></Loading>
    <h4 v-if="!error" class="center-text">{{message}}</h4>
    <h4 v-if="error" class="error center-text">{{error_message}}</h4>
  </div>
</div>
</template>

<script>
import Loading from './Loading'
import { mapActions } from 'vuex'

export default {
  name: 'Dispatcher',
  components: { Loading },
  data () {
    return {
      loading: true,
      message: 'Conectando',
      error: false
    }
  },
  mounted () {
    this.connectServer()
  },
  methods: {
    ...mapActions(['connectServer'])
  }
}
</script>
