<template>
  <div class="w-100">
    <div class="input-wrapper">
      <form @submit.prevent="search">
        <input class="w-100" type=search v-model="query" placeholder="Buscar"/>
      </form>
    </div>
    <div v-if="searching"></div>
  </div>
</template>

<script>
export default {
  name: 'SearchToggle',
  data () {
    return {
      query: '',
      searching: false
    }
  },
  methods: {
    search () {
      alert('Buscando.')
    }
  }
}
</script>

<style scoped>
input {
  border-radius: 40px;
}
</style>
