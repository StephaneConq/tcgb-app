<script lang="ts">
	import type CardModel from '$lib/models/card.js';
	import Card from '../../../../components/Card.svelte';
	import { fetchCards } from '$lib/store/series';
	import { goto } from '$app/navigation';
	import { browser } from '$app/environment';
	let { data } = $props();

	// If your load function passes the params
	const slug = data.slug;
	let cardsDisplay: CardModel[] = $state([]);
	let loading = $state(false);
	fetchCards(slug)
		.then((cards) => {
			cardsDisplay = [...cards];
		})
		.catch((error) => {
			console.error('Error loading series:', error);
			if (error.response && error.response.status === 401) {
				console.log('Unauthorized access detected. Redirecting to login...');

				// Redirect to login page
				if (browser) {
					goto('/login');
				}
			}
		})
		.finally(() => {
			loading = false;
		});
</script>


<div class="height-wo-footer grid-container w-full p-5 grid grid-cols-2 gap-4 overflow-y-auto">
	{#each cardsDisplay as c}
		<Card card={c} />
	{/each}
</div>
