<template>
  <div class='container-sm d-flex flex-column justify-content-center'>
    <h1 class="color-error not-found">404 Not found :(</h1>
    <p>La ruta <strong>{{$route.path}}</strong> no es válida</p>
    <div class="d-flex flex-row justify-content-end">
      <router-link :to="{ name: 'dispatch'}">Sacame de aquí</router-link>
    </div>
  </div>
</template>

<script>
export default {
  name: 'PageNotFound'
}
</script>

<style scoped>
.not-found {
  font-size: 3em;
  font-weight: bold;
}

a {
  text-decoration: none;
}
</style>
