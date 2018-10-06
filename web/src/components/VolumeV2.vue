<template>
    <div class='volume'>
      <span class='icon icon--sm volume__toggle' @click='toggle()'/>
      <div v-if="isOpen" class='volume__control'>
        <RangeInput :value='value' :max='max' :min='min' @change='onValueChange'/>
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
    }
  },
  data () {
    return {
      isOpen: false
    }
  },
  methods: {
    toggle() {
      this.isOpen = !this.isOpen
    },
    onValueChange(value) {
      this.$emit('change', value)
    }
  }
}
</script>

<style lang="scss">
.volume {
    position: relative;

    &__control {
      padding: 15px 10px 10px 10px;
      position: absolute;
      width: 200px;
      bottom: 100px;
      left: -90px;
      background: white;
      box-shadow: 0px 0px 5px #919191;
      -ms-transform: rotate(270deg); /* IE 9 */
      -webkit-transform: rotate(270deg); /* Safari */
      transform: rotate(270deg);
    }

    &__toggle {
      content: url('/static/icons/volume.svg');
    }
}
</style>
