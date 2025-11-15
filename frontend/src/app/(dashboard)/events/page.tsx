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
import { Event, LocationType } from '@/types/event';
import * as eventsApi from '@/lib/api/events';
import { Calendar, MapPin, Users } from 'lucide-react';

const eventFormSchema = z.object({
  title: z.string().min(1, 'タイトルを入力してください'),
  description: z.string().optional(),
  start_date: z.string().min(1, '開始日時を入力してください'),
  end_date: z.string().optional(),
  location_type: z.enum(['online', 'offline', 'hybrid']),
  location_detail: z.string().optional(),
  max_attendees: z.string().optional(),
  tags: z.string().optional(),
});

type EventFormData = z.infer<typeof eventFormSchema>;

const locationTypeLabels: Record<LocationType, string> = {
  online: 'オンライン',
  offline: 'オフライン',
  hybrid: 'ハイブリッド',
};

export default function EventsPage() {
  const { user } = useAuthStore();
  const [events, setEvents] = useState<Event[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [isCreating, setIsCreating] = useState(false);
  const [showCreateForm, setShowCreateForm] = useState(false);

  const {
    register,
    handleSubmit,
    reset,
    formState: { errors },
  } = useForm<EventFormData>({
    resolver: zodResolver(eventFormSchema),
    defaultValues: {
      location_type: 'online',
    },
  });

  useEffect(() => {
    const loadEvents = async () => {
      setIsLoading(true);
      setError(null);
      try {
        const data = await eventsApi.fetchEvents();
        setEvents(data);
      } catch (err: any) {
        const message = err.response?.data?.detail || 'イベントの取得に失敗しました';
        setError(message);
      } finally {
        setIsLoading(false);
      }
    };

    loadEvents();
  }, []);

  const onSubmit = async (formData: EventFormData) => {
    setIsCreating(true);
    setError(null);
    try {
      const tags = formData.tags
        ? formData.tags.split(',').map((tag) => tag.trim()).filter(Boolean)
        : [];

      const newEvent = await eventsApi.createEvent({
        title: formData.title,
        description: formData.description || undefined,
        start_date: new Date(formData.start_date).toISOString(),
        end_date: formData.end_date ? new Date(formData.end_date).toISOString() : undefined,
        location_type: formData.location_type,
        location_detail: formData.location_detail || undefined,
        max_attendees: formData.max_attendees ? parseInt(formData.max_attendees) : undefined,
        tags,
      });
      setEvents((prev) => [newEvent, ...prev]);
      reset({ title: '', description: '', start_date: '', end_date: '', location_type: formData.location_type, location_detail: '', max_attendees: '', tags: '' });
      setShowCreateForm(false);
    } catch (err: any) {
      const message = err.response?.data?.detail || 'イベントの作成に失敗しました';
      setError(message);
    } finally {
      setIsCreating(false);
    }
  };

  const handleJoinEvent = async (eventId: string) => {
    setError(null);
    try {
      await eventsApi.joinEvent(eventId);
      // イベント一覧を再取得して参加状況を更新
      const data = await eventsApi.fetchEvents();
      setEvents(data);
    } catch (err: any) {
      const message = err.response?.data?.detail || 'イベント参加に失敗しました';
      setError(message);
    }
  };

  const myEvents = events.filter((event) => event.owner_id === user?.id);
  const upcomingEvents = events.filter((event) => {
    const startDate = new Date(event.start_date);
    return startDate > new Date() && event.owner_id !== user?.id;
  });

  return (
    <div className="space-y-4 sm:space-y-6">
      <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
        <div>
          <h1 className="text-2xl font-bold text-asoto-text-main sm:text-3xl">イベント</h1>
          <p className="text-xs text-asoto-text-muted sm:text-sm">コミュニティの予定をチェックし、気になるイベントに参加しましょう。</p>
        </div>
        <Button
          className="w-full rounded-full bg-asoto-primary text-white sm:w-auto"
          onClick={() => setShowCreateForm(!showCreateForm)}
        >
          {showCreateForm ? 'キャンセル' : '新しいイベントを作成'}
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
            <CardTitle>新しいイベント</CardTitle>
            <CardDescription>コミュニティで開催するイベントを企画しましょう</CardDescription>
          </CardHeader>
          <CardContent>
            <form className="space-y-4" onSubmit={handleSubmit(onSubmit)}>
              <div className="space-y-2">
                <Label htmlFor="title">タイトル</Label>
                <Input
                  id="title"
                  placeholder="例：牧場見学ツアー"
                  {...register('title')}
                  disabled={isCreating}
                />
                {errors.title && <p className="text-sm text-destructive">{errors.title.message}</p>}
              </div>

              <div className="space-y-2">
                <Label htmlFor="description">説明</Label>
                <textarea
                  id="description"
                  className="min-h-[100px] w-full rounded-md border border-asoto-border bg-transparent p-3 text-sm text-asoto-text-main focus:outline-none focus:ring-2 focus:ring-asoto-primary/50"
                  placeholder="イベントの詳細を記入してください..."
                  {...register('description')}
                  disabled={isCreating}
                />
              </div>

              <div className="grid gap-4 sm:grid-cols-2">
                <div className="space-y-2">
                  <Label htmlFor="start_date">開始日時</Label>
                  <Input
                    id="start_date"
                    type="datetime-local"
                    {...register('start_date')}
                    disabled={isCreating}
                  />
                  {errors.start_date && <p className="text-sm text-destructive">{errors.start_date.message}</p>}
                </div>

                <div className="space-y-2">
                  <Label htmlFor="end_date">終了日時（任意）</Label>
                  <Input
                    id="end_date"
                    type="datetime-local"
                    {...register('end_date')}
                    disabled={isCreating}
                  />
                </div>
              </div>

              <div className="grid gap-4 sm:grid-cols-2">
                <div className="space-y-2">
                  <Label htmlFor="location_type">開催形式</Label>
                  <select
                    id="location_type"
                    className="w-full rounded-md border border-asoto-border bg-asoto-bg-main p-2 text-sm text-asoto-text-main"
                    {...register('location_type')}
                    disabled={isCreating}
                  >
                    <option value="online">オンライン</option>
                    <option value="offline">オフライン</option>
                    <option value="hybrid">ハイブリッド</option>
                  </select>
                </div>

                <div className="space-y-2">
                  <Label htmlFor="max_attendees">定員（任意）</Label>
                  <Input
                    id="max_attendees"
                    type="number"
                    placeholder="例：30"
                    {...register('max_attendees')}
                    disabled={isCreating}
                  />
                </div>
              </div>

              <div className="space-y-2">
                <Label htmlFor="location_detail">場所の詳細</Label>
                <Input
                  id="location_detail"
                  placeholder="例：Zoom URL、住所など"
                  {...register('location_detail')}
                  disabled={isCreating}
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="tags">タグ（カンマ区切り）</Label>
                <Input
                  id="tags"
                  placeholder="例：交流会, 農業, 見学"
                  {...register('tags')}
                  disabled={isCreating}
                />
              </div>

              <Button type="submit" className="w-full" disabled={isCreating}>
                {isCreating ? '作成中...' : 'イベントを作成'}
              </Button>
            </form>
          </CardContent>
        </Card>
      )}

      <div className="grid gap-4 sm:gap-6 lg:grid-cols-2">
        <Card className="bg-asoto-bg-surface border-asoto-border">
          <CardHeader>
            <CardTitle>主催イベント</CardTitle>
            <CardDescription>あなたが企画したイベント</CardDescription>
          </CardHeader>
          <CardContent>
            {isLoading ? (
              <p className="text-sm text-asoto-text-muted">読み込み中...</p>
            ) : myEvents.length === 0 ? (
              <p className="text-sm text-asoto-text-muted">まだイベントを作成していません。</p>
            ) : (
              <div className="space-y-4">
                {myEvents.map((event) => (
                  <EventCard key={event.id} event={event} isOwner={true} />
                ))}
              </div>
            )}
          </CardContent>
        </Card>

        <Card className="bg-asoto-bg-surface border-asoto-border">
          <CardHeader>
            <CardTitle>今後のイベント</CardTitle>
            <CardDescription>コミュニティの予定</CardDescription>
          </CardHeader>
          <CardContent>
            {isLoading ? (
              <p className="text-sm text-asoto-text-muted">読み込み中...</p>
            ) : upcomingEvents.length === 0 ? (
              <p className="text-sm text-asoto-text-muted">今後のイベントはありません。</p>
            ) : (
              <div className="space-y-4">
                {upcomingEvents.map((event) => (
                  <EventCard
                    key={event.id}
                    event={event}
                    isOwner={false}
                    onJoin={() => handleJoinEvent(event.id)}
                  />
                ))}
              </div>
            )}
          </CardContent>
        </Card>
      </div>
    </div>
  );
}

