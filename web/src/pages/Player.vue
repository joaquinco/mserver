<template>
  <div>
    <Header title='Lista'>
      <Banner :visible='!isConnected' :text='bannerConnectionError' type='error' ref='bannerRef'/>
    </Header>
    <div class='container-sm d-flex flex-column justfy-content-around'>
      <Playlist class="player-content"/>
      <PlayerControls class='player-controls' @current-clicked='currentSongClicked'/>
      <Notifications/>
    </div>
  </div>
</template>

<script>
import { mapState, mapGetters } from 'vuex'
import Header from '@/components/Header'
import PlayerControls from '@/components/PlayerControls'
import Playlist from '@/components/Playlist'
import Notifications from '@/components/Notifications'
import Banner from '@/components/Banner'

export default {
  name: 'Player',
  components: {
    PlayerControls,
    Playlist,
    Notifications,
    Header,
    Banner
  },
  computed: {
    ...mapState({
      socket: state => state.comm.socket,
      connectionError: state => state.comm.error
    }),
    ...mapGetters(['isConnected']),
    bannerConnectionError() {
      let message = 'Desconectado'
      if (this.connectionError) {
        message += `: ${this.connectionError}`
      }
      return message
    }
  },
  data() {
    return {}
  },
  methods: {
    currentSongClicked({ pos }) {
      try {
        var bodyRect = document.body.getBoundingClientRect()
        let s = document.getElementsByClassName('song')[pos]
        let coords = s.getBoundingClientRect()
        let offset = coords.top - bodyRect.top - 150
        window.scrollTo(coords.left, offset)
      } catch (e) {}
    }
  }
}
</script>

<style scoped>
.player-content {
  flex: 1;
  padding-top: 80px;
  padding-bottom: 130px;
}

@media (max-width: 550px) {
  .player-content {
    padding-top: 60px;
  }
}

.player-controls {
  position: fixed;
  bottom: 0;
  left: 0;
}
</style>
