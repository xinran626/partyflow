<script setup lang="ts">
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import logo from '@/assets/logo.svg'

const router = useRouter()
const authStore = useAuthStore()

const form = reactive({
  email: '',
  password: '',
})

const loading = ref(false)
const errorMessage = ref('')

async function handleLogin() {
  errorMessage.value = ''
  loading.value = true

  try {
    await authStore.login(form)
    router.push('/dashboard')
  } catch (error) {
    errorMessage.value =
      error instanceof Error ? error.message : 'Login failed.'
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="auth-page">

    <div class="auth-container">

      <div class="brand">
        <img :src="logo" class="logo" />
        <p>Event planning platform</p>
      </div>

      <el-card class="auth-card">

        <h2 class="title">Login</h2>

        <el-form @submit.prevent="handleLogin">

          <el-form-item>
            <el-input
              v-model="form.email"
              placeholder="Email"
              size="large"
            />
          </el-form-item>

          <el-form-item>
            <el-input
              v-model="form.password"
              type="password"
              placeholder="Password"
              show-password
              size="large"
            />
          </el-form-item>

          <el-alert
            v-if="errorMessage"
            :title="errorMessage"
            type="error"
            show-icon
            class="error"
          />

          <el-button
            type="primary"
            size="large"
            :loading="loading"
            class="login-button"
            @click="handleLogin"
          >
            Login
          </el-button>

        </el-form>

        <div class="footer">
          Don’t have an account?
          <router-link to="/register">Register</router-link>
        </div>

      </el-card>

    </div>

  </div>
</template>

<style scoped>

.auth-page {
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;

  background: linear-gradient(
    135deg,
    #e4eaff 0%,
    rgb(248, 251, 209) 40%,
    #fbd9df 100%
  );
}

.auth-container {
  width: 420px;
}

.brand {
  text-align: center;
  margin-bottom: 24px;
  margin-top: 0px;
}

.logo {
  height: 68px;
}

.brand h1 {
  margin: 8px 0 4px;
  font-size: 26px;
}

.brand p {
  color: #888;
  font-size: 14px;
  margin-top: 0px;
}

.auth-card {
  padding: 28px;
  border-radius: 16px;

  background: rgba(255, 255, 255, 0.85);
  backdrop-filter: blur(14px);

  border: 1px solid rgba(255,255,255,0.5);

  box-shadow:
    0 15px 35px rgba(0,0,0,0.15),
    0 4px 12px rgba(0,0,0,0.08);

  transition: all 0.25s ease;
}

.auth-card:hover {
  transform: translateY(-6px);
  box-shadow:
    0 25px 50px rgba(0,0,0,0.18),
    0 10px 20px rgba(0,0,0,0.12);
}

.el-input__wrapper {
  border-radius: 10px;
}

.title {
  text-align: center;
  margin-bottom: 20px;
  margin-top: 0px;
  font-family: "Inter", sans-serif;
  font-weight: 600;
  font-size: 34px;
  letter-spacing: 0.5px;
}

.login-button {
  width: 100%;
  border-radius: 10px;

  background: linear-gradient(
    135deg,
    #4f8bd6,
    #5aa4ff
  );

  border: none;

  transition: all 0.2s ease;
}

.login-button:hover {
  transform: translateY(-1px);
  box-shadow: 0 6px 14px rgba(79,139,214,0.35);
}

.footer {
  margin-top: 18px;
  text-align: center;
  font-size: 14px;
}

.error {
  margin-bottom: 12px;
}

:deep(.el-input__wrapper) {
  border-radius: 10px;
  transition: all 0.2s ease;
}

:deep(.el-input__wrapper.is-focus) {
  box-shadow: 0 0 0 2px rgba(79,139,214,0.25);
}

</style>