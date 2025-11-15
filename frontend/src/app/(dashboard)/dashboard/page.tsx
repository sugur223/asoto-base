'use client';

import { useEffect, useState } from 'react';
import Link from 'next/link';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { useAuthStore } from '@/stores/authStore';
import * as goalsApi from '@/lib/api/goals';
import * as logsApi from '@/lib/api/logs';
import * as eventsApi from '@/lib/api/events';
import * as pointsApi from '@/lib/api/points';
import { Goal } from '@/types/goal';
import { Log } from '@/types/log';
import { Event } from '@/types/event';
import { TrendingUp, Target, FileText, Calendar, Award } from 'lucide-react';

export default function DashboardPage() {
  const { user } = useAuthStore();
  const [goals, setGoals] = useState<Goal[]>([]);
  const [logs, setLogs] = useState<Log[]>([]);
  const [events, setEvents] = useState<Event[]>([]);
  const [totalPoints, setTotalPoints] = useState(0);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const loadDashboardData = async () => {
      setIsLoading(true);
      try {
        const [goalsData, logsData, eventsData, pointsData] = await Promise.all([
          goalsApi.fetchGoals(),
          logsApi.fetchLogs(),
          eventsApi.fetchEvents(),
          pointsApi.fetchUserPoints(),
        ]);
        setGoals(goalsData.filter(g => g.status === 'active').slice(0, 3));
        setLogs(logsData.slice(0, 3));
        setEvents(eventsData.filter(e => new Date(e.start_date) > new Date()).slice(0, 5));
        setTotalPoints(pointsData.total_points);
      } catch (err) {
        console.error('Failed to load dashboard data:', err);
      } finally {
        setIsLoading(false);
      }
    };

    loadDashboardData();
  }, [user?.id]);

  const activeGoalsCount = goals.length;
  const thisWeekLogs = logs.filter(log => {
    const date = new Date(log.created_at);
    const weekAgo = new Date();
    weekAgo.setDate(weekAgo.getDate() - 7);
    return date > weekAgo;
  }).length;

  return (
    <div className="space-y-4 sm:space-y-6">
      <div>
        <h1 className="text-2xl font-semibold text-asoto-text-main sm:text-3xl">ダッシュボード</h1>
        <p className="text-xs text-asoto-text-muted sm:text-sm">日々の「あそと」を俯瞰し、軽やかに次の一歩を決めましょう。</p>
      </div>

      <div className="grid gap-3 sm:grid-cols-2 sm:gap-4 lg:grid-cols-4">
        <Card className="bg-gradient-to-br from-asoto-primary to-asoto-primary/80 text-white">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">累計ポイント</CardTitle>
            <Award className="h-4 w-4" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{totalPoints} pt</div>
            <p className="text-xs text-white/80">活動を続けよう</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">進行中の目標</CardTitle>
            <Target className="h-4 w-4 text-asoto-primary" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{activeGoalsCount}</div>
            <p className="text-xs text-asoto-text-muted">達成に向けて</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">今週のログ</CardTitle>
            <FileText className="h-4 w-4 text-asoto-accent" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{thisWeekLogs}</div>
            <p className="text-xs text-asoto-text-muted">内省を続けよう</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">今後のイベント</CardTitle>
            <Calendar className="h-4 w-4 text-asoto-secondary" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{events.length}</div>
            <p className="text-xs text-asoto-text-muted">参加してみよう</p>
          </CardContent>
        </Card>
      </div>

      <div className="grid gap-4 sm:gap-6 lg:grid-cols-2">
        <Card className="bg-asoto-bg-surface border-asoto-border">
          <CardHeader>
            <div className="flex items-center justify-between">
              <div>
                <CardTitle>進行中の目標</CardTitle>
                <CardDescription>あなたが取り組んでいる目標</CardDescription>
              </div>
              <Link href="/goals">
                <Button variant="ghost" size="sm">すべて見る</Button>
              </Link>
            </div>
          </CardHeader>
          <CardContent>
            {isLoading ? (
              <p className="text-sm text-asoto-text-muted">読み込み中...</p>
            ) : goals.length === 0 ? (
              <div className="text-center py-8">
                <p className="text-sm text-asoto-text-muted mb-4">まだ目標がありません</p>
                <Link href="/goals">
                  <Button size="sm">目標を作成する</Button>
                </Link>
              </div>
            ) : (
              <div className="space-y-3">
                {goals.map((goal) => (
                  <div key={goal.id} className="rounded-lg border border-asoto-border p-3">
                    <div className="flex items-start justify-between gap-2">
                      <h4 className="font-medium text-asoto-text-main text-sm">{goal.title}</h4>
                      <span className="text-xs text-asoto-primary font-medium">{goal.progress}%</span>
                    </div>
                    <div className="mt-2 h-2 w-full bg-asoto-bg-main rounded-full overflow-hidden">
                      <div
                        className="h-full bg-asoto-primary transition-all"
                        style={{ width: `${goal.progress}%` }}
                      />
                    </div>
                  </div>
                ))}
              </div>
            )}
          </CardContent>
        </Card>

        <Card className="bg-asoto-bg-surface border-asoto-border">
          <CardHeader>
            <div className="flex items-center justify-between">
              <div>
                <CardTitle>最近のログ</CardTitle>
                <CardDescription>あなたの振り返り</CardDescription>
              </div>
              <Link href="/logs">
                <Button variant="ghost" size="sm">すべて見る</Button>
              </Link>
            </div>
          </CardHeader>
          <CardContent>
            {isLoading ? (
              <p className="text-sm text-asoto-text-muted">読み込み中...</p>
            ) : logs.length === 0 ? (
              <div className="text-center py-8">
                <p className="text-sm text-asoto-text-muted mb-4">まだログがありません</p>
                <Link href="/logs">
                  <Button size="sm">ログを書く</Button>
                </Link>
              </div>
            ) : (
              <div className="space-y-3">
                {logs.map((log) => (
                  <div key={log.id} className="rounded-lg border border-asoto-border p-3">
                    <h4 className="font-medium text-asoto-text-main text-sm">{log.title}</h4>
                    <p className="mt-1 text-xs text-asoto-text-muted line-clamp-2">{log.content}</p>
                    <p className="mt-2 text-xs text-asoto-text-muted">
                      {formatDate(log.created_at)}
                    </p>
                  </div>
                ))}
              </div>
            )}
          </CardContent>
        </Card>
      </div>

      <Card className="bg-asoto-bg-surface border-asoto-border">
        <CardHeader>
          <div className="flex items-center justify-between">
            <div>
              <CardTitle>今後のイベント</CardTitle>
              <CardDescription>コミュニティの予定</CardDescription>
            </div>
            <Link href="/events">
              <Button variant="ghost" size="sm">すべて見る</Button>
            </Link>
          </div>
        </CardHeader>
        <CardContent>
          {isLoading ? (
            <p className="text-sm text-asoto-text-muted">読み込み中...</p>
          ) : events.length === 0 ? (
            <div className="text-center py-8">
              <p className="text-sm text-asoto-text-muted mb-4">今後のイベントはありません</p>
              <Link href="/events">
                <Button size="sm">イベントを作成する</Button>
              </Link>
            </div>
          ) : (
            <div className="space-y-3">
              {events.map((event) => (
                <div key={event.id} className="rounded-lg border border-asoto-border p-3 hover:bg-asoto-bg-main/50 transition-colors">
                  <div className="flex items-start justify-between gap-4">
                    <div className="flex-1">
                      <h4 className="font-medium text-asoto-text-main text-sm">{event.title}</h4>
                      {event.description && (
                        <p className="mt-1 text-xs text-asoto-text-muted line-clamp-1">{event.description}</p>
                      )}
                    </div>
                    <span className="text-xs text-asoto-text-muted whitespace-nowrap">
                      {formatDate(event.start_date)}
                    </span>
                  </div>
                </div>
              ))}
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
}

function formatDate(value?: string | null) {
  if (!value) return '-';
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return '-';
  return date.toLocaleDateString('ja-JP', { month: 'short', day: 'numeric' });
}
