import { apiClient } from './client';
import { Step, CreateStepInput, UpdateStepInput } from '@/types/step';

/**
 * ステップを作成
 */
export async function createStep(goalId: string, data: CreateStepInput): Promise<Step> {
  const response = await apiClient.post<Step>(`/goals/${goalId}/steps`, data);
  return response.data;
}

/**
 * ステップを更新
 */
export async function updateStep(stepId: string, data: UpdateStepInput): Promise<Step> {
  const response = await apiClient.patch<Step>(`/steps/${stepId}`, data);
  return response.data;
}

/**
 * ステップを完了
 */
export async function completeStep(stepId: string): Promise<Step> {
  const response = await apiClient.post<Step>(`/steps/${stepId}/complete`);
  return response.data;
}

/**
 * ステップを削除
 */
export async function deleteStep(stepId: string): Promise<void> {
  await apiClient.delete(`/steps/${stepId}`);
}
