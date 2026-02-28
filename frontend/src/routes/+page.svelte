<script>
    import {onMount} from "svelte";
    import Qna from "$lib/components/qna.svelte";
    import Result from "$lib/components/result.svelte";


    // function cleanNumInput(e) {
    //     const cleanedNum = e.currentTarget.value.replace(/\D/g, '');
    //     formData.age = cleanedNum;
    //     e.currentTarget.value = cleanedNum;
    // }

    let foods = $state("");

    async function testSearchAPI() {
        fetch("http://localhost:8000/api/search?q=sushi", {
            method: "GET",
            headers: {
                "Content-Type": "application/json"
            },
        })
        .then(response => response.json())
        .then(data => {
            foods = data.results;
            console.log("table under this");
            console.table($state.snapshot(foods));
        })
    }
</script>

<!-- <form> -->
<!--     <input  -->
<!--         id="email" type="text"  -->
<!--         bind:value={formData.username} placeholder="Enter name" -->
<!--     /> -->
<!--     <input id="age" type="text"  -->
<!--     oninput={cleanNumInput} -->
<!--     inputmode="numeric" bind:value={formData.age} placeholder="Enter age" maxlength="3"/> -->
<!--     <button onclick={handleInput} type="submit">Submit</button> -->
<!-- </form> -->

<button onclick={testSearchAPI}>Test Search API (query: sushi)</button>
{#each foods as food}
    <p>{food.name}</p>
{/each}

<Qna />
<Result />
