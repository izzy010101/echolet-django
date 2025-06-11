<template>
  <div>
    <h1>Ovo je test Vue komponenta</h1>
    <p>{{ message }}</p>
  </div>
</template>

<script>
export default {
  props: {
    message: String
  }
}
</script>