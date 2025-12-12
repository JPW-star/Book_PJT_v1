<script setup>
import { useRouter } from 'vue-router';

const props = defineProps({
  thread: {
    type: Object,
    required: true,
  },
});

const router = useRouter();

const goDetail = () => {
  router.push({ name: 'thread-detail', params: { id: props.thread.id } });
};

const formatDate = (dateString) => {
  return new Date(dateString).toLocaleDateString(undefined, {
    year: 'numeric', month: 'short', day: 'numeric'
  });
};
</script>

<template>
  <div class="thread-item" @click="goDetail">
    <div class="thread-main">
      <h3 class="thread-title">{{ thread.title }}</h3>
      <p class="book-title">on <span>{{ thread.book_title }}</span></p>

      <div class="meta-bottom">
        <span class="author">by {{ thread.user.username }}</span>
        <span class="separator">•</span>
        <span class="date">{{ formatDate(thread.created_at) }}</span>
      </div>
    </div>

    <div class="thread-stats">
      <div class="stat">
        <span class="icon">♥</span>
        <span class="count">{{ thread.like_count }}</span>
      </div>
      <div class="stat">
        <span class="icon">💬</span>
        <span class="count">{{ thread.comment_count }}</span>
      </div>
    </div>
  </div>
</template>

<style scoped>
.thread-item {
  background: #1e1e1e;
  border-radius: 12px;
  padding: 1.5rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  cursor: pointer;
  transition: transform 0.2s, background-color 0.2s;
  border: 1px solid transparent;
}

.thread-item:hover {
  transform: translateY(-2px);
  background: #252525;
  border-color: #333;
}

.thread-main {
  flex: 1;
}

.thread-title {
  font-size: 1.25rem;
  font-weight: 700;
  margin-bottom: 0.4rem;
  color: #fff;
}

.book-title {
  font-size: 0.9rem;
  color: #aaa;
  margin-bottom: 0.8rem;
}

.book-title span {
  color: #ff9800;
  font-weight: 500;
}

.meta-bottom {
  font-size: 0.85rem;
  color: #666;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.author {
  color: #bbb;
}

.thread-stats {
  display: flex;
  gap: 1.5rem;
  padding-left: 2rem;
}

.stat {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.2rem;
  color: #888;
}

.icon {
  font-size: 1.2rem;
}

.count {
  font-size: 0.9rem;
  font-weight: 600;
}
</style>
