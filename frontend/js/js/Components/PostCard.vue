<template>
    <div class="mb-8 p-6 rounded-lg shadow bg-white hover:shadow-md transition">
      <h2 class="text-xl font-semibold mb-1 text-gray-900">{{ post.title }}</h2>
      <p class="text-sm text-gray-500 mb-2">
        {{ formatDate(post.published_at) }}
      </p>
      <p class="text-gray-700">
        {{ post.excerpt }}
      </p>
    </div>
  </template>
  
  <script setup>
  defineProps({ post: Object })
  
  function formatDate(date) {
    return new Date(date).toLocaleDateString()
  }
  </script>
  