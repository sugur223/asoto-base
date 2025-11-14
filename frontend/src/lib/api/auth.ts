import { apiClient } from './client';
import Cookies from 'js-cookie';

export interface RegisterData {
  full_name: string;  // バックエンドに合わせて username → full_name
  email: string;
  password: string;
}

export interface LoginData {
  email: string;
  password: string;
}

export interface User {
  id: string;
  full_name: string | null;  // バックエンドに合わせて username → full_name
  email: string;
  is_active: boolean;
  created_at: string;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
}

/**
 * ユーザー登録
 */
export const register = async (data: RegisterData): Promise<User> => {
  const response = await apiClient.post<User>('/auth/register', data);
  return response.data;
};

/**
 * ログイン
 */
export const login = async (data: LoginData): Promise<AuthResponse> => {
  // FastAPIのOAuth2PasswordRequestFormに合わせてform-dataで送信
  const formData = new URLSearchParams();
  formData.append('username', data.email); // usernameフィールドにメールアドレスを設定
  formData.append('password', data.password);

  const response = await apiClient.post<AuthResponse>('/auth/login', formData, {
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
    },
  });

  // トークンをCookieに保存（7日間有効）
  Cookies.set('access_token', response.data.access_token, { expires: 7 });

  return response.data;
};

/**
 * ログアウト
 */
export const logout = (): void => {
  Cookies.remove('access_token');
};

/**
 * 現在のユーザー情報を取得
 */
export const getCurrentUser = async (): Promise<User> => {
  const response = await apiClient.get<User>('/auth/me');
  return response.data;
};

/**
 * 認証状態を確認（トークンの有無のみ）
 */
export const isAuthenticated = (): boolean => {
  return !!Cookies.get('access_token');
};
