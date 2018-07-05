<template>
  <div class="w-100 d-flex flex-column align-items-center">
    <SongList :songs='songs' v-if="songsExist"/>
    <h4 v-if="!songsExist">Agregá canciones gil</h4>
  </div>
</template>

<script>
import { mapState } from 'vuex'
import SongList from '@/components/SongList'

export default {
  name: 'Playlist',
  components: { SongList },
  data() {
    return {
      songs: [],
      loading: false,
      error: null
    }
  },
  computed: {
    ...mapState({
      api: state => state.comm.api
    }),
    songsExist() {
      return this.songs.length > 0 && this.loaded
    }
  },
  mounted() {
    this.fetchPlaylistSongs()
  },
  methods: {
    fetchPlaylistSongs() {
      this.api.playlist.get().then(response => {
        this.songs = response.data
        this.loaded = true
        // TODO: add songs to state
      })
    }
  }
}
</script>

<style>
</style>
