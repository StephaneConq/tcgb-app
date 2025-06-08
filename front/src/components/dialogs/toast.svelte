<script>
	import { toasts } from '$lib/store/toast';
	import { fly } from 'svelte/transition';
</script>

<div class="toast-container">
	{#each $toasts as toast (toast.id)}
		<div class="toast toast-{toast.type}" transition:fly={{ y: 30, duration: 300 }}>
			<span>{toast.message}</span>
		</div>
	{/each}
</div>

<style>
	.toast-container {
		position: fixed;
		bottom: 20px;
        width: 100vw;
		z-index: 9999;
		display: flex;
		flex-direction: column;
		align-items: center;
        justify-content: center;
		gap: 10px;
	}

	.toast {
		padding: 12px 16px;
		border-radius: 8px;
		color: white;
		box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
		min-width: 200px;
        width: 80%;
	}

	.toast-info {
		background-color: #2865a1;
	}

	.toast-success {
		background-color: #4caf50;
	}

	.toast-error {
		background-color: #f44336;
	}
</style>
