<template>
  <div>
    <Header title="Lista">
      <router-link to="/search">
        <div class="icon icon-search"></div>
      </router-link>
      <NotificationsButton class="ml-3"/>
    </Header>
    <div class="container-sm d-flex flex-column justfy-content-around content-with-header">
      <Playlist class="player-content"/>
      <PlayerControls class="player-controls" @current-clicked="currentSongClicked"/>
      <Notifications/>
    </div>
  </div>
</template>

<script>
import Header from '@/components/Header'
import PlayerControls from '@/components/PlayerControls'
import Playlist from '@/components/Playlist'
import Notifications from '@/components/Notifications'
import NotificationsButton from '@/components/NotificationsButton'

export default {
  name: 'Player',
  components: {
    PlayerControls,
    Playlist,
    Notifications,
    Header,
    NotificationsButton
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
  padding-bottom: 130px;
}

.player-controls {
  position: fixed;
  bottom: 0;
  left: 0;
}

.icon-search {
  content: url('/static/icons/search.svg');
}
</style>
