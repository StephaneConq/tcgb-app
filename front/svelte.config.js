import adapter from '@sveltejs/adapter-node';
import { vitePreprocess } from '@sveltejs/vite-plugin-svelte';

/** @type {import('@sveltejs/kit').Config} */
const config = {
  preprocess: vitePreprocess(),

  kit: {
    serviceWorker: {
      register: true,
    },
    adapter: adapter({
      // default is 'build'
      out: 'build'
    })
  }
};

export default config;