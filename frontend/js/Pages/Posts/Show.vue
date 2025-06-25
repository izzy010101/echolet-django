<script setup>
import Header from '@/Components/Header.vue'
import Footer from '@/Components/Footer.vue'
import { Head } from '@inertiajs/vue3'
import CommentsSection from '@/Components/Comments/CommentSection.vue'

const props = defineProps({
    post: Object,
    comments: Object,
    auth: Object,
})

console.log("props", props)
</script>

<template>
    <Head :title="post.title" />

    <div class="min-h-screen bg-white dark:bg-gray-900 text-gray-900 dark:text-white">
        <Header :auth="auth" />

        <main class="max-w-4xl mx-auto p-8">
            <h1 class="text-4xl font-bold mb-6">{{ post.title }}</h1>
            <article class="prose dark:prose-invert" v-html="post.body"></article>

            <div class="mt-12">
                <h2 class="text-2xl font-semibold mb-4">Comments</h2>

              <p>Total comments: {{ comments?.length }}</p>

                <div v-if="comments.length > 0">
                    <CommentsSection
                        :comments="comments"
                        :post-id="post.id"
                        :user="user"
                    />
                </div>

                <div
                    v-else
                    class="bg-white dark:bg-gray-900 border rounded p-4 text-gray-500 dark:text-gray-400 text-sm"
                >
                    No comments for this post yet.
                    <span v-if="!user"> Login to comment.</span>
                </div>
            </div>
        </main>

        <Footer />
    </div>
</template>
