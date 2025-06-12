import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path'

export default defineConfig({
  plugins: [vue()],
  root: '.', // or ./frontend
  build: {
    outDir: '../backend/static/', // or wherever Django collects static
    emptyOutDir: true,
    rollupOptions: {
      input: './js/app.js',
    },
  },
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './js'),
    },
  },
  server: {
    port: 5171,
    proxy: {
    '/register/': 'http://127.0.0.1:8000',
    '/login/': 'http://127.0.0.1:8000',
    // more backend routes if needed
    },
    hot: true,
  },
})