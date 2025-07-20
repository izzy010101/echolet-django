<script setup>
import AuthenticatedLayout from '@/Layouts/AuthenticatedLayout.vue';
import { Head, useForm } from '@inertiajs/vue3';
import AppLayout from '@/Layouts/AppLayout.vue'
import { ref, watch, watchEffect } from 'vue'
import EditPostModal from '@/Components/EditPostModal.vue'
import NoResults from '@/Components/NoResults.vue'
import Swal from 'sweetalert2'
import { usePage } from '@inertiajs/vue3'
import { router } from '@inertiajs/vue3';

const props = defineProps({
    posts: {
        type: Array,
        default: () => [],
    },
    categories: {
        type: Array,
        default: () => [],
    },
    footerCategories: Array,
    auth: Object,
});

const form = useForm({
    title: '',
    content: '',
    category_id: '',
});

const page = usePage()
const query = page.props.query || ''

const flashMessage = ref('')
const showFlash = ref(false)
const localSuccessMessage = ref('')
const skipValidation = ref(false)

watchEffect(() => {
    const msg = page.props.flash?.success
    if (msg) {
        flashMessage.value = msg
        showFlash.value = true
        setTimeout(() => showFlash.value = false, 3000)
    }
})

const validationErrors = ref({
    title: '',
    content: '',
    category_id: ''
})
watch(() => form.title, (value) => {
    if (skipValidation.value) return
    validationErrors.value.title = value.length < 3 ? 'Title must be at least 3 characters.' : ''
})

watch(() => form.content, (value) => {
    if (skipValidation.value) return
    validationErrors.value.content = value.length < 10 ? 'Content must be at least 10 characters.' : ''
})

watch(() => form.category_id, (value) => {
    if (skipValidation.value) return
    validationErrors.value.category_id = value === '' ? 'Please select a category.' : ''
})

const submit = () => {
    form.post('/posts/store', {
      preserveScroll: true,
      onSuccess: () => {
        form.reset();
        window.location.reload();
      },
      onError: () => {
        console.log("errors...")
        console.log(form.errors) // should now contain title, content
      },
    })
};

const showEditModal = ref(false)
const postBeingEdited = ref(null)

const startEditing = (post) => {
    postBeingEdited.value = post
    showEditModal.value = true
}

const refreshAfterEdit = () => {
    localSuccessMessage.value = 'Post updated successfully.'
    router.reload({ preserveScroll: true })
    setTimeout(() => localSuccessMessage.value = '', 3000)
}

const deletePost = (id) => {
    Swal.fire({
        title: 'Are you sure?',
        text: 'Do you want to delete this blog post?',
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#e3342f',
        cancelButtonColor: '#6c757d',
        confirmButtonText: 'Yes, delete it!',
        background: document.documentElement.classList.contains('dark') ? '#1f2937' : '#fff',
        color: document.documentElement.classList.contains('dark') ? '#f3f4f6' : '#111',
    }).then((result) => {
        if (result.isConfirmed) {
            router.delete(`/posts/${id}/delete/`, {
                preserveScroll: true,
                onSuccess: () => {
                    localSuccessMessage.value = 'Post deleted successfully.'
                    setTimeout(() => localSuccessMessage.value = '', 3000)
                },
            })
        }
    })
}


</script>

