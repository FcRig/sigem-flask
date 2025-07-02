import { computed } from 'vue'

export function useVeiculoFormatter(result) {
  const tipoDocumentoProprietario = computed(() => {
    const val = result.value?.descricaoTipoDocumentoProprietario || result.value?.tipo_documento
    if (!val) return val
    if (/cnpj/i.test(val) || val === 'PJ') return 'CNPJ'
    if (/cpf/i.test(val) || val === 'PF') return 'CPF'
    return val
  })

  const situacaoVeiculo = computed(() => {
    const val = result.value?.situacaoVeiculo
    if (val === 'EM_CIRCULACAO') return 'EM CIRCULAÇÃO'
    return val
  })

  function formatRestricao(value) {
    if (value === 'ALIENCAO FIDUCIARIA') return 'ALIENÇÃO FIDUCIÁRIA'
    if (value === 'SEM RESTRICAO') return 'SEM RESTRIÇÃO'
    return value
  }

  const restricao1 = computed(() => formatRestricao(result.value?.restricao1))
  const restricao2 = computed(() => formatRestricao(result.value?.restricao2))
  const restricao3 = computed(() => formatRestricao(result.value?.restricao3))
  const restricao4 = computed(() => formatRestricao(result.value?.restricao4))

  return {
    tipoDocumentoProprietario,
    situacaoVeiculo,
    restricao1,
    restricao2,
    restricao3,
    restricao4,
  }
}
