import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '@/views/HomeView.vue'
import CommunityView from '@/views/CommunityView.vue'
import LoginView from '@/views/LoginView.vue'
import SignupView from '@/views/SignupView.vue'
import ProfileView from '@/views/ProfileView.vue'
import BookDetailView from '@/views/BookDetailView.vue'
import ThreadDetailView from '@/views/ThreadDetailView.vue'
import ThreadCreateView from '@/views/ThreadCreateView.vue'
import { useAuthStore } from '@/stores/auth'

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: [
        {
            path: '/',
            name: 'home',
            component: HomeView,
        },
        {
            path: '/books/:isbn13',
            name: 'book-detail',
            component: BookDetailView,
        },
        {
            path: '/community',
            name: 'community',
            component: CommunityView,
        },
        {
            path: '/community/create',
            name: 'thread-create',
            component: ThreadCreateView,
            meta: { requiresAuth: true }
        },
        {
            path: '/community/:id',
            name: 'thread-detail',
            component: ThreadDetailView,
        },
        {
            path: '/login',
            name: 'login',
            component: LoginView,
        },
        {
            path: '/signup',
            name: 'signup',
            component: SignupView,
        },
        {
            path: '/profile/:username',
            name: 'profile',
            component: ProfileView,
            meta: { requiresAuth: true }
        },
    ],
})

router.beforeEach((to, from) => {
    const authStore = useAuthStore()
    if (to.meta.requiresAuth && !authStore.isAuthenticated) {
        return { name: 'login' }
    }
})

export default router
