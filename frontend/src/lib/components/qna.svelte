<script>
    import { browser } from '$app/environment';
    
    let answers = {
        mood: '',
        budget: '',
        group: '',
        rating: '',
        dietary: ''
    };

    async function submitQuiz() {
        if (!browser) return;

        const { goto } = await import('$app/navigation');

        const moodMap = {
            "Something filling": "Sushi Steakhouse Pasta Buffet BBQ Italian",
            "Something quick": "Pizza Sandwiches Burgers Wraps FastFood",
            "Something comforting": "Ramen Noodles Bakery Soup Diner",
            "Something fun with friends": "Tacos Korean BBQ DimSum Wings Pub Mexican",
            "Breakfast/brunch food": "Cafe Pancakes Breakfast Pastry Smoothie"
        };

        const prefs = {
            category: moodMap[answers.mood] || "General",
            vibe: answers.group,
            max_price: answers.budget === "Budget-friendly" ? 15.0 : 35.0,
            min_rating: answers.rating === "Don’t care" ? 0.0 : parseFloat(answers.rating),
            dietary: answers.dietary === "No preference" ? "None" : answers.dietary
        };

        try {
            const response = await fetch('/api/api/recommendations', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(prefs)
            });

            if (response.ok) {
                const data = await response.json();
                sessionStorage.setItem('hungryResults', JSON.stringify(data.results));
                await goto('/result');
            }
        } catch (err) {
            console.error("Connection failed:", err);
        }
    }

    $: isComplete = answers.mood && answers.budget && answers.group && answers.rating && answers.dietary;
</script>

<div class="page">
	<header class="topbar">
		<h1>Hungry</h1>
	</header>

	<!-- decorations -->
    <img src="/src/lib/assets/cookie.png" alt="" class="decor cookies sticker" />
	<img src="/src/lib/assets/tomato.png" alt="" class="decor tomato sticker" />
	<img src="/src/lib/assets/heart_toast.png" alt="" class="decor toast sticker" />
	<img src="/src/lib/assets/cookie.png" alt="" class="decor cookies sticker" />
		<img src="/src/lib/assets/tomato.png" alt="" class="decor tomato sticker" />
	<img src="/src/lib/assets/heart_toast.png" alt="" class="decor toast sticker" />

	<div class="content">
		<div class="card">
			<h2>Tell us your taste</h2>
			<p class="subtitle">Answer a few quick questions so we can find your best match.</p>

			<div class="form">
				<label>
					<span>Q1. What are you in the mood for right now?</span>
					<select bind:value={answers.mood}>
						<option value="">Select one</option>
						<option value="Something filling">Something filling</option>
						<option value="Something quick">Something quick</option>
						<option value="Something comforting">Something comforting</option>
						<option value="Something fun with friends">Something fun with friends</option>
						<option value="Breakfast/brunch food">Breakfast/brunch food</option>
					</select>
				</label>

				<label>
					<span>Q2. How much do you want to spend?</span>
					<select bind:value={answers.budget}>
						<option value="">Select one</option>
						<option value="Budget-friendly">Budget-friendly</option>
						<option value="Medium price">Medium price</option>
						<option value="Don’t care">Don’t care</option>
					</select>
				</label>

				<label>
					<span>Q3. Who are you eating with?</span>
					<select bind:value={answers.group}>
						<option value="">Select one</option>
						<option value="Just me">Just me</option>
						<option value="Me and one other person">Me and one other person</option>
						<option value="A group">A group</option>
					</select>
				</label>

				<label>
					<span>Q4. What minimum rating do you want?</span>
					<select bind:value={answers.rating}>
						<option value="">Select one</option>
						<option value="3.5+">3.5+</option>
						<option value="4.0+">4.0+</option>
						<option value="4.5+">4.5+</option>
						<option value="Don’t care">Don’t care</option>
					</select>
				</label>

				<label>
					<span>Q5. Any dietary preference?</span>
					<select bind:value={answers.dietary}>
						<option value="">Select one</option>
						<option value="Halal">Halal</option>
						<option value="No preference">No preference</option>
					</select>
				</label>

				<button on:click={submitQuiz} disabled={!isComplete}>
					Show my matches
				</button>
			</div>
		</div>
	</div>
</div>

<style>
	:global(body) {
		margin: 0;
		font-family: Arial, sans-serif;
		background: #f97296;
	}

	.page {
		min-height: 100vh;
		display: flex;
		flex-direction: column;
		background: #f97296;
		position: relative;
		overflow: hidden;
	}

	.topbar {
		height: 110px;
		background: #232323;
		display: flex;
		align-items: center;
		padding: 0 32px;
		box-sizing: border-box;
		position: relative;
		z-index: 5;
	}

	.topbar h1 {
		margin: 0;
		font-family: 'League Spartan', Arial, sans-serif;
		font-size: clamp(3rem, 5vw, 4.5rem);
		font-weight: 800;
		color: #ff1a1a;
		line-height: 1;
	}

	.content {
		flex: 1;
		display: flex;
		align-items: center;
		justify-content: center;
		padding: 24px;
		box-sizing: border-box;
		position: relative;
		z-index: 3;
	}

	.card {
		width: min(760px, 100%);
		background: #ff1a1a;
		border-radius: 32px;
		padding: 40px 32px;
		color: white;
		box-sizing: border-box;
		box-shadow: 0 20px 40px rgba(0, 0, 0, 0.18);
		position: relative;
		z-index: 3;
	}

	h2 {
		margin: 0 0 10px;
		font-size: clamp(2rem, 4vw, 3.5rem);
		font-style: italic;
	}

	.subtitle {
		margin: 0 0 24px;
		font-size: 1rem;
		line-height: 1.5;
		opacity: 0.95;
	}

	.form {
		display: grid;
		gap: 18px;
	}

	label {
		display: grid;
		gap: 8px;
	}

	span {
		font-weight: 700;
		line-height: 1.4;
	}

	select {
		border: none;
		border-radius: 16px;
		padding: 14px 16px;
		font-size: 1rem;
		background: white;
		color: #111;
	}

	button {
		margin-top: 10px;
		border: none;
		background: #1f1f1f;
		color: white;
		padding: 16px 24px;
		border-radius: 999px;
		font-size: 1rem;
		cursor: pointer;
	}

	button:disabled {
		opacity: 0.6;
		cursor: not-allowed;
	}
    .decor {
	position: absolute;
	pointer-events: none;
	object-fit: contain;
	z-index: 2;
    }

    .sticker {
	filter:
		drop-shadow(2px 0 0 white)
		drop-shadow(-2px 0 0 white)
		drop-shadow(0 2px 0 white)
		drop-shadow(0 -2px 0 white)
		drop-shadow(0 6px 10px rgba(0,0,0,0.18));
}

    .tomato {
	right: -25px;
	top: 60px;
	width: 30%;
    transform: rotate(12deg);
    }

    .toast {
	left: -90px;
	bottom: -70px;
	width: 50%;
    transform: rotate(-30deg);
    }

    .cookies {
	right: -20px;
	bottom: -20px;
	width: 30%;
    position: absolute;
	z-index: 2;
    }

	@media (max-width: 850px) {
		.topbar {
			height: 88px;
			padding: 0 20px;
		}

		.content {
			padding: 20px;
		}

		.card {
			padding: 32px 24px;
		}
	}
</style>
