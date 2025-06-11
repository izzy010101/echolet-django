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
    hot: true,
  },
})