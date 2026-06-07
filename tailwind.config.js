/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './src/frontend/**/*.html',
    './src/frontend/**/*.js',
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#f3f4fb', 100: '#e4e6f6', 200: '#ccd0ee', 300: '#acb2e3',
          400: '#8b92d5', 500: '#6e76c4', 600: '#5b63b0', 700: '#4a5194',
          800: '#3a3f76', 900: '#292d57', 950: '#1a1d3a',
        },
        accent: {
          50: '#fef7f4', 100: '#fdebe3', 200: '#fad4c2', 300: '#f5b598',
          400: '#ee936a', 500: '#e07340', 600: '#c55a2e', 700: '#a3461f',
          800: '#803515', 900: '#5c250e',
        },
        neutral: {
          50: '#fafaf9', 100: '#f5f3f1', 200: '#e8e4e0', 300: '#d4cec8',
          400: '#a89f96', 500: '#7d7368', 600: '#5e554c', 700: '#4a423b',
          800: '#332d28', 900: '#1f1b18', 950: '#14100e',
        },
        dark: {
          bg: '#0f1117', surface: '#1a1d27', border: '#2a2d3a',
        },
      },
      fontFamily: {
        display: ['"DM Serif Display"', '"Noto Serif SC"', 'serif'],
        body: ['"Inter"', '"Noto Sans SC"', 'sans-serif'],
        mono: ['"JetBrains Mono"', 'monospace'],
      },
    },
  },
}
