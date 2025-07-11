<template>
  <div class="grid grid-cols-4 gap-4">
    <div 
      v-for="color in colors" 
      :key="color"
      :class="[
        'h-10 w-10 rounded-full cursor-pointer border-4 transition-all',
        color === selectedColor ? 'border-black dark:border-white scale-110' : 'border-transparent'
      ]"
      :style="{ backgroundColor: themeMap[color] }"
      @click="updateColor(color)"
    />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const colors = ['blue', 'emerald', 'rose', 'amber', 'violet', 'indigo']
const themeMap = {
  blue: '#3b82f6',
  emerald: '#10b981',
  rose: '#f43f5e',
  amber: '#f59e0b',
  violet: '#8b5cf6',
  indigo: '#6366f1',
}

const selectedColor = ref('blue')

onMounted(async () => {
  const res = await axios.get('/api/user/theme-color')
  selectedColor.value = res.data.theme_color
  document.documentElement.style.setProperty('--primary-color', themeMap[selectedColor.value])
})

const updateColor = async (color) => {
  selectedColor.value = color
  document.documentElement.style.setProperty('--primary-color', themeMap[color])
  await axios.put('/api/user/theme-color', { theme_color: color })
}
</script>
