<script setup>
import Header from '../Components/Header.vue'
import Footer from '../Components/Footer.vue'
</script>

<template>
    <div class="min-h-screen flex flex-col bg-white dark:bg-gray-900 text-gray-900 dark:text-gray-100 transition-colors duration-300">
    <Header />

    <main class="flex-grow">
      <slot />
    </main>

    <Footer />
  </div>
</template>
