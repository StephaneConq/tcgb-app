<script lang="ts">
	import { get } from 'svelte/store';
	import { cardsRead } from '$lib/store/cards';
	import Card from '../../components/Card.svelte';
	import { onDestroy, onMount } from 'svelte';
	import { goto } from '$app/navigation';

	const cards = $state(get(cardsRead));

	onMount(() => {
		if (!get(cardsRead).length) {
			goto('/');
		}
	});

	onDestroy(() => {
		cardsRead.set([]);
	});
</script>

<div class="height-wo-footer grid-container w-full p-5 grid grid-cols-2 gap-4 overflow-y-auto">
	{#each cards as c, i}
		<Card bind:card={cards[i]} displaySet={false} />
	{/each}
</div>
