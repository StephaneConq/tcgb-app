<script lang="ts">
	import CameraButton from './CameraButton.svelte';
	import { cardsRead } from '../lib/store/cards';
	import SaveCollectionButton from './SaveCollectionButton.svelte';
	import { goto } from '$app/navigation';

	const currentCardsRead = $derived($cardsRead);

</script>
	

<footer class="shadow-2xl w-[90vw] flex items-center justify-evenly py-3 bg-white rounded-4xl my-5">
	<button
		onclick="{() => goto('/collections')}"
		aria-label="camera button"
		class="size-12 text-xl shadow-2xl border flex shrink-0 items-center justify-center rounded-full bg-white text-[#2865a1]"
	>
		<span class="iconify" data-icon="mdi-search"></span>
	</button>

	<CameraButton />

	{#if currentCardsRead.length > 0}
		<SaveCollectionButton />
	{:else}
		<button
			aria-label="camera button"
			class="shadow-2xl border size-12 text-xl flex shrink-0 items-center justify-center rounded-full bg-white text-[#2865a1]"
		>
			<span class="iconify" data-icon="mdi-image-multiple"></span>
		</button>
	{/if}
</footer>
