<script setup>
import CommentItem from './CommentItem.vue'
import CommentForm from './CommentForm.vue'
import {usePage} from "@inertiajs/vue3";

const props = defineProps({
    comments: Array,
    postId: Number,
    user: Object,
})

</script>

<template>
    <div class="space-y-6">


        <!-- List all top-level comments -->
        <CommentItem
            v-for="comment in comments"
            :key="comment.id"
            :comment="comment"
            :post-id="postId"
            :user="user"
        />
    </div>
</template>
