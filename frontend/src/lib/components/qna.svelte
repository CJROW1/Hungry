<script lang="ts">
	import { goto } from '$app/navigation';

	let category = $state('');
	let vibe = $state('');
	let maxPrice = $state(25);
	let minRating = $state(4);
	let dietary = $state('None');

	function submitPreferences() {
		const params = new URLSearchParams({
			category,
			vibe,
			maxPrice: String(maxPrice),
			minRating: String(minRating),
			dietary
		});

		goto(`/results?${params.toString()}`);
	}
</script>

<div class="page">
	<div class="card">
		<h1>Tell us your taste</h1>
		<p class="subtitle">Answer a few quick questions so we can find your best match.</p>

		<div class="form">
			<label>
				<span>Category</span>
				<select bind:value={category}>
					<option value="">Select a category</option>
					<option value="Sushi">Sushi</option>
					<option value="Burgers">Burgers</option>
					<option value="Pizza">Pizza</option>
					<option value="Korean">Korean</option>
					<option value="Indian">Indian</option>
					<option value="Healthy">Healthy</option>
					<option value="Dessert">Dessert</option>
				</select>
			</label>

			<label>
				<span>Vibe</span>
				<select bind:value={vibe}>
					<option value="">Select a vibe</option>
					<option value="Small and cozy">Small and cozy</option>
					<option value="Big portions">Big portions</option>
					<option value="Fancy">Fancy</option>
					<option value="Comfort food">Comfort food</option>
					<option value="Fast and simple">Fast and simple</option>
				</select>
			</label>

			<label>
				<span>Max Price ($)</span>
				<input type="number" min="1" bind:value={maxPrice} />
			</label>

			<label>
				<span>Minimum Rating</span>
				<input type="number" min="0" max="5" step="0.1" bind:value={minRating} />
			</label>

			<label>
				<span>Dietary</span>
				<select bind:value={dietary}>
					<option value="None">None</option>
					<option value="Vegetarian">Vegetarian</option>
					<option value="Vegan">Vegan</option>
					<option value="Halal">Halal</option>
					<option value="Gluten-free">Gluten-free</option>
					<option value="Dairy-free">Dairy-free</option>
				</select>
			</label>

			<button
				class="submit"
				onclick={submitPreferences}
				disabled={!category || !vibe}
			>
				Show my matches
			</button>
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
		box-sizing: border-box;
	}

	.card {
		width: min(720px, 100%);
		background: #ff1a1a;
		border-radius: 32px;
		padding: 40px 32px;
		color: white;
		box-sizing: border-box;
		box-shadow: 0 20px 40px rgba(0, 0, 0, 0.18);
	}

	h1 {
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
	}

	select,
	input {
		border: none;
		border-radius: 16px;
		padding: 14px 16px;
		font-size: 1rem;
		background: white;
		color: #111;
	}

	.submit {
		margin-top: 10px;
		border: none;
		background: #1f1f1f;
		color: white;
		padding: 16px 24px;
		border-radius: 999px;
		font-size: 1rem;
		cursor: pointer;
	}

	.submit:disabled {
		opacity: 0.6;
		cursor: not-allowed;
	}
</style>