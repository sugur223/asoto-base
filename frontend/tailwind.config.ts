import type { Config } from 'tailwindcss'

const config: Config = {
  content: [
    './src/pages/**/*.{js,ts,jsx,tsx,mdx}',
    './src/components/**/*.{js,ts,jsx,tsx,mdx}',
    './src/app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        background: 'var(--background)',
        foreground: 'var(--foreground)',
        asoto: {
          primary: 'var(--asoto-primary)',       // #122341 深いネイビー
          secondary: 'var(--asoto-secondary)',   // #F5E83A 明るいイエロー
          accent: 'var(--asoto-accent)',         // #22C55E グリーン
          success: 'var(--asoto-success)',       // #16A34A
          warning: 'var(--asoto-warning)',       // #F59E0B
          error: 'var(--asoto-error)',           // #DC2626
          info: 'var(--asoto-info)',             // #2563EB
          'text-main': 'var(--asoto-text-main)', // #0F172A
          'text-muted': 'var(--asoto-text-muted)', // #6B7280
          'bg-main': 'var(--asoto-bg-main)',     // #F0F9F4 淡い緑
          'bg-surface': 'var(--asoto-bg-surface)', // #FFFFFF
          'bg-accent': 'var(--asoto-bg-accent)', // #E8F5E9 濃い淡緑
          border: 'var(--asoto-border)',         // #D1E7DD 淡い緑のボーダー
        },
      },
    },
  },
  plugins: [],
}
export default config
