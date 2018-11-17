<template>
  <div class='header' :class="{'header--fixed':fixed}">
    <slot></slot>
    <div class='container-sm header__content'>
      <h1 class='header__title'>{{title}}</h1>
      <div class='header__actions'>
        <router-link to='/search' class='header__entry'><div class='icon icon-search'></div></router-link>
        <NotificationsButton class='header__entry'/>
      </div>
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
    },
    fixed: {
      default: true
    }
  }
}
</script>

<style lang='scss' scoped>
.header {
  box-shadow: 0px 0px 5px #919191;
  background-color: white;

  > {
    transition: 300ms ease-in-out;
  }

  &--fixed {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    z-index: 100;
  }

  &__content {
    padding-top: 10px;
    padding-bottom: 10px;
    display: flex;
    flex-direction: row;
    justify-content: space-between;
  }

  &__title {
    flex: 1;
    margin-bottom: 0;
  }

  &__entry {
    margin-left: 10px;
  }

  &__actions {
    display: flex;
    flex-direction: row;
    align-items: center;
  }
}

.icon-search {
  content: url("/static/icons/search.svg");
}
</style>
