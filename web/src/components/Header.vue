<template>
  <div class="header" :class="{'header--fixed':fixed}">
    <Banner :visible="!isConnected" :text="bannerConnectionError" type="error"/>
    <div class="container-sm header__content">
      <h1 class="header__title">{{title}}</h1>
      <div class="header__actions">
        <slot></slot>
      </div>
    </div>
  </div>
</template>

<script>
import { mapGetters, mapState } from 'vuex'
import Banner from '@/components/Banner'

export default {
  name: 'Header',
  components: { Banner },
  props: {
    title: {
      type: String,
      required: false,
      default: ''
    },
    fixed: {
      default: true
    }
  },
  computed: {
    ...mapState({
      connectionError: state => state.comm.error
    }),
    ...mapGetters(['isConnected']),
    bannerConnectionError() {
      let message = 'Desconectado'
      if (this.connectionError) {
        message += `: ${this.connectionError}`
      }
      return message
    }
  }
}
</script>

<style lang='scss' scoped>
.header {
  box-shadow: 0px 0px 5px #919191;
  background-color: white;

  > {
    transition: 300ms ease-in-out;
  }

  &--fixed {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    z-index: 100;
  }

  &__content {
    padding-top: 10px;
    padding-bottom: 10px;
    display: flex;
    flex-direction: row;
    justify-content: space-between;
  }

  &__title {
    flex: 1;
    margin-bottom: 0;
  }

  &__entry {
    margin-left: 10px;
  }

  &__actions {
    display: flex;
    flex-direction: row;
    align-items: center;
  }
}
</style>
