<script setup lang="ts">
import { onMounted, reactive, ref } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { createEvent, getEvents, updateEvent, deleteEvent } from '@/api/events'
import type { Event } from '@/types/event'
import EventTable from '@/components/events/EventTable.vue'
import EventFormDialog from '@/components/events/EventFormDialog.vue'

const events = ref<Event[]>([])
const loading = ref(false)
const submitting = ref(false)
const errorMessage = ref('')

const createDialogVisible = ref(false)
const editDialogVisible = ref(false)

const currentEvent = reactive({
  id: 0,
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
  createDialogVisible.value = true
}

function openEditDialog(event: Event) {
  currentEvent.id = event.id
  currentEvent.name = event.name
  currentEvent.date = event.date ?? ''
  currentEvent.location = event.location ?? ''
  editDialogVisible.value = true
}

async function handleCreateEvent(payload: {
  name: string
  date: string
  location: string
}) {
  if (!payload.name.trim()) {
    errorMessage.value = 'Event name is required.'
    return
  }

  submitting.value = true
  errorMessage.value = ''

  try {
    await createEvent(payload)
    createDialogVisible.value = false
    await fetchEvents()
  } catch (error) {
    errorMessage.value =
      error instanceof Error ? error.message : 'Failed to create event.'
  } finally {
    submitting.value = false
  }
}

async function handleUpdateEvent(payload: {
  name: string
  date: string
  location: string
}) {
  if (!payload.name.trim()) {
    errorMessage.value = 'Event name is required.'
    return
  }

  submitting.value = true
  errorMessage.value = ''

  try {
    await updateEvent(currentEvent.id, payload)
    editDialogVisible.value = false
    await fetchEvents()
  } catch (error) {
    errorMessage.value =
      error instanceof Error ? error.message : 'Failed to update event.'
  } finally {
    submitting.value = false
  }
}

async function handleDeleteEvent(event: Event) {
  try {
    await ElMessageBox.confirm(
      `Are you sure you want to delete "${event.name}"? This action cannot be undone.`,
      'Delete Event',
      {
        confirmButtonText: 'Delete',
        cancelButtonText: 'Cancel',
        type: 'warning',
      }
    )

    await deleteEvent(event.id)
    ElMessage.success('Event deleted successfully.')
    await fetchEvents()
  } catch (error) {
    if (error === 'cancel' || error === 'close') return

    errorMessage.value =
      error instanceof Error ? error.message : 'Failed to delete event.'
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
      v-if="errorMessage"
      :title="errorMessage"
      type="error"
      show-icon
      class="page-alert"
    />

    <EventTable
      :events="events"
      :loading="loading"
      @edit="openEditDialog"
      @delete="handleDeleteEvent"
    />

    <EventFormDialog
      v-model="createDialogVisible"
      title="Create Event"
      submit-text="Create"
      :loading="submitting"
      @submit="handleCreateEvent"
    />

    <EventFormDialog
      v-model="editDialogVisible"
      title="Edit Event"
      submit-text="Save"
      :loading="submitting"
      :initial-data="currentEvent"
      @submit="handleUpdateEvent"
    />
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
</style>