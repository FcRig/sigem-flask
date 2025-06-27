import api from './api'

export function fetchUsers() {
  return api.get('/api/auth/users')
}

export function createUser(payload) {
  return api.post('/api/auth/users', payload)
}

export function fetchUser(id) {
  return api.get(`/api/auth/users/${id}`)
}

export function updateUser(id, payload) {
  return api.put(`/api/auth/users/${id}`, payload)
}

export function deleteUser(id) {
  return api.delete(`/api/auth/users/${id}`)
}
