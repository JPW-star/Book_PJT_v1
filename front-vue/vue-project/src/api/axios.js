import axios from 'axios';
import { useAuthStore } from '@/stores/auth';

const instance = axios.create({
    baseURL: 'http://127.0.0.1:8000/api/v1/', // Django API V1 Base URL
    timeout: 5000,
});

instance.interceptors.request.use(
    (config) => {
        const authStore = useAuthStore();
        if (authStore.token) {
            config.headers.Authorization = `Bearer ${authStore.token}`;
        }
        return config;
    },
    (error) => Promise.reject(error)
);

instance.interceptors.response.use(
    (response) => response,
    async (error) => {
        // Token Refresh logic could go here
        return Promise.reject(error);
    }
);

export default instance;
