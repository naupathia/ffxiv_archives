import type { Metadata } from 'next'
import './globals.css'
import { roboto, roboto_mono } from './ui/fonts'

export const metadata: Metadata = {
  title: 'TEA Tools',
  description: 'Search for FFXIV lore',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className={roboto.className}>{children}</body>
    </html>
  )
}
