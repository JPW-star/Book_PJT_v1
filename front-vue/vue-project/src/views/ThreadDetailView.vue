<script setup>
import { ref, onMounted, computed } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useAuthStore } from '@/stores/auth';
import axios from '@/api/axios';
import CommentForm from '@/components/community/CommentForm.vue';
import CommentList from '@/components/community/CommentList.vue';

const route = useRoute();
const router = useRouter();
const authStore = useAuthStore();

const thread = ref(null);
const loading = ref(true);
const error = ref('');

const threadId = route.params.id;
const isOwner = computed(() => {
  return authStore.user && thread.value && authStore.user.username === thread.value.user.username;
});

const fetchThreadDetail = async () => {
  try {
    const response = await axios.get(`community/threads/${threadId}/`);
    thread.value = response.data;
  } catch (err) {
    console.error('Failed to load thread:', err);
    error.value = 'Failed to load review.';
  } finally {
    loading.value = false;
  }
};

const handleLike = async () => {
  if (!authStore.isAuthenticated) {
    alert('Please log in to like.');
    return;
  }

  try {
    const response = await axios.post(`community/threads/${threadId}/likes/`);
    // Update local state is tricky because serializer has like_count but not "is_liked_by_me"
    // But the response returns updated count and 'liked' boolean
    thread.value.like_count = response.data.count;
    // We might want to toggle visual state of button too, but we need "isLiked" from backend potentially
    // For simple MVP, just update count.
  } catch (err) {
    console.error(err);
  }
};

const handleDelete = async () => {
  if (!confirm('Are you sure you want to delete this review?')) return;
  try {
    await axios.delete(`community/threads/${threadId}/`);
    router.push({ name: 'community' }); // Or Home
  } catch (err) {
    console.error(err);
    alert('Failed to delete review.');
  }
};

const onCommentAdded = (newComment) => {
  // Add to list, serializer returns user object nested? 
  // Wait, comment serializer in backend: user = UserListSerializer(read_only=True)
  // So yeah, it should be fine.
  // However, thread.comments is what we iterate on.
  thread.value.comments.push(newComment);
};

const onCommentDeleted = (commentId) => {
  thread.value.comments = thread.value.comments.filter(c => c.id !== commentId);
};

onMounted(() => {
  fetchThreadDetail();
});
</script>

<template>
  <div class="thread-container">
    <div v-if="loading" class="loading">Loading...</div>
    <div v-else-if="error" class="error">{{ error }}</div>

    <div v-else class="thread-detail">
      <!-- Book Header Link -->
      <RouterLink :to="{ name: 'book-detail', params: { isbn13: thread.book.isbn13 } }" class="book-link">
        ← Back to {{ thread.book.title }}
      </RouterLink>

      <!-- Main Content -->
      <article class="thread-content">
        <div class="header">
          <div class="meta">
            <span class="author">By {{ thread.user.username }}</span>
            <span class="rating">Rating: {{ thread.rating }} / 5</span>
            <span class="date">{{ new Date(thread.created_at).toLocaleDateString() }}</span>
          </div>

          <h1 class="thread-title">{{ thread.title }}</h1>
        </div>

        <div class="body-text">
          {{ thread.content }}
        </div>

        <!-- Thread Actions (Like & Owner controls) -->
        <div class="thread-actions">
          <button @click="handleLike" class="btn-like">
            ♥ LIKE {{ thread.like_count }}
          </button>

          <div v-if="isOwner" class="owner-actions">
            <!-- Edit could be implemented here -->
            <button @click="handleDelete" class="btn-delete-thread">Delete Review</button>
          </div>
        </div>
      </article>

      <!-- Comments Section -->
      <section class="comments-section">
        <h3>Comments ({{ thread.comments.length }})</h3>

        <div v-if="authStore.isAuthenticated">
          <CommentForm :threadId="Number(threadId)" @comment-added="onCommentAdded" />
        </div>
        <div v-else class="login-prompt">
          <RouterLink :to="{ name: 'login' }">Log in</RouterLink> to leave a comment.
        </div>

        <CommentList :comments="thread.comments" @comment-deleted="onCommentDeleted" />
      </section>
    </div>
  </div>
</template>

<style scoped>
.thread-container {
  max-width: 900px;
  margin: 0 auto;
  padding: 3rem 2rem;
}

.loading,
.error {
  text-align: center;
  padding: 4rem;
  color: #888;
}

.book-link {
  display: inline-block;
  margin-bottom: 2rem;
  color: #ff9800;
  font-weight: 500;
}

.book-link:hover {
  text-decoration: underline;
}

/* Thread Content */
.thread-content {
  background: #1e1e1e;
  padding: 3rem;
  border-radius: 16px;
  margin-bottom: 3rem;
}

.meta {
  display: flex;
  gap: 1.5rem;
  color: #888;
  font-size: 0.9rem;
  margin-bottom: 1rem;
}

.author {
  color: #fff;
  font-weight: 600;
}

.rating {
  color: #ff9800;
}

.thread-title {
  font-size: 2.5rem;
  font-weight: 800;
  color: #fff;
  margin-bottom: 2rem;
  line-height: 1.2;
}

.body-text {
  line-height: 1.8;
  color: #ddd;
  font-size: 1.1rem;
  white-space: pre-wrap;
  margin-bottom: 3rem;
  padding-bottom: 3rem;
  border-bottom: 1px solid #333;
}

.thread-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.btn-like {
  background: #2a2a2a;
  border: 1px solid #444;
  color: #fff;
  padding: 0.6rem 1.2rem;
  border-radius: 50px;
  cursor: pointer;
  font-weight: 600;
  transition: all 0.2s;
}

.btn-like:hover {
  background: #333;
  border-color: #ff9800;
  color: #ff9800;
}

.btn-delete-thread {
  background: transparent;
  border: 1px solid #ff5252;
  color: #ff5252;
  padding: 0.5rem 1rem;
  border-radius: 8px;
  cursor: pointer;
  font-size: 0.9rem;
}

.btn-delete-thread:hover {
  background: rgba(255, 82, 82, 0.1);
}

/* Comments Section */
.comments-section h3 {
  font-size: 1.5rem;
  margin-bottom: 2rem;
  padding-left: 0.5rem;
  border-left: 4px solid #ff9800;
  line-height: 1;
}

.login-prompt {
  background: #1e1e1e;
  padding: 1.5rem;
  border-radius: 12px;
  text-align: center;
  color: #888;
}

.login-prompt a {
  color: #ff9800;
  font-weight: 700;
}
</style>
