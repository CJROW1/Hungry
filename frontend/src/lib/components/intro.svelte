<script>
	import { goto } from '$app/navigation';

	function startQuiz() {
		goto('/qa');
	}
</script>

<div class="page">
    <img src="/src/lib/assets/star.png" alt="" class="decor star" />
    <img src="/src/lib/assets/cookie.png" alt="" class="decor cookies sticker" />
	<img src="/src/lib/assets/tomato.png" alt="" class="decor tomato sticker" />
	<img src="/src/lib/assets/heart_toast.png" alt="" class="decor toast sticker" />
	<img src="/src/lib/assets/cookie.png" alt="" class="decor cookies sticker" />

	<header class="topbar">
		<h1>Hungry</h1>
	</header>

	<div class="card">
		<div class="character-wrap">
			<img class="character" src="/src/lib/assets/character.png" alt="Food mascot character sticker"/>
		</div>

		<div class="text-content">
			<p class="small">Hey foodie,</p>
			<h2>Let’s find your perfect food match.</h2>
			<p class="description">
				We’ll start with a short Q&amp;A to learn your taste in food.
				Think of it like a dating app... but for your next meal!
			</p>

			<button on:click={startQuiz}>Start Q&amp;A</button>
		</div>
	</div>
</div>

<style>
	:global(body) {
		font-family: Arial, sans-serif;
		background: #f97296;
	}

	.page {
		min-height: 100vh;
		display: flex;
		flex-direction: column;
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
        z-index: 8;
	}

	.topbar h1 {
		margin: 0;
		font-family: 'League Spartan', Arial, sans-serif;
		font-size: clamp(3rem, 5vw, 4.5rem);
		font-weight: 800;
		color: #ff1a1a;
		line-height: 1;
	}

	.card {
		width: min(1100px, 100%);
		min-height: calc(100vh - 110px);
		margin: 0 auto;
		display: flex;
		align-items: center;
		justify-content: space-between;
		gap: 32px;
		padding: 48px 24px;
		box-sizing: border-box;
		overflow: hidden;
	}

	.character-wrap {
		flex: 1;
		display: flex;
		justify-content: center;
		align-items: center;
	}

	.character {
		width: min(400px, 100%);
		height: auto;
		object-fit: contain;
	}

	.text-content {
		flex: 1;
		color: white;
        z-index: 10;
	}

	.small {
		font-size: 1.6rem;
        font-family: 'Times New Roman', Times, serif;
		margin: 0 0 12px 0;
		opacity: 0.95;
	}


	h2 {
		font-size: clamp(2.2rem, 5vw, 4.5rem);
		line-height: 1.05;
		margin: 0 0 20px 0;
		font-style: italic;
		color: white;
	}

    .description {
	    position: relative;
	    z-index: 10;
	    display: inline-block;
	    background: rgba(255, 255, 255, 0.12);
	    border: 2px solid white;
	    border-radius: 20px;
	    padding: 18px 22px;
        font-size: 1.1rem;
        line-height: 1.6;
        max-width: 520px;
        margin-bottom: 28px;
        backdrop-filter: blur(6px);
	    -webkit-backdrop-filter: blur(6px);
    }

	button {
		border: none;
		background: #1f1f1f;
		color: white;
		padding: 16px 28px;
		border-radius: 999px;
		font-size: 1rem;
		cursor: pointer;
		transition: transform 0.15s ease;
	}

	button:hover {
		transform: translateY(-2px);
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

    .star{
        position: absolute;
        left: -80px;
        pointer-events: none;
        z-index: -7;
        opacity: 0.80;
        filter: blur(4px);
    }

    .tomato {
	right: 110px;
	top: 110px;
	width: 10%;
    transform: rotate(12deg);
    }

    .toast {
	left: -90px;
	bottom: -70px;
	width: 30%;
    transform: rotate(-30deg);
    }

    .cookies {
	right: 20px;
	bottom: 20px;
	width: 20%;
    position: absolute;
	z-index: 2;
    }

	@media (max-width: 850px) {
		.topbar {
			height: 88px;
			padding: 0 20px;
		}

		.card {
			min-height: calc(100vh - 88px);
			flex-direction: column;
			text-align: center;
			padding: 32px 24px;
		}

		.description {
			margin-left: auto;
			margin-right: auto;
		}
	}
</style>