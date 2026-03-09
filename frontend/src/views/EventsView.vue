<script setup lang="ts">
import { onMounted, reactive, ref } from 'vue'
import { createEvent, getEvents } from '@/api/events'
import type { Event } from '@/types/event'

const events = ref<Event[]>([])
const loading = ref(false)
const dialogVisible = ref(false)
const submitting = ref(false)
const errorMessage = ref('')

const form = reactive({
  name: '',
  date: '',
  location: '',
})

async function fetchEvents() {
  loading.value = true
  errorMessage.value = ''

  try {
    const data = await getEvents()
    events.value = data.events
  } catch (error) {
    errorMessage.value =
      error instanceof Error ? error.message : 'Failed to load events.'
  } finally {
    loading.value = false
  }
}

function openCreateDialog() {
  form.name = ''
  form.date = ''
  form.location = ''
  errorMessage.value = ''
  dialogVisible.value = true
}

async function handleCreateEvent() {
  if (!form.name.trim()) {
    errorMessage.value = 'Event name is required.'
    return
  }

  submitting.value = true
  errorMessage.value = ''

  try {
    await createEvent({
      name: form.name,
      date: form.date,
      location: form.location,
    })

    dialogVisible.value = false
    await fetchEvents()
  } catch (error) {
    errorMessage.value =
      error instanceof Error ? error.message : 'Failed to create event.'
  } finally {
    submitting.value = false
  }
}

onMounted(() => {
  fetchEvents()
})
</script>

<template>
  <div class="events-page">
    <div class="page-header">
      <div>
        <h1 class="page-title">Events</h1>
        <p class="page-subtitle">Create and manage your events.</p>
      </div>

      <el-button type="primary" @click="openCreateDialog">
        Create Event
      </el-button>
    </div>

    <el-alert
      v-if="errorMessage && !dialogVisible"
      :title="errorMessage"
      type="error"
      show-icon
      class="page-alert"
    />

    <el-card class="events-card">
      <el-table :data="events" v-loading="loading" empty-text="No events yet">
        <el-table-column prop="name" label="Event Name" min-width="220" />
        <el-table-column prop="date" label="Date" min-width="140" />
        <el-table-column prop="location" label="Location" min-width="180" />
        <el-table-column label="Created At" min-width="200">
          <template #default="{ row }">
            {{ new Date(row.createdAt).toLocaleString() }}
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <el-dialog v-model="dialogVisible" title="Create Event" width="480px">
      <el-form label-position="top">
        <el-form-item label="Event Name">
          <el-input v-model="form.name" placeholder="e.g. Muse Anime Night" />
        </el-form-item>

        <el-form-item label="Date">
          <el-input v-model="form.date" placeholder="e.g. 2026-04-11" />
        </el-form-item>

        <el-form-item label="Location">
          <el-input v-model="form.location" placeholder="e.g. Sydney CBD" />
        </el-form-item>

        <el-alert
          v-if="errorMessage"
          :title="errorMessage"
          type="error"
          show-icon
        />
      </el-form>

      <template #footer>
        <el-button @click="dialogVisible = false">Cancel</el-button>
        <el-button type="primary" :loading="submitting" @click="handleCreateEvent">
          Create
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<style scoped>
.events-page {
  padding: 8px;
}

.page-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 20px;
}

.page-title {
  margin: 0;
  font-size: 28px;
  font-weight: 700;
}

.page-subtitle {
  margin: 6px 0 0;
  color: #6b7280;
}

.page-alert {
  margin-bottom: 16px;
}

.events-card {
  border-radius: 16px;
}
</style>