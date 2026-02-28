<script>
    import Intro from "$lib/components/intro.svelte";
    import Result from "$lib/components/result.svelte";


    // function cleanNumInput(e) {
    //     const cleanedNum = e.currentTarget.value.replace(/\D/g, '');
    //     formData.age = cleanedNum;
    //     e.currentTarget.value = cleanedNum;
    // }

    let foods = $state();

    async function testRecommendationAPI() {
        fetch("http://localhost:8000/api/recommendations", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                "category": "Pizza",
                "vibe": "Student Staple",
                "max_price": 100,
                "min_rating": 0,
                "dietary": "",
            })
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

<button onclick={testRecommendationAPI}>Test Search API (query: sushi)</button>
{#each foods as food}
    <p>{food.name}</p>
{/each}

<Intro />
<Result />

