<script setup>
import AppLayout from '@/Layouts/AppLayout.vue'
import { Head } from '@inertiajs/vue3'

defineProps({
    auth: Object,
    footerCategories: Array,
})
</script>

<template>
    <Head title="Contact" />
    <!-- Pass page flag to AppLayout so it knows not to render search bar -->
    <AppLayout :auth="auth" :footer-categories="footerCategories" page="contact">
        <div class="max-w-7xl mx-auto px-6 py-16 md:flex md:justify-between md:items-start gap-12">

            <!-- Left Side - Title -->
            <div class="md:w-1/2 space-y-6 mb-12 md:mb-0">
                <h1 class="text-5xl font-bold text-gray-800 dark:text-white">
                    Get in<br>
                    <span class="text-rose-500 dark:text-rose-400">touch.</span>
                </h1>
                <p class="text-gray-600 dark:text-gray-300 text-lg">
                    Have a question or feedback? We’d love to hear from you. Drop us a message and we’ll respond as soon as we can.
                </p>
            </div>

            <!-- Right Side - Contact Info -->
            <div class="md:w-1/2 space-y-8 text-sm">
                <div class="flex items-start gap-4">
                    <svg class="w-6 h-6 text-rose-500 dark:text-rose-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                              d="M17.657 16.657L13.414 20.9a2 2 0 01-2.828 0L6.343 16.657A8 8 0 1117.657 16.657z" />
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                              d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                    </svg>
                    <div>
                        <h3 class="font-semibold text-base text-gray-900 dark:text-white">Address</h3>
                        <p class="text-gray-600 dark:text-gray-300">Echolet HQ</p>
                        <p class="text-gray-600 dark:text-gray-300">Bulevar Kralja Aleksandra 73, Belgrade</p>
                    </div>
                </div>

                <div class="flex items-start gap-4">
                    <svg class="w-6 h-6 text-rose-500 dark:text-rose-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                              d="M3 5a2 2 0 012-2h3l2 5-2 2c1.5 3 4.5 6 8 7l2-2 5 2v3a2 2 0 01-2 2h-1C10 22 2 14 2 6V5z" />
                    </svg>
                    <div>
                        <h3 class="font-semibold text-base text-gray-900 dark:text-white">Phone</h3>
                        <p class="text-gray-600 dark:text-gray-300">+381 64 123 4567</p>
                    </div>
                </div>

                <div class="flex items-start gap-4">
                    <svg class="w-6 h-6 text-rose-500 dark:text-rose-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                              d="M3 8l7.89 4.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                    </svg>
                    <div>
                        <h3 class="font-semibold text-base text-gray-900 dark:text-white">Mail</h3>
                        <p class="text-gray-600 dark:text-gray-300">hello@echolet.com</p>
                    </div>
                </div>

                <div class="flex items-start gap-4">
                    <svg class="w-6 h-6 text-rose-500 dark:text-rose-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                              d="M14 10h4.764a2 2 0 011.789 2.894l-3.5 7A2 2 0 0115.263 21h-4.017c-.163 0-.326-.02-.485-.06L7 20m7-10V5a2 2 0 00-2-2h-.095c-.5 0-.905.405-.905.905 0 .714-.211 1.412-.608 2.006L7 11v9m7-10h-2M7 20H5a2 2 0 01-2-2v-6a2 2 0 012-2h2.5" />
                    </svg>
                    <div>
                        <h3 class="font-semibold text-base text-gray-900 dark:text-white">Follow Us</h3>
                        <div class="flex gap-3 mt-1">
                            <a href="#" class="text-rose-500 hover:underline dark:text-rose-400">Twitter</a>
                            <a href="#" class="text-rose-500 hover:underline dark:text-rose-400">Instagram</a>
                            <a href="#" class="text-rose-500 hover:underline dark:text-rose-400">LinkedIn</a>
                        </div>
                    </div>
                </div>
            </div>

        </div>
    </AppLayout>
</template>
