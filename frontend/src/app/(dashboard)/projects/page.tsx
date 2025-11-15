'use client';

import { useEffect, useState } from 'react';
import { useForm } from 'react-hook-form';
import { z } from 'zod';
import { zodResolver } from '@hookform/resolvers/zod';

import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { useAuthStore } from '@/stores/authStore';
import { Project, ProjectCategory } from '@/types/project';
import * as projectsApi from '@/lib/api/projects';
import { Folder, Users, Calendar } from 'lucide-react';

const projectFormSchema = z.object({
  title: z.string().min(1, 'タイトルを入力してください'),
  description: z.string().optional(),
  category: z.enum(['asobi', 'asoto']),
  start_date: z.string().min(1, '開始日を入力してください'),
  end_date: z.string().optional(),
  frequency: z.string().optional(),
  location_type: z.enum(['online', 'offline', 'hybrid']),
  location_detail: z.string().optional(),
  max_members: z.string().optional(),
  required_skills: z.string().optional(),
  tags: z.string().optional(),
  is_recruiting: z.boolean().optional(),
});

type ProjectFormData = z.infer<typeof projectFormSchema>;

const categoryLabels: Record<ProjectCategory, string> = {
  asobi: '🔍 あそびPJ',
  asoto: '🌱 あそとPJ',
};

