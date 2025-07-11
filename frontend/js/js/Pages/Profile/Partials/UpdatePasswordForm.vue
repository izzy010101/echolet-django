<script setup>
import { useForm } from '@inertiajs/vue3'
import InputLabel from '@/Components/InputLabel.vue'
import TextInput from '@/Components/TextInput.vue'
import InputError from '@/Components/InputError.vue'
import PrimaryButton from '@/Components/PrimaryButton.vue'

const form = useForm({
  current_password: '',
  password: '',
  password_confirmation: '',
})

const updatePassword = () => {
  form.post('/password/update', {
    preserveScroll: true,
    onSuccess: () => form.reset(),
  });
};
</script>

<template>
  <section>
    <h2 class="text-xl font-bold text-gray-900 dark:text-white mb-4 dark:text-white ">Update Password</h2>

    <form @submit.prevent="updatePassword" class="space-y-6">
      <!-- Current Password -->
      <div>
        <InputLabel for="current_password" value="Current Password" />
        <TextInput
          id="current_password"
          v-model="form.current_password"
          type="password"
          autocomplete="current-password"
          class="mt-1 block w-full"
        />
        <InputError :message="form.errors.current_password" class="mt-2" />
      </div>

      <!-- New Password -->
      <div>
        <InputLabel for="password" value="New Password" />
        <TextInput
          id="password"
          v-model="form.password"
          type="password"
          autocomplete="new-password"
          class="mt-1 block w-full"
        />
        <InputError :message="form.errors.password" class="mt-2" />
      </div>

      <!-- Confirm Password -->
      <div>
        <InputLabel for="password_confirmation" value="Confirm Password" />
        <TextInput
          id="password_confirmation"
          v-model="form.password_confirmation"
          type="password"
          autocomplete="new-password"
          class="mt-1 block w-full"
        />
        <InputError :message="form.errors.password_confirmation" class="mt-2" />
      </div>

      <!-- Submit -->
      <div class="flex justify-left">
        <PrimaryButton
        :disabled="form.processing"
        :class="{ 'opacity-50': form.processing }"
        class="bg-rose-500 hover:bg-rose-600 text-white dark:bg-purple-500 dark:hover:bg-purple-600 transition"
        >
          Save
        </PrimaryButton>
      </div>
    </form>
  </section>
</template>