interface EventCardProps {
  event: Event;
  isOwner: boolean;
  onJoin?: () => void;
}

function EventCard({ event, isOwner, onJoin }: EventCardProps) {
  const startDate = new Date(event.start_date);
  const isPast = startDate < new Date();

  return (
    <div className="rounded-lg border border-asoto-border p-4">
      <div className="flex items-start justify-between gap-4">
        <div className="flex-1">
          <h3 className="text-lg font-semibold text-asoto-text-main">{event.title}</h3>
          {event.description && (
            <p className="mt-2 text-sm text-asoto-text-muted line-clamp-2">{event.description}</p>
          )}
        </div>
        <span
          className={`rounded-full px-3 py-1 text-xs font-medium ${
            locationTypeLabels[event.location_type] === 'オンライン'
              ? 'bg-blue-50 text-blue-600'
              : locationTypeLabels[event.location_type] === 'オフライン'
                ? 'bg-green-50 text-green-600'
                : 'bg-purple-50 text-purple-600'
          }`}
        >
          {locationTypeLabels[event.location_type]}
        </span>
      </div>

      <div className="mt-3 space-y-2 text-xs text-asoto-text-muted">
        <div className="flex items-center gap-2">
          <Calendar className="h-4 w-4" />
          <span>{formatDateTime(event.start_date)}</span>
        </div>
        {event.location_detail && (
          <div className="flex items-center gap-2">
            <MapPin className="h-4 w-4" />
            <span className="line-clamp-1">{event.location_detail}</span>
          </div>
        )}
        {event.max_attendees && (
          <div className="flex items-center gap-2">
            <Users className="h-4 w-4" />
            <span>定員: {event.max_attendees}名</span>
          </div>
        )}
      </div>

      {event.tags && event.tags.length > 0 && (
        <div className="mt-3 flex flex-wrap gap-2">
          {event.tags.map((tag, idx) => (
            <span
              key={idx}
              className="rounded-full bg-asoto-bg-main px-3 py-1 text-xs text-asoto-text-muted"
            >
              #{tag}
            </span>
          ))}
        </div>
      )}

      {!isOwner && !isPast && (
        <div className="mt-4">
          <Button
            variant="outline"
            size="sm"
            className="w-full sm:w-auto"
            onClick={onJoin}
          >
            参加する
          </Button>
        </div>
      )}
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
