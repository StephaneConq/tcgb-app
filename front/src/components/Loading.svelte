<div class="loading-container">
	<div class="progress-bar"></div>
</div>

<style>
	.loading-container {
		width: 100vw;
		position: absolute;
		top: 0;
		left: 0;
	}

	.progress-bar {
		width: 100%;
		height: 4px;
		background-color: #f0f0f0;
		border-radius: 4px;
		overflow: hidden;
		position: relative;
	}

	.progress-bar::after {
		content: '';
		position: absolute;
		top: 0;
		left: 0;
		height: 100%;
		width: 30%;
		background-color: #2865a1;
		animation: indeterminate 1.5s infinite ease-in-out;
		border-radius: 4px;
	}

	@keyframes indeterminate {
		0% {
			left: -30%;
		}

		100% {
			left: 100%;
		}
	}
</style>
