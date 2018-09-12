<template>
  <div class="song">
    <div class="song__body" :class="{'song--clickable': canSelect, 'song--not-available': !song.available}">
      <strong class="song__position">{{getSongPosition(song)}}</strong>
      <span class="song__name" @click="onSelect()">{{song.title}}</span>
      <span class="song__duration">{{song.duration}}</span>
      <span class="icon song__actions-icon" v-show="hasOtherActions" @click="toggleShowActions()"></span>
    </div>
    <div class="song__actions" v-if="actionsVisible">
      <button
        class='song__action-button'
        v-for="action in otherActions"
        @click.prevent="onSongAction(action.name)"
        type="button"
        :key="action.name">
        {{action.label}}
      </button>
    </div>
  </div>
</template>

<script>
const POSSIBLE_OTHER_ACTIONS = [
  { name: 'remove', label: 'Quitar', validator: song => true },
  { name: 'download', label: 'Solo descargar', validator: song => !song.available },
  { name: 'playnext', label: 'Reproducir siguiente', validator: song => song.available }
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
      var ret = POSSIBLE_OTHER_ACTIONS.filter(
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

<style lang="scss" scoped>
.song {
  .song__body {
    display: flex;
    flex-direction: row;
    align-items: center;
  }

  &--clickable {
    .song__name {
      cursor: pointer;
    }

    .song__body {
      &:active {
        background: linear-gradient(90deg, white, rgba(193, 193, 193, 0.1), white);
      }
    }
  }

  &--not-available {
    .song__name {
      opacity: 0.6;
    }
  }

  .song__position {
    margin-right: 10px
  }

  .song__name {
    flex: 1;
    font-size: 0.8em;
    text-overflow: clip;
    padding-top: 10px;
    padding-bottom: 10px;
  }

  .song__actions-icon {
    content: url("/static/icons/more.svg");
  }

  .song__actions {
    border-top: 1px solid rgba(178, 178, 178, 0.23);
    display: flex;
    flex: row;
    justify-content: space-around;
  }

  .song__action-button {
    border: none;
    padding: 0 10px;
    margin: 0;
  }
}
</style>
