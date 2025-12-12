<script setup>
import { computed } from 'vue';
import { useAuthStore } from '@/stores/auth';
import axios from '@/api/axios';

const props = defineProps({
  comments: {
    type: Array,
    required: true
  }
});

const emit = defineEmits(['comment-deleted']);
const authStore = useAuthStore();
const currentUser = computed(() => authStore.user);

const deleteComment = async (commentId) => {
  if (!confirm('Are you sure you want to delete this comment?')) return;

  try {
    await axios.delete(`community/comments/${commentId}/`);
    emit('comment-deleted', commentId);
  } catch (error) {
    console.error('Failed to delete comment:', error);
    alert('Failed to delete comment.');
  }
};

const formatDate = (dateString) => {
  return new Date(dateString).toLocaleDateString(undefined, {
    year: 'numeric', month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit'
  });
};
</script>

<template>
  <div class="comment-list">
    <div v-if="comments.length === 0" class="no-comments">
      No comments yet. Be the first to share your thoughts!
    </div>

    <div v-else class="comments-wrapper">
      <div v-for="comment in comments" :key="comment.id" class="comment-item">
        <div class="comment-header">
          <span class="username">{{ comment.user.username }}</span>
          <span class="date">{{ formatDate(comment.created_at) }}</span>
        </div>

        <p class="comment-content">{{ comment.content }}</p>

        <div v-if="currentUser && currentUser.username === comment.user.username" class="comment-actions">
          <button @click="deleteComment(comment.id)" class="btn-delete">Delete</button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.comment-list {
  margin-top: 2rem;
}

.no-comments {
  text-align: center;
  color: #777;
  font-style: italic;
  padding: 2rem;
}

.comments-wrapper {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.comment-item {
  background: #1e1e1e;
  padding: 1.5rem;
  border-radius: 12px;
  border-left: 4px solid #333;
}

.comment-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 0.8rem;
  font-size: 0.9rem;
}

.username {
  font-weight: 700;
  color: #fff;
}

.date {
  color: #666;
}

.comment-content {
  color: #ddd;
  line-height: 1.6;
  white-space: pre-wrap;
}

.comment-actions {
  display: flex;
  justify-content: flex-end;
  margin-top: 0.8rem;
}

.btn-delete {
  background: transparent;
  border: none;
  color: #ff5252;
  font-size: 0.85rem;
  cursor: pointer;
  padding: 0;
}

.btn-delete:hover {
  text-decoration: underline;
}
</style>
