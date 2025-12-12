<script setup>
import { ref } from 'vue';
import axios from '@/api/axios';

const props = defineProps({
  threadId: {
    type: Number,
    required: true
  }
});

const emit = defineEmits(['comment-added']);

const content = ref('');
const loading = ref(false);

const submitComment = async () => {
  if (!content.value.trim()) return;

  loading.value = true;
  try {
    const response = await axios.post(`community/threads/${props.threadId}/comments/`, {
      content: content.value
    });
    content.value = ''; // Clear input
    emit('comment-added', response.data);
  } catch (error) {
    console.error('Failed to post comment:', error);
    alert('Failed to post comment.');
  } finally {
    loading.value = false;
  }
};
</script>

<template>
  <div class="comment-form">
    <textarea v-model="content" placeholder="Write a comment..." rows="3" class="comment-input"></textarea>
    <div class="actions">
      <button @click="submitComment" class="btn-submit" :disabled="loading || !content.trim()">
        {{ loading ? 'Posting...' : 'Post Comment' }}
      </button>
    </div>
  </div>
</template>

<style scoped>
.comment-form {
  background: #252525;
  padding: 1.5rem;
  border-radius: 12px;
  margin-bottom: 2rem;
}

.comment-input {
  width: 100%;
  background: #1e1e1e;
  border: 1px solid #333;
  color: #fff;
  padding: 1rem;
  border-radius: 8px;
  resize: none;
  font-family: inherit;
  font-size: 0.95rem;
  transition: border-color 0.2s;
}

.comment-input:focus {
  outline: none;
  border-color: #ff9800;
}

.actions {
  display: flex;
  justify-content: flex-end;
  margin-top: 1rem;
}

.btn-submit {
  background: #ff9800;
  color: #000;
  border: none;
  padding: 0.6rem 1.2rem;
  border-radius: 50px;
  font-weight: 600;
  font-size: 0.9rem;
  cursor: pointer;
  transition: background-color 0.2s;
}

.btn-submit:hover:not(:disabled) {
  background: #ffb74d;
}

.btn-submit:disabled {
  background: #444;
  cursor: not-allowed;
  color: #888;
}
</style>
