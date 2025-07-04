import api from './api'

export function pesquisarAi(payload) {
  return api.post('/api/siscom/pesquisar_ai', payload)
}

export function siscomLogin(payload) {
  return api.post('/api/siscom/login', payload)
}

export function buscarHistorico(payload) {
  return api.post('/api/siscom/historico', payload)
}
