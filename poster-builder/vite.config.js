import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import path from 'path';

export default defineConfig({
  plugins: [react()],
  server: {
    port: 3052,
    fs: {
      allow: [
        path.resolve(__dirname),
        path.resolve(__dirname, '..'),
        path.resolve(__dirname, '../_shared')
      ]
    }
  }
});
