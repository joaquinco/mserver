<template>
  <div class="w-100 d-flex flex-column justify-content-start">
    <Song :class="{'current-song': song.is_current}"
      actions="select,download"
      v-for="song in songs"
      :song="song"
      :key="song.search_key"
      @song-selected="onSongEvent"/>
  </div>
</template>

<script>
import Song from '@/components/Song'

export default {
  name: 'SongList',
  components: { Song },
  props: {
    songs: {
      type: Array,
      required: true
    }
  },
  data() {
    return {}
  },
  methods: {
    onSongEvent(event) {
      this.$emit('song-selected', event)
    }
  }
}
</script>

<style scoped>
.current-song {
  background: linear-gradient(90deg, white, rgba(193, 193, 193, 0.26), white);
}
</style>
