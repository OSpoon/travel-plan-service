import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  server: {
    proxy: {
      '/travel-plan': {
        target: 'http://localhost:8000',
        changeOrigin: true
      }
    }
  }
})