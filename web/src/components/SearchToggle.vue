<template>
  <div class="d-flex flex-column container-search" :class="{'search-fullpage': searchActive, 'container-sm': searchActive, 'w-100': !searchActive}">
    <div class="input-wrapper">
      <form @submit.prevent="onSearch" class="d-flex flex-row align-items-center">
        <input class="w-100" type=search v-model="query" placeholder="Buscar" @focus="onSearchFocus"/>
        <a v-if="searchActive" class="cancel-search ml-2" href="" @click.prevent.stop="cancelSearch">Cancelar</a>
      </form>
    </div>
    <div v-if="searchActive" class="search-results d-flex flex-column align-items-center">
      <div v-if="loadingSources">Cargando fuentes...</div>
      <LoadingLine :is-loading="searching"/>
      <div v-for="(value, key) in searchResults" v-if="!searching && searched" :key="key">
        <h5>Desde {{key}}</h5>
        <SongList v-if="value.length" :songs="value"/>
        <Button v-if="!value.length">Buscar</Button>
      </div>
    </div>
  </div>
</template>

<script>
import { mapState, mapMutations, mapActions } from 'vuex'
import { executeAlso } from '@/utils'
import LoadingLine from '@/components/LoadingLine'
import SongList from '@/components/SongList'

export default {
  name: 'SearchToggle',
  components: {LoadingLine, SongList},
  data () {
    return {
      query: '',
      searchActive: false,
      loadingSources: false,
      error: null,
      searching: false,
      defaultSource: null,
      searched: false
    }
  },
  computed: {
    ...mapState({
      searchSources: state => state.search.sources,
      searchResults: state => state.search.results,
      api: state => state.comm.api
    })
  },
  mounted () {
    if (!this.searchSources.length) {
      this.fetchSearchSources()
    } else {
      this.setDefaultSource(this.searchSources)
    }
  },
  methods: {
    ...mapMutations(['setSearchResults']),
    ...mapActions(['clearSearchResults', 'setSearchSources']),
    onSearch (event) {
      this.search()
    },
    search (source) {
      if (this.searching) {
        return
      }

      this.searching = true

      let always = () => { this.searching = false }

      let params = {query: this.query}
      if (source) {
        params.source = source
      } else {
        source = this.defaultSource
      }

      this.api.search.get({params}).then(
        executeAlso((response) => {
          this.setSearchResults({source, results: response.data})
          this.searched = true
        }, always),
        executeAlso(this.onApiError, always)
      )
    },
    onSearchFocus () {
      this.searchActive = true
    },
    cancelSearch () {
      this.searchActive = false
      this.query = ''
      this.clearSearchResults()
    },
    fetchSearchSources () {
      this.loadingSources = true

      let always = () => { this.loadingSources = false }

      var self = this
      this.api.srpc.search_sources.get().then(
        executeAlso((response) => {
          self.setSearchSources(response.data)
          this.setDefaultSource(response.data)
        }, always),
        executeAlso(self.onApiError, always))
    },
    setDefaultSource (sources) {
      sources.forEach(source => {
        if (source.is_default) {
          this.defaultSource = source.name
        }
      })
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
