import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'asotobase - あそびと仕事をつなぐプラットフォーム',
  description: 'あそびと仕事をつなぐプラットフォーム',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="ja">
      <body>{children}</body>
    </html>
  )
}
