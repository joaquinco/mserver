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
import { mapState, mapMutations } from 'vuex'
import { executeAlso } from '@/utils'

export default {
  name: 'SearchToggle',
  data () {
    return {
      query: '',
      searchActive: false,
      loadingSources: false,
      error: null
    }
  },
  computed: {
    ...mapState({
      searchSources: state => state.search.sources,
      api: state => state.comm.api
    })
  },
  mounted () {
    if (!this.searchSources.length) {
      this.fetchSearchSources()
    }
  },
  methods: {
    ...mapMutations(['setSearchSources']),
    search () {
      alert('Buscando.')
    },
    onSearchFocus () {
      this.searchActive = true
    },
    cancelSearch () {
      this.searchActive = false
      this.query = ''
    },
    fetchSearchSources () {
      this.loadingSources = true

      let always = () => { this.loadingSources = false }

      var self = this
      this.api.srpc.search_sources.get().then(
        executeAlso((response) => self.setSearchSources(response.sources), always),
        executeAlso(self.onApiError, always))
    },
    onApiError (error) {
      this.error = error
      alert(error)
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
