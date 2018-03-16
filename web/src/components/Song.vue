<template>
  <div class="d-flex flex-row song-row justify-content-between">
    <div class="d-flex flex-column">
      <span class="title">{{song.title}}</span>
      <span class="artist" v-if="song.artist">{{song.artist}}</span>
    </div>
    <span class="duration">{{song.duration}}</span>
  </div>
</template>

<script>
export default {
  name: 'Song',
  props: ['song'],
  data () {
    return {}
  }
}
</script>

<style scoped>
.song-row {
  padding: 10px 10px 10px 0;
  border-bottom: 1px solid #b2b2b2;
}

.song-row:last-child {
  border-bottom: none;
}

.artist,
.title {
  text-overflow: clip;
}

.title {
  font-size: 0.8em;
}

.artist {
  font-size: 0.6em;
  color: #b2b2b2;
}

</style>
