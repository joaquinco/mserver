<template>
  <div class='d-flex flex-column w-100 mb-4'>
    <div v-if='loaded' class='d-flex flex-row justify-content-center player-controls'>
      <button class='button button-left'>
        <span class='prev'></span>
      </button>
      <button class='button button-center' @click.prevent='playPause()'>
        <span :class='{play: isPlaying, pause: !isPlaying}'></span>
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
  name: "PlayerControls",
  data() {
    return {
      isPlaying: false,
      loaded: false
    };
  },
  mounted() {
    fetchPlayerState();
  },
  methods: {
    playPause() {
      this.isPlaying = !this.isPlaying;
    },
    fetchPlayerState() {}
  }
};
</script>

<style scoped>
.player-controls {
  box-sizing: border-box;
}

.button {
  padding: 10px;
  color: black;
  margin: 0;
  height: 50px;
  width: 60px;
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

.prev,
.next,
.play,
.pause {
  height: 100%;
  width: 100%;
}

.prev {
  content: url("/static/icons/prev.svg");
}

.next {
  content: url("/static/icons/next.svg");
}

.play {
  content: url("/static/icons/play.svg");
}

.pause {
  content: url("/static/icons/pause.svg");
}
</style>
