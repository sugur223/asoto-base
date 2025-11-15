'use client';

import Link from 'next/link';

import { RegisterForm } from '@/components/auth/RegisterForm';

export default function RegisterPage() {
  return (
    <div className="flex min-h-screen flex-col items-center justify-center bg-asoto-bg-main px-4 py-16 text-asoto-text-main">
      <div className="w-full max-w-md space-y-6">
        <div className="space-y-2 text-center">
          <p className="text-sm font-semibold uppercase tracking-[0.4em] text-asoto-text-muted">asotobase</p>
          <h1 className="text-3xl font-semibold">新規登録</h1>
          <p className="text-sm text-asoto-text-muted">
            既にアカウントをお持ちの方は{' '}
            <Link href="/login" className="text-asoto-primary hover:underline">
              ログイン
            </Link>
            へ。
          </p>
        </div>
        <RegisterForm />
      </div>
    </div>
  );
}
