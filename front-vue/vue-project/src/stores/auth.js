import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import axios from '@/api/axios' // Custom axios instance
import axiosOrigin from 'axios' // Original axios for non-auth calls (like initial login) if needed, but we can use instance

export const useAuthStore = defineStore('auth', () => {
    const token = ref(localStorage.getItem('token'))
    const user = ref(JSON.parse(localStorage.getItem('user')))

    const isAuthenticated = computed(() => !!token.value)

    const login = async (username, password) => {
        try {
            // 1. Get Token
            // Note: Architecture Plan said /api/token/ but axios base is /api/v1/
            // Backend settings showed /api/token/ is at root, not v1. 
            // We need to be careful with URLs.
            // Let's assume we handle the full path for auth or adjust axios base.
            // Actually, let's make a separate naked axios call or override baseURL for this one.
            const response = await axiosOrigin.post('http://127.0.0.1:8000/accounts/api/token/', {
                username,
                password
            })

            const accessToken = response.data.access
            token.value = accessToken
            localStorage.setItem('token', accessToken)

            // 2. Get User Profile
            await fetchProfile(username)

            return true
        } catch (error) {
            console.error('Login failed:', error)
            throw error
        }
    }

    const signup = async (userData) => {
        try {
            // Accounts signup is at /accounts/signup/ -> So it's http://127.0.0.1:8000/accounts/signup/
            // Our axios base is /api/v1/. We need to go up.
            await axiosOrigin.post('http://127.0.0.1:8000/accounts/signup/', userData)
        } catch (error) {
            console.error('Signup failed:', error)
            throw error
        }
    }

    const fetchProfile = async (username) => {
        try {
            // Need to use the intercepted axios instance here
            // Profile URL: /accounts/profile/<username>/
            // This is also NOT under /api/v1/ based on previous steps? 
            // Wait, let's check back-django/book_pjt/urls.py
            // path('accounts/', include('accounts.urls'))
            // path('api/v1/books/', include('books.urls'))
            // path('api/v1/community/', include('community.urls'))
            // So accounts are at root /accounts/. 

            const response = await axios.get(`http://127.0.0.1:8000/accounts/profile/${username}/`)
            user.value = response.data
            localStorage.setItem('user', JSON.stringify(response.data))
        } catch (error) {
            console.error('Fetch profile failed:', error)
        }
    }

    const logout = () => {
        token.value = null
        user.value = null
        localStorage.removeItem('token')
        localStorage.removeItem('user')
    }

    return { token, user, isAuthenticated, login, signup, logout, fetchProfile }
})
