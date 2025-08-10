<script>
    
    let props = $props();
    /**
     * @type {import("$lib/models/set").Set}
	 */
    const set = props.set;
    const slug = props.slug;
    
</script>

<a href={slug + "/" + set._id} class="glassbg p-6 flex flex-col items-center text-center gap-3 rounded-[2vw]">
    <img class="h-[100px]" src={set.serie_logo} alt={set.serie_name} />
    {#if set.symbol_img}
        <img class="w-[50px]" src={set.symbol_img} alt={set.serie_name} />
    {/if}
    <h2 class="text-2xl font-bold">{set.serie_name}</h2>
</a>

<style>
    
</style>

    
