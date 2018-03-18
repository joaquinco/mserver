<template>
  <div class="w-100 d-flex flex-column justify-content-start">
    <Song actions="select,download" v-for="song in songs" :song="song" :key="song.search_key"/>
  </div>
</template>

<script>
import Song from '@/components/Song'

export default {
  name: 'SongList',
  components: {Song},
  props: ['songs'],
  data () {
    return {}
  }
}
</script>

<style scoped>
</style>
