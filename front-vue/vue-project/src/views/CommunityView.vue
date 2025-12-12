<script setup>
import ThreadList from '@/components/community/ThreadList.vue';
</script>

<template>
  <div class="community-container">
    <header class="page-header">
      <h1 class="page-title">Community Reviews</h1>
      <p class="page-desc">See what others are saying about their favorite books.</p>
    </header>

    <ThreadList />
  </div>
</template>

<style scoped>
.community-container {
  max-width: 1000px;
  margin: 0 auto;
  padding: 3rem 2rem;
}

.page-header {
  margin-bottom: 3rem;
  text-align: center;
}

.page-title {
  font-size: 2.5rem;
  font-weight: 800;
  color: #fff;
  margin-bottom: 0.5rem;
}

.page-desc {
  color: #888;
  font-size: 1.1rem;
}
</style>
