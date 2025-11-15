'use client';

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';

export default function ProjectsPage() {
  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-semibold text-asoto-text-main">プロジェクト</h1>
          <p className="text-sm text-asoto-text-muted">興味のあるプロジェクトに参加して、共創を体験しましょう。</p>
        </div>
        <Button className="rounded-full bg-asoto-primary text-white">プロジェクトを作成</Button>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>進行中のプロジェクト</CardTitle>
          <CardDescription>まだプロジェクトがありません。</CardDescription>
        </CardHeader>
        <CardContent className="text-sm text-asoto-text-muted">
          プロジェクトが追加されるとここに表示されます。
        </CardContent>
      </Card>
    </div>
  );
}
