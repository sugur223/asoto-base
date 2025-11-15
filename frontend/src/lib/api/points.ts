import { apiClient } from './client';

export interface Point {
  id: string;
  user_id: string;
  amount: number;
  action_type: string;
  reference_id?: string | null;
  description?: string | null;
  created_at: string;
}

export interface PointsSummary {
  total_points: number;
  recent_points: Point[];
}

/**
 * ユーザーのポイント合計を取得
 */
export async function fetchUserPoints(userId: string): Promise<PointsSummary> {
  const response = await apiClient.get<PointsSummary>(`/users/${userId}/points`);
  return response.data;
}

/**
 * ユーザーのポイント履歴を取得
 */
export async function fetchUserPointsHistory(userId: string): Promise<Point[]> {
  const response = await apiClient.get<Point[]>(`/users/${userId}/points/history`);
  return response.data;
}
