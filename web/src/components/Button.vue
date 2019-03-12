<template>
  <button :disabled="isLoading">
    <slot>Button Label</slot>
  </button>
</template>

<script>
export default {
  name: 'LoadginButton',
  props: {
    isLoading: {
      type: Boolean,
      required: false,
      default: false
    }
  }
}
</script>

<style scoepd>
</style>
