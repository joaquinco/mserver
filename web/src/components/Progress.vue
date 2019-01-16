<template>
    <div class='progress' :style="{width: percentage + '%'}"></div>
</template>

<script>
export default {
  name: 'Progress',
  props: {
    percentage: {
      type: Number,
      required: true
    }
  }
}
</script>

<style lang="scss" scoped>
.progress {
  border-top: #e46f89 2px solid;
  position: absolute;
  left: 0;
  top: 0;
}
</style>
