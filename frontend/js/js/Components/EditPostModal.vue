<script setup>
import { useForm } from '@inertiajs/vue3';
import { onMounted } from 'vue';

const props = defineProps({
    post: Object,
    categories: Array,
});

const emit = defineEmits(['close', 'updated']);

const form = useForm({
    title: '',
    body: '',
    category_id: '',
});

onMounted(() => {
    if (props.post) {
        form.title = props.post.title;
        form.body = props.post.body;
        form.category_id = props.post.category_id;
    }
});

const submit = () => {
    form.put(`/posts/${props.post.id}/update/`, {
        preserveScroll: true,
        onSuccess: () => {
            emit('updated'); //  triggers router.reload in parent
            emit('close');   //  closes modal
        },
    });
};
</script>

<template>
    <div class="fixed inset-0 z-50 flex items-center justify-center bg-black/50">
        <div class="bg-white dark:bg-gray-900 rounded-xl shadow-xl w-full max-w-xl p-6 relative">
            <!-- Close Button -->
            <button
                @click="$emit('close')"
                class="absolute top-2 right-2 text-gray-500 hover:text-gray-800 dark:hover:text-white"
            >
                ✕
            </button>

            <h2 class="text-lg font-bold mb-4 text-gray-800 dark:text-gray-100">Edit Post</h2>

            <form @submit.prevent="submit" class="space-y-4">
                <div>
                    <label class="block text-sm font-medium text-gray-700 dark:text-gray-200 mb-1">Title</label>
                    <input
                        v-model="form.title"
                        type="text"
                        class="w-full px-4 py-2 rounded-lg border dark:bg-gray-800 dark:text-white focus:ring-2 focus:ring-purple-500"
                        :class="{
                      'border-red-500': form.errors.title,
                      'border-gray-300 dark:border-gray-600': !form.errors.title
                    }"
                    />
                    <p v-if="form.errors.title" class="text-red-500 text-sm mt-1">{{ form.errors.title }}</p>
                </div>

                <div>
                    <label class="block text-sm font-medium text-gray-700 dark:text-gray-200 mb-1">Content</label>
                    <textarea
                        v-model="form.body"
                        rows="4"
                        class="w-full px-4 py-2 rounded-lg border dark:bg-gray-800 dark:text-white focus:ring-2 focus:ring-purple-500"
                        :class="{
                        'border-red-500': form.errors.body,
                        'border-gray-300 dark:border-gray-600': !form.errors.body
                      }"
                    />
                    <p v-if="form.errors.body" class="text-red-500 text-sm mt-1">
                        {{ form.errors.body }}
                    </p>
                </div>

                <div>
                    <label class="block text-sm font-medium text-gray-700 dark:text-gray-200 mb-1">Category</label>
                    <select
                        v-model="form.category_id"
                        class="w-full px-4 py-2 rounded-lg border dark:bg-gray-800 dark:text-white focus:ring-2 focus:ring-purple-500"
                        :class="{
              'border-red-500': form.errors.category_id,
              'border-gray-300 dark:border-gray-600': !form.errors.category_id
            }"
                    >
                        <option value="">Select a category</option>
                        <option v-for="cat in categories" :key="cat.id" :value="cat.id">
                            {{ cat.name }}
                        </option>
                    </select>
                    <p v-if="form.errors.category_id" class="text-red-500 text-sm mt-1">{{ form.errors.category_id }}</p>
                </div>

                <div class="flex justify-between items-center pt-2">
                    <button
                        type="submit"
                        :disabled="form.processing"
                        class="bg-gradient-to-r from-purple-500 to-rose-500 hover:from-purple-600 hover:to-rose-600 text-white font-semibold py-2 px-4 rounded-xl transition-all duration-200 shadow"
                        :class="{ 'opacity-50 cursor-not-allowed': form.processing }"
                    >
                        Update Post
                    </button>

                    <button
                        type="button"
                        @click="$emit('close')"
                        class="text-sm text-gray-600 dark:text-gray-300 hover:underline"
                    >
                        Cancel
                    </button>
                </div>
            </form>
        </div>
    </div>
</template>


