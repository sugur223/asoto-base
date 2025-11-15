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
  user_id: string;
  total_points: number;
}

/**
 * 自分のポイント合計を取得
 */
export async function fetchUserPoints(): Promise<PointsSummary> {
  const response = await apiClient.get<PointsSummary>('/users/me/points');
  return response.data;
}

/**
 * 自分のポイント履歴を取得
 */
export async function fetchUserPointsHistory(): Promise<Point[]> {
  const response = await apiClient.get<Point[]>('/users/me/points/history');
  return response.data;
}