<template>
    <Head title="Dashboard" />

    <AppLayout :auth="auth" :footer-categories="footerCategories">

        <template #header>
            <h2 class="text-xl font-semibold leading-tight text-gray-800 dark:text-white">Dashboard</h2>
            <div
                v-if="showFlash"
                class="w-full bg-green-100 dark:bg-green-900 text-green-800 dark:text-green-300 py-3 text-center font-semibold shadow mt-2 rounded"
            >
                {{ flashMessage }}
            </div>
        </template>

      <div class="bg-white dark:bg-gray-900 transition-colors duration-300">
        <div class="py-12">
            <div v-if="localSuccessMessage" class="mb-6 text-center">
                <div class="inline-block bg-green-100 dark:bg-green-900 text-green-800 dark:text-green-300 px-4 py-2 rounded-lg shadow font-medium">
                    {{ localSuccessMessage }}
                </div>
            </div>

            <div class="mx-auto max-w-7xl sm:px-6 lg:px-8 grid grid-cols-1 md:grid-cols-2 gap-6">
                <!-- Left Column -->
                <div>
                    <h3 class="text-lg font-bold mb-4 text-gray-800 dark:text-gray-100">
                        Your Posts
                        <span v-if="query" class="text-sm text-gray-500 dark:text-gray-400">— Results for "{{ query }}"</span>
                    </h3>

                    <div v-if="props.posts.length > 0">
                        <ul class="space-y-4">
                            <li v-for="post in props.posts" :key="post.id" class="p-4 border rounded-xl bg-white dark:bg-gray-800 text-gray-800 dark:text-gray-100 shadow">
                                <h4 class="font-semibold text-lg text-purple-600 dark:text-purple-400">{{ post.title }}</h4>
                                <p class="text-xs text-gray-500 dark:text-gray-400">Posted on {{ new Date(post.created_at).toLocaleDateString() }}</p>
                                <p class="text-sm text-gray-600 dark:text-gray-300">
                                    {{ post.excerpt ?? (post.body?.slice(0, 50) + '...') ?? 'No content available.' }}
                                </p>
                                <p class="text-xs italic text-gray-400 truncate">Slug: {{ post.slug }}</p>
                                <div class="flex items-center justify-between mt-2">
                                    <span class="text-xs text-purple-500">Category: {{ post.category__name || 'Uncategorized' }}</span>

                                    <div class="space-x-2">
                                        <button @click="startEditing(post)" class="text-sm text-blue-600 hover:underline">Edit</button>
                                        <button @click="deletePost(post.id)" class="text-sm text-red-600 hover:underline">Delete</button>
                                    </div>
                                </div>
                            </li>
                        </ul>
                    </div>
                    <NoResults v-else />
                </div>

                <!-- Right Column -->
                <div>
                    <h3 class="text-lg font-bold mb-4 text-gray-800 dark:text-gray-100">New Post</h3>
                    <form @submit.prevent="submit" class="space-y-6 bg-white dark:bg-gray-800 p-6 rounded-2xl shadow">
                        <div>
                            <label class="block text-sm font-medium text-gray-700 dark:text-gray-200 mb-1">Title</label>
                            <input required
                                v-model="form.title"
                                type="text"
                                placeholder="Enter post title"
                                class="w-full px-4 py-2 rounded-lg border dark:bg-gray-900 dark:text-white focus:ring-2 focus:ring-purple-500"
                                :class="{
                                    'border-red-500': validationErrors.title || form.errors.title,
                                    'border-gray-300 dark:border-gray-600': !validationErrors.title && !form.errors.title
                                }"
                            />

                            <div v-if="validationErrors.title || form.errors.title" class="text-red-500 text-sm mt-1">
                                {{ validationErrors.title || form.errors.title }}
                            </div>
                        </div>

                        <div>
                            <label class="block text-sm font-medium text-gray-700 dark:text-gray-200 mb-1">Content</label>
                            <textarea required
                                v-model="form.content"
                                rows="4"
                                placeholder="Write your post..."
                                class="w-full px-4 py-2 rounded-lg border dark:bg-gray-900 dark:text-white focus:ring-2 focus:ring-purple-500"
                                :class="{
                                    'border-red-500': form.errors.content,
                                    'border-gray-300 dark:border-gray-600': !form.errors.content
                                }"
                            ></textarea>
                            <div v-if="form.errors.content" class="text-red-500 text-sm mt-1">{{ form.errors.content }}</div>
                        </div>

                        <div>
                            <label class="block text-sm font-medium text-gray-700 dark:text-gray-200 mb-1">Category</label>
                            <select
                                v-model="form.category_id"
                                class="w-full px-4 py-2 rounded-lg border dark:bg-gray-900 dark:text-white focus:ring-2 focus:ring-purple-500"
                                :class="{
                                    'border-red-500': form.errors.category_id,
                                    'border-gray-300 dark:border-gray-600': !form.errors.category_id
                                }"
                            >
                                <option value="">Select a category</option>
                                <option v-for="cat in props.categories" :key="cat.id" :value="cat.id">{{ cat.name }}</option>
                            </select>
                            <div v-if="form.errors.category_id" class="text-red-500 text-sm mt-1">{{ form.errors.category_id }}</div>
                        </div>

                        <button
                            type="submit"
                            :disabled="form.processing"
                            class="w-full bg-gradient-to-r from-purple-500 to-rose-500 hover:from-purple-600 hover:to-rose-600 text-white font-semibold py-2 px-4 rounded-xl transition-all duration-200 shadow-md"
                            :class="{ 'opacity-50 cursor-not-allowed': form.processing }"
                        >
                            Post
                        </button>
                    </form>
                </div>
            </div>
        </div>
      </div>
    </AppLayout>

    <EditPostModal
        v-if="showEditModal"
        :post="postBeingEdited"
        :categories="props.categories"
        @close="showEditModal = false"
        @updated="refreshAfterEdit"
    />
</template>
