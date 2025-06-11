<script lang="ts">
	import { browser } from '$app/environment';
	import { goto } from '$app/navigation';
	import type Serie from '$lib/models/serie.js';
	import { fetchSeries } from '$lib/store/series.js';
	import Loading from '../../../components/Loading.svelte';
	let { data } = $props();

	// If your load function passes the params
	const slug = data.slug;

	let loading = $state(true);
	let searchValue = $state('');
	let series: Serie[] = $state([]);

	fetchSeries(slug)
		.then((seriesFetched) => {
			series = seriesFetched;
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

	function filterSeries(searchValue: string) {
		return series.filter((serie) => serie.set_id.toLowerCase().includes(searchValue.toLowerCase()));
	}
</script>

{#if loading}
	<Loading />
{:else}
	<div class="height-wo-footer flex flex-col items-center overflow-y-auto p-6">
		<div class="search-container mb-6 w-full max-w-md">
			<label class="flex flex-col">
				<div class="relative">
					<div class="absolute inset-y-0 left-0 flex items-center pl-3 pointer-events-none">
						<svg
							xmlns="http://www.w3.org/2000/svg"
							class="h-5 w-5 text-gray-400"
							fill="none"
							viewBox="0 0 24 24"
							stroke="currentColor"
						>
							<path
								stroke-linecap="round"
								stroke-linejoin="round"
								stroke-width="2"
								d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
							/>
						</svg>
					</div>
					<input
						bind:value={searchValue}
						type="text"
						placeholder="Chercher par code (ex.: sv4a...)"
						class="w-full text-white pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors"
					/>
				</div>
			</label>
		</div>

		<div>
			{#each searchValue ? filterSeries(searchValue) : series as serie}
				<button
					onclick={() => goto(`/collections/${slug}/${serie._id}`)}
					class="flex flex-col justify-around bg-white m-6 p-6 rounded-lg"
				>
					<img src={serie.serie_logo} alt="{serie.serie_name} logo" class="my-3" />
					<p class="flex flex-row items-center justify-between gap-3">
						<img src={serie.symbol_img} alt="{serie.symbol_img} logo" class="max-w-[60px]" />
						<span class="text-2xl font-bold text-blue-400 text-right">{serie.serie_name}</span>
					</p>
				</button>
			{/each}
		</div>
	</div>
{/if}

<style>
	/* Add this style for white placeholder text */
	input::placeholder {
		color: white;
	}
</style>
