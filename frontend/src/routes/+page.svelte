<script>
    import {onMount} from "svelte";

    let formData = $state({
        username: "",
        age: ""
    })

    function cleanNumInput(e) {
        const cleanedNum = e.currentTarget.value.replace(/\D/g, '');
        formData.age = cleanedNum;
        e.currentTarget.value = cleanedNum;
    }

    async function handleInput() {
        fetch("http://localhost:8000/greeting", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                name: formData.username,
                age: Number(formData.age),
            })
        })
        .then(response => response.json())
        .then(data => {
            user = data.message;
        })
    }

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
        })
    )
</script>

<p>Testing API call: {user}</p>
<form>
    <input 
        id="email" type="text" 
        bind:value={formData.username} placeholder="Enter name"
    />
    <input id="age" type="text" 
    oninput={cleanNumInput}
    inputmode="numeric" bind:value={formData.age} placeholder="Enter age" maxlength="3"/>
    <button onclick={handleInput} type="submit">Submit</button>
</form>
