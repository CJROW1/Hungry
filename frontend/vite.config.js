import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';

export default defineConfig({
	plugins: [sveltekit()],
    server: {
        host: true,
        allowedHosts: ['0.0.0.0', 'tungdo.dev', 'hungry.tungdo.dev']
    }
});
