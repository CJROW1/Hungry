<script lang="ts">
    type Food = {
        id?: number;
        name?: string;
        title?: string;
        image?: string;
        url?: string;
        category?: string;
        price?: string;
        match_percentage?: number;
    };

    let {
        foods = [],
        cupidImage = '/src/lib/assets/character.png'
    }: {
        foods?: Food[];
        cupidImage?: string;
    } = $props();

    let currentIndex = $state(0);
    let currentFood = $derived(foods[currentIndex] ?? null);

    // Timer Logic
    let timeLeft = $state(0);
    let timerString = $derived(() => {
        const mins = Math.floor(timeLeft / 60);
        const secs = timeLeft % 60;
        return `${mins}:${secs.toString().padStart(2, '0')}`;
    });

    $effect(() => {
        if (currentFood) timeLeft = Math.floor(Math.random() * 300) + 120;
    });

    $effect(() => {
        const interval = setInterval(() => { if (timeLeft > 0) timeLeft--; }, 1000);
        return () => clearInterval(interval);
    });

    // Savings Logic (Demo-Proof)
    let savings = $derived(() => {
        if (!currentFood?.price) return { percent: 0, original: "$0" };
        const current = parseFloat(currentFood.price.replace('$', ''));
        const percent = 35 + (currentFood.id ? currentFood.id % 20 : 5); 
        const original = (current / (1 - percent / 100)).toFixed(2);
        return { percent, original: `$${original}` };
    });

    function nextDeal() {
        if (currentIndex < foods.length - 1) currentIndex += 1;
    }

    function takeDeal() {
        window.open(currentFood?.url || "https://www.ubereats.com", '_blank');
    }

    function startOver() {
        window.location.href = '/'; 
    }

    function getKeyword(food: Food) {
        if (!food) return "meal";
        const keywords: Record<string, string> = {
            "Sushi": "sushi", "Chinese": "asian-food", "Indian": "curry",
            "Vietnamese": "pho", "Korean": "korean-bbq", "Ramen": "ramen",
            "Burgers": "burger", "Pizza": "pizza", "Mexican": "taco"
        };
        const searchString = `${food.name || ''} ${food.category || ''}`.toLowerCase();
        const match = Object.keys(keywords).find(key => searchString.includes(key.toLowerCase()));
        return match ? keywords[match] : (food.category?.split('/')[0].split(' ')[0].toLowerCase() || "food");
    }
</script>

<svelte:head>
    <title>Hungry | Result</title>
    <link href="https://fonts.googleapis.com/css2?family=League+Spartan:wght@700;900&family=Inter:ital,wght@0,400;0,700;0,900;1,900&display=swap" rel="stylesheet" />
</svelte:head>

