<template>
  <div v-if="show">
    <span class="color-error error">{{message}}</span>
  </div>
</template>

<script>
export default {
  name: 'ApiError',
  props: ['errorResponse'],
  computed: {
    message () {
      let message = ''
      if (this.errorResponse) {
        let error = this.errorResponse
        if (error.response) {
          let status = error.response.status
          switch (status) {
            case 401: case 403: {
              message = 'Mira no te puedo dejar pasar con esos datos'
              break
            }
            case 500: {
              message = 'Pa se rompio todo'
              break
            }
            case 200: case 201: case 203:
            {
              message = ''
              break
            }
            default: {
              message = 'Esto es un error que no tuve en cuenta noverda'
            }
          }
          if (message) {
            message = `${message} (${status})`
          }
        } else if (error.request) {
          message = 'El servidor no estaría respondiendo'
        } else {
          message = 'Error! Esto está mal programado'
        }
      }
      return message
    },
    show () {
      return Boolean(this.message)
    }
  }
}
</script>

<style scoped>
.error {
  font-size: 1.1em;
}
</style>
