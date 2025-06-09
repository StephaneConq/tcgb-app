<script lang="ts">
	import '../app.css';
	import Toast from '../components/dialogs/toast.svelte';
	import Footer from '../components/Footer.svelte';
	import { afterNavigate, beforeNavigate, goto } from '$app/navigation';
	import { loading } from '$lib/auth';
	import { onMount } from 'svelte';
	import { getAuth, onAuthStateChanged } from 'firebase/auth';

	let { children } = $props();
	let currentPath = $state('');

	let display = $derived(loading);

	function checkLogin() {
		const auth = getAuth();
		onAuthStateChanged(auth, (user) => {
			if (!user) {
				goto('/login');
			}
		});
	}

	onMount(() => {
		checkLogin();
	});

	beforeNavigate(({ to }) => {
		if (to?.route.id === '/login') {
			return;
		}
		checkLogin();
	});

	// Set initial path and update on navigation
	afterNavigate(({ to }) => {
		if (to) {
			currentPath = to.url.pathname;
		}
	});

</script>

<main
	class="bg-[url('/image.png')] bg-center bg-no-repeat w-screen h-screen flex flex-col justify-between bg-[#2865a1] items-center"
>
	{#if display}
		<div class="h-full">
			{@render children()}
		</div>

		{#if currentPath !== '/login'}
			<Footer />
		{/if}
	{/if}

	<Toast />
</main>
