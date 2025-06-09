import { user, authPromise } from '$lib/auth';
import { get } from 'svelte/store';
import axios from 'axios';

// Create axios instance with default config
const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL
});

// Request interceptor - adds auth token to requests
api.interceptors.request.use(
  async config => {
    await authPromise;
    const token = get(user)?.accessToken;
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`;
    }
    return config;
  },
  error => {
    return Promise.reject(error);
  }
);

// Response interceptor - handles 401 Unauthorized errors
api.interceptors.response.use(
  response => {
    return response;
  },
  error => {
    // Check if error is due to unauthorized access
    if (error.response && error.response.status === 401) {
      console.log('Unauthorized access detected (axios). Redirecting to login...');
      
      // Redirect to login page
      // window.location.href = '/login';
    }
    
    return Promise.reject(error);
  }
);

export default api;
