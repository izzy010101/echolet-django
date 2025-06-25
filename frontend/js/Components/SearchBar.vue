<script setup>
import { ref } from 'vue'
import { router, usePage } from '@inertiajs/vue3'

const search = ref('')
const page = usePage()

function submitSearch() {
    const path = page.url
    const query = search.value.trim()

    if (!query) return

    if (path.startsWith('/dashboard')) {
        router.get('/dashboard', { q: query })
    } else if (path.startsWith('/categories')) {
        router.get('/categories', { q: query })
    } else if (path.startsWith('/blog')) {
        router.get('/blog', { q: query })
    } else {
        // Default: home page → search blog posts
        router.get('/', { q: query })
    }
}
</script>

<template>
    <form @submit.prevent="submitSearch" class="w-full">
        <input
            v-model="search"
            type="text"
            placeholder="Search..."
            class="w-full px-3 py-1.5 rounded-md border border-gray-300 bg-white text-sm text-gray-800 placeholder:text-gray-400
             dark:bg-gray-800 dark:text-white dark:border-gray-700 focus:outline-none focus:ring-2 focus:ring-rose-500 transition"
        />
    </form>
</template>
