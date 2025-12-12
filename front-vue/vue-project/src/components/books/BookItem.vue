<script setup>
import { computed } from 'vue';
import { useRouter } from 'vue-router';

const props = defineProps({
  book: {
    type: Object,
    required: true,
  },
});

const router = useRouter();

const goDetail = () => {
  router.push({ name: 'book-detail', params: { isbn13: props.book.isbn13 } });
};
</script>

<template>
  <div class="book-card" @click="goDetail">
    <div class="image-container">
      <img :src="book.cover" :alt="book.title" loading="lazy" />
      <div class="overlay">
        <span>View Details</span>
      </div>
    </div>
    <div class="info">
      <h3 class="title">{{ book.title }}</h3>
      <p class="author">{{ book.author }}</p>
    </div>
  </div>
</template>

<style scoped>
.book-card {
  background-color: #1e1e1e;
  border-radius: 12px;
  overflow: hidden;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  cursor: pointer;
  display: flex;
  flex-direction: column;
}

.book-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.4);
}

.image-container {
  position: relative;
  width: 100%;
  padding-top: 140%;
  /* Aspect Ratio for book cover */
  background-color: #2c2c2c;
  overflow: hidden;
}

.image-container img {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.5s ease;
}

.book-card:hover .image-container img {
  transform: scale(1.05);
}

.overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.6);
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.overlay span {
  color: #fff;
  font-weight: 600;
  border: 1px solid #fff;
  padding: 0.5rem 1rem;
  border-radius: 20px;
}

.book-card:hover .overlay {
  opacity: 1;
}

.info {
  padding: 1rem;
  flex: 1;
  display: flex;
  flex-direction: column;
}

.title {
  font-size: 1rem;
  font-weight: 700;
  margin-bottom: 0.4rem;
  line-height: 1.4;
  color: #fff;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.author {
  font-size: 0.85rem;
  color: #aaa;
  margin-top: auto;
}
</style>
