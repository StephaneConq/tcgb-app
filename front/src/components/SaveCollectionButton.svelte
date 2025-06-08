<script>
	import { cardsRead } from '$lib/store/cards';
	import { get } from 'svelte/store';
	import { saveCards } from '$lib/store/collection';
	import { goto } from '$app/navigation';
	import { addToast } from '$lib/store/toast';

	let loading = $state(false);

	function handleSave() {
		loading = true;
		saveCards(get(cardsRead).filter((c) => c.selected))
			.then(
				() => {
					addToast('Cards saved!', 'success');
					goto('/');
				},
				() => {
					addToast('Error saving cards', 'error');
				}
			)
			.finally(() => {
				loading = false;
			});
	}
</script>

{#if loading}
	<div class="animate-spin rounded-full h-10 w-10 border-b-2 border-[#2865a1]"></div>
{:else}
	<button
		aria-label="camera button"
		onclick={handleSave}
		class="size-12 text-xl shadow-2xl border flex shrink-0 items-center justify-center rounded-full bg-[#2865a1] text-white"
	>
		<span class="iconify" data-icon="mdi-content-save"></span>
	</button>
{/if}
