/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './rentalapp/templates/**/*.{html,js}',
    './rental_business/templates/**/*.{html,js}',
    './node_modules/flowbite/**/*.js',
    './node_modules/swiper/**/*.js',
  ],
  theme: {
    extend: {},

    fontFamily: {
    'sans': ['Helvetica', 'Arial', 'sans-serif'],
    'serif': ['Georgia', 'Cambria', 'Times New Roman','Times','serif'],
    'mono': ['Menlo', 'Monaco', 'Consolas', 'Liberation Mono', 'Courier New', 'monospace'],
    
    "gtw": ["GT Walsheim", "Helvetica Neue", "Helvetica", "Arial", "sans-serif"],
    
    "interTight": ["Inter Tight", "Inter Tight Placeholder", "sans-serif"],

    "inter": ["Inter", "sans-serif"],

    "clash": ["Clash Display Semibold", "sans-serif"],
    },
  },
  plugins: [
    require('flowbite/plugin'),
]
}

