import { computed, ref } from 'vue'
import { defineStore } from 'pinia'
import type { LoginPayload, RegisterPayload, User } from '@/types/auth'

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

  async function login(payload: LoginPayload) {
    // 这里先用 mock，后面再替换成真实 API
    if (!payload.email || !payload.password) {
      throw new Error('Email and password are required.')
    }

    const mockUser: User = {
      id: 1,
      name: 'Eliza',
      email: payload.email,
      systemRole: 'user',
    }

    setAuth('mock-token', mockUser)
  }

  async function register(payload: RegisterPayload) {
    if (!payload.name || !payload.email || !payload.password) {
      throw new Error('All fields are required.')
    }

    const mockUser: User = {
      id: 1,
      name: payload.name,
      email: payload.email,
      systemRole: 'user',
    }

    setAuth('mock-token', mockUser)
  }

  return {
    user,
    token,
    isAuthenticated,
    login,
    register,
    logout,
  }
})