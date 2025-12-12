<script setup>
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import axios from '@/api/axios';

const route = useRoute();
const router = useRouter();

const bookIsbn = route.query.isbn;
const book = ref(null);

const title = ref('');
const content = ref('');
const rating = ref(5);
const loading = ref(false);
const error = ref('');

const fetchBookInfo = async () => {
  if (!bookIsbn) return;
  try {
    const response = await axios.get(`books/${bookIsbn}/`);
    book.value = response.data;
  } catch (err) {
    console.error('Failed to fetch book info', err);
    error.value = 'Failed to load book information.';
  }
};

const handleSubmit = async () => {
  if (!title.value.trim() || !content.value.trim()) {
    error.value = 'Please fill in all fields.';
    return;
  }

  loading.value = true;
  error.value = '';

  try {
    const payload = {
      book_isbn13: bookIsbn,
      title: title.value,
      content: content.value,
      rating: rating.value
    };

    const response = await axios.post('community/threads/', payload);
    const newThreadId = response.data.id;

    // Redirect to the new thread detail page
    router.push({ name: 'thread-detail', params: { id: newThreadId } });

  } catch (err) {
    console.error('Failed to create thread', err);
    error.value = 'Failed to post review. Please try again.';
  } finally {
    loading.value = false;
  }
};

onMounted(() => {
  if (!bookIsbn) {
    error.value = 'No book selected.';
  } else {
    fetchBookInfo();
  }
});
</script>

<template>
  <div class="create-container">
    <div class="form-card">
      <h1 class="page-title">Write a Review</h1>

      <!-- Selected Book Info -->
      <div v-if="book" class="selected-book">
        <img :src="book.cover" :alt="book.title" class="book-thumb" />
        <div class="book-info">
          <h3>{{ book.title }}</h3>
          <p>{{ book.author }}</p>
        </div>
      </div>
      <div v-else-if="!error" class="loading-book">Loading book info...</div>

      <form @submit.prevent="handleSubmit" class="thread-form">
        <!-- Rating -->
        <div class="form-group">
          <label>Rating</label>
          <div class="rating-input">
            <span v-for="star in 5" :key="star" class="star" :class="{ active: star <= rating }"
              @click="rating = star">★</span>
          </div>
        </div>

        <div class="form-group">
          <label for="title">Title</label>
          <input id="title" v-model="title" type="text" placeholder="Give your review a headline" required />
        </div>

        <div class="form-group">
          <label for="content">Review</label>
          <textarea id="content" v-model="content" rows="10" placeholder="Share your thoughts about this book..."
            required></textarea>
        </div>

        <div v-if="error" class="error-msg">{{ error }}</div>

        <div class="actions">
          <button type="button" @click="$router.back()" class="btn-cancel">Cancel</button>
          <button type="submit" class="btn-submit" :disabled="loading">
            {{ loading ? 'Posting...' : 'Post Review' }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<style scoped>
.create-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 3rem 2rem;
}

.form-card {
  background: #1e1e1e;
  padding: 3rem;
  border-radius: 16px;
}

.page-title {
  font-size: 2rem;
  font-weight: 700;
  margin-bottom: 2rem;
  color: #fff;
  text-align: center;
}

/* Selected Book Display */
.selected-book {
  display: flex;
  align-items: center;
  gap: 1.5rem;
  background: #2c2c2c;
  padding: 1.5rem;
  border-radius: 12px;
  margin-bottom: 2rem;
}

.book-thumb {
  width: 60px;
  height: 90px;
  object-fit: cover;
  border-radius: 4px;
}

.book-info h3 {
  font-size: 1.1rem;
  color: #fff;
  margin-bottom: 0.3rem;
}

.book-info p {
  color: #aaa;
  font-size: 0.9rem;
}

/* Form Styles */
.thread-form {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

label {
  font-weight: 600;
  color: #ccc;
  font-size: 0.95rem;
}

input,
textarea {
  background: #121212;
  border: 1px solid #333;
  color: #fff;
  padding: 1rem;
  border-radius: 8px;
  font-size: 1rem;
  font-family: inherit;
  transition: border-color 0.2s;
}

input:focus,
textarea:focus {
  outline: none;
  border-color: #ff9800;
}

textarea {
  resize: vertical;
}

/* Rating Stars */
.rating-input {
  display: flex;
  gap: 0.5rem;
}

.star {
  font-size: 2rem;
  color: #444;
  cursor: pointer;
  transition: color 0.2s;
}

.star.active {
  color: #ff9800;
}

/* Actions */
.actions {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  margin-top: 1rem;
}

.btn-cancel {
  background: transparent;
  border: 1px solid #555;
  color: #ccc;
  padding: 0.8rem 1.5rem;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
}

.btn-submit {
  background: #ff9800;
  border: none;
  color: #000;
  padding: 0.8rem 2rem;
  border-radius: 8px;
  font-weight: 700;
  cursor: pointer;
  transition: background-color 0.2s;
}

.btn-submit:hover:not(:disabled) {
  background: #ffb74d;
}

.error-msg {
  color: #ff5252;
  text-align: center;
}
</style>
