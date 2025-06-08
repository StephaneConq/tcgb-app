<script>
import { goto } from '$app/navigation';

const licences = [
    {
        slug: 'pokemon',
        name: 'Pokémon',
        image: 'pokemon.png'
    }
]
</script>

<div class="flex flex-col items-center justify-center h-full">

    <h1 class="text-4xl font-bold m-6 text-white">Licences</h1>

    {#each licences as licence}

    <button 
    onclick="{() => goto(`/collections/${licence.slug}`)}"
    class="flex flex-col items-center justify-center w-5/6 p-6 bg-white rounded-lg shadow-lg">
        <img src={licence.image} alt={licence.name} class="" />
    </button>

    {/each}
    
</div>