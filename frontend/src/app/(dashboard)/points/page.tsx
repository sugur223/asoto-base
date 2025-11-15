'use client';

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';

export default function PointsPage() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-semibold text-asoto-text-main">ポイント</h1>
        <p className="text-sm text-asoto-text-muted">あそとの活動で貯まったポイントを確認しましょう。</p>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>あなたのポイント</CardTitle>
          <CardDescription>まだポイントはありません。</CardDescription>
        </CardHeader>
        <CardContent>
          <p className="text-4xl font-semibold text-asoto-primary">0 pt</p>
        </CardContent>
      </Card>
    </div>
  );
}
