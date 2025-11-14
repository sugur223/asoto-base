export type GoalCategory = 'relationship' | 'activity' | 'sensitivity';
export type GoalStatus = 'active' | 'completed' | 'archived';

export interface Goal {
  id: string;
  user_id: string;
  title: string;
  description?: string | null;
  category: GoalCategory;
  status: GoalStatus;
  progress: number;
  due_date?: string | null;
  completed_at?: string | null;
  created_at: string;
  updated_at: string;
}

export interface CreateGoalInput {
  title: string;
  description?: string;
  category: GoalCategory;
  due_date?: string;
}

export interface UpdateGoalInput {
  title?: string;
  description?: string;
  category?: GoalCategory;
  status?: GoalStatus;
  progress?: number;
  due_date?: string;
}
