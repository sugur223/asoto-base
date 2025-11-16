export type StepStatus = 'pending' | 'in_progress' | 'completed';

export interface Step {
  id: string;
  goal_id: string;
  title: string;
  description?: string | null;
  order: number;
  status: StepStatus;
  estimated_minutes?: number | null;
  actual_minutes?: number | null;
  due_date?: string | null;
  completed_at?: string | null;
  created_at: string;
  updated_at: string;
}

export interface CreateStepInput {
  title: string;
  description?: string;
  order: number;
  estimated_minutes?: number;
  due_date?: string;
}

export interface UpdateStepInput {
  title?: string;
  description?: string;
  order?: number;
  status?: StepStatus;
  estimated_minutes?: number;
  actual_minutes?: number;
  due_date?: string;
}
