<template>
<div class='notifications' :class='{visible}'>
  <div class='d-flex flex-column justify-content-start' v-if='visible'>
    <div class='notification-header d-flex flex-row justify-content-between mx-4'>
      <strong class='mr-4'>Notificaciones</strong>
      <div>
        <a class='close mr-1' @click='clearNotifications()'>Limpiar</a>
        <a class='close' @click='toggleNotificationTab()'>Cerrar</a>
      </div>
    </div>
    <Notification v-for='obj in notifications' :noti='obj' :key='obj.id'/>
    <div v-if='notifications.length==0' class='center-text content-placeholder'>No hay notificaciones</div>
  </div>
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
      notifications: state => state.async.notifications,
      visible: state => state.views.notification_tab_visible
    })
  },
  data() {
    return {}
  },
  methods: {
    ...mapMutations(['clearNotifications', 'toggleNotificationTab'])
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
  box-shadow: 0px 0px 10px #919191;
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

.notification-header {
  border-bottom: 1px solid rgb(242, 242, 242);
  padding-bottom: 7px;
  margin-bottom: 7px;
}
</style>
