'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { Sheet, SheetContent, SheetTrigger } from '@/components/ui/sheet';
import { Button } from '@/components/ui/button';
import { Menu } from 'lucide-react';
import { useState } from 'react';

const navItems = [
  { name: 'ダッシュボード', href: '/dashboard' },
  { name: '目標管理', href: '/goals' },
  { name: '内省ログ', href: '/logs' },
  { name: 'イベント', href: '/events' },
  { name: 'プロジェクト', href: '/projects' },
  { name: 'ポイント', href: '/points' },
];

export function MobileSidebar() {
  const pathname = usePathname();
  const [open, setOpen] = useState(false);

  return (
    <Sheet open={open} onOpenChange={setOpen}>
      <SheetTrigger asChild>
        <Button variant="ghost" size="icon" className="lg:hidden">
          <Menu className="h-5 w-5" />
        </Button>
      </SheetTrigger>
      <SheetContent side="left" className="w-64 p-0">
        <div className="flex h-full flex-col gap-6 px-6 py-8">
          <Link href="/dashboard" className="flex items-center gap-3 px-2" onClick={() => setOpen(false)}>
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
                  onClick={() => setOpen(false)}
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
        </div>
      </SheetContent>
    </Sheet>
  );
}
