<template>
  <div class="d-flex flex-row song-row justify-content-start">
    <span class="icon icon-add" v-if="canSelect" title="Agregar" @click="onSelect()"></span>
    <span class="icon icon-download" v-if="canDownload" title="Descargar" @click="onDownload()"></span>
    <div class="d-flex flex-row justify-content-between song-info">
      <div class="d-flex flex-column" :class="{'not-available': !song.available}">
        <span class="title">{{song.title}}</span>
        <span class="artist" v-if="song.artist">{{song.artist}}</span>
      </div>
      <span class="duration">{{song.duration}}</span>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Song',
  props: {
    song: {
      type: Object,
      required: true
    },
    actions: {
      type: String,
      required: false,
      default: 'select'
    }
  },
  data() {
    return {}
  },
  computed: {
    canDownload() {
      return this.actions.includes('download') && !this.song.available
    },
    canSelect() {
      return this.actions.includes('select')
    }
  },
  methods: {
    onDownload() {
      this.onSongAction('download')
    },
    onSelect() {
      this.onSongAction('select')
    },
    onSongAction(action) {
      let event = {
        action,
        song: this.song,
        created: new Date()
      }
      this.$emit('song-selected', event)
    }
  }
}
</script>

<style scoped>
.song-row {
  padding: 10px 10px 10px 0;
  border-bottom: 1px solid rgba(178, 178, 178, 0.23);
}

.song-info {
  flex: 1;
}

.not-available {
  opacity: 0.6;
}

.song-row:last-child {
  border-bottom: none;
}

.artist,
.title {
  text-overflow: clip;
}

.title {
  font-size: 0.8em;
}

.artist {
  font-size: 0.6em;
  color: #b2b2b2;
}

.icon {
  height: 25px;
  border: 1px solid #b2b2b2;
  padding: 5px 0;
  border-radius: 5px;
  margin-right: 10px;
  cursor: pointer;
}
.icon:hover {
  border: 1px solid black;
}

.icon-download {
  content: url("/static/icons/download.svg");
}
.icon-add {
  content: url("/static/icons/plus.svg");
}
</style>
