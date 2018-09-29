<template>
  <div
      class="song"
      :class="{'song--clickable': canSelect, 'song--not-available': !song.available, 'song--already-added': song.isAlreadySelected}"
  >
    <div class="song__body" @click="onSelect()">
      <strong class="song__position">{{getSongPosition(song)}}</strong>
      <span class="song__name">{{song.title}}</span>
      <span @click.stop="toggleShowActions()" class="song__toggle-actions">
        <span class="song__duration">{{song.duration}}</span>
        <span class="icon song__actions-icon" v-show="hasOtherActions"></span>
      </span>
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
    <div class="song__overlay"><span>Agregada</span></div>
  </div>
</template>

<script>
const POSSIBLE_OTHER_ACTIONS = [
  { name: 'remove', label: 'Quitar', validator: song => true },
  {
    name: 'download',
    label: 'Solo descargar',
    validator: song => !song.available
  },
  {
    name: 'playnext',
    label: 'Reproducir siguiente',
    validator: song => song.available
  }
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
      return this.actions.includes('select') && !this.song.isAlreadySelected
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
      if (this.song.isAlreadySelected) {
        return
      }

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
  &__body {
    display: flex;
    flex-direction: row;
    align-items: center;
  }

  &__overlay {
    display: none;
  }

  &--clickable {
    .song__body {
      cursor: pointer;
    }
  }

  &--not-available {
    .song__name {
      opacity: 0.6;
    }
  }

  &--already-added {
    position: relative;

    .song__name,
    .song__position,
    .song__duration,
    .song__actions-icon {
      opacity: 0.2;
    }

    .song__overlay {
      display: flex;
      flex-direction: row;
      justify-content: center;
      align-items: center;
      top: 0;
      left: 0;
      position: absolute;
      height: 100%;
      width: 100%;
      font-weight: bold;
      letter-spacing: 2px;
    }
  }

  &__position {
    margin-right: 10px;
  }

  &__name {
    flex: 1;
    font-size: 0.8em;
    text-overflow: clip;
    padding-top: 10px;
    padding-bottom: 10px;
  }

  &__actions-icon {
    content: url("/static/icons/more.svg");
    padding: 7px 1px;
  }

  &__actions {
    border-top: 1px solid rgba(178, 178, 178, 0.23);
    display: flex;
    flex: row;
    justify-content: space-around;
  }

  &__action-button {
    border: none;
    padding: 0 10px;
    margin: 0;
  }

  &__toggle-actions {
    display: flex;
    flex-direction: row;
    align-items: center;
  }
}
</style>
