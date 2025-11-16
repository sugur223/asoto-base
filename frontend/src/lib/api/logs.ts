import { apiClient } from './client';
import { Log, CreateLogInput, UpdateLogInput } from '@/types/log';

/**
 * 内省ログ一覧を取得
 */
export async function fetchLogs(): Promise<Log[]> {
  const response = await apiClient.get<Log[]>('/logs');
  return response.data;
}

/**
 * 内省ログ詳細を取得
 */
export async function fetchLog(logId: string): Promise<Log> {
  const response = await apiClient.get<Log>(`/logs/${logId}`);
  return response.data;
}

/**
 * 内省ログを作成
 */
export async function createLog(data: CreateLogInput): Promise<Log> {
  const response = await apiClient.post<Log>('/logs', data);
  return response.data;
}

/**
 * 内省ログを更新
 */
export async function updateLog(logId: string, data: UpdateLogInput): Promise<Log> {
  const response = await apiClient.patch<Log>(`/logs/${logId}`, data);
  return response.data;
}

/**
 * 内省ログを削除
 */
export async function deleteLog(logId: string): Promise<void> {
  await apiClient.delete(`/logs/${logId}`);
}
