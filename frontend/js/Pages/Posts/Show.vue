<script setup>
import Header from '@/Components/Header.vue'
import Footer from '@/Components/Footer.vue'
import { Head } from '@inertiajs/vue3'

const props = defineProps({
    post: Object,
    auth: Object,
})
</script>

<template>
    <Head :title="post.title" />

    <div class="min-h-screen bg-white dark:bg-gray-900 text-gray-900 dark:text-white">
        <Header :auth="auth" />

        <main class="max-w-4xl mx-auto p-8">
            <h1 class="text-4xl font-bold mb-6">{{ post.title }}</h1>
            <article class="prose dark:prose-invert" v-html="post.body"></article>
        </main>

        <Footer />
    </div>
</template>
