import { computed } from 'vue'

export function useVeiculoFormatter(result) {
  const tipoDocumentoProprietario = computed(() => {
    const val = result.value?.descricaoTipoDocumentoProprietario || result.value?.tipo_documento
    if (!val) return val
    if (/cnpj/i.test(val) || val === 'PJ') return 'CNPJ'
    if (/cpf/i.test(val) || val === 'PF') return 'CPF'
    return val
  })
  
  function formatCpf(cpf) {
    const digits = (cpf || '').replace(/\D/g, '')
    if (digits.length === 11)
      return digits.replace(/(\d{3})(\d{3})(\d{3})(\d{2})/, '$1.$2.$3-$4')
    return cpf
  }
  
  function formatCnpj(cnpj) {
    const digits = (cnpj || '').replace(/\D/g, '')
    if (digits.length === 14)
      return digits.replace(/(\d{2})(\d{3})(\d{3})(\d{4})(\d{2})/, '$1.$2.$3/$4-$5')
    return cnpj
  }

  const documentoProprietario = computed(() => {
    const doc = result.value?.documentoProprietario
    if (!doc) return doc
    if (tipoDocumentoProprietario.value === 'CPF') return formatCpf(doc)
    if (tipoDocumentoProprietario.value === 'CNPJ') return formatCnpj(doc)
    return doc
  })

  const situacaoVeiculo = computed(() => {
    const val = result.value?.situacaoVeiculo
    if (val === 'EM_CIRCULACAO') return 'EM CIRCULAÇÃO'
    return val
  })

  function formatRestricao(value) {
    if (value === 'ALIENACAO FIDUCIARIA') return 'ALIENAÇÃO FIDUCIÁRIA'
    if (value === 'SEM RESTRICAO') return 'SEM RESTRIÇÃO'
    return value
  }

  const restricao1 = computed(() => formatRestricao(result.value?.restricao1))
  const restricao2 = computed(() => formatRestricao(result.value?.restricao2))
  const restricao3 = computed(() => formatRestricao(result.value?.restricao3))
  const restricao4 = computed(() => formatRestricao(result.value?.restricao4))

  return {
    tipoDocumentoProprietario,
    documentoProprietario,
    situacaoVeiculo,
    restricao1,
    restricao2,
    restricao3,
    restricao4,
  }
}
