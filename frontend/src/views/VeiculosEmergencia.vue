<template>
  <v-container>
    <v-row>
      <v-col cols="12" md="4">
        <v-card class="pa-4 mb-4" elevation="2" title="Auto de Infração">
          <v-form ref="formRef" v-model="valid">
            <v-text-field
              v-model="numeroAi"
              label="Número do Auto de Infração"
              :rules="[rules.required]"
            />
            <v-btn color="primary" class="mt-2" @click="buscar" :disabled="!valid">
              Pesquisar
            </v-btn>
            <v-btn color="secondary" class="mt-2 ml-2" @click="limpar">
              Limpar
            </v-btn>
          </v-form>
        </v-card>
      </v-col>
    </v-row>

    <v-card v-if="localInfo" class="pa-4 mb-2" elevation="2">
      <v-card-title>Local da Infração</v-card-title>
      <v-card-text>
        <v-row dense>
          <v-col cols="12" md="6">
            <v-text-field
              :model-value="localInfo.codigo_municipio_uf"
              label="Código/Município/UF"
              readonly
            />
          </v-col>
          <v-col cols="6" md="3">
            <v-text-field
              :model-value="localInfo.rodovia"
              label="BR"
              readonly
            />
          </v-col>
          <v-col cols="6" md="3">
            <v-text-field
              :model-value="localInfo.km"
              label="Km"
              readonly
            />
          </v-col>
          <v-col cols="6" md="3">
            <v-text-field
              :model-value="localInfo.sentido"
              label="Sentido"
              readonly
            />
          </v-col>
          <v-col cols="6" md="3">
            <v-text-field
              :model-value="localInfo.data_hora"
              label="Data/Hora"
              readonly
            />
          </v-col>
        </v-row>
        <v-chip v-if="foraCircunscricao" color="red" class="mt-2" dark>
          Fora da Circunscrição
        </v-chip>
        <v-chip v-else color="green" class="mt-2" dark>
          Circunscrição do Rio Grande do Sul
        </v-chip>
      </v-card-text>
    </v-card>

    <v-card v-if="amparoInfo && !foraCircunscricao" class="pa-4 mb-2" elevation="2">
      <v-card-title>Amparo legal</v-card-title>
      <v-card-text>
        <v-row dense>
          <v-col cols="12" md="3">
            <v-text-field
              :model-value="amparoInfo.codigo"
              label="Código"
              readonly
            />
          </v-col>
          <v-col cols="12" md="5">
            <v-text-field
              :model-value="amparoInfo.descricao"
              label="Descrição"
              readonly
            />
          </v-col>
          <v-col cols="12" md="4">
            <v-text-field
              :model-value="amparoInfo.amparo"
              label="Amparo legal"
              readonly
            />
          </v-col>
        </v-row>
      </v-card-text>
      <v-chip
        v-if="checked"
        class="mb-4"
        :color="permitido ? 'green' : 'red'"
        dark
      >
        {{
          permitido
            ? 'Enquadramento legal permitido'
            : 'Enquadramento legal não permitido'
        }}
      </v-chip>
    </v-card>
    
    <v-card v-if="envolvidos.length && !foraCircunscricao" class="pa-4" elevation="2">
      <v-card-title>Envolvidos</v-card-title>
      <v-card-text>
        <v-row dense>
          <v-col cols="12" md="6" v-for="env in envolvidos" :key="env.id">
            <v-card class="mb-2">
              <v-card-text>
                <v-row dense>
                  <v-col cols="12">
                    <v-text-field
                      :model-value="env.nome"
                      label="Nome"
                      readonly
                    />
                  </v-col>
                  <v-col cols="12">
                    <v-text-field
                      :model-value="env.envolvimentoAuto || env.envolvimentoProcesso || env.envolvimento"
                      label="Envolvimento"
                      readonly
                    />
                  </v-col>
                  <v-col cols="6">
                    <v-text-field
                      :model-value="env.tipoDocumento"
                      label="Tipo Documento"
                      readonly
                    />
                  </v-col>
                  <v-col cols="6">
                    <v-text-field
                      :model-value="env.numeroDocumento"
                      label="Número Documento"
                      readonly
                    />
                  </v-col>
                </v-row>
                <v-chip
                  v-if="showInstituicao(env)"
                  color="green"
                  class="mt-2"
                >
                  Proprietário/possuidor previsto em lei:
                  {{ instituicaoNome(env.numeroDocumento) }}
                </v-chip>
                <v-chip
                  v-else
                  color="red"
                  class="mt-2"
                >
                  Proprietário/possuidor não previsto em lei
                </v-chip>
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>
      </v-card-text>
    </v-card>
    <v-card class="pa-4 my-2" elevation="2">
      <v-card-title>Requerimento</v-card-title>
      <v-file-input
        accept="application/pdf"
        v-model="arquivoPdf"
        label="Arquivo PDF"
      />
    </v-card>
    <v-form
      v-if="!foraCircunscricao && ((requireManualJustificativa && !justificativa) || editJustificativa)"
      ref="manualFormRef"
      v-model="manualValid"
      class="mt-4"
    >
      <v-card class="pa-4" elevation="2">
        <v-card-title class="d-flex justify-space-between align-center">
          Justificativa
          <v-btn
            v-if="editJustificativa"
            size="small"
            variant="text"
            color="secondary"
            @click="editJustificativa = false"
          >
            Cancelar
          </v-btn>
        </v-card-title>
        <v-card-text>
          <v-textarea
            v-model="motivoManual"
            label="Motivo"
            :rules="[rules.required]"
          />
          <v-text-field
            v-model="justificativaManual"
            label="Justificativa por não ter substituto"
            :rules="[rules.required]"
          />
        </v-card-text>
      </v-card>
    </v-form>
    <v-card v-if="justificativa && !editJustificativa && !foraCircunscricao" class="pa-4 mb-2" elevation="2">
      <v-card-title class="d-flex justify-space-between align-center">
        Justificativa
        <v-btn size="small" @click="enableManualEdit" color="primary">Alterar</v-btn>
      </v-card-title>
      <v-card-text>
        <v-row dense>
          <v-col cols="12" md="4">
            <v-text-field
              :model-value="justificativa.orgao"
              label="Órgão"
              readonly
            />
          </v-col>
          <v-col cols="12" md="8">
            <v-text-field
              :model-value="justificativa.motivo"
              label="Motivo"
              readonly
            />
          </v-col>
          <v-col cols="12">
            <v-textarea
              :model-value="justificativa.justificativa"
              label="Justificativa"
              readonly
            />
          </v-col>
        </v-row>
      </v-card-text>
    </v-card>
    <v-btn
      v-if="!foraCircunscricao && (justificativa || requireManualJustificativa)"
      color="primary"
      class="mt-4"
      :disabled="!justificativa && !manualValid"
      @click="enviarSolicitacao"
    >
      Solicitar Cancelamento
    </v-btn>

    <v-dialog v-model="cancelamentoDialog" max-width="600">
      <v-card>
        <v-card-title class="d-flex justify-space-between align-center">
          Solicitação de Cancelamento
          <v-btn icon="mdi-close" size="small" @click="fecharCancelamento" />
        </v-card-title>
        <v-card-text>
          <v-row dense>
            <v-col cols="12" md="4">
              <v-text-field
                :model-value="cancelamentoInfo?.numeroProtocolo"
                label="Número do Protocolo"
                readonly
              />
            </v-col>
          </v-row>
          <v-data-table
            :headers="historicoHeaders"
            :items="cancelamentoInfo?.eventos"
            :items-per-page="-1"
            hide-default-footer
          >
            <template #item.dataHora="{ item }">
              {{ new Date(item.dataHora).toLocaleString('pt-BR') }}
            </template>
          </v-data-table>
          <v-alert
            v-if="uploadStatus !== null"
            :type="uploadStatus ? 'success' : 'error'"
            class="mt-2"
          >
            {{ uploadStatus ? 'Arquivo enviado com sucesso' : 'Erro ao enviar arquivo' }}
          </v-alert>
        </v-card-text>
      </v-card>
    </v-dialog>
    <v-alert v-if="cancelamentoInfo === false" type="warning" class="mt-4">
      Não há registro de protocolo da solicitação
    </v-alert>


  </v-container>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useStore } from 'vuex'
