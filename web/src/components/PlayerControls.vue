<template>
  <div class='d-flex flex-column w-100 mb-4'>
    <ApiError :errorResponse="error"/>
    <div v-show='loaded && !error' class='d-flex flex-row justify-content-center player-controls'>
      <button class='button button-left'>
        <span class='prev'></span>
      </button>
      <button class='button button-center' @click.prevent='playPause()'>
        <span :class='{play: isPlaying, pause: isPaused, stop: isStoped}'></span>
      </button>
      <button class='button button-right'>
        <span class='next'></span>
      </button>
    </div>
    <!-- Progress bar -->
  </div>
</template>

<script>
import { mapState, mapMutations } from 'vuex'
import ApiError from '@/components/ApiError'

export default {
  name: 'PlayerControls',
  components: { ApiError },
  data() {
    return {
      loaded: false,
      error: null
    }
  },
  computed: {
    ...mapState({
      playerState: state => state.player.status.state,
      api: state => state.comm.api,
      socket: state => state.comm.socket
    }),
    isPlaying() {
      return this.playerState === 'play'
    },
    isStoped() {
      return this.playerState === 'stop'
    },
    isPaused() {
      return this.playerState === 'pause'
    }
  },
  mounted() {
    this.fetchPlayerState()
  },
  methods: {
    ...mapMutations(['setPlayerStatus']),
    fetchPlayerState() {
      this.api.srpc.player_status.get().then(
        response => {
          this.setPlayerStatus(response.data)
          this.loaded = true
        },
        error => {
          this.error = error
        }
      )
    },
    playPause() {
      let event = (this.isPlaying && 'player.pause') || 'player.play'
      this.socket.emit(event)
    }
  }
}
</script>

<style scoped>
.player-controls {
  box-sizing: border-box;
}

.button {
  padding: 10px;
  color: black;
  margin: 0;
  height: 50px;
  width: 60px;
  background-color: white;
}

.button-left {
  border-radius: 30% 0 0 30%;
}

.button-center {
  border-radius: 0;
  border-right: none;
  border-left: none;
}

.button-right {
  border-radius: 0 30% 30% 0;
}

.prev,
.next,
.play,
.pause,
.stop {
  height: 100%;
  width: 100%;
}

.prev {
  content: url("/static/icons/prev.svg");
}

.next {
  content: url("/static/icons/next.svg");
}

.play {
  content: url("/static/icons/play.svg");
}

.pause {
  content: url("/static/icons/pause.svg");
}

.stop {
  content: url("/static/icons/stop.svg");
}
</style>
