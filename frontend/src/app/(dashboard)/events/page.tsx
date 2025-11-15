'use client';

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';

export default function EventsPage() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-semibold text-asoto-text-main">イベント</h1>
        <p className="text-sm text-asoto-text-muted">コミュニティの予定をチェックし、気になるイベントに参加しましょう。</p>
      </div>
      <Card>
        <CardHeader>
          <CardTitle>予定されているイベント</CardTitle>
          <CardDescription>現在予定されているイベントはありません。</CardDescription>
        </CardHeader>
        <CardContent className="text-sm text-asoto-text-muted">
          イベントが追加されるとここに表示されます。
        </CardContent>
      </Card>
    </div>
  );
}
