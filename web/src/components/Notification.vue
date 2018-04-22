<template>
  <div class='d-flex flex-column notification-container align-items-start'>
    <strong class='message'>{{noti.message}}</strong>
    <span class='timestamp'>{{noti.created | moment("from", "now")}}</span>
  </div>
</template>

<script>
export default {
  name: 'Notification',
  props: {
    'noti': {
      type: Object,
      required: true
    }
  }
}
</script>

<style scoped>
.notification-container {
  padding: 5px 20px;
  background-color: white;
  margin-bottom: 2px;
}
.message {
  font-size: 1.1em;
}
.timestamp {
  color: #b2b2b2;
  font-size: 0.9em;
}
</style>
