import { apiClient } from './client';
import { Project, CreateProjectInput, UpdateProjectInput } from '@/types/project';

/**
 * プロジェクト一覧を取得
 */
export async function fetchProjects(): Promise<Project[]> {
  const response = await apiClient.get<Project[]>('/projects');
  return response.data;
}

/**
 * プロジェクト詳細を取得
 */
export async function fetchProject(projectId: string): Promise<Project> {
  const response = await apiClient.get<Project>(`/projects/${projectId}`);
  return response.data;
}

/**
 * プロジェクトを作成
 */
export async function createProject(data: CreateProjectInput): Promise<Project> {
  const response = await apiClient.post<Project>('/projects', data);
  return response.data;
}

/**
 * プロジェクトを更新
 */
export async function updateProject(projectId: string, data: UpdateProjectInput): Promise<Project> {
  const response = await apiClient.patch<Project>(`/projects/${projectId}`, data);
  return response.data;
}

/**
 * プロジェクトを削除
 */
export async function deleteProject(projectId: string): Promise<void> {
  await apiClient.delete(`/projects/${projectId}`);
}

/**
 * プロジェクトに参加申請
 */
export async function joinProject(projectId: string): Promise<void> {
  await apiClient.post(`/projects/${projectId}/join`);
}
