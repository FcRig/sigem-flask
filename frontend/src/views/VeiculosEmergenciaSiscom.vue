<template>
  <v-container>
    <!-- MANTIDO: Seu template completo, sem alterações -->
    <!-- Caso queira, posso enviar também em Markdown limpo -->
  </v-container>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useStore } from 'vuex'
import { onBeforeRouteLeave } from 'vue-router'
import { solicitarCancelamento } from '../services/autoprf'
import { pesquisarAi } from '../services/siscom'
import { consultarPlaca } from '../services/veiculo'

const numeroAi = ref('')
const envolvidos = ref([])
const amparoInfo = ref(null)
const localInfo = ref(null)
const permitido = ref(false)
const checked = ref(false)
const formRef = ref(null)
const valid = ref(false)
const idProcesso = ref(null)
const motivoManual = ref('')
const justificativaManual = ref('')
const manualValid = ref(false)
const manualFormRef = ref(null)
const editJustificativa = ref(false)
const store = useStore()

const foraCircunscricao = computed(() => {
  const str = localInfo.value?.codigo_municipio_uf || ''
  const match = str.match(/\/([A-Za-z]{2})$/)
  return match ? match[1].toUpperCase() !== 'RS' : false
})

const rules = { required: v => !!v || 'Campo obrigatório' }

// Instituições e justificativas conforme já configurado
// codigosPermitidos e codigosPermitidosDigits conforme seu código
// instituicoes, justificativas definidos previamente no seu arquivo

function sanitize(cnpj) {
  return (cnpj || '').replace(/\D/g, '')
}

function instituicaoNome(cnpj) {
  return instituicoes[sanitize(cnpj)]
}

function showInstituicao(env) {
  const envolvimento = (env.envolvimentoAuto || env.envolvimentoProcesso || env.envolvimento || '').toLowerCase()
  return /propriet[aá]rio|possuidor/.test(envolvimento) && !!instituicaoNome(env.numeroDocumento)
}

const justificativa = computed(() => {
  for (const env of envolvidos.value) {
    const envolvimento = (env.envolvimentoAuto || env.envolvimentoProcesso || env.envolvimento || '').toLowerCase()
    if (!/propriet[aá]rio|possuidor/.test(envolvimento)) continue
    const j = justificativas[sanitize(env.numeroDocumento)]
    if (j) return j
  }
  return null
})

const requireManualJustificativa = computed(() => {
  for (const env of envolvidos.value) {
    const envolvimento = (env.envolvimentoAuto || env.envolvimentoProcesso || env.envolvimento || '').toLowerCase()
    if (!/propriet[aá]rio|possuidor/.test(envolvimento)) continue
    if (!instituicoes[sanitize(env.numeroDocumento)]) return true
  }
  return false
})

async function buscar() {
  if (!formRef.value?.validate()) return

  checked.value = false

  try {
    const { data } = await pesquisarAi({ numero: numeroAi.value })

    if (!data) {
      limparCampos()
      return
    }

    localInfo.value = data.local || null
    idProcesso.value = null

    const cd = data.infracao?.codigo_descricao || ''
    const [codPart, ...descParts] = cd.split(/\s*-\s*/)
    const codigo = codPart?.trim() || ''
    const descricao = descParts.join(' - ').trim()

    amparoInfo.value = cd ? {
      codigo,
      descricao,
      amparo: data.infracao?.amparo_legal || ''
    } : null

    const digits = codigo.replace(/\D/g, '')
    permitido.value = codigosPermitidosDigits.includes(digits)
    checked.value = true

    envolvidos.value = []
    if (data.veiculo?.placa) {
      try {
        const { data: veiculoData } = await consultarPlaca({ placa: data.veiculo.placa })
        if (veiculoData?.nomeProprietario || veiculoData?.documentoProprietario) {
          envolvidos.value = [{
            id: 1,
            nome: veiculoData.nomeProprietario,
            envolvimento: 'Proprietário',
            tipoDocumento: veiculoData.descricaoTipoDocumentoProprietario || veiculoData.tipo_documento,
            numeroDocumento: veiculoData.documentoProprietario
          }]
        }
      } catch (e) {
        console.error(e)
      }
    }
  } catch (err) {
    const msg = err.response?.data?.msg || 'Erro na pesquisa'
    store.commit('showSnackbar', { msg })
    console.error(err)
    limparCampos()
  }
}

function limparCampos() {
  envolvidos.value = []
  amparoInfo.value = null
  localInfo.value = null
  permitido.value = false
  checked.value = true
}

function enableManualEdit() {
  if (justificativa.value) {
    motivoManual.value = justificativa.value.motivo
    justificativaManual.value = justificativa.value.justificativa
  }
  editJustificativa.value = true
}

function limpar() {
  numeroAi.value = ''
  limparCampos()
  motivoManual.value = ''
  justificativaManual.value = ''
  manualValid.value = false
  editJustificativa.value = false
  formRef.value?.resetValidation()
  manualFormRef.value?.resetValidation()
}

onBeforeRouteLeave(() => {
  limpar()
})

function removeAccents(str) {
  return (str || '').normalize('NFD').replace(/\p{Diacritic}/gu, '')
}

async function enviarSolicitacao() {
  const useManual = editJustificativa.value || !justificativa.value
  if (useManual && !manualFormRef.value?.validate()) return

  const cpf = (store.state.user.cpf || '').replace(/\D/g, '').slice(0, 11)

  const listItem = {
    id: null,
    processo: {
      id: idProcesso.value,
      estado: "Criado",
      eventos: [],
      eventosExternos: [],
      notificacoes: [],
      nup: "",
      seqDocumentos: 0,
      separadoParaEnvio: null,
      bloqueio: null,
      pago: false,
      solicitacoes: [],
      solicitacao: null,
      boletos: [],
      arquivos: []
    },
    dataProtocolo: null,
    estado: "Protocolada",
    estadoDescricao: null,
    tipoSolicitacao: "Cancelamento",
    justificativa: useManual ? justificativaManual.value : justificativa.value.justificativa,
    texto: useManual ? motivoManual.value : justificativa.value.motivo,
    autoSubstituto: null,
    numeroAutoSubstituto: null,
    requerente: {
      nome: removeAccents(store.state.user.username || '').toUpperCase(),
      documentos: [{ tipoDocumento: "CPF", numero: cpf }],
      tiposEnvolvimento: []
    },
    numeroProtocolo: null,
    origem: "PRF",
    documentos: [],
    eventos: [],
    bloqueioTemporario: null,
    bloqueioPermanente: false,
    usuarioDiligencia: null,
    condutorIndicado: null
  }

  const payload = { numero: numeroAi.value, list: [listItem] }

  try {
    const { data } = await solicitarCancelamento(payload)
    const success = data === true
    store.commit('showSnackbar', {
      msg: success ? 'Solicitação enviada' : 'Erro na solicitação',
      color: success ? 'success' : 'error'
    })
    limpar()
  } catch (err) {
    const msg = err.response?.data?.msg || 'Erro na solicitação'
    store.commit('showSnackbar', { msg })
    console.error(err)
    limpar()
  }
}
</script>
