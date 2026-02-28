<script>
	import { goto } from '$app/navigation';

	function startQuiz() {
		goto('/qa');
	}
</script>

<div class="page">
	<header class="topbar">
		<h1>Hungry</h1>
	</header>

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
		margin: 0;
		font-family: Arial, sans-serif;
		background: #ff0000;
	}

	.page {
		min-height: 100vh;
		display: flex;
		flex-direction: column;
	}

	.topbar {
		height: 110px;
		background: #232323;
		display: flex;
		align-items: center;
		padding: 0 32px;
		box-sizing: border-box;
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

	h2 {
		font-size: clamp(2.2rem, 5vw, 4.5rem);
		line-height: 1.05;
		margin: 0 0 20px 0;
		font-style: italic;
		color: white;
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