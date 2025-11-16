export type ProjectCategory = 'asobi' | 'asoto';
export type ProjectStatus = 'planning' | 'active' | 'paused' | 'completed' | 'cancelled';
export type ProjectVisibility = 'public' | 'private' | 'members_only';
export type MemberRole = 'owner' | 'admin' | 'member' | 'viewer';
export type MemberStatus = 'pending' | 'active' | 'inactive';
export type TaskStatus = 'todo' | 'in_progress' | 'done';

export interface Project {
  id: string;
  owner_id: string;
  title: string;
  description?: string | null;
  category: ProjectCategory;
  status: ProjectStatus;
  start_date: string;
  end_date?: string | null;
  frequency?: string | null;
  location_type: 'online' | 'offline' | 'hybrid';
  location_detail?: string | null;
  is_recruiting: boolean;
  max_members?: number | null;
  required_skills: string[];
  tags: string[];
  visibility: ProjectVisibility;
  created_at: string;
  updated_at: string;
}

export interface CreateProjectInput {
  title: string;
  description?: string;
  category: ProjectCategory;
  start_date: string;
  end_date?: string;
  frequency?: string;
  location_type: 'online' | 'offline' | 'hybrid';
  location_detail?: string;
  is_recruiting?: boolean;
  max_members?: number;
  required_skills?: string[];
  tags?: string[];
  visibility?: ProjectVisibility;
}

export interface UpdateProjectInput {
  title?: string;
  description?: string;
  category?: ProjectCategory;
  status?: ProjectStatus;
  start_date?: string;
  end_date?: string;
  frequency?: string;
  location_type?: 'online' | 'offline' | 'hybrid';
  location_detail?: string;
  is_recruiting?: boolean;
  max_members?: number;
  required_skills?: string[];
  tags?: string[];
  visibility?: ProjectVisibility;
}
