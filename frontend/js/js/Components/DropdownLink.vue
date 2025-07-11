<template>
  <div class="dropdown">
    <slot></slot>
  </div>
</template>

<script>
export default {
  name: 'Dropdown',
}
</script>

<style scoped>
.dropdown {
  position: relative;
}
</style>