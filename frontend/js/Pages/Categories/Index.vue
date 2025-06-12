<script setup>
import Header from '@/Components/Header.vue'
import Footer from '@/Components/Footer.vue'
import {Head, Link} from '@inertiajs/vue3'
import { ref, computed } from 'vue'

const props = defineProps({
    auth: Object,
    categories: Array,
})

const currentIndex = ref(0)
const currentCategory = computed(() => props.categories[currentIndex.value])

function selectCategory(index) {
    currentIndex.value = index
}

console.log(props.categories)
console.log(currentCategory)

</script>

<template>
    <Head title="Categories Index" />
    <div class="min-h-screen bg-gradient-to-br from-[#e3e3e3] to-[#ffffff] dark:from-gray-900 dark:to-black transition-colors duration-300">
        <Header :auth="auth" />

        <main class="max-w-7xl mx-auto px-4 py-20 flex gap-10">
            <!-- Left: Categories List -->
            <nav class="w-1/3 overflow-y-auto max-h-[80vh] border-r border-gray-300 dark:border-gray-700 pr-4">
                <h1 class="text-4xl font-extrabold text-gray-800 dark:text-white mb-6">Categories</h1>

                <ul class="space-y-6">
                    <li
                        v-for="(category, index) in categories"
                        :key="category.id"
                        @click="selectCategory(index)"
                        :class="[
              'cursor-pointer flex items-center gap-4 p-3 rounded-xl transition-all',
              index === currentIndex ? 'bg-white/80 dark:bg-white/20 shadow-lg scale-105' : 'hover:bg-white/30 dark:hover:bg-white/10'
            ]"
                    >
                        <img
                            :src="category.image || '/placeholder.svg'"
                            alt=""
                            class="w-16 h-16 object-cover rounded-lg flex-shrink-0"
                        />
                        <div>
                            <h2 class="text-xl font-semibold text-gray-900 dark:text-white">{{ category.name }}</h2>
                            <p class="text-gray-600 dark:text-gray-300 text-sm max-w-xs truncate">{{ category.description }}</p>
                        </div>
                    </li>
                </ul>
            </nav>

            <!-- Right: Posts for Selected Category -->
            <section class="flex-1 overflow-y-auto max-h-[80vh] p-4 bg-gray-50 dark:bg-gray-900 rounded-2xl shadow-lg">
                <h2 class="text-3xl font-bold mb-8 text-gray-900 dark:text-white">
                    Posts in "{{ currentCategory.name }}"
                </h2>

                <div
                    v-if="currentCategory.posts && currentCategory.posts.length > 0"
                    class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6"
                >
                    <article
                        v-for="post in currentCategory.posts"
                        :key="post.id"
                        class="bg-white dark:bg-gray-800 rounded-lg shadow p-5 flex flex-col"
                    >
                        <h3 class="text-xl font-semibold mb-2 text-gray-900 dark:text-white">{{ post.title }}</h3>
                        <p class="text-gray-700 dark:text-gray-300 flex-grow">{{ post.excerpt || post.content.slice(0, 100) + '...' }}</p>
                        <Link
                            :href="route('posts.show', post.id)"
                            class="mt-4 inline-block text-primary hover:underline"
                        >
                            Read more
                        </Link>
                    </article>
                </div>

                <p v-else class="text-gray-700 dark:text-gray-300">No posts in this category yet.</p>
            </section>
        </main>

        <Footer :categories="categories" />
    </div>
</template>

<style scoped>
nav {
    scroll-behavior: smooth;
}
</style>
