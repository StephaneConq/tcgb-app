<script>
	import { page } from '$app/state';
	import { onMount } from 'svelte';
	import { api } from '$lib/api';
	import Set from './Set.svelte';

	let { data } = $props();

	const { slug } = page.params;
	/**
	 * @type {boolean}
	 */
	let loading = $derived(true);
	/**
	 * @type {import("$lib/models/set").Set[]}
	 */
	let sets = $derived([]);
	let search = $state('');

    /**
	 * @type {import("$lib/models/set").Set[]}
	 */
	let displayedSets = $derived.by(() => {
        // First filter based on search
		let filtered = !search.trim() 
			? [...sets]
			: sets.filter(
				(set) =>
					set.set_id.toLowerCase().includes(search.toLowerCase()) ||
					set.serie_name.toLowerCase().includes(search.toLowerCase())
			);
        return [...filtered].sort((a, b) => {
            const aDate = new Date(a.date);
            const bDate = new Date(b.date);
            return aDate.valueOf() - bDate.valueOf();
        });
    });

	onMount(async () => {
		const response = await api.get(`/api/sets?licence=${slug}`);
		loading = false;
		sets = response.series;
		displayedSets = [...sets];
	});

	let timeout = $derived(0);

	function runSearch() {
		if (timeout) {
			clearTimeout(timeout);
		}
		timeout = setTimeout(() => {
			displayedSets = [];

			if (search === '') {
				displayedSets = [...sets];
				return;
			}

			const filteredSets = sets.filter(
				(set) =>
					set.serie_name.toLowerCase().includes(search.toLowerCase()) ||
					set.set_id.toLowerCase().includes(search.toLowerCase())
			);
            // required to update the display
			setTimeout(() => {
				displayedSets = [...filteredSets];
			});
		});
	}
</script>

<section class="align-center flex flex-col justify-center gap-6">
	<section>
		<div>
			<label for="search" class="block text-sm/6 font-medium text-gray-900"></label>
			<div class="mt-2">
				<div class="">
					<input
						bind:value={search}
						onkeyup={runSearch}
						id="search"
						type="text"
						name="search"
						placeholder="Rechercher"
						class="block w-full min-w-0 grow rounded-md border-gray-300 py-1.5 pr-3 pl-1 text-base text-gray-900 placeholder:text-gray-400 focus:outline-none sm:text-sm/6"
					/>
				</div>
			</div>
		</div>
	</section>

	{#if loading}
		<p>Loading...</p>
	{/if}
	{#each displayedSets as set}
		<Set {set} {slug} />
	{/each}
</section>

<style>
</style>