import { onBeforeRouteLeave } from 'vue-router'
import {
  pesquisarAutoInfracao,
  obterEnvolvidos,
  solicitarCancelamento,
  obterHistorico,
  anexarArquivo
} from '../services/autoprf'
import {
  instituicoes,
  justificativas,
  codigosPermitidosDigits
} from '../constants/veiculosEmergencia'

const numeroAi = ref('')
const envolvidos = ref([])
const amparoInfo = ref(null)
const localInfo = ref(null)
const permitido = ref(false)
const checked = ref(false)
const formRef = ref(null)
const valid = ref(false)
const autoId = ref(null)
const idProcesso = ref(null)
const motivoManual = ref('')
const justificativaManual = ref('')
const manualValid = ref(false)
const manualFormRef = ref(null)
const editJustificativa = ref(false)
const store = useStore()
const cancelamentoInfo = ref(null)
const cancelamentoDialog = ref(false)
const arquivoPdf = ref(null)
const uploadStatus = ref(null)
const historicoHeaders = [{ title: 'Data e Hora', key: 'dataHora' }]

const foraCircunscricao = computed(() => {
  const str = localInfo.value?.codigo_municipio_uf || ''
  const match = str.match(/\/([A-Za-z]{2})$/)
  if (!match) return false
  return match[1].toUpperCase() !== 'RS'
})

const rules = { required: v => !!v || 'Campo obrigatório' }

function sanitize(cnpj) {
  return (cnpj || '').replace(/\D/g, '')
}

function instituicaoNome(cnpj) {
  return instituicoes[sanitize(cnpj)]
}

