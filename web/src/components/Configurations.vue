<template>
  <div class="configuration">
    <h2 class="configuration__section-title">Reproductor</h2>
    <ul>
      <li class="configuration__row">
        <label for="input-repeat">Repetir</label>
        <input type="checkbox" id="input-repeat" :checked="player_repeat" @change="toggleRepeat()">
      </li>
      <li class="configuration__row">
        <label for="input-random">Aleatorio</label>
        <input type="checkbox" id="input-random" :checked="player_random" @change="toggleRandom()">
      </li>
      <li class="configuration__row">
        <label for="input-consume">Consumir</label>
        <input
          type="checkbox"
          id="input-consume"
          :checked="player_consume"
          @change="toggleConsume()"
        >
      </li>
      <li class="configuration__row">
        <label for="input-crossfade">Crossfade</label>
        <div>
          <input
            type="number"
            id="input-crossfade"
            :value="player_crossfade"
            min="0"
            max="9"
            @input="setPlayerCrossfade"
          >
          <span>segundos</span>
        </div>
      </li>
    </ul>
    <div>
      <router-link to="/player-stats">Estado del reproductor</router-link>
    </div>
    <h2 class="configuration__section-title">Canciones</h2>
    <div>
      <Button
        :isLoading="playlistClearing"
        @click.native="clearCurrentPlaylist()"
      >Borrar lista de reproducción</Button>
    </div>
    <div>
      <Button :isLoading="songDbUpdating" @click.native="updateSongDB()">Actualizar BD</Button>
    </div>
    <h2 class="configuration__section-title">About</h2>
    <div class="configuration__row">
      <span>Versión MPD</span>
      <span>{{mpd_version}}</span>
    </div>
    <div class="configuration__row">
      <span>Versión MServer</span>
      <span>{{mserver_version}}</span>
    </div>
  </div>
</template>

<script>
import { mapState, mapActions } from 'vuex'
import Button from '@/components/Button'

export default {
  name: 'Configurations',
  components: { Button },
  computed: {
    ...mapState({
      player_status: ({ player: { status } }) => status,
      player_state: ({ player: { state } }) => state,
      mpd_version: ({ player: { version } }) => version,
      mserver_version: ({ server: { version } }) => version,
      player_repeat: ({ player: { status } }) => status && status.repeat,
      player_random: ({ player: { status } }) => status && status.random,
      player_consume: ({ player: { status } }) => status && status.consume,
      player_crossfade: ({ player: { status } }) =>
        status && (status.xfade || 0)
    })
  },
  data() {
    return {
      songDbUpdating: false,
      playlistClearing: false
    }
  },
  methods: {
    ...mapActions([
      'updateDB',
      'clearPlaylist',
      'toggleMPDConfiguration',
      'setCrossfade'
    ]),
    updateSongDB() {
      this.fakeLoad('songDbUpdating', 1500)
      this.updateDB()
    },
    clearCurrentPlaylist() {
      this.fakeLoad('playlistClearing', 1500)
      this.clearPlaylist()
    },
    fakeLoad(loadingKey, loadingTime) {
      this[loadingKey] = true

      setTimeout(() => {
        this[loadingKey] = false
      }, loadingTime)
    },
    toggleRepeat() {
      this.toggleMPDConfiguration('repeat')
    },
    toggleRandom() {
      this.toggleMPDConfiguration('random')
    },
    toggleConsume() {
      this.toggleMPDConfiguration('consume')
    },
    setPlayerCrossfade({ target: { value } }) {
      this.setCrossfade(value)
    }
  }
}
</script>

<style lang="scss" scoped>
.configuration__section-title {
  width: 100%;
  border-bottom: 1px solid #dddddd;
  font-size: 1.8em;
  margin-top: 20px;
}

.configuration__row {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
}

input {
  margin-bottom: 0;
}
</style>
