import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import * as authApi from '@/lib/api/auth';

export interface User {
  id: string;
  full_name: string | null;
  email: string;
  is_active: boolean;
  created_at: string;
}

interface AuthState {
  user: User | null;
  isLoading: boolean;
  error: string | null;

  // アクション
  login: (email: string, password: string) => Promise<void>;
  register: (full_name: string, email: string, password: string) => Promise<void>;
  logout: () => void;
  fetchCurrentUser: () => Promise<void>;
  clearError: () => void;
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set) => ({
      user: null,
      isLoading: false,
      error: null,

      /**
       * ログイン
       */
      login: async (email: string, password: string) => {
        set({ isLoading: true, error: null });
        try {
          await authApi.login({ email, password });
          // ログイン成功後、ユーザー情報を取得
          const user = await authApi.getCurrentUser();
          set({ user, isLoading: false });
        } catch (error: any) {
          let errorMessage = 'ログインに失敗しました';

          if (error.response?.data?.detail) {
            // FastAPIのエラーレスポンス処理
            const detail = error.response.data.detail;
            if (typeof detail === 'string') {
              errorMessage = detail;
            } else if (Array.isArray(detail)) {
              // バリデーションエラーの場合（配列）
              errorMessage = detail.map((err: any) => err.msg).join(', ');
            }
          }

          set({ error: errorMessage, isLoading: false });
          throw error;
        }
      },

      /**
       * ユーザー登録
       */
      register: async (full_name: string, email: string, password: string) => {
        set({ isLoading: true, error: null });
        try {
          await authApi.register({ full_name, email, password });
          // 登録後、自動的にログイン
          await authApi.login({ email, password });
          const user = await authApi.getCurrentUser();
          set({ user, isLoading: false });
        } catch (error: any) {
          let errorMessage = '登録に失敗しました';

          if (error.response?.data?.detail) {
            // FastAPIのエラーレスポンス処理
            const detail = error.response.data.detail;
            if (typeof detail === 'string') {
              errorMessage = detail;
            } else if (Array.isArray(detail)) {
              // バリデーションエラーの場合（配列）
              errorMessage = detail.map((err: any) => err.msg).join(', ');
            }
          }

          set({ error: errorMessage, isLoading: false });
          throw error;
        }
      },

      /**
       * ログアウト
       */
      logout: () => {
        authApi.logout();
        set({ user: null, error: null });
      },

      /**
       * 現在のユーザー情報を取得（認証状態の復元用）
       */
      fetchCurrentUser: async () => {
        if (!authApi.isAuthenticated()) {
          set({ user: null });
          return;
        }

        set({ isLoading: true });
        try {
          const user = await authApi.getCurrentUser();
          set({ user, isLoading: false });
        } catch (error) {
          // トークンが無効な場合はログアウト状態にする
          set({ user: null, isLoading: false });
        }
      },

      /**
       * エラーをクリア
       */
      clearError: () => set({ error: null }),
    }),
    {
      name: 'auth-storage',
      partialize: (state) => ({ user: state.user }), // userのみを永続化
    }
  )
);