function showInstituicao(env) {
  const envolvimento = (env.envolvimentoAuto || env.envolvimentoProcesso || env.envolvimento || '').toLowerCase()
  if (!/propriet[aá]rio|possuidor/.test(envolvimento)) return false
  return !!instituicaoNome(env.numeroDocumento)
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
    const cnpj = sanitize(env.numeroDocumento)
    if (!instituicoes[cnpj]) return true
  }
  return false
})

async function buscar() {
  if (!formRef.value?.validate()) return
  checked.value = false
  try {
    const { data } = await pesquisarAutoInfracao({ auto_infracao: numeroAi.value })
    
    if (data.id) {
      autoId.value = data.id
      idProcesso.value = data.idProcesso
      localInfo.value = data.local || null
      const cd = data.infracao?.codigo_descricao || ''
      const [codPart, ...descParts] = cd.split(/\s*-\s*/)
      const codigo = codPart?.trim() || ''
      const descricao = descParts.join(' - ').trim()
      amparoInfo.value = cd
        ? {
            codigo,
            descricao,
            amparo: data.infracao?.amparo_legal || ''
          }
        : null

      const digits = codigo.replace(/\D/g, '')
      permitido.value = codigosPermitidosDigits.includes(digits)
      checked.value = true

      const res = await obterEnvolvidos(data.id)
      envolvidos.value = res.data.filter(env => {
        const envolvimento = (env.envolvimentoAuto || env.envolvimentoProcesso || env.envolvimento || '').toLowerCase()
        return !/condutor/.test(envolvimento)
      })
    } else {
      envolvidos.value = []
      amparoInfo.value = null
      localInfo.value = null
      permitido.value = false
      checked.value = true
    }
  } catch (err) {
    const msg = err.response?.data?.msg
    if (/Sessão AutoPRF expirada/i.test(msg) || /Sessão não iniciada/i.test(msg)) {
      store.commit('showSnackbar', { msg: 'Faça login no AutoPRF' })
    } else {
      console.error(err)
    }
    envolvidos.value = []
    amparoInfo.value = null
    localInfo.value = null
    permitido.value = false
    checked.value = true
  }
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
  envolvidos.value = []
  amparoInfo.value = null
  localInfo.value = null
  permitido.value = false
  checked.value = false
  motivoManual.value = ''
  justificativaManual.value = ''
  manualValid.value = false
  editJustificativa.value = false
  cancelamentoInfo.value = null
  cancelamentoDialog.value = false
  arquivoPdf.value = null
  uploadStatus.value = null
  formRef.value?.resetValidation()
  manualFormRef.value?.resetValidation()
}

function fecharCancelamento() {
  cancelamentoDialog.value = false
  cancelamentoInfo.value = null
  uploadStatus.value = null
}

onBeforeRouteLeave(() => {
  limpar()
  cancelamentoInfo.value = null
  cancelamentoDialog.value = false
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
    justificativa: useManual
      ? justificativaManual.value
      : justificativa.value.justificativa,
    texto: useManual ? motivoManual.value : justificativa.value.motivo,
    autoSubstituto: null,
    numeroAutoSubstituto: null,
    requerente: {
      nome: removeAccents(store.state.user.username || '').toUpperCase(),
      documentos: [
        {
          tipoDocumento: "CPF",
          numero: cpf
        }
      ],
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

  const payload = {
    numero: numeroAi.value,
    list: [listItem]
  }

  try {
    if (arquivoPdf.value) {
      try {
        await anexarArquivo(idProcesso.value, arquivoPdf.value)
        uploadStatus.value = true
      } catch (e) {
        console.error(e)
        uploadStatus.value = false
      }
    } else {
      uploadStatus.value = null
    }

    const { data } = await solicitarCancelamento(payload)
    console.log(data)
    if (data === true) {
      store.commit('showSnackbar', { msg: 'Solicitação enviada', color: 'success' })
    } else {
      store.commit('showSnackbar', { msg: 'Erro na solicitação' })
    }
    limpar()
    try {
      const { data: hist } = await obterHistorico(idProcesso.value)
      const item = (hist.solicitacoes || []).find(s =>
        /cancelamento/i.test(s.tipoSolicitacao)
      )
      if (item) {
        cancelamentoInfo.value = {
          numeroProtocolo: item.numeroProtocolo,
          eventos: item.eventos || []
        }
        cancelamentoDialog.value = true
      } else {
        cancelamentoInfo.value = false
      }
    } catch (e) {
      console.error(e)
      cancelamentoInfo.value = false
    }
  } catch (err) {
    const msg = err.response?.data?.msg
    if (/Sessão AutoPRF expirada/i.test(msg) || /Sessão não iniciada/i.test(msg)) {
      store.commit('showSnackbar', { msg: 'Faça login no AutoPRF' })
    } else {
      store.commit('showSnackbar', { msg: msg || 'Erro na solicitação' })
    }
    limpar()
  }
}

</script>
