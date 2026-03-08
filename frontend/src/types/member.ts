export type EventRole = 'team_leader' | 'finance_manager' | 'manager'

export interface EventMember {
  id: number
  eventId: number
  userId: number
  name: string
  email: string
  role: EventRole
}