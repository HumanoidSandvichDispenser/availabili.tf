import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    vue(),
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    }
  },
  server: {
    proxy: {
      '/api': {
        target: 'http://localhost:5000',
        changeOrigin: true,
        secure: false,
        configure: (proxy) => {
          proxy.on('proxyReq', (proxyReq, req, res) => {
            const cookie = req.headers.cookie;
            if (cookie) {
              proxyReq.setHeader('Cookie', cookie);
            }
          });

          proxy.on('proxyRes', (proxyRes, req, res) => {
            const cookie = proxyRes.headers['set-cookie'];
            if (cookie) {
              res.setHeader('Set-Cookie', cookie);
            }
          });
        }
      }
    }
  }
})
