<script lang="ts">
	import { get } from 'svelte/store';
	import { cardsRead, getCard } from '$lib/store/cards';
	import type CardModel from '$lib/models/card';
	import { saveCards, removeCard } from '$lib/store/collection';
	import { addToast } from '$lib/store/toast';
	import LoadingSpinner from './LoadingSpinner.svelte';
	import { browser } from '$app/environment';
	import { goto } from '$app/navigation';

	// Define props with $bindable directly inside $props()
	let {
		card = $bindable(),
		displaySet = false,
	} = $props<{
		card: CardModel;
		displaySet?: boolean;
	}>();

	let cards = $state(get(cardsRead));
	let loading = $state(false);

	// Local state for the inputs
	let setId = $state(card.set_id || '');
	let cardNumber = $state(card.card_number || '');
	let selected = $state(true);

	// update cards in store
	const handleCheck = () => {
		if (displaySet) return;
		selected = !selected;
		const newCards = cards.map((c: CardModel) => {
			if (c.set_id === card.set_id && c.card_number === card.card_number) {
				return {
					...c,
					selected
				};
			}
			return c;
		});
		cardsRead.set(newCards);
	};

	const handleCardAdd = () => {
		loading = true;
		saveCards([card])
			.then(
				() => {
					addToast('Carte ajoutée', 'success');
					card.count = (card.count || 0) + 1;
				},
				(error) => {
					console.error('Error saving cards:', error);
					if (error.response && error.response.status === 401) {
						console.log('Unauthorized access detected. Redirecting to login...');

						// Redirect to login page
						if (browser) {
							goto('/login');
						}
					}
				}
			)
			.finally(() => {
				loading = false;
			});
	};

	const handleCardRemove = () => {
		if (card.count === 1) {
			const res = confirm('Supprimer cette carte de la collection ?');
			if (!res) return;
		}
		loading = true;
		removeCard(card.ref)
			.then(
				() => {
					addToast('Carte supprimée', 'success');
					card.count = (card.count || 0) - 1;
					if (card.count === 0) {
						card.selected = false;
					}
				},
				(error) => {
					console.error('Error saving cards:', error);
					if (error.response && error.response.status === 401) {
						console.log('Unauthorized access detected. Redirecting to login...');

						// Redirect to login page
						if (browser) {
							goto('/login');
						}
					}
				}
			)
			.finally(() => {
				loading = false;
			});
	};

	let timeoutId: ReturnType<typeof setTimeout> | null = $state(null);
	const handleParamChange = () => {		
		if (timeoutId) {
			clearTimeout(timeoutId);
		}

		timeoutId = setTimeout(() => {
			loading = true;
			cardNumber = cardNumber.toUpperCase();
			setId = setId.toUpperCase();
			getCard(cardNumber, setId)
				.then(
					(cardFetched) => {
						cards = cards.map((c) => {
							if (c._id === card._id) {
								return {...cardFetched, selected: card.selected};
							}
							return c;
						});
						card = {...cardFetched, selected: card.selected};
						cardsRead.set(cards);						
					},
					(error) => {
						console.error('Error getting card:', error);
						addToast('Une erreur a eu lieu, merci de changer les paramètres de la carte', 'error');
						setId = card.set_id;
						cardNumber = card.card_number;
						if (error.response && error.response.status === 401) {
							console.log('Unauthorized access detected. Redirecting to login...');

							// Redirect to login page
							if (browser) {
								goto('/login');
							}
						}
					}
				)
				.finally(() => {
					loading = false;
				});
		}, 1000);
	};
</script>

<div class="card-container {!selected && 'disabled'} {!displaySet && 'h-fit'}">
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
			<input
				disabled={displaySet}
				type="text"
				id="set"
				bind:value={setId}
				onkeydown={handleParamChange}
				placeholder="Card set"
			/>
		</div>

		<div class="input-group">
			<label for="number">Number:</label>
			<input
				disabled={displaySet}
				type="text"
				id="number"
				bind:value={cardNumber}
				onkeydown={handleParamChange}
				placeholder="Card number"
			/>
		</div>
	</div>
	{#if displaySet}
		<div class="actions-container">
			{#if loading}
				<div class="actions flex flex-row justify-center items-center">
					<LoadingSpinner />
				</div>
			{:else}
				<div class="actions flex flex-row justify-between items-center">
					{#if !card.count}
						<button
							onclick={handleCardAdd}
							class="bg-[#2865a1] hover:bg-blue-700 text-white p-2 rounded-full shadow-lg transform hover:scale-105 transition-all duration-200"
						>
							<span>Ajouter à la collection</span>
						</button>
					{:else}
						<button
							onclick={handleCardRemove}
							class="bg-red-500 hover:bg-red-800 text-white font-bold p-3 rounded-full shadow-lg transform hover:scale-105 transition-all duration-200"
							aria-label="remove from collection"
						>
							<span class="iconify" data-icon="mdi-minus"></span>
						</button>

						<span class="text-center">{card.count}</span>
						<button
							onclick={handleCardAdd}
							class="bg-[#2865a1] hover:bg-blue-700 text-white font-bold p-3 rounded-full shadow-lg transform hover:scale-105 transition-all duration-200"
							aria-label="add to collection"
						>
							<span class="iconify" data-icon="mdi-plus"></span>
						</button>
					{/if}
				</div>
			{/if}
		</div>
	{:else}
		{#if loading}
			<div class="actions flex flex-row justify-center items-center">
				<LoadingSpinner />
			</div>
		{/if}
	{/if}

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

	.actions-container {
		margin-top: auto; /* Push the actions to the bottom */
		min-height: 40px; /* Reserve space even when actions aren't displayed */
	}
</style>
