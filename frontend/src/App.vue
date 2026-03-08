<script setup lang="ts">
import { computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import logo from '@/assets/logo.svg'
import {
  Calendar,
  DataAnalysis,
  Document,
  House,
  SwitchButton,
} from '@element-plus/icons-vue'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()

const isAuthPage = computed(() => {
  return route.path === '/login' || route.path === '/register'
})

function handleLogout() {
  authStore.logout()
  router.push('/login')
}

onMounted(() => {
  if (authStore.token && !authStore.user) {
    authStore.fetchMe().catch(() => {
      authStore.logout()
      router.push('/login')
    })
  }
})
</script>

<template>
  <router-view v-if="isAuthPage" />

  <el-container v-else class="layout-container">
    <el-aside width="220px" class="sidebar">
      <div class="logo">
        <img :src="logo" alt="PartyFlow logo" class="logo-image" />
      </div>

      <el-menu router :default-active="route.path" class="menu">
        <el-menu-item index="/dashboard">
          <el-icon><House /></el-icon>
          <span>Dashboard</span>
        </el-menu-item>

        <el-menu-item index="/events">
          <el-icon><Calendar /></el-icon>
          <span>Events</span>
        </el-menu-item>

        <el-menu-item index="/finance">
          <el-icon><Document /></el-icon>
          <span>Finance</span>
        </el-menu-item>

        <el-menu-item index="/reports">
          <el-icon><DataAnalysis /></el-icon>
          <span>Reports</span>
        </el-menu-item>
      </el-menu>
    </el-aside>

    <el-container>
      <el-header class="header">
        <span>PartyFlow Admin</span>

        <div class="header-right">
          <span v-if="authStore.user">{{ authStore.user.name }}</span>

          <el-button text @click="handleLogout">
            <el-icon><SwitchButton /></el-icon>
            Logout
          </el-button>
        </div>
      </el-header>

      <el-main class="main">
        <router-view />
      </el-main>
    </el-container>
  </el-container>
</template>

<style scoped>
.layout-container {
  height: 100vh;
}

.sidebar {
  background: #ffffff;
  border-right: 1px solid #eaeaea;
}

.logo {
  height: 76px;
  display: flex;
  align-items: center;
  padding: 16px 20px;
  box-sizing: border-box;
  border-bottom: 1px solid #eaeaea;
}

.logo-image {
  height: 38px;
  width: auto;
  display: block;
}

.menu {
  border-right: none;
}

.header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-size: 18px;
  font-weight: 600;
  border-bottom: 1px solid #eaeaea;
  background: #fff;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 14px;
  font-weight: 500;
}

.main {
  background: #f7f8fa;
}
</style>