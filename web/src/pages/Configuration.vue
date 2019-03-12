<template>
  <div>
    <Header title="Configuración">
      <router-link to="player">Atras</router-link>
    </Header>
    <div class="container-sm content-with-header">
      <Configurations/>
    </div>
  </div>
</template>

<script>
import Header from '@/components/Header'
import Configurations from '@/components/Configurations'

export default {
  name: 'Configuration',
  components: { Header, Configurations }
}
</script>

<style lang="scss">
</style>
