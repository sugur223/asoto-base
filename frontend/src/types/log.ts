export type LogVisibility = 'private' | 'public' | 'friends_only';

export interface Log {
  id: string;
  user_id: string;
  title: string;
  content: string;
  tags: string[];
  visibility: LogVisibility;
  created_at: string;
  updated_at: string;
}

export interface CreateLogInput {
  title: string;
  content: string;
  tags?: string[];
  visibility?: LogVisibility;
}

export interface UpdateLogInput {
  title?: string;
  content?: string;
  tags?: string[];
  visibility?: LogVisibility;
}
