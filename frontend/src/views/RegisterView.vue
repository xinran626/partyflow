<script setup lang="ts">
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const form = reactive({
  name: '',
  email: '',
  password: '',
  confirmPassword: '',
})

const loading = ref(false)
const errorMessage = ref('')

async function handleRegister() {
  errorMessage.value = ''

  if (form.password !== form.confirmPassword) {
    errorMessage.value = 'Passwords do not match.'
    return
  }

  loading.value = true

  try {
    await authStore.register({
      name: form.name,
      email: form.email,
      password: form.password,
    })
    router.push('/dashboard')
  } catch (error) {
    errorMessage.value =
      error instanceof Error ? error.message : 'Registration failed.'
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="auth-page">
    <el-card class="auth-card">
      <h1 class="auth-title">Register</h1>

      <el-form @submit.prevent="handleRegister">
        <el-form-item label="Name">
          <el-input v-model="form.name" placeholder="Enter your name" />
        </el-form-item>

        <el-form-item label="Email">
          <el-input v-model="form.email" placeholder="Enter your email" />
        </el-form-item>

        <el-form-item label="Password">
          <el-input
            v-model="form.password"
            type="password"
            placeholder="Create a password"
            show-password
          />
        </el-form-item>

        <el-form-item label="Confirm Password">
          <el-input
            v-model="form.confirmPassword"
            type="password"
            placeholder="Confirm your password"
            show-password
          />
        </el-form-item>

        <el-alert
          v-if="errorMessage"
          :title="errorMessage"
          type="error"
          show-icon
          class="mb-16"
        />

        <el-button
          type="primary"
          :loading="loading"
          class="full-width"
          @click="handleRegister"
        >
          Register
        </el-button>

        <div class="auth-footer">
          Already have an account?
          <router-link to="/login">Login</router-link>
        </div>
      </el-form>
    </el-card>
  </div>
</template>

<style scoped>
.auth-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f7f8fa;
}

.auth-card {
  width: 420px;
  padding: 12px;
}

.auth-title {
  margin-bottom: 24px;
  text-align: center;
}

.full-width {
  width: 100%;
}

.auth-footer {
  margin-top: 16px;
  text-align: center;
}

.mb-16 {
  margin-bottom: 16px;
}
</style>