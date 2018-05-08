<template>
<div class='notifications' :class='{visible}'>
  <div class='d-flex flex-column justify-content-start' v-if='visible'>
    <div class='d-flex flex-row justify-content-between mx-4'>
      <strong class='mr-4'>Notificaciones</strong>
      <div>
        <span class='close mr-1' @click='clearNotifications()'>Limpiar</span>
        <span class='close' @click='toggleView()'>Cerrar</span>
      </div>
    </div>
    <Notification v-for='obj in notifications' :noti='obj' :key='obj.id'/>
    <div v-if='notifications.length==0' class='center-text content-placeholder'>No hay notificaciones</div>
  </div>
  <span class='toggle color-error' v-if='!visible' @click='toggleView()'>
    {{notifications.length}}
  </span>
</div>
</template>

<script>
import { mapState, mapMutations } from 'vuex'
import Notification from '@/components/Notification'

export default {
  name: 'Notifications',
  components: { Notification },
  computed: {
    ...mapState({
      notifications: (state) => state.async.notifications
    })
  },
  data () {
    return {
      visible: false
    }
  },
  methods: {
    ...mapMutations(['clearNotifications']),
    toggleView () {
      this.visible = !this.visible
    }
  }
}
</script>

<style scoped>
.notifications {
  position: fixed;
  right: 10px;
  top: 10px;
  z-index: 3;
}
.toggle {
  border-radius: 10px;
  box-shadow: -2px 2px 4px #919191;
  font-size: 1.5em;
  padding: 5px 10px;
  cursor: pointer;
  user-select: none;
  background-color: white;
}
.toggle:hover {
  font-weight: bold;
}
.visible {
  background-color: white;
  box-shadow: -1px 1px 1px #919191;
  padding: 10px 0;
  overflow-y: auto;
  max-height: 100%;
  top: 0;
  right: 0;
}

@media (max-width: 576px) {
  .visible {
    width: 100vw;
  }
}
</style>
