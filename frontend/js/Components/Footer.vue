<script setup>
import { BookOpen, Facebook, Twitter, Instagram, Linkedin} from 'lucide-vue-next';
import {Link, usePage } from '@inertiajs/vue3';
import NewsletterSubscribe from '@/Components/NewsletterSubscribe.vue';

const { props } = usePage()
const categories = props.categories || []

</script>

<template>
    <footer class="bg-gray-50 dark:bg-gray-900 text-gray-700 dark:text-gray-300">
        <div class="max-w-7xl mx-auto px-4 py-12">

            <!-- Main Grid -->
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8 mb-12">

                <!-- Brand -->
                <div>
                    <div class="flex items-center space-x-2 mb-2">
                        <BookOpen class="h-8 w-8 text-pink-500" />
                        <span class="text-xl font-bold text-black dark:text-white">Echolet</span>
                    </div>
                    <p class="text-sm text-gray-600 dark:text-gray-400">
                        Insightful stories from founders. Stay inspired and informed with the latest in tech, business, and ideas.
                    </p>
                    <div class="flex space-x-4 mt-4">
                        <a href="#" class="hover:text-pink-500 dark:hover:text-pink-400 transition"><Facebook class="h-5 w-5" /></a>
                        <a href="#" class="hover:text-pink-500 dark:hover:text-pink-400 transition"><Twitter class="h-5 w-5" /></a>
                        <a href="#" class="hover:text-pink-500 dark:hover:text-pink-400 transition"><Instagram class="h-5 w-5" /></a>
                        <a href="#" class="hover:text-pink-500 dark:hover:text-pink-400 transition"><Linkedin class="h-5 w-5" /></a>
                    </div>
                </div>

                <!-- Navigation -->
                <div>
                    <h3 class="text-sm font-semibold text-black dark:text-white uppercase mb-3">Explore</h3>
                    <ul class="space-y-2 text-sm">
                        <li><Link href="/" class="hover:text-pink-500 dark:hover:text-pink-400">Home</Link></li>
                        <li><Link href="/topics" class="hover:text-pink-500 dark:hover:text-pink-400">Topics</Link></li>
                        <li><Link href="/about" class="hover:text-pink-500 dark:hover:text-pink-400">About</Link></li>
                        <li><Link href="/contact" class="hover:text-pink-500 dark:hover:text-pink-400">Contact</Link></li>
                    </ul>
                </div>

                <!-- Categories -->
                <div>
                    <h3 class="text-sm font-semibold text-black dark:text-white uppercase mb-3">Categories</h3>
                    <ul class="space-y-2 text-sm">
                        <li v-for="category in categories" :key="category.id">
                            <a href="#" class="hover:text-pink-500 dark:hover:text-pink-400">
                                {{ category.name }}
                            </a>
                        </li>
                    </ul>
                </div>

                <!-- Newsletter -->
                <div>
                    <h3 class="text-sm font-semibold text-black dark:text-white uppercase mb-3">Subscribe</h3>
                    <p class="text-sm text-gray-600 dark:text-gray-400 mb-4">Get the latest stories straight to your inbox.</p>
                    <div class="bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg p-4 shadow-sm">
                        <NewsletterSubscribe />
                    </div>
                </div>

            </div>

            <!-- Separator -->
            <div class="border-t border-gray-200 dark:border-gray-800 pt-6 flex flex-col md:flex-row justify-between items-center text-sm text-gray-500 dark:text-gray-400">
                <p>&copy; {{ new Date().getFullYear() }} Echolet. All rights reserved.</p>
                <div class="mt-4 md:mt-0 flex space-x-6">
                    <a href="#" class="hover:text-pink-500 dark:hover:text-pink-400">Privacy</a>
                    <a href="#" class="hover:text-pink-500 dark:hover:text-pink-400">Terms</a>
                    <a href="#" class="hover:text-pink-500 dark:hover:text-pink-400">Cookies</a>
                </div>
            </div>
        </div>
    </footer>
</template>


