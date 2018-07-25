<template>
  <div>
    <div class="d-flex flex-row song-row justify-content-start align-items-center"
      :class="{'song-clickable': canSelect}">
      <strong class="song-position">{{getSongPosition(song)}}</strong>
      <div class="d-flex flex-row justify-content-between song-info" @click="onSelect()">
        <div class="d-flex flex-column" :class="{'not-available': !song.available}">
          <span class="title">{{song.title}}</span>
          <span class="artist" v-if="song.artist">{{song.artist}}</span>
        </div>
      </div>
      <span class="duration">{{song.duration}}</span>
      <span class="icon icon-actions noselect" v-show="hasOtherActions" @click="toggleShowActions()"></span>
    </div>
    <div v-if="actionsVisible">
      <div class="d-flex flex-row justify-content-center align-items-center">
        <button
          class='action-button'
          v-for="action in otherActions"
          @click.prevent="onSongAction(action.name)"
          type="button"
          :key="action.name">
          {{action.label}}
        </button>
      </div>
    </div>
  </div>
</template>

<script>
const POSSTIBLE_OTHER_ACTIONS = [
  { name: 'remove', label: 'Quitar', validator: song => true },
  { name: 'download', label: 'Download', validator: song => !song.available }
]

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
    },
    actionsTimeout: {
      type: Number,
      required: false,
      default: 5 * 1000
    }
  },
  data() {
    return {
      actionsVisible: false,
      actionsTimeoutId: null
    }
  },
  computed: {
    canSelect() {
      return this.actions.includes('select')
    },
    hasOtherActions() {
      return this.otherActions.length
    },
    otherActions() {
      var ret = POSSTIBLE_OTHER_ACTIONS.filter(
        obj => this.actions.includes(obj.name) && obj.validator(this.song)
      )
      return ret
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
      setTimeout(this.closeActions, 150)
    },
    getSongPosition(song) {
      if (song && song.pos != null) {
        return song.pos + 1
      }
    },
    toggleShowActions() {
      this.actionsVisible = !this.actionsVisible
      clearTimeout(this.actionsTimeoutId)
      if (this.actionsVisible) {
        this.actionsTimeoutId = setTimeout(
          this.closeActions,
          this.actionsTimeout
        )
      }
    },
    closeActions() {
      this.actionsVisible = false
      clearTimeout(this.actionsTimeoutId)
    }
  },
  destroyed() {
    clearTimeout(this.actionsTimeoutId)
  }
}
</script>

<style scoped>
.song-row {
  padding: 10px 10px 10px 0;
  border-bottom: 1px solid rgba(178, 178, 178, 0.23);
}

.song-clickable {
  cursor: pointer;
}

.song-clickable:hover {
  background: linear-gradient(90deg, white, rgba(193, 193, 193, 0.26), white);
}

.song-clickable:active {
  background: linear-gradient(90deg, white, rgba(193, 193, 193, 0.1), white);
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

.icon-actions {
  content: url("/static/icons/more.svg");
}

.action-button {
  border: none;
  padding: 0 10px;
  margin: 0;
}
.song-position {
  margin: 0 10px;
}
</style>
