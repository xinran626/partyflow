export interface Event {
    id: number
    name: string
    date?: string | null
    location?: string | null
    createdBy: number
    createdAt: string
  }
  
  export interface CreateEventPayload {
    name: string
    date: string
    location: string
  }