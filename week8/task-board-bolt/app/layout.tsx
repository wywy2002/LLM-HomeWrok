import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'Task Board — Bolt Edition',
  description: 'A lightweight task management board built with bolt.new',
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className="bg-gray-50 min-h-screen font-sans antialiased">{children}</body>
    </html>
  );
}
