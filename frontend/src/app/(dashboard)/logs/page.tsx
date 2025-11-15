'use client';

import { useEffect, useState } from 'react';
import { useForm } from 'react-hook-form';
import { z } from 'zod';
import { zodResolver } from '@hookform/resolvers/zod';

import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { useAuthStore } from '@/stores/authStore';
import { Log, LogVisibility } from '@/types/log';
import * as logsApi from '@/lib/api/logs';

const logFormSchema = z.object({
  title: z.string().min(1, 'タイトルを入力してください'),
  content: z.string().min(1, '内容を入力してください'),
  tags: z.string().optional(),
  visibility: z.enum(['private', 'public']),
});

type LogFormData = z.infer<typeof logFormSchema>;

const visibilityLabels: Record<LogVisibility, string> = {
  private: '非公開',
  public: '公開',
  friends_only: '友達のみ',
};

export default function LogsPage() {
  const { user } = useAuthStore();
  const [logs, setLogs] = useState<Log[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [isCreating, setIsCreating] = useState(false);
  const [showCreateForm, setShowCreateForm] = useState(false);

  const {
    register,
    handleSubmit,
    reset,
    formState: { errors },
  } = useForm<LogFormData>({
    resolver: zodResolver(logFormSchema),
    defaultValues: {
      visibility: 'private',
    },
  });

  useEffect(() => {
    const loadLogs = async () => {
      setIsLoading(true);
      setError(null);
      try {
        const data = await logsApi.fetchLogs();
        setLogs(data);
      } catch (err: any) {
        const message = err.response?.data?.detail || 'ログの取得に失敗しました';
        setError(message);
      } finally {
        setIsLoading(false);
      }
    };

    loadLogs();
  }, []);

  const onSubmit = async (formData: LogFormData) => {
    setIsCreating(true);
    setError(null);
    try {
      const tags = formData.tags
        ? formData.tags.split(',').map((tag) => tag.trim()).filter(Boolean)
        : [];

      const newLog = await logsApi.createLog({
        title: formData.title,
        content: formData.content,
        tags,
        visibility: formData.visibility as LogVisibility,
      });
      setLogs((prev) => [newLog, ...prev]);
      reset({ title: '', content: '', tags: '', visibility: formData.visibility });
      setShowCreateForm(false);
    } catch (err: any) {
      const message = err.response?.data?.detail || 'ログの作成に失敗しました';
      setError(message);
    } finally {
      setIsCreating(false);
    }
  };

  const handleDeleteLog = async (logId: string) => {
    if (!confirm('このログを削除してもよろしいですか？')) return;

    setError(null);
    try {
      await logsApi.deleteLog(logId);
      setLogs((prev) => prev.filter((log) => log.id !== logId));
    } catch (err: any) {
      const message = err.response?.data?.detail || 'ログの削除に失敗しました';
      setError(message);
    }
  };

  const myLogs = logs.filter((log) => log.user_id === user?.id);
  const publicLogs = logs.filter((log) => log.visibility === 'public' && log.user_id !== user?.id);

  return (
    <div className="space-y-4 sm:space-y-6">
      <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
        <div>
          <h1 className="text-2xl font-bold text-asoto-text-main sm:text-3xl">内省ログ</h1>
          <p className="text-xs text-asoto-text-muted sm:text-sm">日々の気づきや学びを蓄積しましょう。</p>
        </div>
        <Button
          className="w-full rounded-full bg-asoto-primary text-white sm:w-auto"
          onClick={() => setShowCreateForm(!showCreateForm)}
        >
          {showCreateForm ? 'キャンセル' : '新しいログを書く'}
        </Button>
      </div>

      {error && (
        <div className="rounded-md border border-destructive/20 bg-destructive/10 p-3 text-sm text-destructive">
          {error}
        </div>
      )}

      {showCreateForm && (
        <Card className="bg-asoto-bg-surface border-asoto-border">
          <CardHeader>
            <CardTitle>新しいログ</CardTitle>
            <CardDescription>今日の気づきや学びを記録しましょう</CardDescription>
          </CardHeader>
          <CardContent>
            <form className="space-y-4" onSubmit={handleSubmit(onSubmit)}>
              <div className="space-y-2">
                <Label htmlFor="title">タイトル</Label>
                <Input
                  id="title"
                  placeholder="例：初めてのチーム振り返り"
                  {...register('title')}
                  disabled={isCreating}
                />
                {errors.title && <p className="text-sm text-destructive">{errors.title.message}</p>}
              </div>

              <div className="space-y-2">
                <Label htmlFor="content">内容</Label>
                <textarea
                  id="content"
                  className="min-h-[200px] w-full rounded-md border border-asoto-border bg-transparent p-3 text-sm text-asoto-text-main focus:outline-none focus:ring-2 focus:ring-asoto-primary/50"
                  placeholder="どんなことがあったか、何を学んだか、これからどうするか..."
                  {...register('content')}
                  disabled={isCreating}
                />
                {errors.content && <p className="text-sm text-destructive">{errors.content.message}</p>}
              </div>

              <div className="space-y-2">
                <Label htmlFor="tags">タグ（カンマ区切り）</Label>
                <Input
                  id="tags"
                  placeholder="例：振り返り, チーム, コミュニケーション"
                  {...register('tags')}
                  disabled={isCreating}
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="visibility">公開設定</Label>
                <select
                  id="visibility"
                  className="w-full rounded-md border border-asoto-border bg-asoto-bg-main p-2 text-sm text-asoto-text-main"
                  {...register('visibility')}
                  disabled={isCreating}
                >
                  <option value="private">非公開</option>
                  <option value="public">公開</option>
                </select>
              </div>

              <Button type="submit" className="w-full" disabled={isCreating}>
                {isCreating ? '作成中...' : 'ログを投稿'}
              </Button>
            </form>
          </CardContent>
        </Card>
      )}

      <div className="grid gap-4 sm:gap-6 lg:grid-cols-2">
        <Card className="bg-asoto-bg-surface border-asoto-border">
          <CardHeader>
            <CardTitle>マイログ</CardTitle>
            <CardDescription>あなたの振り返り記録</CardDescription>
          </CardHeader>
          <CardContent>
            {isLoading ? (
              <p className="text-sm text-asoto-text-muted">読み込み中...</p>
            ) : myLogs.length === 0 ? (
              <p className="text-sm text-asoto-text-muted">まだログが登録されていません。</p>
            ) : (
              <div className="space-y-4">
                {myLogs.map((log) => (
                  <div key={log.id} className="rounded-lg border border-asoto-border p-4">
                    <div className="flex items-start justify-between gap-4">
                      <div className="flex-1">
                        <h3 className="text-lg font-semibold text-asoto-text-main">{log.title}</h3>
                        <p className="mt-2 text-sm text-asoto-text-muted line-clamp-3">{log.content}</p>
                      </div>
                      <span
                        className={`rounded-full px-3 py-1 text-xs font-medium ${
                          log.visibility === 'public'
                            ? 'bg-asoto-primary/10 text-asoto-primary'
                            : 'bg-asoto-border text-asoto-text-muted'
                        }`}
                      >
                        {visibilityLabels[log.visibility]}
                      </span>
                    </div>
                    {log.tags && log.tags.length > 0 && (
                      <div className="mt-3 flex flex-wrap gap-2">
                        {log.tags.map((tag, idx) => (
                          <span
                            key={idx}
                            className="rounded-full bg-asoto-bg-main px-3 py-1 text-xs text-asoto-text-muted"
                          >
                            #{tag}
                          </span>
                        ))}
                      </div>
                    )}
                    <div className="mt-3 flex items-center gap-3 text-xs text-asoto-text-muted">
                      <span>作成: {formatDate(log.created_at)}</span>
                    </div>
                    <div className="mt-4 flex flex-wrap gap-2">
                      <Button
                        variant="ghost"
                        size="sm"
                        className="text-red-600 hover:bg-red-50 hover:text-red-700"
                        onClick={() => handleDeleteLog(log.id)}
                      >
                        削除
                      </Button>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </CardContent>
        </Card>

        <Card className="bg-asoto-bg-surface border-asoto-border">
          <CardHeader>
            <CardTitle>コミュニティのログ</CardTitle>
            <CardDescription>他のメンバーの公開ログ</CardDescription>
          </CardHeader>
          <CardContent>
            {isLoading ? (
              <p className="text-sm text-asoto-text-muted">読み込み中...</p>
            ) : publicLogs.length === 0 ? (
              <p className="text-sm text-asoto-text-muted">まだ公開ログがありません。</p>
            ) : (
              <div className="space-y-4">
                {publicLogs.map((log) => (
                  <div key={log.id} className="rounded-lg border border-asoto-border p-4">
                    <h3 className="text-lg font-semibold text-asoto-text-main">{log.title}</h3>
                    <p className="mt-2 text-sm text-asoto-text-muted line-clamp-3">{log.content}</p>
                    {log.tags && log.tags.length > 0 && (
                      <div className="mt-3 flex flex-wrap gap-2">
                        {log.tags.map((tag, idx) => (
                          <span
                            key={idx}
                            className="rounded-full bg-asoto-bg-main px-3 py-1 text-xs text-asoto-text-muted"
                          >
                            #{tag}
                          </span>
                        ))}
                      </div>
                    )}
                    <div className="mt-3 flex items-center gap-3 text-xs text-asoto-text-muted">
                      <span>作成: {formatDate(log.created_at)}</span>
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
