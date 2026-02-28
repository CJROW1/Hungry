<script>
    import { onMount } from 'svelte';
    import Result from "$lib/components/result.svelte";

    let foodData = $state([]);

    onMount(() => {
        const saved = sessionStorage.getItem('hungryResults');
        if (saved) {
            foodData = JSON.parse(saved);
        }
    });
</script>

{#if foodData.length > 0}
    <Result foods={foodData} />
{:else}
    <p>Loading matches...</p>
{/if}