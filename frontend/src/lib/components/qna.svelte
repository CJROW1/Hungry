<script>
	import { goto } from '$app/navigation';

	function startQuiz() {
		goto('/qa');
	}
</script>

<div class="page">
	<div class="card">
		<div class="character-wrap">
			<img
				class="character"
				src="/character.png"
				alt="Food mascot character"
			/>
		</div>

		<div class="text-content">
			<p class="small">Hey foodie 🍟</p>
			<h1>Let’s find your perfect food match.</h1>
			<p class="description">
				We’ll start with a short Q&amp;A to learn your taste in food.
				Think of it like a dating app... but for your next meal.
			</p>

			<button on:click={startQuiz}>Start Q&amp;A</button>
		</div>
	</div>
</div>

<style>
	:global(body) {
		margin: 0;
		font-family: Arial, sans-serif;
		background: #ff0000;
	}

	.page {
		min-height: 100vh;
		display: flex;
		align-items: center;
		justify-content: center;
		padding: 24px;
	}

	.card {
		width: min(1100px, 100%);
		min-height: 80vh;
		background: linear-gradient(180deg, #ff2b2b 0%, #ff1a1a 100%);
		border-radius: 32px;
		display: flex;
		align-items: center;
		justify-content: space-between;
		gap: 32px;
		padding: 48px;
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
		width: min(380px, 100%);
		height: auto;
		object-fit: contain;
	}

	.text-content {
		flex: 1;
		color: white;
	}

	.small {
		font-size: 1.1rem;
		margin: 0 0 12px 0;
		opacity: 0.95;
	}

	h1 {
		font-size: clamp(2.2rem, 5vw, 4.5rem);
		line-height: 1.05;
		margin: 0 0 20px 0;
		font-style: italic;
	}

	.description {
		font-size: 1.1rem;
		line-height: 1.6;
		max-width: 520px;
		margin-bottom: 28px;
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

	@media (max-width: 850px) {
		.card {
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