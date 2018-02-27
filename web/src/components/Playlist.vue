<template>
  <div class="w-100 d-flex flex-column align-items-center">
    <template v-if="songs">
      <Song v-for="song in songs" :song="song" :key="song.key"/>
    </template>
    <h4>Agregá canciones gil</h4>
  </div>
</template>

<script>
export default {
  name: 'Playlist',
  data () {
    return {
      songs: []
    }
  }
}
</script>

<style>
</style>
