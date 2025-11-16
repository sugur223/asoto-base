'use client';

import { useEffect } from 'react';
import { usePathname } from 'next/navigation';
import { useAuthStore } from '@/stores/authStore';

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();
  const { fetchCurrentUser } = useAuthStore();

  useEffect(() => {
    // ページ読み込み時に認証状態を復元
    // 認証画面以外でのみ実行
    if (!pathname?.startsWith('/login') && !pathname?.startsWith('/register')) {
      fetchCurrentUser();
    }
  }, [pathname, fetchCurrentUser]);

  return <>{children}</>;
}
