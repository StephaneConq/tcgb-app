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
	let { card = $bindable(), displaySet = false } = $props<{
		card: CardModel;
		displaySet?: boolean;
	}>();

	let cards = $state(get(cardsRead));
	let loading = $state(false);
	let cardIndex = $state(0);
	// Local state for the inputs
	let setId = $state(card.set_id || '');
	let cardNumber = $state(card.card_number || '');

	$effect(() => {
		if (card.card_versions) {
			card.selectedCard = card.card_versions[cardIndex];
		} else {
			card.selectedCard = card;
		}
		// Only initialize the selected state if it hasn't been set by user interaction
		if (card.selected === undefined) {
			card.selected = !!!card.selectedCard.count;
		}
		updateStoreCards();
	});

	const handleCardSwitch = (direction: 'previous' | 'next') => {
		if (cardIndex === 0 && direction === 'previous') {
			cardIndex = card.card_versions.length - 1;
		} else if (cardIndex === card.card_versions.length - 1 && direction === 'next') {
			cardIndex = 0;
		} else {
			if (direction === 'previous') {
				cardIndex--;
			} else if (direction === 'next') {
				cardIndex++;
			}
		}

		card.selectedCard = card.card_versions[cardIndex];
		updateStoreCards();
	};

	const updateStoreCards = () => {
		// Update the card in the cardsRead store
		const updatedCards = get(cardsRead).map((c: CardModel) => {
			if (c._id === card._id) {
				return {
					...c,
					selectedCard: card.selectedCard,
					// Store the selected card index so we know which version to save
					selectedCardIndex: cardIndex,
					selected: card.selected
				};
			}
			return c;
		});

		cardsRead.set(updatedCards);
	};

	// update cards in store
	const handleCheck = () => {
		if (displaySet) return;
		card.selected = !card.selected;
		updateStoreCards();
	};

	const handleCardAdd = () => {
		loading = true;
		saveCards([card])
			.then(
				() => {
					addToast('Carte ajoutée', 'success');
					card.selectedCard.count = (card.selectedCard.count || 0) + 1;
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
		if (card.selectedCard.count === 1) {
			const res = confirm('Supprimer cette carte de la collection ?');
			if (!res) return;
		}
		loading = true;
		removeCard(card.ref)
			.then(
				() => {
					addToast('Carte supprimée', 'success');
					card.selectedCard.count = (card.selectedCard.count || 0) - 1;
					if (card.selectedCard.count === 0) {
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
								return { ...cardFetched, selected: card.selected };
							}
							return c;
						});
						card = { ...cardFetched, selected: card.selected };
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

	// Add this new state variable to track visibility of inputs
	let showInputs = $state(false);

	// Add this function to toggle input visibility
	const toggleInputs = () => {
		showInputs = !showInputs;
	};
</script>

{#if card.selectedCard}
	<section class="flex flex-col justify-center items-center gap-2">
		{#if card.card_versions && card.card_versions.length > 1}
			<button
				onclick={() => handleCardSwitch('previous')}
				aria-label="Previous card version"
				class="text-white text-2xl"
			>
				<span class="iconify" data-icon="mdi-arrow-up-drop-circle"></span>
			</button>
		{/if}
		<div class="card-wrapper">
			{#if card.selectedCard.count > 0 && !displaySet}
				<img src="icons/sac-de-courses.svg" alt="Owned icon" class="owned-icon" />
			{/if}
			<div class="card-container glass-bg {!card.selected && !displaySet && 'disabled'}">
				<button
					class="card-image"
					onclick={() => {
						handleCheck();
					}}
				>
					{#if card.selectedCard.card_img}
						<img src={card.selectedCard.card_img} alt="Card illustration" />
					{:else}
						<div class="placeholder-image">No image available</div>
					{/if}
				</button>

				<div class="card-details">
					<div class="details-header">
						<button
							class="toggle-button w-full flex flex-row justify-between items-center"
							onclick={toggleInputs}
							aria-label={showInputs ? 'Cacher' : 'Afficher'}
						>
							<h4 class="details-title text-white">Détails</h4>
							<span class="iconify" data-icon={showInputs ? 'mdi-chevron-up' : 'mdi-chevron-down'}
							></span>
						</button>
					</div>

					{#if showInputs}
						<div class="input-group">
							<label for="set">Set:</label>
							<input
								class="text-white"
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
								class="text-white"
								disabled={displaySet}
								type="text"
								id="number"
								bind:value={cardNumber}
								onkeydown={handleParamChange}
								placeholder="Card number"
							/>
						</div>
					{/if}
				</div>

				<div class="actions-container flex-grow">
					{#if displaySet}
						{#if loading}
							<div class="actions flex flex-row justify-center items-center">
								<LoadingSpinner />
							</div>
						{:else}
							<div class="actions flex flex-row justify-center items-center w-full gap-5">
								{#if !card.selectedCard.count}
									<button
										onclick={handleCardAdd}
										class="bg-[#2865a1] hover:bg-blue-700 text-white p-3 rounded-full shadow-lg transform hover:scale-105 transition-all duration-200"
									>
										<span>Ajouter</span>
									</button>
								{:else}
									<button
										onclick={handleCardRemove}
										class="bg-red-500 hover:bg-red-800 text-white font-bold p-3 rounded-full shadow-lg transform hover:scale-105 transition-all duration-200"
										aria-label="remove from collection"
									>
										<span class="iconify" data-icon="mdi-minus"></span>
									</button>

									<span class="text-center text-white">{card.selectedCard.count}</span>
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
					{:else if loading}
						<div class="actions flex flex-row justify-center items-center">
							<LoadingSpinner />
						</div>
					{/if}
				</div>
			</div>
		</div>

		{#if card.card_versions && card.card_versions.length > 1}
			<button
				onclick={() => handleCardSwitch('next')}
				aria-label="Next card version"
				class="text-white text-2xl"
			>
				<span class="iconify" data-icon="mdi-arrow-down-drop-circle"></span>
			</button>
		{/if}
	</section>
{/if}

<style>
	.card-container {
		padding: 12px;
		display: flex;
		flex-direction: column;
		gap: 10px;
		width: 100%;
		height: 100%; /* Make sure it takes full height */
	}

	/* Add this to your existing styles */
	.card-wrapper {
		position: relative;
		width: 100%;
		min-height: 350px;
		display: flex;
		flex-direction: column;
	}

	.actions-container {
		margin-top: auto; /* Push the actions to the bottom */
		min-height: 40px; /* Reserve space even when actions aren't displayed */
		display: flex;
		flex-direction: column;
		justify-content: flex-end; /* Align content to the bottom */
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
		color: white;
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
		color: white;
	}

	input {
		padding: 8px;
		border: 1px solid #ddd;
		border-radius: 4px;
		font-size: 0.9rem;
	}

	/* Add these new styles */
	.details-header {
		display: flex;
		justify-content: space-between;
		align-items: center;
		margin-bottom: 8px;
	}

	.details-title {
		font-size: 0.9rem;
		font-weight: 600;
		margin: 0;
	}

	.toggle-button {
		background: none;
		border: none;
		cursor: pointer;
		color: white;
		padding: 4px;
		border-radius: 4px;
	}

	.owned-icon {
		position: absolute;
		width: 40px;
		height: 40px;
		top: -15px;
		right: -15px;
		z-index: 10;
		filter: drop-shadow(0 2px 3px rgba(0, 0, 0, 0.3));
	}
</style>
