<script setup>
import Header from '@/Components/Header.vue'
import Footer from '@/Components/Footer.vue'
</script>

<template>
  <div class="min-h-screen flex flex-col bg-white dark:bg-gray-900">
    <Header />

    <main class="flex-grow">
      <slot />
    </main>

    <Footer />
  </div>
</template>
