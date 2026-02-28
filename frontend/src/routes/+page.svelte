<script>
    import {onMount} from "svelte";

    let number = $state(1);
    let test_call = $state("");
    let user = $state("")

    onMount(async () =>
        fetch("http://localhost:8000/greeting", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                name: "Jesse",
                age: 99,
            })
        })
        .then(response => response.json())
        .then(data => {
            user = data.message;
            console.log("state below this");
            console.log($state.snapshot(test_call));
        })
    )
</script>

<h1>Welcome to SvelteKit</h1>
<p>Visit <a href="https://svelte.dev/docs/kit">svelte.dev/docs/kit</a> to read the documentation</p>
<p>Testing API call {number}</p>
<p>Testing API call: {user}</p>
