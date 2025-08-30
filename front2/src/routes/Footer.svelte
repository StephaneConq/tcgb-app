<script>
	import { page } from '$app/state';
</script>

<footer class="flex justify-center">
	<nav class="glassbg">
		<ul>
			<li aria-current={page.url.pathname === '/' ? 'page' : undefined}>
				<a href="/">Home</a>
			</li>
			<li aria-current={page.url.pathname.startsWith('/read') ? 'page' : undefined}>
				<a href="/read">Photo</a>
			</li>
			<li aria-current={page.url.pathname.startsWith('/tcg') ? 'page' : undefined}>
				<a href="/tcg">TCG</a>
			</li>
			<li aria-current={page.url.pathname === '/other' ? 'page' : undefined}>
				<a href="/other">Autres</a>
			</li>
		</ul>
	</nav>
</footer>

<style>
	footer {
		padding: 0;
		position: fixed;
		bottom: 0;
		width: 100%;
	}

	nav {
		display: flex;
		justify-content: center;
		padding: 0 30px;
		border-top-left-radius: 20px;
		border-top-right-radius: 20px;
	}

	ul {
		position: relative;
		padding: 0;
		margin: 0;
		height: 3em;
		display: flex;
		justify-content: center;
		align-items: center;
		list-style: none;
		background: var(--background);
		background-size: contain;
	}

	li {
		position: relative;
		height: 100%;
	}

	li[aria-current='page']::before {
		--size: 6px;
		content: '';
		width: 0;
		height: 0;
		position: absolute;
		top: 0;
		left: calc(50% - var(--size));
		border: var(--size) solid transparent;
		border-top: var(--size) solid var(--color-theme-1);
	}

	nav a {
		display: flex;
		height: 100%;
		align-items: center;
		padding: 0 0.5rem;
		color: var(--color-text);
		font-weight: 700;
		font-size: 0.8rem;
		text-transform: uppercase;
		letter-spacing: 0.1em;
		text-decoration: none;
		transition: color 0.2s linear;
	}

	a:hover {
		color: var(--color-theme-1);
	}
</style>
