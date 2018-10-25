<template>
    <div class='volume'>
      <span class='icon icon--sm volume__toggle' @click='toggle()'/>
      <div v-if="isOpen" class='volume__control'  @touchmove.stop>
        <RangeInput :value='value' :max='max' :min='min' @change='onValueChange'/>
        <span class='volume__value'>{{value}}%</span>
      </div>
    </div>
</template>

<script>
import RangeInput from '@/components/RangeInput'

export default {
  name: 'VolumeV2',
  components: { RangeInput },
  props: {
    value: {
      default: 50
    },
    change: {
      type: Function,
      required: false
    },
    max: {
      type: Number,
      default: 100
    },
    min: {
      type: Number,
      default: 0
    },
    step: {
      type: Number,
      default: 1
    },
    closeOnClickOutside: {
      default: true
    }
  },
  data () {
    return {
      isOpen: false
    }
  },
  mounted() {
    if (this.closeOnClickOutside) {
      window.addEventListener('click', this.onWindowClick)
    }
  },
  destroyed() {
    if (this.closeOnClickOutside) {
      window.removeEventListener('click', this.onWindowClick)
    }
  },
  methods: {
    toggle() {
      this.isOpen = !this.isOpen
    },
    onValueChange(value) {
      this.$emit('change', value)
    },
    onWindowClick (event) {
      if (!this.$el.contains(event.target)) {
        this.isOpen = false
      }
    }
  }
}
</script>

<style lang="scss">
.volume {
    position: relative;

    &__control {
      display: flex;
      flex-direction: row;
      padding: 15px 35px 15px 20px;
      position: absolute;
      width: 240px;
      bottom: 120px;
      left: -112px;
      background: white;
      box-shadow: 0px 0px 5px #919191;
      transform: rotate(270deg);
    }

    &__value {
      position: absolute;
      right: 0;
      top: 57%;
      transform: rotate(90deg) translateX(-50%);
    }

    &__toggle {
      content: url('/static/icons/volume.svg');
    }
}
</style>
