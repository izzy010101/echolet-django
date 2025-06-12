<script setup>
import AuthenticatedLayout from '@/Layouts/AuthenticatedLayout.vue'
import { Head } from '@inertiajs/vue3'

import UpdateProfileInformationForm from './Partials/UpdateProfileInformationForm.vue'
import UpdatePasswordForm from './Partials/UpdatePasswordForm.vue'
import DeleteUserForm from './Partials/DeleteUserForm.vue'

defineProps({
  mustVerifyEmail: Boolean,
  status: String,
})
</script>

<template>
  <Head title="Profile" />

  <AuthenticatedLayout>
    <section class="min-h-screen bg-gradient-to-br from-rose-50 via-pink-50 to-purple-50 dark:from-gray-900 dark:to-gray-950 py-12 px-4">
      <div class="w-full max-w-2xl mx-auto space-y-12">

        <div class="bg-white dark:bg-gray-800 rounded-2xl shadow-xl p-8">
          <UpdateProfileInformationForm :must-verify-email="mustVerifyEmail" :status="status" />
        </div>

        <div class="bg-white dark:bg-gray-800 rounded-2xl shadow-xl p-8">
          <UpdatePasswordForm />
        </div>

        <div class="bg-white dark:bg-gray-800 rounded-2xl shadow-xl p-8">
          <DeleteUserForm />
        </div>

      </div>
    </section>
  </AuthenticatedLayout>
</template>
