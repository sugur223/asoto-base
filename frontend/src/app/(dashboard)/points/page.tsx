'use client';

import { useEffect, useState } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { useAuthStore } from '@/stores/authStore';
import * as pointsApi from '@/lib/api/points';
import { TrendingUp, Award, Calendar } from 'lucide-react';

const actionTypeLabels: Record<string, string> = {
  step_complete: 'ステップ完了',
  goal_complete: '目標達成',
  log_create: '内省ログ投稿',
  event_create: 'イベント作成',
  event_join: 'イベント参加',
  project_create: 'プロジェクト作成',
  project_join: 'プロジェクト参加',
  task_complete: 'タスク完了',
};

export default function PointsPage() {
  const { user } = useAuthStore();
  const [totalPoints, setTotalPoints] = useState(0);
  const [pointsHistory, setPointsHistory] = useState<pointsApi.Point[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const loadPoints = async () => {
      setIsLoading(true);
      setError(null);
      try {
        const [summary, history] = await Promise.all([
          pointsApi.fetchUserPoints(),
          pointsApi.fetchUserPointsHistory(),
        ]);
        setTotalPoints(summary.total_points);
        setPointsHistory(history);
      } catch (err: any) {
        const message = err.response?.data?.detail || 'ポイントの取得に失敗しました';
        setError(message);
      } finally {
        setIsLoading(false);
      }
    };

    loadPoints();
  }, []);

  const recentPoints = pointsHistory.slice(0, 10);
  const thisWeekPoints = pointsHistory.filter((p) => {
    const date = new Date(p.created_at);
    const weekAgo = new Date();
    weekAgo.setDate(weekAgo.getDate() - 7);
    return date > weekAgo;
  }).reduce((sum, p) => sum + p.amount, 0);

  return (
    <div className="space-y-4 sm:space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-asoto-text-main sm:text-3xl">ポイント</h1>
        <p className="text-xs text-asoto-text-muted sm:text-sm">あそとの活動で貯まったポイントを確認しましょう。</p>
      </div>

      {error && (
        <div className="rounded-md border border-destructive/20 bg-destructive/10 p-3 text-sm text-destructive">
          {error}
        </div>
      )}

      <div className="grid gap-3 sm:grid-cols-2 sm:gap-4">
        <Card className="bg-gradient-to-br from-asoto-primary to-asoto-primary/80 text-white">
          <CardHeader>
            <CardDescription className="text-white/80">累計ポイント</CardDescription>
            <CardTitle className="flex items-center gap-2">
              <Award className="h-6 w-6" />
              <span className="text-4xl font-bold">{totalPoints} pt</span>
            </CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-sm text-white/80">
              活動を続けてポイントを貯めましょう！
            </p>
          </CardContent>
        </Card>

        <Card className="bg-asoto-bg-surface border-asoto-border">
          <CardHeader>
            <CardDescription>今週の獲得ポイント</CardDescription>
            <CardTitle className="flex items-center gap-2">
              <TrendingUp className="h-6 w-6 text-asoto-accent" />
              <span className="text-4xl font-bold text-asoto-accent">{thisWeekPoints} pt</span>
            </CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-sm text-asoto-text-muted">
              過去7日間の獲得ポイント
            </p>
          </CardContent>
        </Card>
      </div>

      <Card className="bg-asoto-bg-surface border-asoto-border">
        <CardHeader>
          <CardTitle>ポイント獲得履歴</CardTitle>
          <CardDescription>最近の活動とポイント</CardDescription>
        </CardHeader>
        <CardContent>
          {isLoading ? (
            <p className="text-sm text-asoto-text-muted">読み込み中...</p>
          ) : recentPoints.length === 0 ? (
            <p className="text-sm text-asoto-text-muted">まだポイント履歴がありません。</p>
          ) : (
            <div className="space-y-3">
              {recentPoints.map((point) => (
                <div
                  key={point.id}
                  className="flex items-start justify-between gap-4 rounded-lg border border-asoto-border p-3 hover:bg-asoto-bg-main/50 transition-colors"
                >
                  <div className="flex-1 space-y-1">
                    <div className="flex items-center gap-2">
                      <span className="text-sm font-medium text-asoto-text-main">
                        {actionTypeLabels[point.action_type] || point.action_type}
                      </span>
                      <span className={`rounded-full px-2 py-0.5 text-xs font-medium ${
                        point.amount >= 50
                          ? 'bg-yellow-50 text-yellow-600'
                          : point.amount >= 10
                            ? 'bg-blue-50 text-blue-600'
                            : 'bg-gray-50 text-gray-600'
                      }`}>
                        +{point.amount} pt
                      </span>
                    </div>
                    {point.description && (
                      <p className="text-xs text-asoto-text-muted line-clamp-1">{point.description}</p>
                    )}
                    <div className="flex items-center gap-2 text-xs text-asoto-text-muted">
                      <Calendar className="h-3 w-3" />
                      <span>{formatDateTime(point.created_at)}</span>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </CardContent>
      </Card>

      <Card className="bg-asoto-bg-surface border-asoto-border">
        <CardHeader>
          <CardTitle>ポイントの貯め方</CardTitle>
          <CardDescription>以下の活動でポイントが獲得できます</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid gap-3 sm:grid-cols-2">
            <PointRule title="内省ログ投稿" points={5} icon="📝" />
            <PointRule title="ステップ完了" points={10} icon="✅" />
            <PointRule title="イベント参加" points={10} icon="🎉" />
            <PointRule title="プロジェクト参加" points={10} icon="🤝" />
            <PointRule title="タスク完了" points={10} icon="📌" />
            <PointRule title="プロジェクト作成（あそび）" points={30} icon="🔍" />
            <PointRule title="イベント作成" points={50} icon="🎊" />
            <PointRule title="プロジェクト作成（あそと）" points={50} icon="🌱" />
            <PointRule title="目標達成" points={50} icon="🎯" />
          </div>
        </CardContent>
      </Card>
    </div>
  );
}

interface PointRuleProps {
  title: string;
  points: number;
  icon: string;
}

function PointRule({ title, points, icon }: PointRuleProps) {
  return (
    <div className="flex items-center justify-between rounded-lg border border-asoto-border bg-white p-3">
      <div className="flex items-center gap-2">
        <span className="text-xl">{icon}</span>
        <span className="text-sm font-medium text-asoto-text-main">{title}</span>
      </div>
      <span className="text-sm font-bold text-asoto-primary">+{points} pt</span>
    </div>
  );
}

function formatDateTime(value?: string | null) {
  if (!value) return '-';
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return '-';
  return date.toLocaleString('ja-JP', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  });
}
