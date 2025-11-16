import { apiClient } from './client';
import { Event, EventParticipant, CreateEventInput, UpdateEventInput } from '@/types/event';

/**
 * イベント一覧を取得
 */
export async function fetchEvents(): Promise<Event[]> {
  const response = await apiClient.get<Event[]>('/events');
  return response.data;
}

/**
 * イベント詳細を取得
 */
export async function fetchEvent(eventId: string): Promise<Event> {
  const response = await apiClient.get<Event>(`/events/${eventId}`);
  return response.data;
}

/**
 * イベントを作成
 */
export async function createEvent(data: CreateEventInput): Promise<Event> {
  const response = await apiClient.post<Event>('/events', data);
  return response.data;
}

/**
 * イベントを更新
 */
export async function updateEvent(eventId: string, data: UpdateEventInput): Promise<Event> {
  const response = await apiClient.patch<Event>(`/events/${eventId}`, data);
  return response.data;
}

/**
 * イベントを削除
 */
export async function deleteEvent(eventId: string): Promise<void> {
  await apiClient.delete(`/events/${eventId}`);
}

/**
 * イベントに参加
 */
export async function joinEvent(eventId: string): Promise<EventParticipant> {
  const response = await apiClient.post<EventParticipant>(`/events/${eventId}/join`);
  return response.data;
}

/**
 * イベントから離脱
 */
export async function leaveEvent(eventId: string): Promise<void> {
  await apiClient.delete(`/events/${eventId}/leave`);
}

/**
 * イベント参加者一覧を取得
 */
export async function fetchEventParticipants(eventId: string): Promise<EventParticipant[]> {
  const response = await apiClient.get<EventParticipant[]>(`/events/${eventId}/participants`);
  return response.data;
}
