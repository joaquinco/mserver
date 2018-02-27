<template>
  <div class='container-sm d-flex flex-column justfy-content-around h-100vh'>
    <SearchToggle/>
    <Playlist class="player-content"/>
    <PlayerControls/>
  </div>
</template>
<script>
import PlayerControls from '@/components/PlayerControls'
import SearchToggle from '@/components/SearchToggle'
import Playlist from '@/components/Playlist'

export default {
  name: 'Player',
  components: { PlayerControls, SearchToggle, Playlist },
  data () {
    return {
    }
  }
}
</script>

<style scoped>
.player-content {
  flex: 1;
}
</style>
