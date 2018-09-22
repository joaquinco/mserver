<template>
    <div class='notification-wrapper d-flex' @click='toggleNotificationTab()'>
        <span class='icon icon-notification noselect'>i</span>
        <span class='notification-badge' v-if='showBadge'>{{notifications.length}}</span>
    </div>
</template>

<script>
import { mapState, mapMutations } from 'vuex'

export default {
  name: 'NotificationsButton',
  computed: {
    ...mapState({
      notifications: state => state.async.notifications
    }),
    showBadge() {
      return this.notifications.length
    }
  },
  data() {
    return {}
  },
  methods: {
    ...mapMutations(['toggleNotificationTab'])
  }
}
</script>

<style scoped>
.icon-notification {
  content: url("/static/icons/info.svg");
}

.notification-wrapper {
  cursor: pointer;
  position: relative;
  vertical-align: middle;
}

.notification-badge {
  border-radius: 50%;
  background-color: red;
  color: white;
  font-size: 7px;
  padding: 2px 6px;
  position: absolute;
  top: -1px;
  right: -6px;
}
</style>