<div class="page">
    <header class="topbar">
        <h1>Hungry</h1>
    </header>

    <section class="hero">
        {#if currentFood}
            <div class="content">
                <div class="photo-wrap">
                    <div class="photo-card">
                        <img src={`images/${getKeyword(currentFood)}.jpg`} alt="match" />
                        
                        <div class="price-tag">
                            <span class="now">{currentFood.price || '$0'}</span>
                            <span class="was">{savings().original}</span>
                        </div>

                        <div class="timer-float">
                            <span class="pulse-dot"></span>
                            ENDS IN {timerString()}
                        </div>
                    </div>
                </div>

                <div class="center-copy">
                    <span class="match-count">Match {currentIndex + 1} of {foods.length}</span>

                    <div class="badge-row">
                        {#if currentFood.match_percentage}
                            <div class="match-badge">{currentFood.match_percentage}% MATCH</div>
                        {/if}
                        <div class="save-badge">SAVE {savings().percent}%</div>
                    </div>

                    <h2 class="headline"><i>The perfect match for you has arrived!</i></h2>

                    <p class="restaurant-name">{currentFood.name || 'Unnamed Deal'}</p>

                    <div class="actions">
                        <button class="primary" onclick={takeDeal}>Just right for me!</button>
                        <button class="secondary" onclick={nextDeal}>Explore other options</button>
                        <button class="start-over" onclick={startOver}>Start Over</button>
                    </div>
                </div>

                <div class="cupid-wrap">
                    <img src={cupidImage} alt="Cupid" />
                </div>
            </div>
        {:else}
            <div class="empty-state">
                <h2 class="headline">No matches found.</h2>
                <button class="start-over" onclick={startOver}>Try Again</button>
            </div>
        {/if}
    </section>
</div>

<style>
    :global(body) { margin: 0; font-family: 'Inter', sans-serif; background: #f97296; }
    .page { min-height: 100vh; display: flex; flex-direction: column; }
    .topbar { height: 110px; background: #232323; display: flex; align-items: center; padding: 0 32px; }
    .topbar h1 { font-family: 'League Spartan', sans-serif; font-size: 3rem; color: #ff1a1a; margin: 0; }
    
    .hero { flex: 1; padding: 40px 32px; position: relative; }
    .content { max-width: 1400px; margin: 0 auto; display: grid; grid-template-columns: 1.1fr 1.2fr 0.7fr; align-items: center; gap: 40px; }

    .photo-card { position: relative; background: #fff; padding: 18px; border-radius: 24px; transform: rotate(-5deg); box-shadow: 0 30px 60px rgba(0,0,0,0.2); }
    .photo-card img { width: 100%; aspect-ratio: 1/1; border-radius: 16px; object-fit: cover; }
    
    .price-tag { position: absolute; bottom: -10px; right: -15px; background: #232323; color: white; padding: 12px 24px; border-radius: 16px; transform: rotate(5deg); box-shadow: 0 10px 20px rgba(0,0,0,0.3); display: flex; flex-direction: column; align-items: center; }
    .price-tag .now { font-weight: 900; font-size: 1.8rem; color: #ffd700; }
    .price-tag .was { font-size: 0.9rem; text-decoration: line-through; opacity: 0.5; }

    .timer-float { position: absolute; top: 20px; left: -10px; background: #ff1a1a; color: white; padding: 8px 16px; border-radius: 8px; font-weight: 800; font-size: 0.85rem; transform: rotate(-2deg); display: flex; align-items: center; gap: 8px; }
    .pulse-dot { width: 8px; height: 8px; background: white; border-radius: 50%; animation: blink 1s infinite; }
    @keyframes blink { 0%, 100% { opacity: 1; } 50% { opacity: 0.3; } }

    .center-copy { display: flex; flex-direction: column; }
    .match-count { color: #232323; font-weight: 800; text-transform: uppercase; letter-spacing: 0.2em; margin-bottom: 12px; font-size: 0.8rem; }
    .badge-row { display: flex; gap: 12px; margin-bottom: 20px; }
    .match-badge, .save-badge { padding: 10px 20px; border-radius: 999px; font-family: 'League Spartan', sans-serif; font-weight: 900; font-size: 0.85rem; }
    .match-badge { background: #232323; color: white; }
    .save-badge { background: #ffffff; color: #ff1a1a; }
    
    /* Headline Styles */
    .headline { 
        color: #fff9e6; 
        font-family: 'League Spartan', sans-serif;
        font-size: clamp(2.5rem, 4vw, 3.8rem); 
        font-weight: 900; 
        line-height: 0.95; 
        margin: 0 0 15px;
        text-shadow: 2px 4px 0px rgba(35, 35, 35, 0.2);
    }

    .headline i { font-style: italic; }

    .restaurant-name { 
        color: #232323; 
        font-size: 2.5rem; /* Slightly larger per your previous request */
        font-weight: 900; 
        text-transform: uppercase; 
        font-family: 'Inter', sans-serif; 
        margin: 0 0 35px; 
        line-height: 1;
        letter-spacing: -0.02em;
    }

    .actions { display: flex; flex-direction: column; gap: 16px; width: min(430px, 100%); }
    .primary, .secondary, .start-over { border: none; border-radius: 999px; padding: 22px 28px; font-size: 1.1rem; font-weight: 800; cursor: pointer; transition: all 0.2s cubic-bezier(0.175, 0.885, 0.32, 1.275); text-align: center; }
    
    .primary { background: #232323; color: white; }
    .secondary { background: white; color: #232323; }
    .start-over { background: transparent; border: 3px solid #232323; color: #232323; margin-top: 10px; }
    
    .primary:hover { transform: scale(1.03); background: #000; }
    .secondary:hover { transform: scale(1.03); background: #f0f0f0; }

    .cupid-wrap img { width: min(380px, 100%); }

    @media (max-width: 1100px) {
        .content { grid-template-columns: 1fr; text-align: center; }
        .center-copy { align-items: center; }
    }
</style>