import { get, writable } from 'svelte/store';
import { browser } from '$app/environment';
import { initializeApp } from 'firebase/app';
import { 
  getAuth, 
  onAuthStateChanged, 
  type User
} from 'firebase/auth';

// Firebase configuration
const firebaseConfig = {
  apiKey: import.meta.env.VITE_FIREBASE_API_KEY,
  authDomain: import.meta.env.VITE_FIREBASE_AUTH_DOMAIN,
  projectId: import.meta.env.VITE_FIREBASE_PROJECT_ID,
  storageBucket: import.meta.env.VITE_FIREBASE_STORAGE_BUCKET,
  messagingSenderId: import.meta.env.VITE_FIREBASE_MESSAGING_SENDER_ID,
  appId: import.meta.env.VITE_FIREBASE_APP_ID
};

// Initialize Firebase
export const app = browser ? initializeApp(firebaseConfig) : undefined;
export const auth = browser ? getAuth(app) : null;

// Create a store for the user
export const user = writable<User | null>(null);
export const loading = writable(true);

let successCallback: any = null;
export const authPromise = new Promise((resolve) => {
  successCallback = resolve;
});

if (browser) {
  onAuthStateChanged(auth, (userData: User | null) => {    
    user.set(userData);
    console.log('user', get(user));
    successCallback();
    loading.set(false);
  });
}
