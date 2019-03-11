<template>
  <div class="w-100 d-flex flex-column justify-content-start">
    <Song
      :class="{'current-song': isSongHighlighted(song)}"
      :actions="songActions"
      :default-action="defaultSongAction"
      v-for="song in songs"
      :song="song"
      :key="song.search_key || song.pos"
      @song-selected="onSongEvent"
    />
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
    },
    songActions: {
      type: String,
      required: false
    },
    defaultSongAction: {
      required: false,
      default: 'play'
    },
    isSongHighlighted: {
      type: Function,
      required: false,
      default: () => false
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
