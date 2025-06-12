<script setup>
import AppLayout from '@/Layouts/AppLayout.vue'
import { Head } from '@inertiajs/vue3';
import { Link } from '@inertiajs/vue3'
const props = defineProps({
  featured: Object,
  posts: Array,
  auth: Object,
})

</script>

<template>
  <Head title="Home" />
  <AppLayout :auth="auth">
      <div class="min-h-screen bg-white dark:bg-gray-900 transition-colors duration-300">
      <section class="py-16 lg:py-24">
        <div class="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
          <div class="text-center mb-16">
            <h1 class="text-4xl lg:text-6xl font-bold text-gray-900 mb-6 leading-tight">
              Welcome to Echolet
            </h1>
            <p class="text-xl text-gray-600 max-w-3xl mx-auto leading-relaxed">
              Stories, insights, and advice from developers and founders building in the modern web.
            </p>
          </div>

          <!-- Featured Article -->
          <div v-if="featured" class="bg-gray-50 rounded-2xl p-8 lg:p-12 mb-16">
            <div class="grid lg:grid-cols-2 gap-12 items-center">
              <div>
                <h2 class="text-3xl lg:text-4xl font-bold text-gray-900 mb-4 leading-tight">
                  {{ featured.title }}
                </h2>
                <p class="text-lg text-gray-600 mb-6 leading-relaxed">
                  {{ featured.excerpt }}
                </p>
                <p class="text-sm text-gray-500 mb-2">
                  Published: {{ new Date(featured.published_at).toLocaleDateString() }}
                </p>
                <p class="text-sm text-gray-500 mb-8">
                  Author ID: {{ featured.user_id }}
                </p>
                <button class="inline-flex items-center px-6 py-3 bg-gray-900 text-white font-medium rounded-lg hover:bg-gray-800 transition-colors">
                  Read Full Story
                </button>
              </div>
              <div class="relative">
                <img :src="featured.image ?? '/images/sample.jpg'" alt="Featured" class="rounded-xl shadow-lg" />
              </div>
            </div>
          </div>

          <!-- Latest Stories -->
          <div class="grid lg:grid-cols-3 gap-8">
            <div v-for="post in posts" :key="post.id" class="bg-white p-6 rounded-lg shadow hover:shadow-lg transition">
              <h3 class="text-xl font-semibold text-gray-900 mb-2">{{ post.title }}</h3>
              <p class="text-gray-600 mb-4">{{ post.excerpt }}</p>
              <p class="text-sm text-gray-500 mb-2">
                Published: {{ new Date(post.published_at).toLocaleDateString() }}
              </p>
              <Link :href="`/posts/${post.id}/`" class="text-blue-600 hover:underline">
                Read more ->
              </Link>
            </div>
          </div>
        </div>
      </section>
    </div>
  </AppLayout>
</template>
