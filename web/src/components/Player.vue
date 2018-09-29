<template>
  <div>
    <Header title='Playlist'/>
    <div class='container-sm d-flex flex-column justfy-content-around'>
      <Playlist class="player-content"/>
      <PlayerControls class='player-controls'/>
      <Notifications/>
    </div>
  </div>
</template>

<script>
import { mapState } from 'vuex'
import Header from '@/components/Header'
import PlayerControls from '@/components/PlayerControls'
import Playlist from '@/components/Playlist'
import Notifications from '@/components/Notifications'

export default {
  name: 'Player',
  components: {
    PlayerControls,
    Playlist,
    Notifications,
    Header
  },
  computed: {
    ...mapState({
      socket: state => state.comm.socket
    })
  },
  data() {
    return {}
  },
  mounted() {
    this.socket.on('disconnect', reason => {
      this.$router.push({ name: 'dispatch' })
    })
  }
}
</script>

<style scoped>
.player-content {
  flex: 1;
  padding-bottom: 160px;
}

.player-controls {
  position: fixed;
  bottom: 0;
  left: 0;
}
</style>
