<script>
    import { api } from '$lib/api';
	import Card from '$lib/components/Card.svelte';
    import OtherItem from '$lib/components/OtherItem.svelte';
    
    let imageFile = $state(null);
    let imagePreview = $state(null);
    let error = $state('');
    let isUploading = $state(false);
    let fileInputRef;
    let cards = $state([]);
    let otherItems = $state([]);

    // Handle file selection
    function handleFileSelect(event) {
        const file = event.target.files[0];
        if (file) {
            // Check if file is an image
            if (!file.type.startsWith('image/')) {
                error = 'Please select an image file';
                return;
            }
            
            imageFile = file;
            error = '';
            
            // Create preview
            const reader = new FileReader();
            reader.onload = (e) => {
                imagePreview = e.target.result;
            };
            reader.readAsDataURL(file);
        }
    }

    // Upload the image to the API
    async function uploadImage() {
        if (!imageFile) return;

        isUploading = true;
        error = '';

        try {
            const formData = new FormData();
            formData.append('image', imageFile);

            // Send to your API
            const result = await api.post('/api/cards/read', formData);

            console.log('Upload successful:', result);
            // Reset after successful upload
            // imageFile = null;
            // imagePreview = null;
            cards = result.cards;
            otherItems = result.other_items;
            
        } catch (err) {
            console.error('Upload failed:', err);
            error = 'Failed to upload image. Please try again.';
        } finally {
            isUploading = false;
        }
    }

    // Trigger file input click
    function triggerFileInput() {
        fileInputRef?.click();
    }
</script>

<div class="max-w-md mx-auto p-4">
    <h1 class="text-2xl font-bold mb-6">Charger une photo</h1>
    
    {#if error}
        <div class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4" role="alert">
            {error}
        </div>
    {/if}

    {#if imagePreview}
        <div class="mb-4">
            <img 
                src={imagePreview} 
                alt="Selected card" 
                class="max-w-full h-auto rounded-lg shadow-md border border-gray-200"
            />
        </div>
        
        <div class="flex gap-2">
            <button
                onclick={() => {
                    imageFile = null;
                    imagePreview = null;
                }}
                class="flex-1 bg-gray-200 hover:bg-gray-300 text-gray-800 font-bold py-2 px-4 rounded"
            >
                Changer d'image
            </button>
            <button
                onclick={uploadImage}
                disabled={isUploading}
                class="flex-1 bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded disabled:opacity-50"
            >
                {isUploading ? 'Chargement...' : 'Lecture'}
            </button>
        </div>
    {:else}
        <div class="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center">
            <button
                onclick={triggerFileInput}
                class="w-full bg-blue-500 hover:bg-blue-700 text-white font-bold py-3 px-4 rounded"
            >
                Choisir image
            </button>
            <p class="mt-2 text-sm text-gray-500">ou glisser et déposer une image ici</p>
        </div>
        
        <input
            type="file"
            accept="image/*"
            bind:this={fileInputRef}
            onchange={handleFileSelect}
            class="hidden"
        />
    {/if}

    {#if cards.length > 0}
        <section class="flex flex-wrap">
            {#each cards as card}
                {#if card.card_versions}
                    {#each card.card_versions as version}
                        <section class="flex w-[50%] p-2">
                            <Card card={version} />
                        </section>
                    {/each}
                {/if}
                {#if !card.card_versions}
                    <section class="flex w-[50%] p-2">
                        <Card card={card} />
                    </section>
                {/if}
            {/each}
        </section>
    {/if}

    {#if otherItems.length > 0}
        <section class="flex flex-wrap">
            {#each otherItems as item}
                <section class="flex w-[50%] p-2">
                    <OtherItem item={item} />
                </section>
            {/each}
        </section>
    {/if}
</div>