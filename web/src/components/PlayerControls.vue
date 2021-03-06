<template>
  <div class="d-flex flex-column player-controls-container align-items-center">
    <Progress :percentage="progressPercentage"/>
    <div v-show="isConnected" class="d-flex flex-column align-items-center w-100">
      <p class="song-title mb-0" @click="focusCurrentSong()">{{currentSongTitle}}</p>
      <div class="d-flex flex-row justify-content-around w-100">
        <span>{{currentSongPosition}}</span>
      </div>
      <div
        class="d-flex flex-row justify-content-around align-items-center player-controls-wrapper"
      >
        <router-link to="/config" class="icon icon--sm player-settings"></router-link>
        <div class="d-flex flex-row justify-content-center player-controls">
          <button class="button button-left" @click.prevent="previous()">
            <span class="prev"></span>
          </button>
          <button class="button button-center" @click.prevent="playPause()">
            <span :class="{play: isPaused, pause: isPlaying, stop: isStoped}"></span>
          </button>
          <button class="button button-right" @click.prevent="next()">
            <span class="next"></span>
          </button>
        </div>
        <VolumeV2 class="volume-wrapper" @change="onVolumeChange" :value="status.volume"/>
      </div>
    </div>
  </div>
</template>

<script>
import { mapState, mapGetters } from 'vuex'
import VolumeV2 from '@/components/VolumeV2'
import Progress from '@/components/Progress'

export default {
  name: 'PlayerControls',
  components: { VolumeV2, Progress },
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
    ...mapGetters(['isConnected']),
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
    progressPercentage() {
      if (this.time != null && this.totalTime) {
        return (this.time / this.totalTime) * 100
      }
      return 0
    }
  },
  methods: {
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
  content: url('/static/icons/prev.svg');
}

.next {
  content: url('/static/icons/next.svg');
}

.play {
  content: url('/static/icons/play.svg');
}

.pause {
  content: url('/static/icons/pause.svg');
}

.stop {
  content: url('/static/icons/stop.svg');
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
  content: url('/static/icons/player-configuration.svg');
  border-radius: 0;
}
.text-toggle.disbled {
  text-decoration: line-through;
}
</style>
