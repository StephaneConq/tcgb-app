<script lang="ts">
	import { onDestroy, onMount } from 'svelte';
	import { uploadedFile, scanFile } from '$lib/store/fileUpload';
	import { goto } from '$app/navigation';

	let loading = $state(false);
	let imageUrl: string = $state('');

	uploadedFile.subscribe((file) => {
		if (file) {
			// Create a URL for the file to display it
			imageUrl = URL.createObjectURL(file);
		} else {
			imageUrl = '';
		}
	});

	onMount(() => {
		if (!imageUrl) {
			goto('/');
		}
	});

	onDestroy(() => {
		uploadedFile.set(null);
	});

	function handleScan() {
		loading = true;
		scanFile().then(
			() => {
				loading = false;
                goto('/scan');
				uploadedFile.set(null);
			},
			() => {
				loading = false;
			}
		);
	}
</script>

<div class="p-10 flex flex-col justify-between items-center h-full">
	<img src={imageUrl} class="max-h-[60vh]" alt="Pokemon cards" />

	{#if loading}
		<div class="flex items-center justify-center">
			<div class="animate-spin rounded-full h-10 w-10 border-b-2 border-white"></div>
			<span class="ml-3 text-white font-medium">Traitement en cours...</span>
		</div>
	{:else}
		<button
			onclick={handleScan}
			class="glass-bg text-white font-bold py-3 px-8 rounded-full shadow-lg transform hover:scale-105 transition-all duration-200 flex items-center gap-2"
		>
			<svg
				xmlns="http://www.w3.org/2000/svg"
				class="h-5 w-5"
				viewBox="0 0 20 20"
				fill="currentColor"
			>
				<path
					fill-rule="evenodd"
					d="M4 4a2 2 0 012-2h8a2 2 0 012 2v2h-2V4H6v2H4V4zm2 6a2 2 0 012-2h8a2 2 0 012 2v8a2 2 0 01-2 2H8a2 2 0 01-2-2v-8zm2 0v8h8v-8H8z"
					clip-rule="evenodd"
				/>
			</svg>
			Scanner
		</button>
	{/if}
</div>
