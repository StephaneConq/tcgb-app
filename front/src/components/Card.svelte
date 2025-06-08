<!-- 
TODO
- sur une carte, modifier le set ou la collection
- voir la collection
- voir si on a déjà la carte

-->

<script lang="ts">
	import { get } from 'svelte/store';
	import { cardsRead } from '../lib/store/cards';
	import type CardModel from "$lib/models/card";

	const { card } = $props();
	const cards = $state(get(cardsRead));

	// Local state for the inputs
	let setName = $state(card.set_tag || '');
	let cardNumber = $state(card.card_number || '');
	let selected = $state(true);

	// update cards in store
	const handleCheck = () => {
		selected = !selected;
		const newCards = cards.map((c: CardModel) => {
			if (c.set_tag === card.set_tag && c.card_number === card.card_number) {
				return {
					...c,
					selected
				};
			}
			return c;
		});
		cardsRead.set(newCards)
	};
</script>

<div class="card-container {!selected && 'disabled'}">
	<button
		class="card-image"
		onclick={() => {
			handleCheck();
		}}
	>
		{#if card.card_img}
			<img src={card.card_img} alt="Card illustration" />
		{:else}
			<div class="placeholder-image">No image available</div>
		{/if}
	</button>

	<div class="card-details">
		<div class="input-group">
			<label for="set">Set:</label>
			<input type="text" id="set" bind:value={setName} placeholder="Card set" />
		</div>

		<div class="input-group">
			<label for="number">Number:</label>
			<input type="text" id="number" bind:value={cardNumber} placeholder="Card number" />
		</div>
	</div>
</div>

<style>
	.card-container {
		border: 1px solid #ddd;
		border-radius: 8px;
		padding: 12px;
		margin-bottom: 16px;
		background-color: white;
		box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
		display: flex;
		flex-direction: column;
		gap: 10px;
		max-height: max-content;
	}

	.card-container.disabled {
		opacity: 0.5;
	}

	.card-image {
		width: 100%;
		display: flex;
		justify-content: center;
		align-items: center;
	}

	.card-image img {
		max-width: 100%;
		border-radius: 4px;
	}

	.placeholder-image {
		width: 100%;
		height: 200px;
		background-color: #f0f0f0;
		display: flex;
		justify-content: center;
		align-items: center;
		color: #666;
		border-radius: 4px;
	}

	.card-details {
		display: flex;
		flex-direction: column;
		gap: 8px;
	}

	.input-group {
		display: flex;
		flex-direction: column;
	}

	label {
		font-size: 0.8rem;
		margin-bottom: 2px;
		color: #555;
	}

	input {
		padding: 8px;
		border: 1px solid #ddd;
		border-radius: 4px;
		font-size: 0.9rem;
	}
</style>
