<script>
	let answers = {
		mood: '',
		budget: '',
		group: '',
		rating: '',
		dietary: ''
	};

	const questions = [
		{
			id: 'mood',
			text: 'Q1. What are you in the mood for right now?',
			options: [
				'Something filling',
				'Something quick',
				'Something comforting',
				'Something fun with friends',
				'Breakfast/brunch food'
			]
		},
		{
			id: 'budget',
			text: 'Q2. How much do you want to spend?',
			options: ['Budget-friendly', 'Medium price', 'Don’t care']
		},
		{
			id: 'group',
			text: 'Q3. Who are you eating with?',
			options: ['Just me', 'Me and one other person', 'A group']
		},
		{
			id: 'rating',
			text: 'Q4. What minimum rating do you want?',
			options: ['3.5+', '4.0+', '4.5+', 'Don’t care']
		},
		{
			id: 'dietary',
			text: 'Q5. Any dietary preference?',
			options: ['Halal', 'No preference']
		}
	];

	$: isComplete =
		answers.mood &&
		answers.budget &&
		answers.group &&
		answers.rating &&
		answers.dietary;

	function submitQuiz() {
		console.log(answers);
	}
</script>

<div class="page">
	<h1>Tell us your taste ✨</h1>

	{#each questions as question}
		<section>
			<h2>{question.text}</h2>

			{#each question.options as option}
				<label>
					<input
						type="radio"
						name={question.id}
						value={option}
						bind:group={answers[question.id]}
					/>
					{option}
				</label>
			{/each}
		</section>
	{/each}

	<button on:click={submitQuiz} disabled={!isComplete}>
		See My Matches
	</button>
</div>