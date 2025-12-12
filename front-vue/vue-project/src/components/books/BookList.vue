<script setup>
import { ref, onMounted } from 'vue';
import axios from '@/api/axios';
import BookItem from './BookItem.vue';

const books = ref([]);
const loading = ref(true);

const fetchBooks = async () => {
  try {
    const response = await axios.get('books/');
    books.value = response.data;
  } catch (error) {
    console.error('Failed to fetch books:', error);
  } finally {
    loading.value = false;
  }
};

onMounted(() => {
  fetchBooks();
});
</script>

<template>
  <div class="book-list-container">
    <div v-if="loading" class="loading">
      <div class="spinner"></div>
    </div>

    <div v-else class="book-grid">
      <BookItem v-for="book in books" :key="book.isbn13" :book="book" />
    </div>
  </div>
</template>

<style scoped>
.book-list-container {
  padding: 2rem 0;
}

.book-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 2rem;
}

.loading {
  display: flex;
  justify-content: center;
  padding: 4rem 0;
}

.spinner {
  width: 40px;
  height: 40px;
  border: 4px solid rgba(255, 255, 255, 0.1);
  border-left-color: #fff;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

@media (max-width: 768px) {
  .book-grid {
    grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
    gap: 1rem;
  }
}
</style>
