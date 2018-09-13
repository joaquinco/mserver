<template>
  <div class="w-100 d-flex flex-column align-items-center">
    <SongList :songs='songs' v-if="songsExist" songActions='select,remove'
            @song-selected="onSongSelected" :isSongHighlighted="isSongCurrent"/>
    <h4 v-if="!songsExist">Agregá canciones</h4>
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
    fetchPlaylistSongs() {
      this.api.playlist.get().then(response => {
        this.setCurrentPlaylistSongs(response.data)
        this.loaded = true
      })
    },
    onSongSelected({ song, action }) {
      if (action === 'select') {
        this.socket.emit('player.select', song)
      } else if (action === 'remove') {
        this.socket.emit('player.remove', song)
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
