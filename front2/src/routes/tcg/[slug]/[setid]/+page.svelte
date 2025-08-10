<script>
	import { page } from '$app/state';
	import { api } from '$lib/api';
	import { onMount } from 'svelte';
	import Card from '$lib/components/Card.svelte';

	const { setid } = page.params;
	let loading = $state(true);
	/**
	 * @type {import("$lib/models/card").Card[]}
	 */
	let cards = $state([]);
	let search = $state('');
	let sortOrder = $state('asc'); // 'asc' or 'desc'

	// Use $derived.by with proper dependency tracking
	let displayedCards = $derived.by(() => {
		// First filter based on search
		let filtered = !search.trim() 
			? [...cards]
			: cards.filter(
				(card) =>
					card.card_name.toLowerCase().includes(search.toLowerCase()) ||
					card.card_number.toLowerCase().includes(search.toLowerCase())
			);
		
		// Then sort the filtered results
		// Important: create a new array to ensure reactivity
		return [...filtered].sort((a, b) => {
			if (sortOrder === 'asc') {
				return a.int_number - b.int_number;
			} else {
				return b.int_number - a.int_number;
			}
		});
	});

	function toggleSortOrder() {
		sortOrder = sortOrder === 'asc' ? 'desc' : 'asc';
	}

	onMount(() => {
		api
			.get(`/api/sets/${setid}/cards`)
			.then((response) => {
				cards = response.cards;
			})
			.catch((error) => {
				console.error(error);
			})
			.finally(() => {
				loading = false;
			});
	});
</script>

<section class="flex flex-col gap-6">
	<section>
		<div>
			<label for="search" class="block text-sm/6 font-medium text-gray-900"></label>
			<div class="mt-2">
				<div class="">
					<input
						bind:value={search}
						id="search"
						type="text"
						name="search"
						placeholder="Rechercher"
						class="block w-full min-w-0 grow rounded-md border-gray-300 py-1.5 pr-3 pl-1 text-base text-gray-900 placeholder:text-gray-400 focus:outline-none sm:text-sm/6"
					/>
				</div>
			</div>
		</div>

		<button
			type="button"
			onclick={toggleSortOrder}
			class="flex items-center justify-center"
			title={`Sort ${sortOrder === 'asc' ? 'descending' : 'ascending'}`}
		>
			{#if sortOrder === 'asc'}
				<svg
					xmlns="http://www.w3.org/2000/svg"
					class="h-5 w-5"
					viewBox="0 0 20 20"
					fill="currentColor"
				>
					<path
						fill-rule="evenodd"
						d="M14.707 12.293a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L9 14.586V3a1 1 0 012 0v11.586l2.293-2.293a1 1 0 011.414 0z"
						clip-rule="evenodd"
					/>
				</svg>
			{:else}
				<svg
					xmlns="http://www.w3.org/2000/svg"
					class="h-5 w-5"
					viewBox="0 0 20 20"
					fill="currentColor"
				>
					<path
						fill-rule="evenodd"
						d="M5.293 7.707a1 1 0 010-1.414l4-4a1 1 0 011.414 0l4 4a1 1 0 01-1.414 1.414L11 5.414V17a1 1 0 11-2 0V5.414L6.707 7.707a1 1 0 01-1.414 0z"
						clip-rule="evenodd"
					/>
				</svg>
			{/if}
			<span>Trié par numéro: {sortOrder === 'asc' ? 'Ascendant' : 'Descendant'}</span>
		</button>
	</section>

	<section class="flex flex-wrap">
		{#if loading}
			<p>Loading...</p>
		{/if}
		{#each displayedCards as card (card._id || card.card_number)}
			<section class="flex w-[50%] p-2">
				<Card {card} />
			</section>
		{/each}
	</section>
</section>