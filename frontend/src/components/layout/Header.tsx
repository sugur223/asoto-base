'use client';

import { useAuthStore } from '@/stores/authStore';
import { Button } from '@/components/ui/button';
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu';
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar';
import { Bell, LogOut, User, Settings } from 'lucide-react';
import { useRouter } from 'next/navigation';
import { MobileSidebar } from './MobileSidebar';

export function Header() {
  const { user, logout } = useAuthStore();
  const router = useRouter();

  const handleLogout = () => {
    logout();
    router.push('/login');
  };

  const getUserInitials = () => {
    if (!user?.full_name) return 'U';
    return user.full_name
      .split(' ')
      .map((n) => n[0])
      .join('')
      .toUpperCase()
      .slice(0, 2);
  };

  return (
    <header className="sticky top-0 z-10 flex-shrink-0 border-b border-asoto-border bg-asoto-bg-surface shadow-sm">
      <div className="flex items-center justify-between px-4 py-4 sm:px-10">
        {/* 左側: モバイルメニューボタン + ページタイトル */}
        <div className="flex items-center gap-3">
          <MobileSidebar />
          <div className="rounded-lg bg-asoto-accent/20 px-4 py-2">
            <h1 className="text-lg font-black text-asoto-primary sm:text-2xl">
              こんにちは、{user?.full_name || 'ゲスト'}さん
            </h1>
            <p className="hidden text-sm text-asoto-text-muted sm:block">
              誰もがあそぶように、シゴトができる社会を。
            </p>
          </div>
        </div>

        {/* 右側: 通知 + ユーザーメニュー */}
        <div className="flex items-center gap-2 sm:gap-4">
          {/* 通知アイコン */}
          <Button variant="ghost" size="icon" className="relative hidden rounded-full border border-asoto-primary/20 text-asoto-primary hover:bg-asoto-secondary/20 sm:inline-flex">
            <Bell className="h-5 w-5" />
            <span className="absolute top-1 right-1 h-2 w-2 rounded-full bg-asoto-secondary shadow-sm"></span>
          </Button>

          {/* ユーザーメニュー */}
          <DropdownMenu>
            <DropdownMenuTrigger asChild>
              <Button variant="ghost" className="relative h-10 w-10 rounded-full">
                <Avatar className="h-10 w-10 ring-2 ring-asoto-secondary/30">
                  <AvatarImage src={user?.avatar_url || undefined} alt={user?.full_name || ''} />
                  <AvatarFallback className="bg-asoto-primary text-asoto-secondary font-semibold">
                    {getUserInitials()}
                  </AvatarFallback>
                </Avatar>
              </Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent className="w-56" align="end" forceMount>
              <DropdownMenuLabel className="font-normal">
                <div className="flex flex-col space-y-1">
                  <p className="text-sm font-medium leading-none">{user?.full_name}</p>
                  <p className="text-xs leading-none text-muted-foreground">{user?.email}</p>
                </div>
              </DropdownMenuLabel>
              <DropdownMenuSeparator />
              <DropdownMenuItem onClick={() => router.push('/profile')}>
                <User className="mr-2 h-4 w-4" />
                <span>プロフィール</span>
              </DropdownMenuItem>
              <DropdownMenuItem onClick={() => router.push('/settings')}>
                <Settings className="mr-2 h-4 w-4" />
                <span>設定</span>
              </DropdownMenuItem>
              <DropdownMenuSeparator />
              <DropdownMenuItem onClick={handleLogout} className="text-red-600">
                <LogOut className="mr-2 h-4 w-4" />
                <span>ログアウト</span>
              </DropdownMenuItem>
            </DropdownMenuContent>
          </DropdownMenu>
        </div>
      </div>
    </header>
  );
}
