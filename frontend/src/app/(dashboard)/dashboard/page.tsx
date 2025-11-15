'use client';

import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';

export default function DashboardPage() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-semibold text-asoto-text-main">ダッシュボード</h1>
        <p className="text-sm text-asoto-text-muted">日々の「あそと」を俯瞰し、軽やかに次の一歩を決めましょう。</p>
      </div>

      <div className="grid gap-4 md:grid-cols-3">
        <Card>
          <CardHeader>
            <CardDescription>コミュニティ</CardDescription>
          </CardHeader>
          <CardContent>
            <p className="text-3xl font-semibold text-asoto-primary">2,400+</p>
          </CardContent>
        </Card>
        <Card>
          <CardHeader>
            <CardDescription>進行中のPJ</CardDescription>
          </CardHeader>
          <CardContent>
            <p className="text-3xl font-semibold text-asoto-accent">180</p>
          </CardContent>
        </Card>
        <Card>
          <CardHeader>
            <CardDescription>今週のイベント</CardDescription>
          </CardHeader>
          <CardContent>
            <p className="text-3xl font-semibold text-asoto-warning">7件</p>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
