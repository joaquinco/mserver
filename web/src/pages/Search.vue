<template>
  <div class="container-search pt-3">
    <div class="d-flex flex-column container-sm">
      <div class="d-flex flex-row align-items-center">
        <form @submit.prevent="globalSearch()" class="d-flex flex-row align-items-center col">
          <input
            class="w-100 search-input"
            type="search"
            v-model="query"
            placeholder="Buscar"
            id="input-search"
            :disabled="loadingSources"
          >
          <router-link class="close ml-2" to="/player">Cancelar</router-link>
        </form>
      </div>
      <div class="search-results d-flex flex-column mt-4">
        <div v-if="loadingSources">Cargando fuentes...</div>
        <LoadingLine :is-loading="globalSearching"/>
        <h3 v-if="saerchedQuery && searched && !globalSearching">Q: {{saerchedQuery}}</h3>
        <div v-for="(value, key) in searchResults" v-if="!globalSearching && searched" :key="key">
          <div class="d-flex flex-row justify-content-between">
            <h5 class="source-title">{{searchSourcesByName[key].readable_name}}</h5>
            <Button
              v-if="!value.length && !sourceSearched[key]"
              :is-loading="sourceSearching[key]"
              @click.native="search(key)"
            >Buscar</Button>
          </div>
          <p
            v-if="!value.length && sourceSearched[key]"
            class="center-text no-results"
          >No hay resultados</p>
          <SongList
            v-if="value.length"
            :songs="value"
            @song-selected="onSongSelected"
            songActions="add,remove,download,playNext,play"
            :defaultSongAction="defaultSongAction"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapState, mapMutations, mapActions, mapGetters } from 'vuex'
import { executeAlso, isInt } from '@/utils'
import LoadingLine from '@/components/LoadingLine'
import SongList from '@/components/SongList'
import Button from '@/components/Button'
import NotificationsButton from '@/components/NotificationsButton'

export default {
  name: 'Search',
  components: { LoadingLine, SongList, Button, NotificationsButton },
  data() {
    return {
      query: '',
      saerchedQuery: '',
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
    }),
    ...mapGetters(['searchSourcesByName'])
  },
  mounted() {
    if (!this.searchSources.length) {
      this.fetchSearchSources()
    } else {
      this.onSourcesLoaded(this.searchSources)
    }

    this.focusInput()
  },
  methods: {
    ...mapMutations(['setSearchResults']),
    ...mapActions(['clearSearchResults', 'setSearchSources', 'onSongAction']),
    globalSearch() {
      this.clearResults()
      this.search()
      this.globalSearching = true
    },
    search(source) {
      this.saerchedQuery = this.query

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
    onSongSelected(params) {
      this.onSongAction(params)
    },
    focusInput() {
      document.getElementById('input-search').focus()
    },
    defaultSongAction(song) {
      return isInt(song.pos) ? 'play' : 'add'
    }
  }
}
</script>

<style lang="scss" scoped>
.container-search {
  background: white;
  width: 100%;
  left: 0;
}

.container-search form {
  margin-bottom: 0;
}

.search-input {
  border-radius: 10px;
  margin-bottom: 0;
  height: 34px;
}

.search-results {
  flex: 1;
}
.source-title {
  margin-bottom: 0;
}

.no-results {
  color: #b2b2b2;
  margin-bottom: 0;
}
</style>
