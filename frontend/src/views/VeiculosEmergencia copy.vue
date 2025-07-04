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

    <v-card v-if="amparoInfo" class="pa-4 mb-2" elevation="2">
      <v-card-title>Amparo legal</v-card-title>
      <v-card-text>
        <div><strong>Código:</strong> {{ amparoInfo.codigo }}</div>
        <div><strong>Descrição:</strong> {{ amparoInfo.descricao }}</div>
        <div><strong>Amparo legal:</strong> {{ amparoInfo.amparo }}</div>
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
    
    <v-card v-if="envolvidos.length" class="pa-4" elevation="2">
      <v-card-title>Envolvidos</v-card-title>
      <v-card-text>
        <v-row dense>
          <v-col cols="12" md="6" v-for="env in envolvidos" :key="env.id">
            <v-card class="mb-2">
              <v-card-text>
                  <div><strong>Nome:</strong> {{ env.nome }}</div>
                  <div><strong>Envolvimento:</strong> {{ env.envolvimentoAuto || env.envolvimentoProcesso || env.envolvimento }}</div>
                  <div><strong>Tipo Documento:</strong> {{ env.tipoDocumento }}</div>
                  <div><strong>Número Documento:</strong> {{ env.numeroDocumento }}</div>
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
    <v-card v-if="justificativa" class="pa-4 mb-2" elevation="2">
      <v-card-title>Justificativa</v-card-title>
      <v-card-text>
        <div><strong>Órgão:</strong> {{ justificativa.orgao }}</div>
        <div><strong>Motivo:</strong> {{ justificativa.motivo }}</div>
        <div><strong>Justificativa:</strong> {{ justificativa.justificativa }}</div>
      </v-card-text>
    </v-card>
    <v-btn
      v-if="justificativa"
      color="primary"
      class="mt-4"
      @click="enviarSolicitacao"
    >
      Solicitação de Cancelamento
    </v-btn>
  </v-container>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useStore } from 'vuex'
import { onBeforeRouteLeave } from 'vue-router'
import {
  pesquisarAutoInfracao,
  obterEnvolvidos,
  solicitarCancelamento
} from '../services/autoprf'

const numeroAi = ref('')
const envolvidos = ref([])
const amparoInfo = ref(null)
const permitido = ref(false)
const checked = ref(false)
const formRef = ref(null)
const valid = ref(false)
const autoId = ref(null)
const idProcesso = ref(null)
const store = useStore()

const rules = { required: v => !!v || 'Campo obrigatório' }

const instituicoes = {
  '89175541000164': 'Brigada Militar',
  '00058163000125': 'Polícia Civil',
  '28610005000155': 'Corpo de Bombeiros',
  '02510700000151': 'EPTC',
  '00394429000179': 'PRF',
  '07963160000130': 'SUSEPE',
  '09734605000187': 'Polícia Legislativa',
  '87934675000196': 'Estado do Rio Grande do Sul'
}

const justificativas = {
  '00394429000179': {
    orgao: 'PRF',
    motivo:
      'Enquadramento no art. 280, § 6º do CTB, por se tratar de viatura oficial de órgão policial (Polícia Rodoviária Federal). Requerimento em anexo',
    justificativa: 'Viatura policial.'
  },
  '00058163000125': {
    orgao: 'Polícia Civil',
    motivo:
      'Enquadramento no art. 280, § 6º do CTB, por se tratar de viatura oficial de órgão policial (Polícia Civil do Rio Grande do Sul). Requerimento em anexo',
    justificativa: 'Viatura policial.'
  },
  '09734605000187': {
    orgao: 'Polícia Legislativa',
    motivo:
      'Enquadramento no art. 280, § 6º do CTB, por se tratar de viatura oficial de órgão policial (Polícia Legislativa). Requerimento em anexo',
    justificativa: 'Viatura policial.'
  },
  '07963160000130': {
    orgao: 'SUSEPE',
    motivo:
      'Enquadramento no art. 280, § 6º do CTB, por se tratar de viatura oficial da polícia penal (Superintendência dos Serviços Penitenciários do Estado do Rio Grande do Sul). Requerimento em anexo',
    justificativa: 'Viatura policial.'
  },
  '89175541000164': {
    orgao: 'Brigada Militar',
    motivo:
      'Enquadramento no art. 280, § 6º do CTB, por se tratar de viatura oficial de órgão policial (Brigada Militar do Rio Grande do Sul). Requerimento em anexo',
    justificativa: 'Viatura policial.'
  },
  '87934675000196': {
    orgao: 'Estado do Rio Grande do Sul',
    motivo:
      'Enquadramento no art. 280, § 6º do CTB, por se tratar de viatura oficial de órgão policial (Brigada Militar do Rio Grande do Sul). Requerimento em anexo',
    justificativa: 'Viatura policial.'
  }
}

// Relação de códigos com enquadramento legal permitido
const codigosPermitidos = ['745-50', '746-30', '747-10']
const codigosPermitidosDigits = codigosPermitidos.map(c => c.replace(/\D/g, ''))


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

async function buscar() {
  if (!formRef.value?.validate()) return
  checked.value = false
  try {
    const { data } = await pesquisarAutoInfracao({ auto_infracao: numeroAi.value.trim() })
    console.log(data)
    if (data.id) {
      autoId.value = data.id
      idProcesso.value = data.idProcesso
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
      permitido.value = false
      checked.value = true
    }
  } catch (err) {
    console.error(err)
    envolvidos.value = []
    amparoInfo.value = null
    permitido.value = false
    checked.value = true
  }
}

function limpar() {
  numeroAi.value = ''
  envolvidos.value = []
  amparoInfo.value = null
  permitido.value = false
  checked.value = false
  formRef.value?.resetValidation()
}

onBeforeRouteLeave(() => {
  limpar()
})

function removeAccents(str) {
  return (str || '').normalize('NFD').replace(/\p{Diacritic}/gu, '')
}

async function enviarSolicitacao() {
  if (!justificativa.value) return

  const cpf = (store.state.user.cpf || '').replace(/\D/g, '').slice(0, 11)

  const listItem = {
    processo: { id: idProcesso.value },
    tipoSolicitacao: 'CANCELAMENTO',
    justificativa: justificativa.value.justificativa,
    texto: justificativa.value.motivo,
    requerente: {
      nome: removeAccents(store.state.user.username || '').toUpperCase(),
      documentos: [
        {
          tipoDocumento: "CPF",
          numero: cpf
        }
      ]
    }
  }

  const payload = { numero: numeroAi.value.trim(), list: [listItem] }
  console.log(payload) 

  try {
    const { data } = await solicitarCancelamento(payload)
    if (data === 1 || data === true) {
      store.commit('showSnackbar', { msg: 'Solicitação enviada', color: 'success' })
    }
  } catch (err) {
    store.commit('showSnackbar', { msg: err.response?.data?.msg || 'Erro na solicitação' })
  }
}
</script>
