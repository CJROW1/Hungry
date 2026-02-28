<script>
    import {onMount} from "svelte";

    let number = $state(1);
    let test_call = $state("");

    onMount(async () =>
        fetch("https://www.thecocktaildb.com/api/json/v1/1/filter.php?i=Bourbon")
        .then(response => response.json())
        .then(data => {
            test_call = data.drinks[0].strDrink;
            console.log("state below this");
            console.log($state.snapshot(test_call));
        })
    )
</script>

<h1>Welcome to SvelteKit</h1>
<p>Visit <a href="https://svelte.dev/docs/kit">svelte.dev/docs/kit</a> to read the documentation</p>
<p>Testing API call {number}</p>
<p>Testing API call {test_call}</p>
