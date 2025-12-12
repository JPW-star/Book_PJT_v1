<script setup>
import { computed } from 'vue';
import { RouterLink, useRouter } from 'vue-router';
import { useAuthStore } from '@/stores/auth';

const authStore = useAuthStore();
const router = useRouter();

const isAuthenticated = computed(() => authStore.isAuthenticated);
const user = computed(() => authStore.user);

const logout = () => {
  authStore.logout();
  router.push({ name: 'home' });
};
</script>

<template>
  <nav class="navbar">
    <div class="nav-container">
      <!-- Logo -->
      <RouterLink :to="{ name: 'home' }" class="logo">
        <span class="logo-icon">Book</span>The Garden
      </RouterLink>

      <!-- Navigation Links -->
      <div class="nav-links">
        <RouterLink :to="{ name: 'home' }" class="nav-item">Books</RouterLink>
        <RouterLink :to="{ name: 'community' }" class="nav-item">Community</RouterLink>
      </div>

      <!-- Auth Buttons -->
      <div class="auth-buttons">
        <template v-if="isAuthenticated">
          <!-- Profile Link -->
          <RouterLink v-if="user" :to="{ name: 'profile', params: { username: user.username } }"
            class="nav-item profile-link">
            {{ user.username }}
          </RouterLink>
          <button @click="logout" class="btn-secondary">Logout</button>
        </template>
        <template v-else>
          <RouterLink :to="{ name: 'login' }" class="nav-item">Log in</RouterLink>
          <RouterLink :to="{ name: 'signup' }" class="btn-primary">Sign up</RouterLink>
        </template>
      </div>
    </div>
  </nav>
</template>

<style scoped>
.navbar {
  position: sticky;
  top: 0;
  z-index: 1000;
  background-color: rgba(18, 18, 18, 0.95);
  backdrop-filter: blur(10px);
  border-bottom: 1px solid #333;
  padding: 1rem 0;
}

.nav-container {
  max-width: 1280px;
  margin: 0 auto;
  padding: 0 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

/* Logo */
.logo {
  font-size: 1.5rem;
  font-weight: 700;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #fff;
}

.logo-icon {
  background: #fff;
  color: #000;
  padding: 0.1rem 0.5rem;
  border-radius: 4px;
  font-weight: 900;
}

/* Nav Links */
.nav-links {
  display: flex;
  gap: 2rem;
}

.nav-item {
  color: #aaa;
  font-weight: 500;
  font-size: 0.95rem;
}

.nav-item:hover,
.router-link-active {
  color: #fff;
}

/* Auth Buttons */
.auth-buttons {
  display: flex;
  align-items: center;
  gap: 1.5rem;
}

.btn-primary {
  background-color: #fff;
  color: #000;
  padding: 0.6rem 1.5rem;
  border-radius: 50px;
  font-weight: 600;
  font-size: 0.9rem;
  transition: transform 0.2s, background-color 0.2s;
}

.btn-primary:hover {
  background-color: #e0e0e0;
  transform: translateY(-1px);
}

.btn-secondary {
  background: transparent;
  border: 1px solid #555;
  color: #fff;
  padding: 0.5rem 1.2rem;
  border-radius: 50px;
  cursor: pointer;
  font-size: 0.85rem;
  transition: all 0.2s;
}

.btn-secondary:hover {
  border-color: #fff;
}

.profile-link {
  font-weight: 600;
  color: #fff;
}
</style>
