<script lang="ts">
	import type CardModel from '$lib/models/card.js';
	import Card from '../../../../components/Card.svelte';
	import { fetchCards } from '$lib/store/series';
	import { goto } from '$app/navigation';
	import { browser } from '$app/environment';
	import Loading from '../../../../components/Loading.svelte';

	let { data } = $props();

	// If your load function passes the params
	const slug = data.slug;
	let cardsDisplay: CardModel[] = $state([]);
	let loading = $state(true);

	fetchCards(slug)
		.then((cards) => {
			cardsDisplay = [...cards];
		})
		.catch((error) => {
			console.error('Error loading cards:', error);
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

{#if loading}
	<Loading />
{:else}
	<div class="height-wo-footer grid-container w-full p-5 grid grid-cols-2 gap-4 overflow-y-auto">
		{#each cardsDisplay as c, i (c._id)}
			<Card bind:card={cardsDisplay[i]} displaySet={true} />
		{/each}
	</div>
{/if}
