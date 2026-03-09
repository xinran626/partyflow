<script setup lang="ts">
import { reactive, watch } from 'vue'

interface EventFormData {
  name: string
  date: string
  location: string
}

const props = defineProps<{
  modelValue: boolean
  title: string
  loading?: boolean
  initialData?: Partial<EventFormData>
  submitText?: string
}>()

const emit = defineEmits<{
  'update:modelValue': [value: boolean]
  submit: [payload: EventFormData]
}>()

const form = reactive<EventFormData>({
  name: '',
  date: '',
  location: '',
})

watch(
  () => props.modelValue,
  (open) => {
    if (open) {
      form.name = props.initialData?.name ?? ''
      form.date = props.initialData?.date ?? ''
      form.location = props.initialData?.location ?? ''
    }
  },
  { immediate: true }
)

function handleClose() {
  emit('update:modelValue', false)
}

function handleSubmit() {
  emit('submit', {
    name: form.name,
    date: form.date,
    location: form.location,
  })
}
</script>

<template>
  <el-dialog
    :model-value="modelValue"
    :title="title"
    width="480px"
    @close="handleClose"
  >
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
          placeholder="Select a date"
          style="width: 100%"
        />
      </el-form-item>

      <el-form-item label="Location">
        <el-input v-model="form.location" placeholder="e.g. Sydney CBD" />
      </el-form-item>
    </el-form>

    <template #footer>
      <el-button @click="handleClose">Cancel</el-button>
      <el-button type="primary" :loading="loading" @click="handleSubmit">
        {{ submitText || 'Save' }}
      </el-button>
    </template>
  </el-dialog>
</template>