<template>
  <div class='container-sm d-flex flex-column justfy-content-around h-100vh'>
    <SearchToggle class='mt-3'/>
    <Playlist class="player-content mt-3"/>
    <PlayerControls/>
    <Notifications/>
  </div>
</template>
<script>
import PlayerControls from "@/components/PlayerControls";
import SearchToggle from "@/components/SearchToggle";
import Playlist from "@/components/Playlist";
import Notifications from "@/components/Notifications";

export default {
  name: "Player",
  components: {
    PlayerControls,
    SearchToggle,
    Playlist,
    Notifications
  },
  data() {
    return {};
  }
};
</script>

<style scoped>
.player-content {
  flex: 1;
}
</style>
