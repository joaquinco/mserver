<template>
  <div class='d-flex flex-column w-100'>
    <div class='d-flex flex-row justify-content-center player-controls'>
      <button class='button button-left'>
        <span class='prev'></span>
      </button>
      <button class='button button-center'>
        <span class='play'></span>
      </button>
      <button class='button button-right'>
        <span class='next'></span>
      </button>
    </div>
    <!-- Progress bar -->
  </div>
</template>

<script>
export default {
  name: 'PlayerControls',
  data () {
    return {}
  }
}
</script>

<style scoped>
.player-controls {
  box-sizing: border-box;
}

.button {
  padding: 10px;
  color: black;
  margin: 0;
}

.button-left {
  border-radius: 30% 0 0 30%;
}

.button-center {
  border-radius: 0;
  border-right: none;
  border-left: none;
}

.button-right {
  border-radius: 0 30% 30% 0;
}

.button,
.prev,
.next,
.play,
.pause {
  height: 50px;
  width: 60px;
}

.prev {
  background: url('../assets/icons/prev.svg')
}

.next {
  background: url('../assets/icons/next.svg')
}

.play {
  background: url('../assets/icons/play.svg')
}

.pause {
  background: url('../assets/icons/pause.svg')
}

</style>
