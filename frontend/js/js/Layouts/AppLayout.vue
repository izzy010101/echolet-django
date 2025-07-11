<script setup>
import Header from '@/Components/Header.vue'
import FooterComponent from '@/Components/Footer.vue'


</script>

<template>
  <div>
    <Header />
    <main>
      <slot />
    </main>
      <FooterComponent />
  </div>
</template>
