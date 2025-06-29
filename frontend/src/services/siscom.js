import api from './api'

export function pesquisarAi(payload) {
  return api.post('/api/siscom/pesquisar_ai', payload)
}
