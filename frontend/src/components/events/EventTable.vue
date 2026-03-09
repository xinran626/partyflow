<script setup lang="ts">
import type { Event } from '@/types/event'

defineProps<{
  events: Event[]
  loading: boolean
}>()

const emit = defineEmits<{
  edit: [event: Event]
  delete: [event: Event]
}>()
</script>

<template>
  <el-card class="events-card">
    <el-table :data="events" v-loading="loading" empty-text="No events yet">
      <el-table-column prop="name" label="Event Name" min-width="220" />

      <el-table-column label="Date" min-width="140">
        <template #default="{ row }">
          {{ row.date || '-' }}
        </template>
      </el-table-column>

      <el-table-column label="Location" min-width="180">
        <template #default="{ row }">
          {{ row.location || '-' }}
        </template>
      </el-table-column>

      <el-table-column label="Created At" min-width="200">
        <template #default="{ row }">
            {{ new Date(row.createdAt).toLocaleString('en-AU', {
                timeZone: 'Australia/Sydney',
                year: 'numeric',
                month: 'short',
                day: 'numeric',
                hour: '2-digit',
                minute: '2-digit'
                }) }}
        </template>
      </el-table-column>

      <el-table-column label="Action" width="180">
        <template #default="{ row }">
          <div class="action-buttons">
            <button class="action-link edit" @click="emit('edit', row)">
              Edit
            </button>

            <button class="action-link delete" @click="emit('delete', row)">
            Delete
            </button>
          </div>
        </template>
      </el-table-column>
    </el-table>
  </el-card>
</template>

<style scoped>
.events-card {
  border-radius: 16px;
}

.action-buttons {
  display: flex;
  align-items: center;
  gap: 16px;
}

.action-link {
  background: none;
  border: none;
  padding: 0;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
}

.action-link.edit {
  color: #ff7a1a;
}

.action-link.delete {
  color: #ef4444;
}

.action-link:hover {
  text-decoration: underline;
}
</style>