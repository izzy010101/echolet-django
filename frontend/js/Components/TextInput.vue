<script setup>
import { onMounted, ref } from 'vue'

const model = defineModel({
  type: String,
  required: true,
})

const input = ref(null)

onMounted(() => {
  if (input.value.hasAttribute('autofocus')) {
    input.value.focus()
  }
})

defineExpose({ focus: () => input.value.focus() })
</script>

<template>
  <input
    class="w-full rounded-lg border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-800 text-gray-900 dark:text-white placeholder:text-gray-400 dark:placeholder:text-gray-500
           focus:outline-none focus:ring-2 focus:ring-purple-500 dark:focus:ring-purple-400 transition duration-200"
    v-model="model"
    ref="input"
  />
</template>
