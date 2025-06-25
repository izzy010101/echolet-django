<script setup>
import {useForm} from '@inertiajs/vue3'
import {defineEmits} from 'vue'

const emit = defineEmits(['submitted'])

const props = defineProps({
    postId: Number,
    auth: Object,
    parentId: {
        type: Number,
        default: null,
    },
    initialContent: {
        type: String,
        default: '',
    },
    commentId: {
        type: Number,
        default: null,
    },
})

const form = useForm({
    content: props.initialContent, // initialize with existing content
    post_id: props.postId,
    parent_id: props.parentId,
})

const submit = () => {
    if (props.commentId) {
        form.put(route('comments.update', props.commentId), {
            preserveScroll: true,
            onSuccess: () => {
                form.reset()
                emit('submitted')
            },
        })
    } else {
        form.post(route('comments.store'), {
            preserveScroll: true,
            onSuccess: () => {
                form.reset()
                emit('submitted')
            },
        })
    }
}
</script>

<template>
    <form @submit.prevent="submit" class="space-y-3">
        <textarea
            v-model="form.content"
            class="w-full p-3 border rounded dark:bg-gray-800 dark:text-white"
            rows="3"
            placeholder="Write a comment..."
        ></textarea>
        <div class="text-sm text-red-500" v-if="form.errors.content">
            {{ form.errors.content }}
        </div>
        <button
            type="submit"
            class="bg-rose-500 text-white px-4 py-2 rounded hover:bg-rose-600 transition"
        >
            {{ commentId ? 'Update Comment' : 'Post Comment' }}
        </button>
    </form>
</template>
