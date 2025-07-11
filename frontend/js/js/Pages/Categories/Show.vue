<script setup>
import Header from '@/Components/Header.vue'
import Footer from '@/Components/Footer.vue'
import {Head} from "@inertiajs/vue3";

const props = defineProps({
    auth: Object,
    category: Object,
    posts: Array,
    categories: Array,
})
</script>

<template>
    <Head title="Show Categories" />
    <div class="min-h-screen bg-white dark:bg-gray-900 text-gray-900 dark:text-white transition-colors duration-300">
        <Header :auth="auth" />

        <main class="py-12 px-4 max-w-5xl mx-auto">
            <h1 class="text-3xl font-bold mb-6">Posts in {{ category.name }}</h1>

            <div class="space-y-4">
                <div
                    v-for="post in posts"
                    :key="post.id"
                    class="p-4 border rounded-lg dark:border-gray-700"
                >
                    <h2 class="text-xl font-semibold">{{ post.title }}</h2>
                    <p class="text-sm text-gray-600 dark:text-gray-400">{{ post.excerpt }}</p>
                </div>
            </div>
        </main>

        <Footer :categories="categories" />
    </div>
</template>
