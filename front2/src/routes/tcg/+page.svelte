<script>
    import pokemon from '$lib/images/pokemon_tcg.png'
    import onePiece from '$lib/images/onepiece_tcg.jpg'

    let { data } = $props();

    const series = $derived([
            {
                name: "Pokemon",
                path: "/tcg/pokemon",
                image: pokemon,
                id: "pokemon"
            },
            {
                name: "One Piece",
                path: "/tcg/one piece",
                image: onePiece,
                id: "one-piece"
            }
        ])
    
</script>

<section class="series">
    {#each series as serie}
        <a class="flex flex-col items-center glassbg p-6" href={serie.path}>
            <img src={serie.image} alt={serie.name} />
        </a>
    {/each}
</section>

<style>
    .series {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 1rem;
    }

    .series a {
        border-radius: 16px;
    }

</style>
