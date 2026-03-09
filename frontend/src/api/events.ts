import { apiRequest } from '@/api/client'
import type { CreateEventPayload, Event } from '@/types/event'

export async function getEvents() {
  return apiRequest<{ events: Event[] }>('/events/', {
    method: 'GET',
  })
}

export async function createEvent(payload: CreateEventPayload) {
  return apiRequest<{ message: string; event: Event }>('/events/', {
    method: 'POST',
    body: JSON.stringify(payload),
  })
}

export async function updateEvent(
  id: number,
  payload: Partial<CreateEventPayload>
) {
  return apiRequest<{ message: string; event?: Event }>(`/events/${id}`, {
    method: 'PUT',
    body: JSON.stringify(payload),
  })
}

export async function deleteEvent(id: number) {
  return apiRequest<{ message: string }>(`/events/${id}`, {
    method: 'DELETE',
  })
}