<script>
    import { api } from '$lib/api';

    let props = $props();
    /**
     * @type {import("$lib/models/item").Item}
     */
    const item = props.item;

    function increment() {
        api.patch(`/api/collection`, {
            items: [
                item
            ]
        }).then(() => {
            item.count ? item.count += 1 : item.count = 1;
        });
    }

    function decrement() {
        api.delete(`/api/collection?item_ref=${item._id}&item_type=items`).then(() => {
            item.count ? item.count -= 1 : item.count = 0;
        });
    }
</script>

<div
    class="flex w-60 flex-col overflow-hidden rounded-xl bg-white shadow-lg transition-all duration-200 ease-in-out hover:-translate-y-1 hover:scale-[1.03] hover:shadow-xl dark:bg-zinc-800"
>
    <div class="aspect-[63/88] w-full bg-gray-200 dark:bg-zinc-700">
        <img
            class="h-full w-full object-cover"
            src={item.uploaded_image}
            alt={item.name}
            loading="lazy"
        />
    </div>

    <div class="flex flex-col gap-3 border-t border-gray-200 p-4 dark:border-zinc-700 flex-1">
        <h5 class="text-base leading-tight text-gray-900 dark:text-white">
            {item.type}
        </h5>
        <h3 class="text-base leading-tight font-semibold text-gray-900 dark:text-white">
            {item.name}
        </h3>

        <div class="flex justify-between text-xs text-gray-500 dark:text-zinc-400">
            <span>No. {item.number}</span>
        </div>

        <div class="flex items-center justify-center text-sm mt-auto">
            <div class="flex items-center gap-2">
                <button
                    onclick={decrement}
                    disabled={item.count === 0}
                    aria-label="Decrease count"
                    class="flex h-7 w-7 items-center justify-center rounded-full border border-gray-300 bg-white text-xl leading-none font-bold text-gray-700 transition-colors hover:bg-gray-100 dark:border-zinc-600 dark:bg-zinc-700 dark:text-zinc-200 dark:hover:bg-zinc-600"
                >
                    -
                </button>
                <span class="min-w-[2ch] text-center text-base font-bold text-gray-900 dark:text-white">
                    {item.count}
                </span>
                <button
                    onclick={increment}
                    aria-label="Increase count"
                    class="flex h-7 w-7 items-center justify-center rounded-full border border-gray-300 bg-white text-xl leading-none font-bold text-gray-700 transition-colors hover:bg-gray-100 dark:border-zinc-600 dark:bg-zinc-700 dark:text-zinc-200 dark:hover:bg-zinc-600"
                >
                    +
                </button>
            </div>
        </div>
    </div>
</div>