export default function ProjectsPage() {
  const { user } = useAuthStore();
  const [projects, setProjects] = useState<Project[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [isCreating, setIsCreating] = useState(false);
  const [showCreateForm, setShowCreateForm] = useState(false);

  const {
    register,
    handleSubmit,
    reset,
    formState: { errors },
  } = useForm<ProjectFormData>({
    resolver: zodResolver(projectFormSchema),
    defaultValues: {
      category: 'asobi',
      location_type: 'online',
      is_recruiting: true,
    },
  });

  useEffect(() => {
    const loadProjects = async () => {
      setIsLoading(true);
      setError(null);
      try {
        const data = await projectsApi.fetchProjects();
        setProjects(data);
      } catch (err: any) {
        const message = err.response?.data?.detail || 'プロジェクトの取得に失敗しました';
        setError(message);
      } finally {
        setIsLoading(false);
      }
    };

    loadProjects();
  }, []);

  const onSubmit = async (formData: ProjectFormData) => {
    setIsCreating(true);
    setError(null);
    try {
      const requiredSkills = formData.required_skills
        ? formData.required_skills.split(',').map((s) => s.trim()).filter(Boolean)
        : [];

      const tags = formData.tags
        ? formData.tags.split(',').map((tag) => tag.trim()).filter(Boolean)
        : [];

      const newProject = await projectsApi.createProject({
        title: formData.title,
        description: formData.description || undefined,
        category: formData.category,
        start_date: new Date(formData.start_date).toISOString(),
        end_date: formData.end_date ? new Date(formData.end_date).toISOString() : undefined,
        frequency: formData.frequency || undefined,
        location_type: formData.location_type,
        location_detail: formData.location_detail || undefined,
        max_members: formData.max_members ? parseInt(formData.max_members) : undefined,
        required_skills: requiredSkills,
        tags,
        is_recruiting: formData.is_recruiting,
      });
      setProjects((prev) => [newProject, ...prev]);
      reset();
      setShowCreateForm(false);
    } catch (err: any) {
      const message = err.response?.data?.detail || 'プロジェクトの作成に失敗しました';
      setError(message);
    } finally {
      setIsCreating(false);
    }
  };

  const handleJoinProject = async (projectId: string) => {
    setError(null);
    try {
      await projectsApi.joinProject(projectId);
      const data = await projectsApi.fetchProjects();
      setProjects(data);
    } catch (err: any) {
      const message = err.response?.data?.detail || 'プロジェクト参加に失敗しました';
      setError(message);
    }
  };

  const myProjects = projects.filter((p) => p.owner_id === user?.id);
  const recruitingProjects = projects.filter((p) => p.is_recruiting && p.owner_id !== user?.id);

  return (
    <div className="space-y-4 sm:space-y-6">
      <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
        <div>
          <h1 className="text-2xl font-bold text-asoto-text-main sm:text-3xl">プロジェクト</h1>
          <p className="text-xs text-asoto-text-muted sm:text-sm">興味のあるプロジェクトに参加して、共創を体験しましょう。</p>
        </div>
        <Button
          className="w-full rounded-full bg-asoto-primary text-white sm:w-auto"
          onClick={() => setShowCreateForm(!showCreateForm)}
        >
          {showCreateForm ? 'キャンセル' : 'プロジェクトを作成'}
        </Button>
      </div>

      {error && (
        <div className="rounded-md border border-destructive/20 bg-destructive/10 p-3 text-sm text-destructive">
          {error}
        </div>
      )}

      {showCreateForm && (
        <Card className="bg-asoto-bg-surface border-asoto-border">
          <CardHeader>
            <CardTitle>新しいプロジェクト</CardTitle>
            <CardDescription>継続的な活動を立ち上げましょう</CardDescription>
          </CardHeader>
          <CardContent>
            <form className="space-y-4" onSubmit={handleSubmit(onSubmit)}>
              <div className="space-y-2">
                <Label htmlFor="title">タイトル</Label>
                <Input
                  id="title"
                  placeholder="例：地域農業支援プロジェクト"
                  {...register('title')}
                  disabled={isCreating}
                />
                {errors.title && <p className="text-sm text-destructive">{errors.title.message}</p>}
              </div>

              <div className="space-y-2">
                <Label htmlFor="category">カテゴリ</Label>
                <select
                  id="category"
                  className="w-full rounded-md border border-asoto-border bg-asoto-bg-main p-2 text-sm text-asoto-text-main"
                  {...register('category')}
                  disabled={isCreating}
                >
                  <option value="asobi">🔍 あそびプロジェクト（軽めの取り組み）</option>
                  <option value="asoto">🌱 あそとプロジェクト（本格的な活動）</option>
                </select>
              </div>

              <div className="space-y-2">
                <Label htmlFor="description">説明</Label>
                <textarea
                  id="description"
                  className="min-h-[100px] w-full rounded-md border border-asoto-border bg-transparent p-3 text-sm text-asoto-text-main focus:outline-none focus:ring-2 focus:ring-asoto-primary/50"
                  placeholder="プロジェクトの目的や内容を記入してください..."
                  {...register('description')}
                  disabled={isCreating}
                />
              </div>

              <div className="grid gap-4 sm:grid-cols-2">
                <div className="space-y-2">
                  <Label htmlFor="start_date">開始日</Label>
                  <Input
                    id="start_date"
                    type="date"
                    {...register('start_date')}
                    disabled={isCreating}
                  />
                  {errors.start_date && <p className="text-sm text-destructive">{errors.start_date.message}</p>}
                </div>

                <div className="space-y-2">
                  <Label htmlFor="end_date">終了日（任意）</Label>
                  <Input
                    id="end_date"
                    type="date"
                    {...register('end_date')}
                    disabled={isCreating}
                  />
                </div>
              </div>

              <div className="grid gap-4 sm:grid-cols-2">
                <div className="space-y-2">
                  <Label htmlFor="frequency">活動頻度</Label>
                  <Input
                    id="frequency"
                    placeholder="例：週1回、月2回"
                    {...register('frequency')}
                    disabled={isCreating}
                  />
                </div>

                <div className="space-y-2">
                  <Label htmlFor="location_type">活動形式</Label>
                  <select
                    id="location_type"
                    className="w-full rounded-md border border-asoto-border bg-asoto-bg-main p-2 text-sm text-asoto-text-main"
                    {...register('location_type')}
                    disabled={isCreating}
                  >
                    <option value="online">オンライン</option>
                    <option value="offline">オフライン</option>
                    <option value="hybrid">ハイブリッド</option>
                  </select>
                </div>
              </div>

              <div className="space-y-2">
                <Label htmlFor="location_detail">場所の詳細</Label>
                <Input
                  id="location_detail"
                  placeholder="例：Discord、東京都内など"
                  {...register('location_detail')}
                  disabled={isCreating}
                />
              </div>

              <div className="grid gap-4 sm:grid-cols-2">
                <div className="space-y-2">
                  <Label htmlFor="max_members">最大メンバー数（任意）</Label>
                  <Input
                    id="max_members"
                    type="number"
                    placeholder="例：10"
                    {...register('max_members')}
                    disabled={isCreating}
                  />
                </div>

                <div className="space-y-2">
                  <Label htmlFor="is_recruiting">メンバー募集</Label>
                  <div className="flex items-center gap-2 pt-2">
                    <input
                      id="is_recruiting"
                      type="checkbox"
                      {...register('is_recruiting')}
                      disabled={isCreating}
                      className="h-4 w-4 rounded border-asoto-border"
                    />
                    <label htmlFor="is_recruiting" className="text-sm text-asoto-text-main">
                      メンバーを募集する
                    </label>
                  </div>
                </div>
              </div>

              <div className="space-y-2">
                <Label htmlFor="required_skills">求めるスキル（カンマ区切り）</Label>
                <Input
                  id="required_skills"
                  placeholder="例：農業経験, デザイン, プログラミング"
                  {...register('required_skills')}
                  disabled={isCreating}
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="tags">タグ（カンマ区切り）</Label>
                <Input
                  id="tags"
                  placeholder="例：農業, 地域活性化, SDGs"
                  {...register('tags')}
                  disabled={isCreating}
                />
              </div>

              <Button type="submit" className="w-full" disabled={isCreating}>
                {isCreating ? '作成中...' : 'プロジェクトを作成'}
              </Button>
            </form>
          </CardContent>
        </Card>
      )}

      <div className="grid gap-4 sm:gap-6 lg:grid-cols-2">
        <Card className="bg-asoto-bg-surface border-asoto-border">
          <CardHeader>
            <CardTitle>マイプロジェクト</CardTitle>
            <CardDescription>あなたが主催・参加しているプロジェクト</CardDescription>
          </CardHeader>
          <CardContent>
            {isLoading ? (
              <p className="text-sm text-asoto-text-muted">読み込み中...</p>
            ) : myProjects.length === 0 ? (
              <p className="text-sm text-asoto-text-muted">まだプロジェクトを作成していません。</p>
            ) : (
              <div className="space-y-4">
                {myProjects.map((project) => (
                  <ProjectCard key={project.id} project={project} isOwner={true} />
                ))}
              </div>
            )}
          </CardContent>
        </Card>

        <Card className="bg-asoto-bg-surface border-asoto-border">
          <CardHeader>
            <CardTitle>募集中のプロジェクト</CardTitle>
            <CardDescription>参加できるプロジェクト</CardDescription>
          </CardHeader>
          <CardContent>
            {isLoading ? (
              <p className="text-sm text-asoto-text-muted">読み込み中...</p>
            ) : recruitingProjects.length === 0 ? (
              <p className="text-sm text-asoto-text-muted">募集中のプロジェクトはありません。</p>
            ) : (
              <div className="space-y-4">
                {recruitingProjects.map((project) => (
                  <ProjectCard
                    key={project.id}
                    project={project}
                    isOwner={false}
                    onJoin={() => handleJoinProject(project.id)}
                  />
                ))}
              </div>
            )}
          </CardContent>
        </Card>
      </div>
    </div>
  );
}

interface ProjectCardProps {
  project: Project;
  isOwner: boolean;
  onJoin?: () => void;
}

function ProjectCard({ project, isOwner, onJoin }: ProjectCardProps) {
  return (
    <div className="rounded-lg border border-asoto-border p-4">
      <div className="flex items-start justify-between gap-4">
        <div className="flex-1">
          <div className="flex items-center gap-2">
            <span className="text-lg">{project.category === 'asobi' ? '🔍' : '🌱'}</span>
            <h3 className="text-lg font-semibold text-asoto-text-main">{project.title}</h3>
          </div>
          {project.description && (
            <p className="mt-2 text-sm text-asoto-text-muted line-clamp-2">{project.description}</p>
          )}
        </div>
        <span
          className={`rounded-full px-3 py-1 text-xs font-medium ${
            project.status === 'active'
              ? 'bg-green-50 text-green-600'
              : project.status === 'planning'
                ? 'bg-blue-50 text-blue-600'
                : 'bg-gray-50 text-gray-600'
          }`}
        >
          {project.status === 'active' ? '進行中' : project.status === 'planning' ? '企画中' : project.status}
        </span>
      </div>

      <div className="mt-3 space-y-2 text-xs text-asoto-text-muted">
        <div className="flex items-center gap-2">
          <Calendar className="h-4 w-4" />
          <span>開始: {formatDate(project.start_date)}</span>
          {project.frequency && <span>• {project.frequency}</span>}
        </div>
        {project.max_members && (
          <div className="flex items-center gap-2">
            <Users className="h-4 w-4" />
            <span>最大: {project.max_members}名</span>
          </div>
        )}
        {project.location_detail && (
          <div className="flex items-center gap-2">
            <Folder className="h-4 w-4" />
            <span className="line-clamp-1">{project.location_detail}</span>
          </div>
        )}
      </div>

      {project.required_skills && project.required_skills.length > 0 && (
        <div className="mt-3 flex flex-wrap gap-2">
          {project.required_skills.map((skill, idx) => (
            <span
              key={idx}
              className="rounded-full bg-asoto-primary/10 px-3 py-1 text-xs text-asoto-primary"
            >
              {skill}
            </span>
          ))}
        </div>
      )}

      {project.tags && project.tags.length > 0 && (
        <div className="mt-3 flex flex-wrap gap-2">
          {project.tags.map((tag, idx) => (
            <span
              key={idx}
              className="rounded-full bg-asoto-bg-main px-3 py-1 text-xs text-asoto-text-muted"
            >
              #{tag}
            </span>
          ))}
        </div>
      )}

      {!isOwner && project.is_recruiting && (
        <div className="mt-4">
          <Button
            variant="outline"
            size="sm"
            className="w-full sm:w-auto"
            onClick={onJoin}
          >
            参加リクエスト
          </Button>
        </div>
      )}
    </div>
  );
}

function formatDate(value?: string | null) {
  if (!value) return '-';
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return '-';
  return date.toLocaleDateString('ja-JP', { year: 'numeric', month: 'short', day: 'numeric' });
}
