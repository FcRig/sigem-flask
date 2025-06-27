import api from './api'

export function registerUser(payload) {
  return api.post('/api/auth/register', payload)
}

export function loginUser(payload) {
  return api.post('/api/auth/login', payload)
}

export function fetchCurrentUser() {
  return api.get('/api/auth/me')
}
