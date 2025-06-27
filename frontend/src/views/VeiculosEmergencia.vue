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
  </v-container>
</template>

<script setup>
import { ref } from 'vue'
import { pesquisarAutoInfracao, obterEnvolvidos } from '../services/autoprf'

const numeroAi = ref('')
const envolvidos = ref([])
const amparoInfo = ref(null)
const permitido = ref(false)
const checked = ref(false)
const formRef = ref(null)
const valid = ref(false)

const rules = { required: v => !!v || 'Campo obrigatório' }

const instituicoes = {
  '89175541000164': 'Brigada Militar',
  '00058163000125': 'Polícia Civil',
  '28610005000155': 'Corpo de Bombeiros',
  '02510700000151': 'EPTC'
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

async function buscar() {
  if (!formRef.value?.validate()) return
  checked.value = false
  try {
    const { data } = await pesquisarAutoInfracao({ auto_infracao: numeroAi.value })
    if (data.id) {
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
</script>
