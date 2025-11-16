import api from './api'
import { LoginRequest, RegisterRequest, TokenResponse, User } from '@/types/user'

export const authApi = {
  // ユーザー登録
  register: async (data: RegisterRequest): Promise<User> => {
    const response = await api.post<User>('/auth/register', data)
    return response.data
  },

  // ログイン
  login: async (data: LoginRequest): Promise<TokenResponse> => {
    const response = await api.post<TokenResponse>('/auth/login', data)
    const { access_token } = response.data

    // トークンをローカルストレージに保存
    localStorage.setItem('access_token', access_token)

    return response.data
  },

  // ログアウト
  logout: () => {
    localStorage.removeItem('access_token')
  },

  // 現在のユーザー情報を取得
  getCurrentUser: async (): Promise<User> => {
    const response = await api.get<User>('/auth/me')
    return response.data
  },

  // 認証状態をチェック
  isAuthenticated: (): boolean => {
    return !!localStorage.getItem('access_token')
  },
}
