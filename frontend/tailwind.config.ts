import type { Config } from 'tailwindcss';

export default {
  content: ['./index.html', './src/**/*.{ts,tsx}'],
  theme: {
    screens: {
      xs: '375px',
      sm: '640px',
      md: '1024px',
      lg: '1280px',
      xl: '1920px',
      '2xl': '2560px',
    },
    extend: {},
  },
  plugins: [],
} satisfies Config;
