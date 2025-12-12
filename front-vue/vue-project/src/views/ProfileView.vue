<script setup>
import { ref, onMounted, computed, watch } from 'vue';
import { useRoute } from 'vue-router';
import { useAuthStore } from '@/stores/auth';
import axios from '@/api/axios';

const route = useRoute();
const authStore = useAuthStore();

const profileUser = ref(null);
const loading = ref(true);
const error = ref('');

const username = computed(() => route.params.username);
const isMyself = computed(() => {
  return authStore.user && authStore.user.username === username.value;
});

// Since the serializer returns list of objects for followers, we can just count them for display
const followerCount = computed(() => profileUser.value?.followers?.length || 0);
const followingCount = computed(() => profileUser.value?.followings?.length || 0);

// Check if I am following this user
const isFollowing = computed(() => {
  if (!authStore.user || !profileUser.value) return false;
  // Check if my ID is in their followers list
  return profileUser.value.followers.some(follower => follower.id === authStore.user.id);
});

const fetchProfile = async () => {
  loading.value = true;
  error.value = '';
  try {
    const response = await axios.get(`http://127.0.0.1:8000/accounts/profile/${username.value}/`);
    profileUser.value = response.data;
  } catch (err) {
    console.error('Failed to fetch profile:', err);
    error.value = 'Failed to load user profile.';
  } finally {
    loading.value = false;
  }
};

const handleFollow = async () => {
  if (!authStore.isAuthenticated) {
    alert('Please log in to follow.');
    return;
  }

  try {
    const response = await axios.post(`http://127.0.0.1:8000/accounts/follow/${profileUser.value.id}/`);
    // The endpoint returns { followed: boolean }
    // We need to update the local state to reflect change immediately
    // Refresh profile is safest to get updated lists
    await fetchProfile();

    // Also refresh my own user info in store as my followings list changed
    if (authStore.user) {
      authStore.fetchProfile(authStore.user.username);
    }

  } catch (err) {
    console.error('Follow failed:', err);
    alert('Action failed.');
  }
};

// Watch for route changes (e.g. clicking another user in list)
watch(() => route.params.username, () => {
  fetchProfile();
}, { immediate: true });
</script>

<template>
  <div class="profile-container">
    <div v-if="loading" class="loading">Loading profile...</div>
    <div v-else-if="error" class="error">{{ error }}</div>

    <div v-else class="profile-card">
      <div class="profile-header">
        <div class="avatar-placeholder">
          {{ profileUser.username.charAt(0).toUpperCase() }}
        </div>

        <h1 class="username">{{ profileUser.username }}</h1>

        <div class="stats">
          <div class="stat-item">
            <span class="count">{{ followerCount }}</span>
            <span class="label">Followers</span>
          </div>
          <div class="stat-item">
            <span class="count">{{ followingCount }}</span>
            <span class="label">Following</span>
          </div>
        </div>

        <div class="actions">
          <button v-if="!isMyself" @click="handleFollow" class="btn-follow" :class="{ 'following': isFollowing }">
            {{ isFollowing ? 'Unfollow' : 'Follow' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.profile-container {
  max-width: 600px;
  margin: 0 auto;
  padding: 3rem 2rem;
}

.profile-card {
  background: #1e1e1e;
  border-radius: 16px;
  padding: 3rem;
  text-align: center;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.5);
}

.avatar-placeholder {
  width: 100px;
  height: 100px;
  background: #333;
  color: #fff;
  font-size: 3rem;
  font-weight: 700;
  border-radius: 50%;
  display: flex;
  justify-content: center;
  align-items: center;
  margin: 0 auto 1.5rem;
  text-transform: uppercase;
}

.username {
  font-size: 2rem;
  font-weight: 800;
  color: #fff;
  margin-bottom: 2rem;
}

.stats {
  display: flex;
  justify-content: center;
  gap: 3rem;
  margin-bottom: 3rem;
  padding: 1.5rem 0;
  border-top: 1px solid #333;
  border-bottom: 1px solid #333;
}

.stat-item {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.count {
  font-size: 1.5rem;
  font-weight: 700;
  color: #fff;
}

.label {
  color: #888;
  font-size: 0.9rem;
  text-transform: uppercase;
  letter-spacing: 1px;
}

.btn-follow {
  background: #fff;
  color: #000;
  border: none;
  padding: 0.8rem 3rem;
  border-radius: 50px;
  font-weight: 700;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-follow:hover {
  background: #e0e0e0;
  transform: translateY(-2px);
}

.btn-follow.following {
  background: transparent;
  color: #fff;
  border: 1px solid #fff;
}

.btn-follow.following:hover {
  background: rgba(255, 255, 255, 0.1);
}

.loading,
.error {
  text-align: center;
  padding: 4rem;
  color: #888;
}
</style>
