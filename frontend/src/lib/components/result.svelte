<script lang="ts">
	import { page } from '$app/state';
	import Result from '$lib/components/result.svelte';

	type Preferences = {
		category: string;
		vibe: string;
		maxPrice: number;
		minRating: number;
		dietary: string;
	};

	type Deal = {
		id: number;
		restaurant: string;
		title: string;
		image: string;
		url: string;
	};

	let deals = $state<Deal[]>([]);
	let currentIndex = $state(0);
	let loading = $state(true);
	let error = $state('');

	let preferences = $derived<Preferences>({
		category: page.url.searchParams.get('category') ?? '',
		vibe: page.url.searchParams.get('vibe') ?? '',
		maxPrice: Number(page.url.searchParams.get('maxPrice') ?? 25),
		minRating: Number(page.url.searchParams.get('minRating') ?? 4),
		dietary: page.url.searchParams.get('dietary') ?? 'None'
	});

	let currentDeal = $derived(deals[currentIndex] ?? null);

	$effect(() => {
		loadDeals();
	});

	async function loadDeals() {
		loading = true;
		error = '';

		try {
			const response = await fetch('http://localhost:8000/search', {
				method: 'POST',
				headers: { 'Content-Type': 'application/json' },
				body: JSON.stringify(preferences)
			});

			if (!response.ok) {
				throw new Error('Failed to load deals');
			}

			const data = await response.json();
			deals = data.deals ?? [];
			currentIndex = 0;
		} catch (err) {
			error = err instanceof Error ? err.message : 'Something went wrong';
			deals = [];
		} finally {
			loading = false;
		}
	}

	function nextDeal() {
		currentIndex += 1;
	}

	function takeDeal(deal: Deal) {
		window.open(deal.url, '_blank');
	}

	function dismiss() {
		window.history.back();
	}
</script>

{#if loading}
	<div class="state">Loading deals...</div>
{:else if error}
	<div class="state">Error: {error}</div>
{:else}
	<Result
		deal={currentDeal}
		onNext={nextDeal}
		onTake={takeDeal}
		onDismiss={dismiss}
	/>
{/if}

<style>
	.state {
		min-height: 100vh;
		display: flex;
		align-items: center;
		justify-content: center;
		background: #ff0000;
		color: white;
		font-size: 2rem;
		font-style: italic;
	}
</style>