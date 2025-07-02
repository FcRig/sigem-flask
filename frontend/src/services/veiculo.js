import api from './api'

export function consultarPlaca(payload) {
  return api.post('/api/veiculo/placa', payload)
}
