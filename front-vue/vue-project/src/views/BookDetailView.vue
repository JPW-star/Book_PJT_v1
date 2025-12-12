<script setup>
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import axios from '@/api/axios';
import { useAuthStore } from '@/stores/auth';

const route = useRoute();
const router = useRouter();
const authStore = useAuthStore();

const book = ref(null);
const loading = ref(true);
const error = ref(null);

const isbn13 = route.params.isbn13;

const fetchBookDetail = async () => {
  try {
    const response = await axios.get(`books/${isbn13}/`);
    book.value = response.data;
  } catch (err) {
    console.error('Error fetching book detail:', err);
    error.value = 'Failed to load book details.';
  } finally {
    loading.value = false;
  }
};

const goCreateThread = () => {
  if (!authStore.isAuthenticated) {
    if (confirm('Log in is required to write a review. Go to login page?')) {
      router.push({ name: 'login' });
    }
    return;
  }
  // Pass book info to create page via query or state? 
  // For now, let's just go to create page. 
  // Ideally we should pass the ISBN so it's pre-selected.
  router.push({ name: 'thread-create', query: { isbn: book.value.isbn13 } });
};

onMounted(() => {
  fetchBookDetail();
});
</script>

<template>
  <div class="detail-container">
    <div v-if="loading" class="loading">Loading...</div>
    <div v-else-if="error" class="error">{{ error }}</div>

    <div v-else class="book-detail">
      <!-- Top Section: Cover & Info -->
      <div class="top-section">
        <div class="cover-wrapper">
          <img :src="book.cover" :alt="book.title" class="book-cover" />
        </div>

        <div class="info-wrapper">
          <h2 class="author-name">{{ book.author }}</h2>
          <h1 class="book-title">{{ book.title }}</h1>

          <div class="meta-info">
            <span class="publisher">{{ book.publisher }}</span>
            <span class="isbn">ISBN: {{ book.isbn13 }}</span>
          </div>

          <div class="actions">
            <button @click="goCreateThread" class="btn-create-thread">
              Write a Review
            </button>
            <a :href="`https://www.aladin.co.kr/shop/wproduct.aspx?ISBN=${book.isbn13}`" target="_blank"
              class="btn-shop">
              View on Aladin
            </a>
          </div>

          <div class="genres">
            <!-- Dummy genres as we don't have them in DB yet -->
            <span class="tag">Bestseller</span>
            <span class="tag">Trending</span>
            <span class="tag">Book</span>
          </div>
        </div>
      </div>

      <!-- Bottom Section: Description -->
      <div class="description-section">
        <h3>About this Book</h3>
        <p class="description-text">
          {{ book.descriptions }}
        </p>
      </div>
    </div>
  </div>
</template>

<style scoped>
.detail-container {
  max-width: 1000px;
  margin: 0 auto;
  padding: 3rem 2rem;
}

.loading,
.error {
  text-align: center;
  padding: 4rem;
  font-size: 1.2rem;
  color: #888;
}

/* Top Section Layout */
.top-section {
  display: flex;
  gap: 4rem;
  margin-bottom: 4rem;
}

.cover-wrapper {
  flex-shrink: 0;
  width: 300px;
}

.book-cover {
  width: 100%;
  border-radius: 8px;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.5);
}

.info-wrapper {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.author-name {
  font-size: 1.1rem;
  color: #aaa;
  margin-bottom: 0.5rem;
  font-weight: 500;
}

.book-title {
  font-size: 3rem;
  font-weight: 800;
  line-height: 1.1;
  margin-bottom: 1.5rem;
  color: #fff;
}

.meta-info {
  display: flex;
  gap: 1.5rem;
  color: #888;
  margin-bottom: 2.5rem;
  font-size: 0.95rem;
}

/* Buttons */
.actions {
  display: flex;
  gap: 1rem;
  margin-bottom: 2.5rem;
}

.btn-create-thread {
  background-color: #ff9800;
  color: #000;
  border: none;
  padding: 0.8rem 2rem;
  border-radius: 50px;
  font-weight: 700;
  font-size: 1rem;
  cursor: pointer;
  transition: background-color 0.2s, transform 0.2s;
}

.btn-create-thread:hover {
  background-color: #ffb74d;
  transform: translateY(-2px);
}

.btn-shop {
  background-color: transparent;
  border: 1px solid #555;
  color: #fff;
  padding: 0.8rem 1.5rem;
  border-radius: 50px;
  font-weight: 600;
  display: inline-flex;
  align-items: center;
}

.btn-shop:hover {
  border-color: #fff;
  background-color: rgba(255, 255, 255, 0.05);
}

/* Tags */
.genres {
  display: flex;
  gap: 0.8rem;
}

.tag {
  background: #222;
  padding: 0.4rem 1rem;
  border-radius: 8px;
  font-size: 0.85rem;
  color: #ccc;
}

/* Description */
.description-section {
  background: #1e1e1e;
  padding: 3rem;
  border-radius: 16px;
}

.description-section h3 {
  font-size: 1.5rem;
  margin-bottom: 1.5rem;
  color: #fff;
  font-weight: 700;
}

.description-text {
  line-height: 1.8;
  color: #ddd;
  font-size: 1.05rem;
  white-space: pre-line;
  /* Handle line breaks in description */
}

@media (max-width: 768px) {
  .top-section {
    flex-direction: column;
    gap: 2rem;
    align-items: center;
    text-align: center;
  }

  .cover-wrapper {
    width: 200px;
  }

  .book-title {
    font-size: 2rem;
  }

  .meta-info,
  .actions,
  .genres {
    justify-content: center;
  }
}
</style>
