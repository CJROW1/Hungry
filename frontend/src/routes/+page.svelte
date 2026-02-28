<script>
    import {onMount} from "svelte";
    import Qna from "$lib/components/qna.svelte";
    import Result from "$lib/components/result.svelte";


    // function cleanNumInput(e) {
    //     const cleanedNum = e.currentTarget.value.replace(/\D/g, '');
    //     formData.age = cleanedNum;
    //     e.currentTarget.value = cleanedNum;
    // }

    let food = $state("")

    onMount(async () =>
        fetch("http://localhost:8000/api/search?q={question}", {
            method: "GET",
            headers: {
                "Content-Type": "application/json"
            },
        })
        .then(response => response.json())
        .then(data => {
            food = data.message;
            console.log("table under this");
            console.table(food);
        })
    )
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

<p>Testing API call: {food}</p>
