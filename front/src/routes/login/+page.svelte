<script lang="ts">
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import { browser } from '$app/environment';
	// import { initializeApp } from 'firebase/app';
	import { app } from '$lib/auth';
	import { getAuth, signInWithPopup, GoogleAuthProvider, onAuthStateChanged } from 'firebase/auth';

	let loading = true;
	let error: any = null;

	const auth = browser ? getAuth(app) : null;
	const provider = browser ? new GoogleAuthProvider() : null;

	onMount(() => {
		if (browser && auth) {
			// Check if user is already logged in
			onAuthStateChanged(auth, (user) => {
				loading = false;
				if (user) {
					// User is signed in, redirect to home page
					goto('/');
				}
			});
		}
	});

	async function signInWithGoogle() {
		if (!auth || !provider) return;
		console.log('auth', auth);
		console.log('provider', provider);
		
		
		try {
			loading = true;
			error = null;
			await signInWithPopup(auth, provider);
			goto('/');
		} catch (err) {
			console.error('Error signing in with Google:', err);
			error = err.message;
			loading = false;
		}
	}
</script>

<div class="login-container">
	<div class="login-card">
		<h1>Login</h1>

		{#if loading}
			<div class="loading">Loading...</div>
		{:else}
			{#if error}
				<div class="error-message">
					{error}
				</div>
			{/if}

			<button class="google-signin-button" on:click={signInWithGoogle}>
				<img
					src="https://www.gstatic.com/firebasejs/ui/2.0.0/images/auth/google.svg"
					alt="Google logo"
				/>
				Sign in with Google
			</button>
		{/if}
	</div>
</div>

<style>
	.login-container {
		display: flex;
		justify-content: center;
		align-items: center;
		min-height: 100vh;
		width: 80vw;
	}

	.login-card {
		background-color: white;
		border-radius: 8px;
		box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
		padding: 2rem;
		width: 100%;
		max-width: 400px;
		height: 20vh;
		text-align: center;
	}

	h1 {
		margin-bottom: 2rem;
		color: #333;
	}

	.google-signin-button {
		display: flex;
		align-items: center;
		justify-content: center;
		gap: 10px;
		background-color: white;
		color: #757575;
		border: 1px solid #ddd;
		border-radius: 4px;
		padding: 10px 16px;
		font-size: 16px;
		font-weight: 500;
		cursor: pointer;
		width: 100%;
		transition: background-color 0.3s;
	}

	.google-signin-button:hover {
		background-color: #f5f5f5;
	}

	.google-signin-button img {
		width: 18px;
		height: 18px;
	}

	.loading {
		padding: 1rem;
		color: #666;
	}

	.error-message {
		color: #d32f2f;
		margin-bottom: 1rem;
		padding: 0.5rem;
		background-color: #ffebee;
		border-radius: 4px;
	}
</style>
