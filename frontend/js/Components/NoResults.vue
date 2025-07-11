<script setup>
import { Search } from 'lucide-vue-next'

const props = defineProps({
    message: {
        type: String,
        default: 'No results found',
    },
    subtext: {
        type: String,
        default: 'Try another keyword or explore different categories.',
    },
})
</script>

<template>
    <div class="flex justify-center items-center min-h-[40vh]">
        <div class="bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-700/40 px-10 py-12 rounded-2xl shadow-md max-w-lg w-full text-center">
            <Search class="w-10 h-10 mx-auto text-gray-400 dark:text-gray-500 mb-4" />
            <h2 class="text-2xl font-semibold text-gray-800 dark:text-white mb-2">{{ message }}</h2>
            <p class="text-sm text-gray-500 dark:text-gray-400">{{ subtext }}</p>
        </div>
    </div>
</template>
