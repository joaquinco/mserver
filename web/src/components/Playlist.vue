<template>
  <div class="w-100 d-flex flex-column">
    <h2 v-if="!songsExist && loaded" class="w-100 center-text">Agregá canciones</h2>
    <SongList
      :songs="songs"
      v-if="songsExist"
      songActions="playnow,remove"
      @song-selected="onSongSelected"
      :isSongHighlighted="isSongCurrent"
    />
  </div>
</template>

<script>
import { mapState, mapMutations, mapActions } from 'vuex'
import SongList from '@/components/SongList'

export default {
  name: 'Playlist',
  components: { SongList },
  data() {
    return {
      loaded: false,
      error: null
    }
  },
  computed: {
    ...mapState({
      api: state => state.comm.api,
      socket: state => state.comm.socket,
      songs: state => state.playlist.songs,
      current: state => state.playlist.current
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
    ...mapActions(['playSongNow', 'removeSong']),
    fetchPlaylistSongs() {
      if (this.songs.length) {
        this.loaded = true
      } else {
        this.api.playlist.get().then(response => {
          this.setCurrentPlaylistSongs(response.data)
          this.loaded = true
        })
      }
    },
    onSongSelected({ song, action }) {
      if (action === 'playnow') {
        this.playSongNow(song)
      } else if (action === 'remove') {
        this.removeSong(song)
      }
    },
    isSongCurrent(song) {
      return song.pos === this.current.pos
    }
  }
}
</script>

<style>
</style>
