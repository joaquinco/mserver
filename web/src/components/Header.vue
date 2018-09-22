<template>
  <div class='header'>
      <h1 class='header__title'>{{title}}</h1>
      <div class='header__actions'>
        <router-link to='/search'><span class='header__entry icon icon-search'></span></router-link>
        <NotificationsButton class='header__entry'/>
    </div>
  </div>
</template>

<script>
import NotificationsButton from '@/components/NotificationsButton'

export default {
  name: 'Header',
  components: { NotificationsButton },
  props: {
    title: {
      type: String,
      required: false,
      default: ''
    }
  }
}
</script>

<style lang='scss' scoped>
.header {
  display: flex;
  flex-direction: row;
  justify-content: space-between;

  &__entry {
    margin-left: 10px;
    margin-right: 10px;
  }

  &__title {

  }

  &__actions {
    display: flex;
    flex-direction: row;
  }
}

.icon-search {
  content: url('/static/icons/search.svg');
}
</style>
