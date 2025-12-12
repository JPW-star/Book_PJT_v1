<script setup>
import { ref } from 'vue';
import { useAuthStore } from '@/stores/auth';
import { useRouter } from 'vue-router';

const authStore = useAuthStore();
const router = useRouter();

const username = ref('');
const password = ref('');
const confirmPassword = ref('');
const error = ref('');
const loading = ref(false);

const handleSignup = async () => {
  error.value = '';

  if (password.value.length < 4) {
    error.value = 'Password must be at least 4 characters long.';
    return;
  }

  if (password.value !== confirmPassword.value) {
    error.value = 'Passwords do not match.';
    return;
  }

  loading.value = true;

  try {
    await authStore.signup({
      username: username.value,
      password: password.value,
    });

    // After signup, user might want to auto-login, but let's redirect to login for clarity or auto login
    // For simple flow: Alert success and go to login
    alert('Account created successfully! Please log in.');
    router.push({ name: 'login' });

  } catch (err) {
    console.error(err);
    if (err.response && err.response.data) {
      // Handle Django error format (e.g. { username: ['Exists'] })
      error.value = Object.values(err.response.data).flat().join(' ');
    } else {
      error.value = 'Signup failed. Please try again.';
    }
  } finally {
    loading.value = false;
  }
};
</script>

<template>
  <div class="auth-container">
    <div class="auth-card">
      <h1 class="title">Create Account</h1>
      <p class="subtitle">Join our community of book lovers</p>

      <form @submit.prevent="handleSignup" class="auth-form">
        <div class="form-group">
          <label for="username">Username</label>
          <input id="username" v-model="username" type="text" placeholder="Choose a username" required />
        </div>

        <div class="form-group">
          <label for="password">Password</label>
          <input id="password" v-model="password" type="password" placeholder="Create a password" required />
        </div>

        <div class="form-group">
          <label for="confirmPassword">Confirm Password</label>
          <input id="confirmPassword" v-model="confirmPassword" type="password" placeholder="Repeat password"
            required />
        </div>

        <div v-if="error" class="error-msg">{{ error }}</div>

        <button type="submit" class="btn-submit" :disabled="loading">
          {{ loading ? 'Creating Account...' : 'Sign Up' }}
        </button>
      </form>

      <p class="switch-link">
        Already have an account?
        <RouterLink :to="{ name: 'login' }">Log in</RouterLink>
      </p>
    </div>
  </div>
</template>

<style scoped>
/* Reusing styles from LoginView - In a real large app, should extract to common CSS or component */
.auth-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 80vh;
  padding: 2rem;
}

.auth-card {
  background: #1e1e1e;
  padding: 3rem;
  border-radius: 16px;
  width: 100%;
  max-width: 400px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.5);
  text-align: center;
}

.title {
  font-size: 2rem;
  font-weight: 700;
  margin-bottom: 0.5rem;
  color: #fff;
}

.subtitle {
  color: #888;
  margin-bottom: 2.5rem;
}

.auth-form {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  text-align: left;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

label {
  font-size: 0.9rem;
  color: #ccc;
  font-weight: 500;
}

input {
  background: #2c2c2c;
  border: 1px solid #444;
  color: #fff;
  padding: 0.8rem 1rem;
  border-radius: 8px;
  font-size: 1rem;
  transition: border-color 0.2s;
}

input:focus {
  outline: none;
  border-color: #ff9800;
}

.btn-submit {
  background-color: #fff;
  color: #000;
  border: none;
  padding: 1rem;
  border-radius: 8px;
  font-weight: 700;
  font-size: 1rem;
  cursor: pointer;
  margin-top: 1rem;
  transition: background-color 0.2s;
}

.btn-submit:hover:not(:disabled) {
  background-color: #e0e0e0;
}

.btn-submit:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.error-msg {
  color: #ff5252;
  font-size: 0.9rem;
  text-align: center;
}

.switch-link {
  margin-top: 2rem;
  color: #888;
  font-size: 0.9rem;
}

.switch-link a {
  color: #ff9800;
  font-weight: 600;
  margin-left: 0.4rem;
}

.switch-link a:hover {
  text-decoration: underline;
}
</style>
