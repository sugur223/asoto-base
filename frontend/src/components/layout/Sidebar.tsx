'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';

const navItems = [
  { name: 'ダッシュボード', href: '/dashboard' },
  { name: '目標管理', href: '/goals' },
  { name: '内省ログ', href: '/logs' },
  { name: 'イベント', href: '/events' },
  { name: 'プロジェクト', href: '/projects' },
  { name: 'ポイント', href: '/points' },
];

export function Sidebar() {
  const pathname = usePathname();

  return (
    <aside className="hidden w-64 shrink-0 flex-col gap-6 border-r border-asoto-border bg-white px-6 py-8 lg:flex">
      <Link href="/dashboard" className="flex items-center gap-3 px-2">
        <div className="flex h-10 w-10 items-center justify-center rounded-2xl bg-asoto-primary text-lg font-bold text-white">
          A
        </div>
        <span className="text-lg font-semibold text-asoto-text-main">asotobase</span>
      </Link>

      <nav className="flex flex-1 flex-col gap-1 text-sm font-medium">
        {navItems.map((item) => {
          const isActive = pathname === item.href || pathname?.startsWith(`${item.href}/`);
          return (
            <Link
              key={item.name}
              href={item.href}
              className={`rounded-lg px-4 py-2.5 transition-colors ${
                isActive
                  ? 'bg-asoto-primary text-white'
                  : 'text-asoto-text-main hover:bg-asoto-bg-main'
              }`}
            >
              {item.name}
            </Link>
          );
        })}
      </nav>

      <p className="px-4 text-xs text-asoto-text-muted">© 2025 asotobase</p>
    </aside>
  );
}
