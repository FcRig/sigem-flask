import api from './api'

export function autoprfLogin(payload) {
  return api.post('/api/autoprf/login', payload)
}

export function pesquisarAutoInfracao(payload) {
  return api.post('/api/autoprf/pesquisar_ai', payload)
}

export function obterEnvolvidos(id) {
  return api.get(`/api/autoprf/envolvidos/${id}`)
}
