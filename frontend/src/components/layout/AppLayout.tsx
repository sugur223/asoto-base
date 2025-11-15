'use client';

import type { ReactNode } from 'react';

import { Sidebar } from './Sidebar';
import { Header } from './Header';

interface AppLayoutProps {
  children: ReactNode;
}

export function AppLayout({ children }: AppLayoutProps) {
  return (
    <div className="flex min-h-screen bg-asoto-bg-main text-asoto-text-main">
      {/* Desktop Sidebar - Hidden on mobile/tablet */}
      <Sidebar />

      {/* Main Content Area */}
      <div className="flex flex-1 flex-col">
        <Header />
        <main className="flex-1 overflow-y-auto bg-asoto-bg-main px-4 py-4 sm:px-6 sm:py-6 lg:px-10 lg:py-8">
          <div className="mx-auto w-full space-y-6 sm:space-y-8">{children}</div>
        </main>
      </div>
    </div>
  );
}
