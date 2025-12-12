<script setup>
import BookList from '@/components/books/BookList.vue';
</script>

<template>
  <main class="home-container">
    <!-- Hero Section -->
    <section class="hero">
      <div class="hero-content">
        <h1 class="hero-title">
          BOOKS<br>
          F<span class="highlight">O</span>R ALL
        </h1>
        <p class="hero-subtitle">
          배고프다..
        </p>
      </div>
    </section>

    <!-- Book List Section -->
    <section class="content">
      <h2 class="section-title">Best Sellers</h2>
      <BookList />
    </section>
  </main>
</template>

<style scoped>
.home-container {
  max-width: 1280px;
  margin: 0 auto;
}

/* Hero Section matching the reference vibe */
.hero {
  padding: 4rem 2rem;
  margin-bottom: 2rem;
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
}

.hero-title {
  font-size: 5rem;
  font-weight: 900;
  line-height: 1;
  letter-spacing: -2px;
  margin-bottom: 1.5rem;
  text-transform: uppercase;
  color: #fff;
}

.highlight {
  display: inline-block;
  border: 4px solid #fff;
  border-radius: 50%;
  width: 0.8em;
  height: 0.8em;
  text-align: center;
  line-height: 0.7em;
  margin: 0 5px;
  font-weight: 300;
  /* Visual styling to mimic the "0" circle in the reference image */
}

.hero-subtitle {
  font-size: 1.1rem;
  color: #bbb;
  max-width: 600px;
  margin: 0 auto;
}

.section-title {
  font-size: 1.5rem;
  margin-bottom: 1.5rem;
  font-weight: 700;
  color: #ff9800;
  /* Accent color */
  text-transform: uppercase;
  letter-spacing: 1px;
  padding-left: 2rem;
}

.content {
  padding: 0 2rem;
}

@media (max-width: 768px) {
  .hero-title {
    font-size: 3rem;
  }
}
</style>
