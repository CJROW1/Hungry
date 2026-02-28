<script>
	import { goto } from '$app/navigation';

	let mood = $state('');
	let budget = $state('');
	let groupSize = $state('');
	let minRating = $state('');
	let dietary = $state('');

	function submitPreferences() {
		const params = new URLSearchParams({
			mood,
			budget,
			groupSize,
			minRating,
			dietary
		});

		goto(`/results?${params.toString()}`);
	}
</script>

<div class="page">
	<header class="topbar">
		<h1>Hungry</h1>
	</header>

	<div class="content">
		<div class="card">
			<h2>Tell us your taste</h2>
			<p class="subtitle">Answer a few quick questions so we can find your best match.</p>

			<div class="form">
				<label>
					<span>Q1. What are you in the mood for right now?</span>
					<select bind:value={mood}>
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
					<select bind:value={budget}>
						<option value="">Select one</option>
						<option value="Budget-friendly">Budget-friendly</option>
						<option value="Medium price">Medium price</option>
						<option value="Don’t care">Don’t care</option>
					</select>
				</label>

				<label>
					<span>Q3. Who are you eating with?</span>
					<select bind:value={groupSize}>
						<option value="">Select one</option>
						<option value="Just me">Just me</option>
						<option value="Me and one other person">Me and one other person</option>
						<option value="A group">A group</option>
					</select>
				</label>

				<label>
					<span>Q4. What minimum rating do you want?</span>
					<select bind:value={minRating}>
						<option value="">Select one</option>
						<option value="3.5+">3.5+</option>
						<option value="4.0+">4.0+</option>
						<option value="4.5+">4.5+</option>
						<option value="Don’t care">Don’t care</option>
					</select>
				</label>

				<label>
					<span>Q5. Any dietary preference?</span>
					<select bind:value={dietary}>
						<option value="">Select one</option>
						<option value="Halal">Halal</option>
						<option value="No preference">No preference</option>
					</select>
				</label>

				<button
					onclick={submitPreferences}
					disabled={!mood || !budget || !groupSize || !minRating || !dietary}
				>
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
		background: #ff0000;
	}

	.page {
		min-height: 100vh;
		display: flex;
		flex-direction: column;
		background: #ff0000;
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

	.content {
		flex: 1;
		display: flex;
		align-items: center;
		justify-content: center;
		padding: 24px;
		box-sizing: border-box;
	}

	.card {
		width: min(760px, 100%);
		background: #ff1a1a;
		border-radius: 32px;
		padding: 40px 32px;
		color: white;
		box-sizing: border-box;
		box-shadow: 0 20px 40px rgba(0, 0, 0, 0.18);
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