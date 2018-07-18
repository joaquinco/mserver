<template>
  <div class="w-100 d-flex flex-column align-items-center">
    <SongList :songs='songs' v-if="songsExist"/>
    <h4 v-if="!songsExist">Agregá canciones gil</h4>
  </div>
</template>

<script>
import { mapState, mapMutations } from 'vuex'
import SongList from '@/components/SongList'

export default {
  name: 'Playlist',
  components: { SongList },
  data() {
    return {
      loading: false,
      error: null
    }
  },
  computed: {
    ...mapState({
      api: state => state.comm.api,
      songs: state => state.playlist.songs
    }),
    songsExist() {
      return this.songs.length > 0 && this.loaded
    }
  },
  mounted() {
    this.fetchPlaylistSongs()
  },
  methods: {
    ...mapMutations(['setCurrentPlaylistSongs']),
    fetchPlaylistSongs() {
      this.api.playlist.get().then(response => {
        this.setCurrentPlaylistSongs(response.data)
        this.loaded = true
      })
    }
  }
}
</script>

<style>
</style>
