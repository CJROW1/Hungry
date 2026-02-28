<script lang="ts">
    type Food = {
        id?: number;
        name?: string;
        title?: string;
        image?: string;
        url?: string;
        category?: string;
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

    function nextDeal() {
        if (currentIndex < foods.length - 1) {
            currentIndex += 1;
        }
    }

    function takeDeal() {
        // Redirects to the deal URL or a fallback delivery site
        const fallbackUrl = "https://www.ubereats.com";
        const url = currentFood?.url || fallbackUrl;
        window.open(url, '_blank');
    }

    function startOver() {
        window.location.href = '/'; 
    }

    const imageKeywords = {
        "Sushi": "sushi",
        "Chinese": "asian-food",
        "Indian": "curry",
        "Vietnamese": "pho",
        "Korean": "korean-bbq",
        "Ramen": "ramen",
        "Burgers": "burger",
        "Pizza": "pizza",
        "Pub": "wings",
        "Breakfast": "pancakes",
        "Bakery": "pastry",
        "Mexican": "taco",
        "Italian": "pasta",
        "Steakhouse": "steak",
        "Halal": "kebab",
        "Middle Eastern": "hummus",
        "Healthy": "salad",
        "Cafe": "coffee",
        "African": "stew",
        "Seafood": "seafood",
        "Deli": "sandwich"
    };

    function getKeyword(food: Food) {
        if (!food) return "meal";
        const searchString = `${food.name || ''} ${food.category || ''}`.toLowerCase();
        const match = Object.keys(imageKeywords).find(key => 
            searchString.includes(key.toLowerCase())
        );
        if (match) return imageKeywords[match as keyof typeof imageKeywords];
        return food.category?.split('/')[0].split(' ')[0].toLowerCase() || "food";
    }
</script>

<svelte:head>
    <title>Hungry | Result</title>
    <link rel="preconnect" href="https://fonts.googleapis.com" />
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin="anonymous" />
    <link href="https://fonts.googleapis.com/css2?family=League+Spartan:wght@600;700;800&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet" />
</svelte:head>

<div class="page">
    <header class="topbar">
        <h1>Hungry</h1>
    </header>

    <section class="hero">
        <div class="spark spark-1"></div>
        <div class="spark spark-2"></div>
        <div class="spark spark-3"></div>

        {#if currentFood}
            <div class="content">
                <div class="photo-wrap">
                    <div class="photo-card">
                        <img
                            src={`images/${getKeyword(currentFood)}.jpg`}
                            loading="lazy"
                            alt="food match"
                        />
                    </div>
                </div>

                <div class="center-copy">
                    {#if foods.length > 0}
                        <span class="match-count">
                            Match {currentIndex + 1} of {foods.length}
                        </span>
                    {/if}

                    {#if currentFood.match_percentage}
                        <div class="match-badge">
                            {currentFood.match_percentage}% MATCH
                        </div>
                    {/if}

                    <h2>The perfect match for you has arrived!</h2>

                    <p class="restaurant-name">
                        {currentFood.name || currentFood.title || 'Unnamed Deal'}
                    </p>

                    <div class="actions">
                        <button class="primary" onclick={takeDeal}>
                            Just right for me!
                        </button>

                        <button class="secondary" onclick={nextDeal}>
                            Explore other options
                        </button>

                        <button class="start-over" onclick={startOver}>
                            Start Over
                        </button>
                    </div>
                </div>

                <div class="cupid-wrap">
                    <img src={cupidImage} alt="Cupid illustration" />
                </div>
            </div>
        {:else}
            <div class="empty-state">
                <div class="empty-copy">
                    <h2>No deal selected yet.</h2>
                    <p>Run your search first, then the result card will appear here.</p>
                </div>
                <div class="cupid-wrap empty-cupid">
                    <img src={cupidImage} alt="Cupid illustration" />
                </div>
            </div>
        {/if}
    </section>

    <footer class="bottombar"></footer>
</div>

<style>
    :global(body) {
        margin: 0;
        font-family: 'Inter', sans-serif;
        background: #f97296;
    }

    .page {
        min-height: 100vh;
        background: #f97296;
        display: flex;
        flex-direction: column;
    }

    .topbar, .bottombar {
        background: #232323;
        flex-shrink: 0;
    }

    .topbar {
        height: 110px;
        display: flex;
        align-items: center;
        padding: 0 32px;
    }

    .bottombar {
        height: 70px;
        margin-top: auto;
    }

    .topbar h1 {
        margin: 0;
        font-family: 'League Spartan', sans-serif;
        font-size: clamp(3rem, 5vw, 4.5rem);
        font-weight: 800;
        color: #ff1a1a;
    }

    .hero {
        position: relative;
        flex: 1;
        overflow: hidden;
        padding: 40px 32px;
    }

    .content {
        position: relative;
        z-index: 2;
        max-width: 1400px;
        margin: 0 auto;
        display: grid;
        grid-template-columns: 1.05fr 1fr 0.8fr;
        align-items: center;
        gap: 24px;
    }

    .photo-card {
        width: min(420px, 80vw);
        background: #fff;
        padding: 18px;
        border-radius: 24px;
        transform: rotate(-11deg);
        box-shadow: 0 24px 40px rgba(0, 0, 0, 0.22);
    }

    .photo-card img {
        display: block;
        width: 100%;
        aspect-ratio: 1 / 1;
        object-fit: cover;
        border-radius: 16px;
        background: #232323;
        opacity: 0;
        animation: fadeIn 0.4s ease-in forwards;
    }

    @keyframes fadeIn { to { opacity: 1; } }

    .center-copy {
        display: flex;
        flex-direction: column;
        align-items: flex-start;
    }

    .match-count {
        color: white;
        font-size: 0.85rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        margin-bottom: 8px;
        opacity: 0.9;
    }

    .match-badge {
        background: #ffffff;
        color: #ff1a1a;
        padding: 8px 16px;
        border-radius: 999px;
        font-family: 'League Spartan', sans-serif;
        font-weight: 800;
        margin-bottom: 16px;
    }

    h2 {
        margin: 0 0 20px;
        color: white;
        font-size: clamp(2.2rem, 4vw, 4rem);
        font-style: italic;
        line-height: 1.1;
        max-width: 12ch;
    }

    .restaurant-name {
        margin: 0 0 28px;
        color: white;
        font-weight: 600;
    }

    .actions {
        display: flex;
        flex-direction: column;
        gap: 16px;
        width: min(430px, 100%);
    }

    /* Standardized Button Styles */
    .primary, .secondary, .start-over {
        border: none;
        border-radius: 999px;
        padding: 22px 28px;
        font-size: 1.05rem;
        font-weight: 600;
        cursor: pointer;
        transition: transform 0.15s ease, background 0.15s ease;
        text-align: center;
        width: 100%;
    }

    .primary { background: #000; color: white; }
    .secondary { background: #000; color: white; }
    
    .start-over { 
        background: transparent; 
        border: 2px solid #000; 
        color: #000; 
    }

    .primary:hover, .secondary:hover, .start-over:hover {
        transform: translateY(-2px);
        background: #333;
        color: white;
    }

    .cupid-wrap img { width: min(330px, 100%); }

    .spark {
        position: absolute;
        background: radial-gradient(circle, rgba(255, 255, 255, 0.8) 0%, transparent 70%);
        width: 200px; height: 200px; z-index: 1; opacity: 0.4;
    }
    .spark-1 { left: 10%; bottom: 10%; }
    .spark-2 { right: 10%; top: 10%; }
    
    @media (max-width: 1100px) {
        .content { grid-template-columns: 1fr; justify-items: center; text-align: center; }
        .center-copy { align-items: center; }
    }
</style>