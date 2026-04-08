// @ts-check
import { defineConfig } from 'astro/config';
import tailwindcss from '@tailwindcss/vite';

// https://astro.build/config
export default defineConfig({
  site: 'https://yourdomain.com', // Change to your custom domain or github.io URL
  output: 'static',
  vite: {
    plugins: [tailwindcss()]
  }
});