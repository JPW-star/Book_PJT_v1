<script setup>
import { ref, onMounted } from 'vue';
import axios from '@/api/axios';
import ThreadListItem from './ThreadListItem.vue';

const threads = ref([]);
const loading = ref(true);
const error = ref('');

const fetchThreads = async () => {
  try {
    const response = await axios.get('community/threads/');
    threads.value = response.data;
  } catch (err) {
    console.error('Failed to fetch threads:', err);
    error.value = 'Failed to load community posts.';
  } finally {
    loading.value = false;
  }
};

onMounted(() => {
  fetchThreads();
});
</script>

<template>
  <div class="thread-list">
    <div v-if="loading" class="loading">
      <div class="spinner"></div>
    </div>

    <div v-else-if="error" class="error">{{ error }}</div>

    <div v-else class="list-container">
      <div v-if="threads.length === 0" class="empty-state">
        No reviews yet. Be the first to write one!
      </div>

      <ThreadListItem v-for="thread in threads" :key="thread.id" :thread="thread" />
    </div>
  </div>
</template>

<style scoped>
.list-container {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.empty-state {
  text-align: center;
  padding: 4rem;
  color: #666;
  font-size: 1.1rem;
  background: #1e1e1e;
  border-radius: 12px;
}

.loading {
  display: flex;
  justify-content: center;
  padding: 3rem;
}

.spinner {
  width: 30px;
  height: 30px;
  border: 3px solid rgba(255, 255, 255, 0.1);
  border-left-color: #ff9800;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.error {
  text-align: center;
  color: #ff5252;
  padding: 2rem;
}
</style>
