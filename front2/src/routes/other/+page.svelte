<script>
    import { onMount } from 'svelte';
    import { api } from '$lib/api';
    import OtherItem from '$lib/components/OtherItem.svelte';

    let filters = [];

    let selectedFilters = $state([]);
    let search = $state('');
	let sortOrder = $state('asc'); // 'asc' or 'desc'
    let loading = $state(true);
    let items = $state([]);
    
    let displayedItems = $derived.by(() => {
        // First filter based on search
        let filtered = !search.trim() 
            ? [...items]
            : items.filter(
                (item) =>
                    item.name.toLowerCase().includes(search.toLowerCase()) ||
                    item.number.toLowerCase().includes(search.toLowerCase()) ||
                    item.type.toLowerCase().includes(search.toLowerCase())
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
    
    onMount(() => {
        api.get('/api/collection?item_type=items').then((response) => {
            console.log(response);
            items = response.response;
        }).catch((error) => {
            console.error(error);
        }).finally(() => {
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

	</section>

    <section class="flex flex-wrap">
        {#if loading}
            <p>Loading...</p>
        {/if}
        {#each displayedItems as item (item._id || item.number)}
            <section class="flex w-[50%] p-2">
                <OtherItem {item} />
            </section>
        {/each}
    </section>

</section>

<style>
    
</style>