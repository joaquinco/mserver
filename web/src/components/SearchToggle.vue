<template>
  <div class="d-flex flex-column container-search" :class="{'search-fullpage': searchActive, 'container-sm': searchActive, 'w-100': !searchActive}">
    <div class="input-wrapper">
      <form @submit.prevent="search" class="d-flex flex-row align-items-center">
        <input class="w-100" type=search v-model="query" placeholder="Buscar" @focus="onSearchFocus"/>
        <a v-if="searchActive" class="cancel-search ml-2" href="" @click.prevent.stop="cancelSearch">Cancelar</a>
      </form>
    </div>
    <div v-if="searchActive" class="search-results"></div>
  </div>
</template>

<script>
export default {
  name: 'SearchToggle',
  data () {
    return {
      query: '',
      searchActive: false
    }
  },
  methods: {
    search () {
      alert('Buscando.')
    },
    onSearchFocus () {
      this.searchActive = true
    },
    cancelSearch () {
      this.searchActive = false
      this.query = ''
    }
  }
}
</script>

<style scoped>
.container-search {
  background: white;
}
input {
  border-radius: 10px;
  margin-bottom: 0;
  height: 34px;
}
.cancel-search {
  color: #007aff;
  text-decoration: none;
}
.cancel-search:active {
  opacity: 0.7;
}
.search-fullpage {
  position: fixed;
  height: 100vh;
}
.search-results {
  flex: 1;
}
</style>
