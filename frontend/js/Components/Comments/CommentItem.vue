<script setup>
import CommentForm from './CommentForm.vue';
import { ref } from 'vue';
import { router } from '@inertiajs/vue3';
import { Heart } from 'lucide-vue-next';

const props = defineProps({
    comment: Object,
    postId: Number,
    user: Object,
});
const { user } = props; //for likes

const showReplyForm = ref(false);
const showEditForm = ref(false);
const likesCount = ref(props.comment.likes_count);
const liked = ref(props.comment.is_liked);
const showLoginMessage = ref(false)


// delete comment function
function deleteComment(id) {
    router.delete(route('comments.destroy', id), {
        preserveScroll: true,
        preserveState: true,
    });
}

// toggle for liking the comments
const toggleLike = async () => {
    if (!user) {
        showLoginMessage.value = true
        setTimeout(() => (showLoginMessage.value = false), 3000)
        return
    }

    try {
        const res = await axios.post(`/comments/${props.comment.id}/like`)
        liked.value = res.data.liked
        likesCount.value = res.data.likes_count
    } catch (e) {
        console.error('Like failed:', e)
    }
}
</script>

<template>
    <div class="border rounded bg-white dark:bg-gray-900 p-4 mb-2">
        <div v-if="!showEditForm">
            <strong>{{ comment.user.name }}</strong>
            <p class="mt-1 text-gray-700 dark:text-gray-300">{{ comment.content }}</p>
        </div>

        <CommentForm
            v-if="showEditForm"
            :post-id="postId"
            :parent-id="comment.parent_id"
            :auth="user"
            :initial-content="comment.content"
            :comment-id="comment.id"
            @submitted="showEditForm = false"
        />

        <div class="mt-2 flex space-x-3 items-center">
            <button
                v-if="user"
                @click="showReplyForm = !showReplyForm"
                class="text-xs text-pink-500 hover:underline"
            >
                Reply
            </button>

            <template v-if="user && user.id === comment.user.id">
                <button
                    @click="showEditForm = !showEditForm"
                    class="text-xs text-blue-500 hover:underline"
                >
                    Edit
                </button>
                <button
                    @click="deleteComment(comment.id)"
                    class="text-xs text-red-500 hover:underline"
                >
                    Delete
                </button>
            </template>

            <div class="relative inline-block">
                <!-- Like button -->
                <button @click="toggleLike" class="flex items-center space-x-1 text-xs">
                    <Heart
                        :fill="liked ? 'currentColor' : 'none'"
                        :stroke="liked ? 'rgb(239 68 68)' : 'currentColor'"
                        :class="[
                        'w-4 h-4 transition hover:scale-110',
                        liked ? 'text-red-500' : 'text-gray-500 dark:text-gray-400'
                      ]"
                    />
                    <span class="text-gray-700 dark:text-gray-300">{{ likesCount }}</span>
                </button>

                <!-- Login  to like message-->
                <div
                    v-if="showLoginMessage"
                    class="absolute top-6 left-4 text-xs bg-pink-100 text-pink-700 px-3 py-1 rounded shadow border border-pink-200 whitespace-nowrap"
                >
                    Please log in to like comments.
                </div>
            </div>
        </div>

        <CommentForm
            v-if="showReplyForm"
            :post-id="postId"
            :parent-id="comment.id"
            :auth="user"
            @submitted="showReplyForm = false"
        />

        <div class="ml-4 mt-2 space-y-2">
            <CommentItem
                v-for="reply in comment.replies"
                :key="reply.id"
                :comment="reply"
                :post-id="postId"
                :user="user"
            />
        </div>
    </div>
</template>
