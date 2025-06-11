<script setup>
import {ref} from 'vue'
import {Link, router, usePage} from '@inertiajs/vue3'
import {useDarkMode} from '@/Composables/useDarkMode'
import {Moon, Sun} from 'lucide-vue-next'
import Dropdown from '@/Components/Dropdown.vue'
import DropdownLink from '@/Components/DropdownLink.vue'

const {props} = usePage()
const user = props.auth?.user
const search = ref('')

const {isDark, toggleDarkMode} = useDarkMode()
const mobileMenuOpen = ref(false)

console.log(user)

function logout() {
  router.post('/logout/', {}, {
    onFinish: () => {
      router.visit('/', { replace: true })
    }
  })
}
</script>

<template>
  <header
      class="sticky top-0 z-50 bg-white/90 backdrop-blur border-b border-gray-200 dark:bg-gray-900/90 dark:border-gray-800 shadow-sm">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex items-center justify-between h-16">

      <!-- Logo -->
      <Link href="/" class="text-xl font-bold text-gray-900 dark:text-white">
        Echolet
      </Link>

      <!-- Desktop Navigation -->
      <nav class="hidden md:flex items-center space-x-6">
        <Link href="/" class="text-gray-700 dark:text-gray-300 hover:text-pink-500 dark:hover:text-pink-400 transition">
          Home
        </Link>
        <Link href="/topics"
              class="text-gray-700 dark:text-gray-300 hover:text-pink-500 dark:hover:text-pink-400 transition">Topics
        </Link>
        <Link href="/about"
              class="text-gray-700 dark:text-gray-300 hover:text-pink-500 dark:hover:text-pink-400 transition">About
        </Link>
      </nav>

      <!-- Hamburger (mobile only) -->
      <div class="md:hidden">
        <button @click="mobileMenuOpen = !mobileMenuOpen"
                class="p-2 rounded-md text-gray-700 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-gray-800 focus:outline-none focus:ring-2 focus:ring-pink-500">
          <svg v-if="!mobileMenuOpen" class="w-6 h-6" fill="none" stroke="currentColor" stroke-width="2"
               viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" d="M4 6h16M4 12h16M4 18h16"/>
          </svg>
          <svg v-else class="w-6 h-6" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12"/>
          </svg>
        </button>
      </div>

      <!-- Actions -->
      <div class="hidden md:flex items-center space-x-3">
        <input
            type="text"
            v-model="search"
            placeholder="Search..."
            class="px-3 py-1.5 rounded-md border border-gray-300 bg-white text-sm text-gray-800 placeholder:text-gray-400 dark:bg-gray-800 dark:text-white dark:border-gray-700 focus:outline-none focus:ring-2 focus:ring-primary"
        />

        <button @click="toggleDarkMode" class="p-2 rounded hover:bg-gray-100 dark:hover:bg-gray-800 transition"
                aria-label="Toggle dark mode">
          <Sun v-if="isDark" class="w-5 h-5 text-yellow-400"/>
          <Moon v-else class="w-5 h-5 text-gray-600 dark:text-gray-300"/>
        </button>

        <template v-if="!user">
          <Link href="/login" class="text-sm text-gray-700 dark:text-gray-300 hover:underline">Login</Link>
          <Link href="/register" class="text-sm text-gray-700 dark:text-gray-300 hover:underline">Register</Link>
        </template>

        <template v-if="user">
          <span class="text-sm text-gray-700 dark:text-gray-300 mr-2">Welcome, {{ user.first_name || user.email }}</span>
          <button @click="logout" class="text-sm text-red-600 dark:text-red-400 hover:underline">Logout</button>
        </template>

        <template v-else>
          <Dropdown>
            <template #trigger>
              <button
                  class="flex items-center text-sm font-medium text-gray-700 dark:text-gray-300 hover:text-black dark:hover:text-white focus:outline-none">
                <span>{{ user.name }}</span>
                <svg class="ml-1 w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/>
                </svg>
              </button>
            </template>

            <template #content>
              <DropdownLink :href="route('profile.edit')">Profile</DropdownLink>
              <button @click="logout"
                      class="block w-full px-4 py-2 text-start text-sm text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-800 transition">
                Log Out
              </button>
            </template>
          </Dropdown>
        </template>
      </div>
    </div>

    <!-- Mobile Menu -->
    <div v-if="mobileMenuOpen" class="md:hidden px-4 pb-4 space-y-2 bg-white dark:bg-gray-900 shadow">
      <div class="flex justify-end">
        <button @click="toggleDarkMode" class="p-2 rounded hover:bg-gray-100 dark:hover:bg-gray-800 transition">
          <Sun v-if="isDark" class="w-5 h-5 text-yellow-400"/>
          <Moon v-else class="w-5 h-5 text-gray-600 dark:text-gray-300"/>
        </button>
      </div>

      <Link href="/" class="block text-gray-700 dark:text-gray-300 hover:text-pink-500 dark:hover:text-pink-400">Home
      </Link>
      <Link href="/topics" class="block text-gray-700 dark:text-gray-300 hover:text-pink-500 dark:hover:text-pink-400">
        Topics
      </Link>
      <Link href="/about" class="block text-gray-700 dark:text-gray-300 hover:text-pink-500 dark:hover:text-pink-400">
        About
      </Link>

      <template v-if="!user">
        <Link href="/login" class="block text-gray-700 dark:text-gray-300 hover:text-pink-500 dark:hover:text-pink-400">
          Login
        </Link>
        <Link href="/register"
              class="block text-gray-700 dark:text-gray-300 hover:text-pink-500 dark:hover:text-pink-400">Register
        </Link>
      </template>

      <template v-else>
        <Link :href="route('profile.edit')"
              class="block text-gray-700 dark:text-gray-300 hover:text-pink-500 dark:hover:text-pink-400">Profile
        </Link>
        <button @click="logout"
                class="block w-full text-left text-gray-700 dark:text-gray-300 hover:text-pink-500 dark:hover:text-pink-400">
          Logout
        </button>
      </template>
    </div>
  </header>
</template>
