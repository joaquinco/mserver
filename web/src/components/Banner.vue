<template>
    <div class='banner d-flex justify-content-center align-items-center' :class='extraClasses' v-if='visible'>
        <span>{{text}}</span>
    </div>
</template>
<script>
import { oneOfValidator } from '@/utils'

export default {
  name: 'Banner',
  props: {
    visible: {
      default: true,
      type: Boolean
    },
    text: {
      type: String,
      required: true
    },
    type: {
      type: String,
      validator: oneOfValidator('error', 'nice'),
      required: true
    }
  },
  computed: {
    extraClasses() {
      return `banner--${this.type}`
    }
  }
}
</script>

<style lang="scss" scoped>
@import "~@/assets/variables";

.banner {
  width: 100%;
  padding: 2px;

  &--error {
    background-color: $orange;
    color: white;
  }

  &--nice {
    background-color: $skyblue;
  }
}
</style>
