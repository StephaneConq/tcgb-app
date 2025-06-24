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
	let currentSort = $state<object>({
		'number': 'asc'
	});

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

	function handleSort(criteria: string) {
		currentSort[criteria] = currentSort[criteria] === 'asc' ? 'desc' : 'asc';
		sort();
	}

	function sort() {
		cardsDisplay.sort((a, b) => {
			const aNumber = a?.int_number ?? 0;
			const bNumber = b?.int_number ?? 0;
			
			if (currentSort['number'] === 'asc') {
				return aNumber - bNumber;
			} else {
				return bNumber - aNumber;
			}
		});
	}
</script>

{#if loading}
	<Loading />
{:else}
	<div class="height-wo-footer w-full p-5 gap-4 flex flex-col">
		<div class="h-min flex flex-row justify-start items-center gap-3">
			<button
				onclick={() => handleSort('number')}
				class="glass-bg p-3 rounded-lg text-white font-bold"
			>
				<span class="mr-3">Numéro</span>
				{currentSort.number === 'asc' ? '▼' : '▲'}
			</button>
		</div>

		<div class="grid-container w-full grid grid-cols-2 gap-6 overflow-y-auto">
			{#each cardsDisplay as c, i (c._id)}
				<Card bind:card={cardsDisplay[i]} displaySet={true} />
			{/each}
		</div>
	</div>
{/if}
