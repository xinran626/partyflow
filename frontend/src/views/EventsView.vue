<script setup lang="ts">
import { onMounted, reactive, ref } from 'vue'
import { createEvent, getEvents, updateEvent, deleteEvent } from '@/api/events'
import type { Event } from '@/types/event'

const events = ref<Event[]>([])
const loading = ref(false)

const dialogVisible = ref(false)
const editDialogVisible = ref(false)

const submitting = ref(false)
const errorMessage = ref('')

const form = reactive({
  name: '',
  date: '',
  location: '',
})

const editForm = reactive({
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
  form.name = ''
  form.date = ''
  form.location = ''
  errorMessage.value = ''
  dialogVisible.value = true
}

function openEditDialog(event: Event) {
  editForm.id = event.id
  editForm.name = event.name
  editForm.date = event.date
  editForm.location = event.location
  editDialogVisible.value = true
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

async function handleUpdateEvent() {
  submitting.value = true

  try {
    await updateEvent(editForm.id, {
      name: editForm.name,
      date: editForm.date,
      location: editForm.location,
    })

    editDialogVisible.value = false
    await fetchEvents()
  } finally {
    submitting.value = false
  }
}

async function handleDeleteEvent(eventId: number) {
  if (!confirm('Delete this event?')) return

  await deleteEvent(eventId)
  await fetchEvents()
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

        <!-- ACTION -->
        <el-table-column label="Action" width="180">
        <template #default="{ row }">
          <div class="action-buttons">
            <button class="action-link edit" @click="openEditDialog(row)">
              Edit
            </button>

            <button class="action-link delete" @click="handleDeleteEvent(row.id)">
              Delete
            </button>
          </div>
        </template>
      </el-table-column>

      </el-table>

    </el-card>

    <!-- CREATE EVENT -->

    <el-dialog v-model="dialogVisible" title="Create Event" width="480px">

      <el-form label-position="top">

        <el-form-item label="Event Name">
          <el-input v-model="form.name" placeholder="e.g. Muse Anime Night" />
        </el-form-item>

        <el-form-item label="Date">
          <el-date-picker
            v-model="form.date"
            type="date"
            format="YYYY-MM-DD"
            value-format="YYYY-MM-DD"
            style="width:100%"
          />
        </el-form-item>

        <el-form-item label="Location">
          <el-input v-model="form.location" placeholder="e.g. Sydney CBD" />
        </el-form-item>

      </el-form>

      <template #footer>

        <el-button @click="dialogVisible = false">
          Cancel
        </el-button>

        <el-button
          type="primary"
          :loading="submitting"
          @click="handleCreateEvent"
        >
          Create
        </el-button>

      </template>

    </el-dialog>

    <!-- EDIT EVENT -->

    <el-dialog v-model="editDialogVisible" title="Edit Event" width="480px">

      <el-form label-position="top">

        <el-form-item label="Event Name">
          <el-input v-model="editForm.name" />
        </el-form-item>

        <el-form-item label="Date">
          <el-date-picker
            v-model="editForm.date"
            type="date"
            format="YYYY-MM-DD"
            value-format="YYYY-MM-DD"
            style="width:100%"
          />
        </el-form-item>

        <el-form-item label="Location">
          <el-input v-model="editForm.location" />
        </el-form-item>

      </el-form>

      <template #footer>

        <el-button @click="editDialogVisible=false">
          Cancel
        </el-button>

        <el-button
          type="primary"
          :loading="submitting"
          @click="handleUpdateEvent"
        >
          Save
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