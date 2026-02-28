<script lang="ts">
	type Deal = {
		id: number;
		restaurant: string;
		title: string;
		image: string;
		url: string;
	};

	let {
		deal,
		onNext,
		onTake,
		onDismiss,
		cupidImage = '/cupid.png'
	}: {
		deal: Deal | null;
		onNext?: () => void;
		onTake?: (deal: Deal) => void;
		onDismiss?: () => void;
		cupidImage?: string;
	} = $props();

	function handleTake() {
		if (!deal) return;

		if (onTake) {
			onTake(deal);
			return;
		}

		window.open(deal.url, '_blank');
	}

	function handleNext() {
		onNext?.();
	}

	function handleDismiss() {
		onDismiss?.();
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

		{#if deal}
			<div class="content">
				<div class="photo-wrap">
					<div class="photo-card">
						<img src={deal.image} alt={deal.restaurant} />
					</div>
				</div>

				<div class="center-copy">
					<h2>The perfect match for you have arrived!</h2>

					<div class="actions">
						<button class="primary" onclick={handleTake}>
							Just right for me!
						</button>

						<button class="secondary" onclick={handleNext}>
							Explore other options
						</button>

						<button class="dismiss" onclick={handleDismiss}>
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
				<h2>No more deals found</h2>
				<button class="dismiss" onclick={handleDismiss}>Go back</button>
			</div>
		{/if}
	</section>

	<footer class="bottombar"></footer>
</div>

<style>
	:global(body) {
		margin: 0;
		font-family: 'Inter', sans-serif;
		background: #ff0000;
	}

	.page {
		min-height: 100vh;
		background: #ff0000;
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

	.center-copy h2,
	.empty-state h2 {
		margin: 0 0 28px;
		color: white;
		font-size: clamp(2.2rem, 4vw, 4rem);
		font-style: italic;
		font-weight: 700;
		line-height: 1.1;
		max-width: 12ch;
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
		min-height: 500px;
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		text-align: center;
	}

	.spark {
		position: absolute;
		background: radial-gradient(circle, rgba(255, 215, 245, 0.95) 0%, rgba(255, 215, 245, 0.55) 25%, rgba(255, 215, 245, 0) 70%);
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
		.content {
			grid-template-columns: 1fr;
			justify-items: center;
			text-align: center;
			gap: 30px;
			padding: 20px 0 40px;
		}

		.center-copy {
			align-items: center;
		}

		.center-copy h2 {
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
</style>