/** @type {import('tailwindcss').Config} */
export default {
  content: ['./src/**/*.{astro,html,js,jsx,md,mdx,ts,tsx}'],
  darkMode: 'class',
  theme: {
    extend: {
      // You can add custom fonts or colors here later
    },
  },
  plugins: [
    require('@tailwindcss/typography'),
  ],
};