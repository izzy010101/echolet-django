<script setup>
import GuestLayout from '@/Layouts/GuestLayout.vue';
import InputError from '@/Components/InputError.vue';
import InputLabel from '@/Components/InputLabel.vue';
import PrimaryButton from '@/Components/PrimaryButton.vue';
import TextInput from '@/Components/TextInput.vue';
import { Head, useForm } from '@inertiajs/vue3';
import { Lock } from 'lucide-vue-next';

const props = defineProps({
    email: { type: String, required: true },
    token: { type: String, required: true },
});

const form = useForm({
    token: props.token,
    email: props.email,
    password: '',
    password_confirmation: '',
});

const submit = () => {
    form.post(route('password.store'), {
        onFinish: () => form.reset('password', 'password_confirmation'),
    });
};
</script>

<template>
    <GuestLayout>
        <Head title="Reset Password"/>

        <div
            class="min-h-screen flex items-center justify-center bg-gradient-to-br from-pink-50 via-purple-50 to-rose-50 dark:bg-none dark:bg-white p-6 transition-colors">
            <div
                class="w-full max-w-md bg-white/80 backdrop-blur-sm rounded-3xl shadow-xl border border-white/20 p-8 space-y-6">
                <!-- Icon & Heading -->
                <div class="text-center">
                    <div
                        class="inline-flex items-center justify-center w-16 h-16 bg-gradient-to-r from-purple-500 to-rose-400 rounded-2xl mb-4 shadow-lg">
                        <Lock class="w-8 h-8 text-white"/>
                    </div>
                    <h1 class="text-3xl font-bold bg-gradient-to-r from-gray-900 to-gray-600 bg-clip-text text-transparent">
                        Reset Your Password
                    </h1>
                    <p class="text-sm text-gray-600 mt-2">Enter your new password below</p>
                </div>

                <!-- Form -->
                <form @submit.prevent="submit" class="space-y-5">
                    <!-- Email -->
                    <div>
                        <InputLabel for="email" value="Email" class="text-gray-700"/>
                        <TextInput
                            id="email"
                            type="email"
                            class="mt-1 block w-full rounded-xl bg-gray-50/50 border border-gray-200 text-gray-900 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-purple-500 dark:bg-white dark:text-gray-900 dark:border-gray-200"
                            v-model="form.email"
                            required
                            autocomplete="username"
                        />
                        <InputError class="mt-2" :message="form.errors.email"/>
                    </div>

                    <!-- Password -->
                    <div>
                        <InputLabel for="password" value="Password" class="text-gray-700"/>
                        <TextInput
                            id="password"
                            type="password"
                            class="mt-1 block w-full rounded-xl bg-gray-50/50 border border-gray-200 text-gray-900 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-purple-500 dark:bg-white dark:text-gray-900 dark:border-gray-200"
                            v-model="form.password"
                            required
                            autocomplete="new-password"
                        />
                        <InputError class="mt-2" :message="form.errors.password"/>
                    </div>

                    <!-- Confirm Password -->
                    <div>
                        <InputLabel for="password_confirmation" value="Confirm Password" class="text-gray-700"/>
                        <TextInput
                            id="password_confirmation"
                            type="password"
                            class="mt-1 block w-full rounded-xl bg-gray-50/50 border border-gray-200 text-gray-900 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-purple-500 dark:bg-white dark:text-gray-900 dark:border-gray-200"
                            v-model="form.password_confirmation"
                            required
                            autocomplete="new-password"
                        />
                        <InputError class="mt-2" :message="form.errors.password_confirmation"/>
                    </div>

                    <!-- Submit -->
                    <PrimaryButton
                        class="w-full justify-center bg-gradient-to-r from-purple-500 to-rose-400 hover:from-purple-600 hover:to-rose-500 text-white font-semibold py-3 rounded-xl transition-all duration-200 shadow-lg"
                        :class="{ 'opacity-25': form.processing }"
                        :disabled="form.processing"
                    >
                        Reset Password
                    </PrimaryButton>
                </form>
            </div>
        </div>
    </GuestLayout>
</template>

<style scoped>
.backdrop-blur-sm {
    backdrop-filter: blur(8px);
}
</style>
