'use client';

import { useEffect, useMemo, useState } from 'react';
import { useForm } from 'react-hook-form';
import { z } from 'zod';
import { zodResolver } from '@hookform/resolvers/zod';

import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { useAuthStore } from '@/stores/authStore';
import { Goal, GoalCategory, GoalStatus } from '@/types/goal';
import * as goalsApi from '@/lib/api/goals';

const goalFormSchema = z.object({
  title: z.string().min(1, 'タイトルを入力してください'),
  description: z.string().optional(),
  category: z.enum(['relationship', 'activity', 'sensitivity']),
  due_date: z.string().optional(),
});

type GoalFormData = z.infer<typeof goalFormSchema>;

const categoryLabels: Record<GoalCategory, string> = {
  relationship: '関係性',
  activity: '多動性',
  sensitivity: '感受性',
};

const statusLabels: Record<GoalStatus, string> = {
  active: '進行中',
  completed: '完了',
  archived: 'アーカイブ',
};

export default function GoalsPage() {
  const { user } = useAuthStore();
  const [goals, setGoals] = useState<Goal[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [isCreating, setIsCreating] = useState(false);
  const [updatingGoalId, setUpdatingGoalId] = useState<string | null>(null);

  const {
    register,
    handleSubmit,
    reset,
    formState: { errors },
  } = useForm<GoalFormData>({
    resolver: zodResolver(goalFormSchema),
    defaultValues: {
      category: 'activity',
    },
  });

  useEffect(() => {
    const loadGoals = async () => {
      setIsLoading(true);
      setError(null);
      try {
        const data = await goalsApi.fetchGoals();
        setGoals(data);
      } catch (err: any) {
        const message = err.response?.data?.detail || '目標の取得に失敗しました';
        setError(message);
      } finally {
        setIsLoading(false);
      }
    };

    loadGoals();
  }, []);

  const onSubmit = async (formData: GoalFormData) => {
    setIsCreating(true);
    setError(null);
    try {
      const newGoal = await goalsApi.createGoal({
        title: formData.title,
        description: formData.description || undefined,
        category: formData.category,
        due_date: formData.due_date ? new Date(formData.due_date).toISOString() : undefined,
      });
      setGoals((prev) => [newGoal, ...prev]);
      reset({ title: '', description: '', category: formData.category, due_date: '' });
    } catch (err: any) {
      const message = err.response?.data?.detail || '目標の作成に失敗しました';
      setError(message);
    } finally {
      setIsCreating(false);
    }
  };

  const handleStatusChange = async (goalId: string, status: GoalStatus) => {
    setUpdatingGoalId(goalId);
    setError(null);
    try {
      const updated = await goalsApi.updateGoal(goalId, { status });
      setGoals((prev) => prev.map((goal) => (goal.id === goalId ? updated : goal)));
    } catch (err: any) {
      const message = err.response?.data?.detail || 'ステータスの更新に失敗しました';
      setError(message);
    } finally {
      setUpdatingGoalId(null);
    }
  };

  const summary = useMemo(() => {
    const total = goals.length;
    const active = goals.filter((goal) => goal.status === 'active').length;
    const completed = goals.filter((goal) => goal.status === 'completed').length;
    return { total, active, completed };
  }, [goals]);

  return (
    <div className="space-y-6">
      <div className="flex flex-col gap-2">
        <div>
          <p className="text-sm text-asoto-text-muted">{user?.full_name || user?.email} さんのあそとステップ</p>
          <h1 className="text-3xl font-bold text-asoto-text-main">目標管理</h1>
        </div>
          {error && (
            <div className="rounded-md border border-destructive/20 bg-destructive/10 p-3 text-sm text-destructive">
              {error}
            </div>
          )}
      </div>

      <div className="grid gap-4 md:grid-cols-3">
          <Card className="bg-asoto-bg-surface border-asoto-border">
            <CardHeader>
              <CardTitle>合計</CardTitle>
              <CardDescription>登録済みの目標数</CardDescription>
            </CardHeader>
            <CardContent>
              <p className="text-3xl font-bold text-asoto-text-main">{summary.total}</p>
            </CardContent>
          </Card>
          <Card className="bg-asoto-bg-surface border-asoto-border">
            <CardHeader>
              <CardTitle>進行中</CardTitle>
              <CardDescription>今取り組んでいる目標</CardDescription>
            </CardHeader>
            <CardContent>
              <p className="text-3xl font-bold text-asoto-primary">{summary.active}</p>
            </CardContent>
          </Card>
          <Card className="bg-asoto-bg-surface border-asoto-border">
            <CardHeader>
              <CardTitle>完了</CardTitle>
              <CardDescription>達成済みの目標</CardDescription>
            </CardHeader>
            <CardContent>
              <p className="text-3xl font-bold text-asoto-accent">{summary.completed}</p>
            </CardContent>
          </Card>
      </div>

      <div className="grid gap-6 lg:grid-cols-2">
          <Card className="bg-asoto-bg-surface border-asoto-border">
            <CardHeader>
              <CardTitle>新しい目標</CardTitle>
              <CardDescription>達成したいことを登録しましょう</CardDescription>
            </CardHeader>
            <CardContent>
              <form className="space-y-4" onSubmit={handleSubmit(onSubmit)}>
                <div className="space-y-2">
                  <Label htmlFor="title">タイトル</Label>
                  <Input id="title" placeholder="例：毎週1回の内省を書く" {...register('title')} disabled={isCreating} />
                  {errors.title && <p className="text-sm text-destructive">{errors.title.message}</p>}
                </div>

                <div className="space-y-2">
                  <Label htmlFor="description">説明</Label>
                  <textarea
                    id="description"
                    className="min-h-[96px] w-full rounded-md border border-asoto-border bg-transparent p-3 text-sm text-asoto-text-main focus:outline-none focus:ring-2 focus:ring-asoto-primary/50"
                    placeholder="どんな行動を計画していますか？"
                    {...register('description')}
                    disabled={isCreating}
                  />
                  {errors.description && <p className="text-sm text-destructive">{errors.description.message}</p>}
                </div>

                <div className="space-y-2">
                  <Label htmlFor="category">カテゴリ</Label>
                  <select
                    id="category"
                    className="w-full rounded-md border border-asoto-border bg-asoto-bg-main p-2 text-sm text-asoto-text-main"
                    {...register('category')}
                    disabled={isCreating}
                  >
                    <option value="relationship">関係性（Relationship）</option>
                    <option value="activity">多動性（Activity）</option>
                    <option value="sensitivity">感受性（Sensitivity）</option>
                  </select>
                </div>

                <div className="space-y-2">
                  <Label htmlFor="due_date">期限（任意）</Label>
                  <Input id="due_date" type="date" {...register('due_date')} disabled={isCreating} />
                </div>

                <Button type="submit" className="w-full" disabled={isCreating}>
                  {isCreating ? '作成中...' : '目標を追加'}
                </Button>
              </form>
            </CardContent>
          </Card>

          <Card className="bg-asoto-bg-surface border-asoto-border">
            <CardHeader>
              <CardTitle>目標リスト</CardTitle>
              <CardDescription>最新順で表示します</CardDescription>
            </CardHeader>
            <CardContent>
              {isLoading ? (
                <p className="text-sm text-asoto-text-muted">読み込み中...</p>
              ) : goals.length === 0 ? (
                <p className="text-sm text-asoto-text-muted">まだ目標が登録されていません。</p>
              ) : (
                <div className="space-y-4">
                  {goals.map((goal) => (
                    <div key={goal.id} className="rounded-lg border border-asoto-border p-4">
                      <div className="flex items-start justify-between gap-4">
                        <div>
                          <p className="text-xs text-asoto-text-muted">{categoryLabels[goal.category]}</p>
                          <h3 className="text-lg font-semibold text-asoto-text-main">{goal.title}</h3>
                        </div>
                        <span
                          className={`rounded-full px-3 py-1 text-xs font-medium ${
                            goal.status === 'completed'
                              ? 'bg-asoto-accent/10 text-asoto-accent'
                              : goal.status === 'archived'
                                ? 'bg-asoto-border text-asoto-text-muted'
                                : 'bg-asoto-primary/10 text-asoto-primary'
                          }`}
                        >
                          {statusLabels[goal.status]}
                        </span>
                      </div>
                      {goal.description && (
                        <p className="mt-2 text-sm text-asoto-text-muted">{goal.description}</p>
                      )}
                      <div className="mt-3 flex flex-wrap items-center gap-3 text-xs text-asoto-text-muted">
                        <span>作成: {formatDate(goal.created_at)}</span>
                        {goal.due_date && <span>期限: {formatDate(goal.due_date)}</span>}
                        {goal.completed_at && <span>完了: {formatDate(goal.completed_at)}</span>}
                        <span>進捗: {goal.progress}%</span>
                      </div>
                      <div className="mt-4 flex flex-wrap gap-2">
                        {goal.status !== 'completed' && (
                          <Button
                            variant="outline"
                            size="sm"
                            onClick={() => handleStatusChange(goal.id, 'completed')}
                            disabled={updatingGoalId === goal.id}
                          >
                            {updatingGoalId === goal.id ? '更新中...' : '完了にする'}
                          </Button>
                        )}
                        {goal.status === 'completed' && (
                          <Button
                            variant="outline"
                            size="sm"
                            onClick={() => handleStatusChange(goal.id, 'active')}
                            disabled={updatingGoalId === goal.id}
                          >
                            {updatingGoalId === goal.id ? '更新中...' : '進行中へ戻す'}
                          </Button>
                        )}
                        {goal.status !== 'archived' && (
                          <Button
                            variant="ghost"
                            size="sm"
                            className="text-asoto-text-muted hover:text-asoto-text-main"
                            onClick={() => handleStatusChange(goal.id, 'archived')}
                            disabled={updatingGoalId === goal.id}
                          >
                            {updatingGoalId === goal.id ? '更新中...' : 'アーカイブ'}
                          </Button>
                        )}
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </CardContent>
          </Card>
      </div>
    </div>
  );
}

function formatDate(value?: string | null) {
  if (!value) return '-';
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return '-';
  return date.toLocaleDateString('ja-JP', { year: 'numeric', month: 'short', day: 'numeric' });
}
