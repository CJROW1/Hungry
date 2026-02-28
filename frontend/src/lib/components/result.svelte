<script lang="ts">
	
	type Food = {
		id?: number;
		name?: string;
		title?: string;
		image?: string;
		url?: string;
		match_percentage?: number;
	};

	let {
		foods = [],
		cupidImage = '/cupid.png'
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
        console.log($state.snapshot(currentFood));
        console.log(getKeyword($state.snapshot(currentFood)));
		if (currentFood?.url) {
			window.open(currentFood.url, '_blank');
		}
	}

	function dismiss() {
		console.log('dismiss result');
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
        
        // Search the Name and Category for our specific list first
        const searchString = `${food.name || ''} ${food.category || ''}`.toLowerCase();
        const match = Object.keys(imageKeywords).find(key => 
            searchString.includes(key.toLowerCase())
        );

        if (match) return imageKeywords[match as keyof typeof imageKeywords];

        // Fallback: Use the very first word of the category (most accurate for general cases)
        return food.category?.split('/')[0].split(' ')[0].toLowerCase() || "food";
    }

	function startOver() {
        // This clears the Svelte state and redirects to your home/quiz page
        window.location.href = '/'; 
    }
</script>

<svelte:head>
	<title>Hungry | Result</title>
	<link rel="preconnect" href="https://fonts.googleapis.com" />
	<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin="anonymous" />
	<link
		href="https://fonts.googleapis.com/css2?family=League+Spartan:wght@600;700;800&family=Inter:ital,wght@0,400;0,500;0,600;1,600;1,700&display=swap"
		rel="stylesheet"
	/>
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
                            alt="food"
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
						<button class="dismiss" onclick={dismiss}>
							Dismiss
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
.photo-card img {
        background: #232323; /* Dark placeholder */
        display: block;
        width: 100%;
        aspect-ratio: 1 / 1;
        object-fit: cover;
        border-radius: 16px;
        /* Smooth fade-in effect */
        opacity: 0;
        animation: fadeIn 0.4s ease-in forwards;
    }

    @keyframes fadeIn {
        to { opacity: 1; }
    }
	.page {
		min-height: 100vh;
		background: #f97296;
		display: flex;
		flex-direction: column;
	}

	.topbar,
	.bottombar {
		background: #232323;
		flex-shrink: 0;
	}

	.topbar {
		height: 110px;
		display: flex;
		align-items: center;
		padding: 0 32px;
	}
	.match-badge {
    background: #ffffff;
    color: #ff1a1a;
    padding: 8px 16px;
    border-radius: 999px;
    font-family: 'League Spartan', sans-serif;
    font-weight: 800;
    font-size: 0.9rem;
    margin-bottom: 16px;
    display: inline-block;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    letter-spacing: 0.05em;
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
		line-height: 1;
	}

	.hero {
		position: relative;
		flex: 1;
		background: #ff0000;
		overflow: hidden;
		padding: 40px 32px;
	}

	.content {
		position: relative;
		z-index: 2;
		max-width: 1400px;
		margin: 0 auto;
		min-height: 640px;
		display: grid;
		grid-template-columns: 1.05fr 1fr 0.8fr;
		align-items: center;
		gap: 24px;
	}

	.photo-wrap {
		display: flex;
		justify-content: center;
		align-items: center;
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
	}

	.center-copy {
		display: flex;
		flex-direction: column;
		align-items: flex-start;
		justify-content: center;
		max-width: 520px;
	}

	h2 {
		margin: 0 0 20px;
		color: white;
		font-size: clamp(2.2rem, 4vw, 4rem);
		font-style: italic;
		font-weight: 700;
		line-height: 1.1;
		max-width: 12ch;
	}

	.restaurant-name {
		margin: 0 0 28px;
		color: white;
		font-size: 1.1rem;
		font-weight: 600;
		opacity: 0.95;
	}

	.actions {
		display: flex;
		flex-direction: column;
		align-items: stretch;
		gap: 24px;
		width: min(430px, 100%);
	}

	.primary,
	.secondary {
		border: none;
		background: #000;
		color: white;
		border-radius: 999px;
		padding: 22px 28px;
		font-size: 1.05rem;
		font-weight: 500;
		cursor: pointer;
		transition:
			transform 0.15s ease,
			opacity 0.15s ease;
	}

	.primary:hover,
	.secondary:hover {
		transform: translateY(-2px);
	}

	.dismiss {
		border: none;
		background: transparent;
		color: white;
		font-size: 0.95rem;
		cursor: pointer;
		padding: 6px 0 0;
		align-self: center;
		opacity: 0.95;
	}

	.dismiss:hover {
		text-decoration: underline;
	}

	.cupid-wrap {
		display: flex;
		justify-content: center;
		align-items: center;
	}

	.cupid-wrap img {
		width: min(330px, 100%);
		height: auto;
		object-fit: contain;
	}

	.empty-state {
		position: relative;
		z-index: 2;
		max-width: 1200px;
		min-height: 640px;
		margin: 0 auto;
		display: grid;
		grid-template-columns: 1fr 0.8fr;
		align-items: center;
		gap: 24px;
	}

	.empty-copy {
		color: white;
	}

	.empty-copy p {
		margin: 0;
		font-size: 1.1rem;
		line-height: 1.6;
		max-width: 34ch;
	}

	.empty-cupid {
		justify-content: center;
	}

	.spark {
		position: absolute;
		background: radial-gradient(
			circle,
			rgba(255, 215, 245, 0.95) 0%,
			rgba(255, 215, 245, 0.55) 25%,
			rgba(255, 215, 245, 0) 70%
		);
		filter: blur(3px);
		opacity: 0.95;
		z-index: 1;
		clip-path: polygon(
			50% 0%,
			60% 33%,
			100% 50%,
			60% 67%,
			50% 100%,
			40% 67%,
			0% 50%,
			40% 33%
		);
	}

	.spark-1 {
		width: 300px;
		height: 300px;
		left: 260px;
		bottom: 70px;
		transform: rotate(18deg);
	}

	.spark-2 {
		width: 210px;
		height: 210px;
		left: 540px;
		top: 30px;
		transform: rotate(-12deg);
	}

	.spark-3 {
		width: 180px;
		height: 180px;
		left: 530px;
		top: 200px;
		transform: rotate(20deg);
	}

	@media (max-width: 1100px) {
		.content,
		.empty-state {
			grid-template-columns: 1fr;
			justify-items: center;
			text-align: center;
			gap: 30px;
			padding: 20px 0 40px;
		}

		.center-copy {
			align-items: center;
		}

		h2 {
			max-width: 14ch;
		}

		.actions {
			width: min(430px, 90vw);
		}

		.spark-1 {
			left: 40px;
			bottom: 120px;
		}

		.spark-2 {
			right: 80px;
			left: auto;
			top: 60px;
		}

		.spark-3 {
			left: 50%;
			top: 280px;
			transform: translateX(-50%);
		}
	}

	@media (max-width: 700px) {
		.topbar {
			height: 88px;
			padding: 0 20px;
		}

		.hero {
			padding: 24px 20px 32px;
		}

		.photo-card {
			width: min(320px, 82vw);
			padding: 14px;
			border-radius: 20px;
		}

		.primary,
		.secondary {
			padding: 18px 20px;
			font-size: 1rem;
		}

		.cupid-wrap img {
			width: min(220px, 60vw);
		}

		.spark-1,
		.spark-2,
		.spark-3 {
			opacity: 0.65;
		}
	}
	.match-count {
        color: white;
        font-family: 'Inter', sans-serif;
        font-size: 0.85rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        margin-bottom: 8px;
        opacity: 0.8;
    }	
</style>
