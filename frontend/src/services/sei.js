import api from './api'

export function seiLogin(payload) {
  return api.post('/api/sei/login', payload)
}

export function obterTipos(payload) {
  return api.post('/api/sei/tipos', payload)
}

export function obterUnidades() {
  return api.post('/api/sei/unidades')
}

export function criarProcesso(payload) {
  return api.post('/api/sei/processos', payload)
}
