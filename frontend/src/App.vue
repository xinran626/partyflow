<script setup lang="ts">
import { useRoute } from 'vue-router'
import {
  Calendar,
  DataAnalysis,
  Document,
  House,
} from '@element-plus/icons-vue'
import logo from '@/assets/logo.svg'

const route = useRoute()
</script>

<template>
  <el-container class="layout-container">
    <el-aside width="220px" class="sidebar">
      <div class="logo">
        <img :src="logo" alt="PartyFlow logo" />
        
      </div>

      <el-menu
        router
        :default-active="route.path"
        class="menu"
      >
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
      <el-header class="header">PartyFlow Admin</el-header>
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
  height: 72px;
  display: flex;
  align-items: center;
  padding: 16px 20px;
  box-sizing: border-box;
}


.menu {
  border-right: none;
}

.header {
  display: flex;
  align-items: center;
  font-size: 18px;
  font-weight: 600;
  border-bottom: 1px solid #eaeaea;
  background: #fff;
}

.main {
  background: #f7f8fa;
}
</style>