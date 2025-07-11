<script setup>
import GuestLayout from '@/Layouts/GuestLayout.vue'
import InputError from '@/Components/InputError.vue'
import PrimaryButton from '@/Components/PrimaryButton.vue'
import TextInput from '@/Components/TextInput.vue'
import { Head, useForm } from '@inertiajs/vue3'

defineProps({
  status: String,
})

const form = useForm({
  email: '',
})

const submit = () => {
  form.post(route('password.email'))
}
</script>


<template>
  <GuestLayout>
    <Head title="Forgot Password" />

    <div class="min-h-screen flex items-center justify-center bg-gradient-to-br from-rose-50 via-pink-50 to-purple-50 dark:from-gray-900 dark:to-gray-950 p-6 transition-colors">
      <div class="w-full max-w-md bg-white/80 dark:bg-gray-800/80 backdrop-blur rounded-3xl shadow-xl border border-white/20 dark:border-gray-700 p-8 space-y-6">

        <h2 class="text-2xl font-bold text-center text-gray-800 dark:text-white">
          Forgot your password?
        </h2>
        <p class="text-sm text-gray-600 dark:text-gray-300 text-center">
          No problem. Just enter your email and we’ll send a reset link.
        </p>

        <div v-if="status" class="text-sm font-medium text-green-600 text-center">
          {{ status }}
        </div>

        <form @submit.prevent="submit" class="space-y-6">
          <div>
            <label for="email" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
              Email
            </label>
            <TextInput
                v-model="form.email"
                type="email"
                id="email"
                autocomplete="email"
                class="mt-1 block w-full rounded-lg border-gray-300 text-gray-900 placeholder-gray-400
                        focus:outline-none focus:ring-2 focus:ring-purple-500
                        dark:bg-gray-800 dark:text-white dark:border-gray-700"
                :class="{
                    'border-red-500 focus:border-red-500 focus:ring-red-500 dark:border-red-500 dark:focus:ring-red-500': form.errors.email
                }"
            />
            <InputError :message="form.errors.email" class="mt-2" />
          </div>

          <PrimaryButton
            class="w-full justify-center bg-gradient-to-r from-rose-500 to-pink-600 hover:from-rose-600 hover:to-pink-700 text-white font-semibold py-3 rounded-xl transition-all duration-200 shadow-lg"
            :class="{ 'opacity-25': form.processing }"
            :disabled="form.processing"
          >
            Email Password Reset Link
          </PrimaryButton>
        </form>
      </div>
    </div>
  </GuestLayout>
</template>
