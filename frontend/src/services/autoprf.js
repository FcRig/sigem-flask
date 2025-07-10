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

export function solicitarCancelamento(payload) {
  return api.post('/api/autoprf/solicitacao/cancelamento', payload)
}

export function obterHistorico(idProcesso) {
  return api.get(`/api/autoprf/historico/${idProcesso}`)
}
