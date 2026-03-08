export interface User {
    id: number
    name: string
    email: string
    systemRole: 'user' | 'super_admin'
  }
  
  export interface LoginPayload {
    email: string
    password: string
  }
  
  export interface RegisterPayload {
    name: string
    email: string
    password: string
  }