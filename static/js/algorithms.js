const orderIdInput = document.getElementById('algorithm-order-id');
const expressionInput = document.getElementById('postfix-expression');

document.querySelectorAll('[data-demo]').forEach((button) => {
	button.addEventListener('click', async () => {
		const phaseOutput = button.closest('.algorithm-phase').querySelector('.algorithm-output');
		button.disabled = true;
		phaseOutput.textContent = 'Running demo...';
		const payload = { demo: button.dataset.demo };

		if (['linear-search', 'binary-search', 'bst'].includes(payload.demo)) {
			payload.order_id = Number(orderIdInput.value);
		}
		if (payload.demo === 'postfix-stack') {
			payload.expression = expressionInput.value;
		}

		try {
			const response = await fetch('/api/algorithms/run', {
				method: 'POST',
				headers: { 'Content-Type': 'application/json' },
				body: JSON.stringify(payload),
			});
			const result = await response.json();
			if (!response.ok) throw new Error(result.error || 'The algorithm demo could not run.');
			phaseOutput.textContent = `Complexity: ${result.complexity}\n\n${JSON.stringify(result.result, null, 2)}`;
		} catch (error) {
			phaseOutput.textContent = `Error: ${error.message}`;
		} finally {
			button.disabled = false;
		}
	});
});
