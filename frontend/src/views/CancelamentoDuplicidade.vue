<template>
  <v-container>
    <v-row>
      <v-col cols="12" md="4">
        <v-card class="pa-4 mb-4" elevation="2" title="Autos de Infração">
          <v-form ref="formRef" v-model="valid">
            <v-text-field
              v-model="numeroAi1"
              label="Número do Auto de Infração 1"
              :rules="[rules.required]"
            />
            <v-text-field
              v-model="numeroAi2"
              label="Número do Auto de Infração 2"
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

    <v-card v-if="ai1 && ai2" class="pa-4" elevation="2">
      <v-card-title class="d-flex justify-space-between align-center">
        Cancelamento por Duplicidade
        <v-chip :color="iguais ? 'green' : 'red'" dark>
          {{ iguais ? 'Registros compatíveis' : 'Registros divergentes' }}
        </v-chip>
      </v-card-title>
      <v-card-text>
        <v-row dense>
          <v-col cols="12" md="6">
            <v-text-field :model-value="ai1.infracao?.codigo_descricao" label="AI 1 - Código/Descrição da Infração" readonly />
          </v-col>
          <v-col cols="12" md="6">
            <v-text-field :model-value="ai2.infracao?.codigo_descricao" label="AI 2 - Código/Descrição da Infração" readonly />
          </v-col>
          <v-col cols="12" md="6">
            <v-text-field :model-value="ai1.infracao?.amparo_legal" label="AI 1 - Amparo Legal" readonly />
          </v-col>
          <v-col cols="12" md="6">
            <v-text-field :model-value="ai2.infracao?.amparo_legal" label="AI 2 - Amparo Legal" readonly />
          </v-col>
          <v-col cols="12" md="6">
            <v-text-field :model-value="ai1.veiculo?.placa" label="AI 1 - Placa" readonly />
          </v-col>
          <v-col cols="12" md="6">
            <v-text-field :model-value="ai2.veiculo?.placa" label="AI 2 - Placa" readonly />
          </v-col>
          <v-col cols="12" md="6">
            <v-text-field :model-value="ai1.local?.codigo_municipio_uf" label="AI 1 - Código/Município/UF" readonly />
          </v-col>
          <v-col cols="12" md="6">
            <v-text-field :model-value="ai2.local?.codigo_municipio_uf" label="AI 2 - Código/Município/UF" readonly />
          </v-col>
          <v-col cols="6" md="3">
            <v-text-field :model-value="ai1.local?.rodovia" label="AI 1 - BR" readonly />
          </v-col>
          <v-col cols="6" md="3">
            <v-text-field :model-value="ai2.local?.rodovia" label="AI 2 - BR" readonly />
          </v-col>
          <v-col cols="6" md="3">
            <v-text-field :model-value="ai1.local?.km" label="AI 1 - Km" readonly />
          </v-col>
          <v-col cols="6" md="3">
            <v-text-field :model-value="ai2.local?.km" label="AI 2 - Km" readonly />
          </v-col>
          <v-col cols="6" md="3">
            <v-text-field :model-value="ai1.local?.sentido" label="AI 1 - Sentido" readonly />
          </v-col>
          <v-col cols="6" md="3">
            <v-text-field :model-value="ai2.local?.sentido" label="AI 2 - Sentido" readonly />
          </v-col>
          <v-col cols="6" md="3">
            <v-text-field :model-value="ai1.local?.data_hora" label="AI 1 - Data/Hora" readonly />
          </v-col>
          <v-col cols="6" md="3">
            <v-text-field :model-value="ai2.local?.data_hora" label="AI 2 - Data/Hora" readonly />
          </v-col>
        </v-row>
      </v-card-text>
    </v-card>
  </v-container>
</template>

<script setup>
import { ref, computed } from 'vue'
import { pesquisarAutoInfracao } from '../services/autoprf'

const numeroAi1 = ref('')
const numeroAi2 = ref('')
const ai1 = ref(null)
const ai2 = ref(null)

const formRef = ref(null)
const valid = ref(false)

const rules = { required: v => !!v || 'Campo obrigatório' }

async function buscar() {
  if (!formRef.value?.validate()) return
  try {
    const [res1, res2] = await Promise.all([
      pesquisarAutoInfracao({ auto_infracao: numeroAi1.value }),
      pesquisarAutoInfracao({ auto_infracao: numeroAi2.value })
    ])
    ai1.value = res1.data
    ai2.value = res2.data
  } catch (err) {
    console.error(err)
    ai1.value = null
    ai2.value = null
  }
}

function limpar() {
  numeroAi1.value = ''
  numeroAi2.value = ''
  ai1.value = null
  ai2.value = null
  formRef.value?.resetValidation()
}

const iguais = computed(() => {
  if (!ai1.value || !ai2.value) return false
  const f1 = ai1.value
  const f2 = ai2.value
  return (
    f1.infracao?.codigo_descricao === f2.infracao?.codigo_descricao &&
    f1.infracao?.amparo_legal === f2.infracao?.amparo_legal &&
    f1.veiculo?.placa === f2.veiculo?.placa &&
    f1.local?.codigo_municipio_uf === f2.local?.codigo_municipio_uf &&
    f1.local?.rodovia === f2.local?.rodovia &&
    f1.local?.km === f2.local?.km &&
    f1.local?.sentido === f2.local?.sentido &&
    f1.local?.data_hora === f2.local?.data_hora
  )
})
</script>
