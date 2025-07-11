<script setup>
defineProps({
    message: {
        type: [String, Array],
        default: '',
    },
});
</script>

<template>
    <div v-if="message" class="text-sm text-red-600 mt-1">
        <p v-if="typeof message === 'string'">{{ message }}</p>
        <ul v-else>
            <li v-for="(msg, index) in message" :key="index">{{ msg }}</li>
        </ul>
    </div>
</template>
