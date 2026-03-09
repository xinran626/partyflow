<script setup lang="ts">
import { computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import logo from '@/assets/logo.svg'
import {
  House,
  Calendar,
  Message,
  Setting,
  SwitchButton
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
    <el-aside width="210px" class="sidebar">
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

        <el-menu-item index="/invitations">
          <el-icon><Message /></el-icon>
          <span>Invitations</span>
        </el-menu-item>

        <el-menu-item index="/settings">
          <el-icon><Setting /></el-icon>
          <span>Settings</span>
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
  background: #f6f7fb;
}

.sidebar {
  background: #ffffff;
  border-right: 1px solid #eceef5;
  box-shadow: 0 0 0 1px rgba(0, 0, 0, 0.01);
}

.logo {
  height: 63px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-bottom: 1px solid #f1f3f8;
}

.logo img {
  height: 48px;
}

.menu {
  border-right: none;
  padding: 14px 12px;
}

:deep(.el-menu) {
  border-right: none;
}

:deep(.el-menu-item) {
  height: 44px;
  line-height: 44px;
  border-radius: 12px;
  margin-bottom: 8px;
  font-weight: 500;
  color: #374151;
}

:deep(.el-menu-item:hover) {
  background: #fff4eb;
  color: #ff7a1a;
}

:deep(.el-menu-item.is-active) {
  background: #fff1e6;
  color: #ff7a1a;
}

:deep(.el-menu-item .el-icon) {
  margin-right: 10px;
}

.header {
  height: 64px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 24px;
  font-size: 22px;
  font-weight: 700;
  border-bottom: 1px solid #eceef5;
  background: rgba(255, 255, 255, 0.92);
  backdrop-filter: blur(10px);
}

.header-right {
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 14px;
  font-weight: 500;
}

.user-chip {
  padding: 6px 12px;
  background: #f8fafc;
  border: 1px solid #eceef5;
  border-radius: 999px;
  color: #374151;
}

.main {
  background: #f6f7fb;
  padding: 24px;
}
</style>