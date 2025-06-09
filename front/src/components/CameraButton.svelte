<script lang="ts">
	import { goto } from "$app/navigation";
    import { uploadedFile } from "../lib/store/fileUpload";

	function triggerFileInput() {
		const input = document.querySelector('input[type=file]');
		if (input instanceof HTMLInputElement) {
			input.click();
		}
	}

	function handleFileChange(event: Event) {
		const input = event.target as HTMLInputElement;
		
		if (input.files && input.files.length > 0) {
			const file = input.files[0];
			uploadedFile.set(file as any);
            goto('/image')
			input.files = null;
		}
	}
</script>

<button
	aria-label="camera button"
	onclick={triggerFileInput}
	class="shadow-2xl border text-3xl flex shrink-0 items-center justify-center rounded-full size-16 bg-white text-[#2865a1]"
>
	<span class="iconify" data-icon="mdi-camera"></span>
</button>

<input type="file" accept="image/*" class="hidden" onchange={handleFileChange} />
