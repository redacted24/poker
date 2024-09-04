import { defineConfig, loadEnv } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default ({ mode }) => {
  process.env = {...process.env, ...loadEnv(mode, process.cwd())}
  return defineConfig({
    plugins: [react()],
    base: "./",
    server: {
      host: true,
      port: 443,
      https: {
        key: process.env.VITE_PRIVKEY,
        cert: process.env.VITE_FULLCHAIN,
      },
      proxy: {
        '/api': {
          target: 'http://localhost:5000',
          changeOrigin: true,
          secure: false
        },
      }
    },
  })
}
