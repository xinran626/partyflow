import { computed, ref } from 'vue'
import { defineStore } from 'pinia'
import { apiRequest } from '@/api/client'
import type {
  AuthResponse,
  LoginPayload,
  RegisterPayload,
  User,
} from '@/types/auth'

export const useAuthStore = defineStore('auth', () => {
  const user = ref<User | null>(null)
  const token = ref<string | null>(localStorage.getItem('token'))

  const isAuthenticated = computed(() => !!token.value)

  function setAuth(newToken: string, newUser: User) {
    token.value = newToken
    user.value = newUser
    localStorage.setItem('token', newToken)
  }

  function logout() {
    token.value = null
    user.value = null
    localStorage.removeItem('token')
  }

  async function register(payload: RegisterPayload) {
    const data = await apiRequest<AuthResponse>('/auth/register', {
      method: 'POST',
      body: JSON.stringify(payload),
    })

    setAuth(data.token, data.user)
  }

  async function login(payload: LoginPayload) {
    const data = await apiRequest<AuthResponse>('/auth/login', {
      method: 'POST',
      body: JSON.stringify(payload),
    })

    setAuth(data.token, data.user)
  }

  async function fetchMe() {
    if (!token.value) return

    const data = await apiRequest<{ user: User }>('/auth/me', {
      method: 'GET',
    })

    user.value = data.user
  }

  return {
    user,
    token,
    isAuthenticated,
    login,
    register,
    fetchMe,
    logout,
  }
})