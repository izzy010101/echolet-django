<script setup>
import GuestLayout from '@/Layouts/GuestLayout.vue';
import InputError from '@/Components/InputError.vue';
import PrimaryButton from '@/Components/PrimaryButton.vue';
import { Head, Link, useForm } from '@inertiajs/vue3';
import { User, Mail, Lock, LogIn } from 'lucide-vue-next';
import { ref, watch } from 'vue';
import debounce from 'lodash/debounce';

const props = defineProps({
  errors: {
    type: Object,
    default: () => ({}),
  },
  status: String,
  old_input: {
    type: Object,
    default: () => ({}),
  },
  csrf_token: String,
});

const form = useForm({
  name: props.old_input?.name || '',
  email: props.old_input?.email || '',
  password: '',
  password_confirmation: '',
  _token: props.csrf_token,
});

const validationErrors = ref({
  name: '',
  email: '',
  password: '',
  password_confirmation: '',
});

const touched = ref({
  name: false,
  email: false,
  password: false,
  password_confirmation: false,
});

watch(() => form.errors, (errors) => {
  validationErrors.value.name = errors.name || '';
  validationErrors.value.email = errors.email || '';
  validationErrors.value.password = errors.password || '';
  validationErrors.value.password_confirmation = errors.password_confirmation || '';
});

watch(() => form.name, debounce((val) => {
  if (!val) validationErrors.value.name = 'Name is required.';
  else validationErrors.value.name = '';
}, 300));

watch(() => form.email, debounce((val) => {
  if (!val) validationErrors.value.email = 'Email is required.';
  else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(val)) validationErrors.value.email = 'Please enter a valid email.';
  else validationErrors.value.email = '';
}, 300));

watch(() => form.password, (val) => {
  if (!val) validationErrors.value.password = 'Password is required.';
  else if (val.length < 6) validationErrors.value.password = 'Password must be at least 6 characters.';
  else validationErrors.value.password = '';
});

watch(() => form.password_confirmation, (val) => {
  if (!val) validationErrors.value.password_confirmation = 'Confirmation is required.';
  else if (val !== form.password) validationErrors.value.password_confirmation = 'Passwords do not match.';
  else validationErrors.value.password_confirmation = '';
});

const submit = () => {
  form.post('/register/', {
    onFinish: () => {
      form.reset('password', 'password_confirmation');
    },
  });
};
</script>



<template>
  <GuestLayout>
    <Head title="Register" />

    <div class="min-h-screen bg-gradient-to-br from-rose-50 via-pink-50 to-purple-50 dark:from-gray-900 dark:to-gray-950 flex items-center justify-center p-4">
      <div class="w-full max-w-md space-y-6">
        <div class="text-center">
          <div class="inline-flex items-center justify-center w-16 h-16 bg-gradient-to-r from-purple-500 to-rose-400 rounded-2xl mb-4 shadow-lg">
            <User class="w-8 h-8 text-white" />
          </div>
          <h1 class="text-3xl font-bold bg-gradient-to-r from-gray-900 to-gray-600 bg-clip-text text-transparent dark:from-white dark:to-gray-300">
            Create Your Account
          </h1>
          <p class="text-gray-600 dark:text-gray-400 mt-2">Sign up to get started</p>
        </div>

        <div v-if="status" class="text-sm font-medium text-green-600 text-center">{{ status }}</div>

        <div class="bg-white/80 dark:bg-gray-800/80 backdrop-blur-sm rounded-3xl shadow-xl border border-white/20 dark:border-gray-700 p-8">
          <form @submit.prevent="submit" class="space-y-6">
            <div>
              <label class="text-sm font-semibold text-gray-700 dark:text-white flex items-center gap-2">
                <User class="w-4 h-4 text-purple-500" />
                Name
              </label>
              <input
                v-model="form.name"
                type="text"
                autocomplete="name"
                placeholder="Your full name"
                @blur="touched.name = true"
                class="w-full px-4 py-3 border rounded-xl focus:outline-none mt-1 bg-gray-50 dark:bg-gray-900 text-gray-900 dark:text-white"
                :class="[
                  validationErrors.name ? 'border-red-500 focus:ring-red-500' : 'border-gray-200 dark:border-gray-600 focus:ring-purple-500'
                ]"
              />
              <InputError class="mt-2" :message="validationErrors.name" />
            </div>

            <div>
              <label class="text-sm font-semibold text-gray-700 dark:text-white flex items-center gap-2">
                <Mail class="w-4 h-4 text-purple-500" />
                Email Address
              </label>
              <input
                v-model="form.email"
                type="email"
                autocomplete="username"
                placeholder="you@example.com"
                @blur="touched.email = true"
                class="w-full px-4 py-3 border rounded-xl focus:outline-none mt-1 bg-gray-50 dark:bg-gray-900 text-gray-900 dark:text-white"
                :class="[
                  validationErrors.email ? 'border-red-500 focus:ring-red-500' : 'border-gray-200 dark:border-gray-600 focus:ring-purple-500'
                ]"
              />
              <InputError class="mt-2" :message="validationErrors.email" />
            </div>

            <div>
              <label class="text-sm font-semibold text-gray-700 dark:text-white flex items-center gap-2">
                <Lock class="w-4 h-4 text-purple-500" />
                Password
              </label>
              <input
                v-model="form.password"
                type="password"
                autocomplete="new-password"
                placeholder="Choose a password"
                @blur="touched.password = true"
                class="w-full px-4 py-3 border rounded-xl focus:outline-none mt-1 bg-gray-50 dark:bg-gray-900 text-gray-900 dark:text-white"
                :class="[
                  validationErrors.password ? 'border-red-500 focus:ring-red-500' : 'border-gray-200 dark:border-gray-600 focus:ring-purple-500'
                ]"
              />
              <InputError class="mt-2" :message="validationErrors.password" />
            </div>

            <div>
              <label class="text-sm font-semibold text-gray-700 dark:text-white flex items-center gap-2">
                <Lock class="w-4 h-4 text-purple-500" />
                Confirm Password
              </label>
              <input
                v-model="form.password_confirmation"
                type="password"
                autocomplete="new-password"
                placeholder="Repeat your password"
                @blur="touched.password_confirmation = true"
                class="w-full px-4 py-3 border rounded-xl focus:outline-none mt-1 bg-gray-50 dark:bg-gray-900 text-gray-900 dark:text-white"
                :class="[
                  validationErrors.password_confirmation ? 'border-red-500 focus:ring-red-500' : 'border-gray-200 dark:border-gray-600 focus:ring-purple-500'
                ]"
              />
              <InputError class="mt-2" :message="validationErrors.password_confirmation" />
            </div>

            <PrimaryButton
              class="w-full justify-center bg-gradient-to-r from-purple-500 to-rose-400 hover:from-purple-600 hover:to-rose-500 text-white font-semibold py-3 rounded-xl transition-all duration-200 shadow-lg"
              :class="{ 'opacity-25': form.processing }"
              :disabled="form.processing"
            >
              <span class="flex items-center justify-center gap-2">
                <LogIn class="w-5 h-5" />
                Sign Up
              </span>
            </PrimaryButton>
          </form>

          <p class="text-center text-sm text-gray-600 dark:text-gray-300 mt-6">
            Already have an account?
            <Link href="/login" class="font-medium text-purple-500 hover:text-purple-600">Log in here</Link>
          </p>
        </div>
      </div>
    </div>
  </GuestLayout>
</template>

<style scoped>
.backdrop-blur-sm {
  backdrop-filter: blur(8px);
}
</style>
