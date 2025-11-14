import { Goal, CreateGoalInput, UpdateGoalInput } from '@/types/goal';
import { apiClient } from './client';

export const fetchGoals = async (): Promise<Goal[]> => {
  const response = await apiClient.get<Goal[]>('/goals');
  return response.data;
};

export const createGoal = async (data: CreateGoalInput): Promise<Goal> => {
  const response = await apiClient.post<Goal>('/goals', data);
  return response.data;
};

export const updateGoal = async (goalId: string, data: UpdateGoalInput): Promise<Goal> => {
  const response = await apiClient.patch<Goal>(`/goals/${goalId}`, data);
  return response.data;
};

export const deleteGoal = async (goalId: string): Promise<void> => {
  await apiClient.delete(`/goals/${goalId}`);
};
