import { ref, onMounted } from 'vue'

const isDark = ref(false)

export function useDarkMode() {
  const toggleDarkMode = () => {
    isDark.value = !isDark.value
    document.documentElement.classList.toggle('dark', isDark.value)
    localStorage.setItem('dark-mode', isDark.value)
  }

  onMounted(() => {
    const saved = localStorage.getItem('dark-mode') === 'true'
    isDark.value = saved
    document.documentElement.classList.toggle('dark', saved)
  })

  return { isDark, toggleDarkMode }
}
