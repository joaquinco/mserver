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
      :showAs="listType"
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
      type: String,
      required: false,
      default: 'playnow'
    },
    isSongHighlighted: {
      type: Function,
      required: false,
      default: () => false
    },
    listType: {
      type: String,
      required: false
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
