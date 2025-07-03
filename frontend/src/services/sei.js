import api from './api'

export function seiLogin(payload) {
  return api.post('/api/sei/login', payload)
}
