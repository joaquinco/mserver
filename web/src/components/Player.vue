<template>
  <div class='container-sm d-flex flex-column justfy-content-around'>
    <SearchToggle class='pt-3 search-toggle'/>
    <Playlist class="player-content mt-3"/>
    <PlayerControls class='player-controls'/>
    <Notifications/>
  </div>
</template>
<script>
import PlayerControls from '@/components/PlayerControls'
import SearchToggle from '@/components/SearchToggle'
import Playlist from '@/components/Playlist'
import Notifications from '@/components/Notifications'

export default {
  name: 'Player',
  components: {
    PlayerControls,
    SearchToggle,
    Playlist,
    Notifications
  },
  data() {
    return {}
  }
}
</script>

<style scoped>
.player-content {
  flex: 1;
  padding-bottom: 90px;
  padding-top: 50px;
}

.player-controls {
  position: fixed;
  bottom: 10px;
  left: 50%;
  transform: translateX(-50%);
}
</style>
