<template>
  <div class="container-search container-sm" :class="{'search-fullpage': searchActive}">
    <div class="d-flex flex-column" :class="{'w-100': !searchActive}">
      <div class="input-wrapper">
        <form @submit.prevent="globalSearch()" class="d-flex flex-row align-items-center">
          <input class="w-100" type=search v-model="query" placeholder="Buscar" @focus="onSearchFocus"/>
          <a v-if="searchActive" class="close ml-2" href="" @click.prevent.stop="cancelSearch">Cancelar</a>
        </form>
      </div>
      <div v-if="searchActive" class="search-results d-flex flex-column">
        <div v-if="loadingSources">Cargando fuentes...</div>
        <LoadingLine :is-loading="globalSearching"/>
        <div v-for="(value, key) in searchResults" v-if="!globalSearching && searched" :key="key">
          <div class="d-flex flex-row justify-content-between">
            <h5 class="source-title">Desde {{key}}</h5>
            <LoadingButton
              v-if="!value.length && !sourceSearched[key]"
              :is-loading="sourceSearching[key]"
              @click.native="search(key)">Buscar</LoadingButton>
          </div>
          <p v-if="!value.length && sourceSearched[key]" class="center-text no-results">No hay resultados</p>
          <SongList v-if="value.length" :songs="value" @song-selected="onSongSelected"/>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapState, mapMutations, mapActions } from 'vuex'
import { executeAlso } from '@/utils'
import LoadingLine from '@/components/LoadingLine'
import SongList from '@/components/SongList'
import LoadingButton from '@/components/LoadingButton'

export default {
  name: 'SearchToggle',
  components: { LoadingLine, SongList, LoadingButton },
  data() {
    return {
      query: '',
      searchActive: false,
      loadingSources: false,
      error: null,
      globalSearching: false,
      sourceSearching: {},
      sourceSearched: {},
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
  mounted() {
    if (!this.searchSources.length) {
      this.fetchSearchSources()
    } else {
      this.onSourcesLoaded(this.searchSources)
    }
  },
  methods: {
    ...mapMutations(['setSearchResults']),
    ...mapActions([
      'clearSearchResults',
      'setSearchSources',
      'downloadSong',
      'addSong'
    ]),
    globalSearch() {
      this.clearResults()
      this.search()
      this.globalSearching = true
    },
    search(source) {
      let params = { query: this.query }
      if (source) {
        params.source = source
      } else {
        source = this.defaultSource
      }

      if (this.sourceSearching[source]) {
        return
      }

      this.setSearchLoading(source, true)

      let always = () => {
        this.globalSearching = false
        this.setSearchLoading(source, false)
        this.setSourceSearched(source, true)
      }

      this.api.search.get({ params }).then(
        executeAlso(response => {
          this.setSearchResults({ source, results: response.data })
          this.searched = true
        }, always),
        executeAlso(this.onApiError, always)
      )
    },
    onSearchFocus() {
      this.searchActive = true
    },
    cancelSearch() {
      this.searchActive = this.searched = false
      this.query = ''
      this.clearSearchResults()
    },
    clearResults() {
      this.clearSearchResults()
      this.resetSourceSearched(this.searchSources)
    },
    fetchSearchSources() {
      this.loadingSources = true

      let always = () => {
        this.loadingSources = false
      }

      var self = this
      this.api.srpc.search_sources.get().then(
        executeAlso(response => {
          let sources = response.data
          self.setSearchSources(sources)
          this.onSourcesLoaded(sources)
        }, always),
        executeAlso(self.onApiError, always)
      )
    },
    onSourcesLoaded(sources) {
      sources.forEach(source => {
        let sourceName = source.name
        if (source.is_default) {
          this.defaultSource = sourceName
        }
        this.sourceSearching[sourceName] = false
      })
    },
    resetSourceSearched(sources) {
      sources.forEach(source => {
        this.sourceSearched[source.name] = false
      })
    },
    setSearchLoading(source, state) {
      this.sourceSearching = { ...this.sourceSearching, [source]: state }
    },
    setSourceSearched(source, state) {
      this.sourceSearched = { ...this.sourceSearched, [source]: state }
    },
    onApiError(error) {
      this.error = error
      alert(error)
    },
    onSongSelected({ song, action }) {
      let actions = { download: this.downloadSong, select: this.addSong }
      actions[action](song)
    }
  }
}
</script>

<style scoped>
.container-search {
  background: white;
  position: fixed;
}

input {
  border-radius: 10px;
  margin-bottom: 0;
  height: 34px;
}
/* .search-fullpage {
  position: fixed;
  height: 100vh;
  left: 0;
} */
/* .container-sm {
  height: 97vh;
} */
.search-results {
  flex: 1;
  overflow-y: auto;
}
.source-title {
  margin-bottom: 0;
}

.no-results {
  color: #b2b2b2;
  margin-bottom: 0;
}
</style>
