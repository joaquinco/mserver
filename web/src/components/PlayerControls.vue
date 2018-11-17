<template>
  <div class='d-flex flex-column player-controls-container align-items-center'>
    <div class='play-progress' :class="{'transition-ease': isPlaying}" :style="{width: progressPercentage + '%'}"></div>
    <ApiError :errorResponse="error"/>
    <div v-show='loaded && !error' class='d-flex flex-column align-items-center w-100'>
      <p class='song-title mb-0' @click='focusCurrentSong()'>{{currentSongTitle}}</p>
      <div class='d-flex flex-row justify-content-around w-100'>
        <span>{{currentSongPosition}}</span>
      </div>
      <div class="d-flex flex-row justify-content-around align-items-center player-controls-wrapper">
        <span class='icon icon--sm player-settings'/>
        <div class='d-flex flex-row justify-content-center player-controls'>
          <button class='button button-left' @click.prevent='previous()'>
            <span class='prev'></span>
          </button>
          <button class='button button-center' @click.prevent='playPause()'>
            <span :class='{play: isPaused, pause: isPlaying, stop: isStoped}'></span>
          </button>
          <button class='button button-right' @click.prevent='next()'>
            <span class='next'></span>
          </button>
        </div>
        <VolumeV2 class='volume-wrapper' @change='onVolumeChange' :value='status.volume'/>
      </div>
      <div class='d-flex flex-row justify-content-around player-other-buttons'>
        <span class='text-toggle' :class='{disbled: !isRepeatOn}' @click='toggleRepeat()'>Repetir</span>
        <span class='text-toggle' :class='{disbled: !isShuffleOn}' @click='toggleShuffle()'>Aleatorio</span>
      </div>
    </div>
  </div>
</template>

<script>
import { mapState, mapActions } from 'vuex'
import ApiError from '@/components/ApiError'
import VolumeV2 from '@/components/VolumeV2'

export default {
  name: 'PlayerControls',
  components: { ApiError, VolumeV2 },
  data() {
    return {
      loaded: false,
      error: null
    }
  },
  computed: {
    ...mapState({
      api: state => state.comm.api,
      socket: state => state.comm.socket,
      current: state => state.playlist.current,
      status: state => state.player.status,
      stats: state => state.player.stats,
      time: state => state.playlist.currentTime,
      totalTime: state => state.playlist.totalTime
    }),
    isPlaying() {
      return this.status.state === 'play'
    },
    isStoped() {
      return this.status.state === 'stop'
    },
    isPaused() {
      return this.status.state === 'pause'
    },
    currentSongTitle() {
      const { song } = this.status
      return song ? this.current.title : '...'
    },
    currentSongPosition() {
      const { song, playlistlength } = this.status

      let songPos = '-'

      let playlistLengthInt = playlistlength ? parseInt(playlistlength) : 0

      if (song) {
        songPos = parseInt(song) + 1
      }

      return `${songPos}/${playlistLengthInt > 0 ? playlistLengthInt : '-'}`
    },
    isShuffleOn() {
      return this.status && this.status.random
    },
    isRepeatOn() {
      return this.status && this.status.repeat
    },
    progressPercentage() {
      if (this.time != null && this.totalTime) {
        return this.time / this.totalTime * 100
      }
      return 0
    }
  },
  mounted() {
    this.fetchPlayerState()
  },
  methods: {
    ...mapActions(['setPlayerStatus']),
    fetchPlayerState() {
      this.api.srpc.player_status.get().then(
        response => {
          this.setPlayerStatus(response.data)
          this.loaded = true
          this.socket.emit('player.current')
        },
        error => {
          this.error = error
        }
      )
    },
    playPause() {
      let event = (this.isPlaying && 'player.pause') || 'player.play'
      this.socket.emit(event)
    },
    next() {
      this.socket.emit('player.next')
    },
    previous() {
      this.socket.emit('player.previous')
    },
    toggleRepeat() {
      this.socket.emit('player.repeat', { value: !this.isRepeatOn })
    },
    toggleShuffle() {
      this.socket.emit('player.random', { value: !this.isShuffleOn })
    },
    onVolumeChange(value) {
      this.socket.emit('player.volume', { value })
    },
    focusCurrentSong(event) {
      this.$emit('current-clicked', this.current)
    }
  }
}
</script>

<style scoped>
.player-controls-container {
  background-color: white;
  box-shadow: 0px 0px 5px #919191;
  width: 100%;
}

.play-progress {
  border-top: #e46f89 2px solid;
  position: absolute;
  left: 0;
  top: 0;
}

.transition-ease {
  transition: 1s ease;
}

.player-controls-wrapper {
  width: 50%;
}

@media (max-width: 800px) {
  .player-controls-wrapper {
    width: 100%;
  }
}

.player-controls {
  box-sizing: border-box;
  align-items: center;
}

.button {
  padding: 10px;
  color: black;
  margin: 0;
  height: 50px;
  width: 60px;
  background-color: white;
  border: none;
}

.song-title {
  text-overflow: ellipsis;
  overflow: hidden;
  white-space: nowrap;
  max-width: 90%;
}

.prev,
.next,
.play,
.pause,
.stop {
  height: 100%;
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

.player-other-buttons {
  width: 300px;
}

@media (max-width: 500px) {
  .player-other-buttons {
    width: 100%;
  }
}

.text-toggle {
  color: #e46f89;
  cursor: pointer;
}
.text-toggle:hover {
  opacity: 0.7;
}
.volume-wrapper {
  display: inline-flex;
}
.player-settings {
  content: url("/static/icons/player-configuration.svg");
  border-radius: 0;
}
.text-toggle.disbled {
  text-decoration: line-through;
}
</style>
