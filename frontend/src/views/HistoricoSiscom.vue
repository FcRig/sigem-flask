<template>
  <v-container>
    <v-row>
      <v-col cols="12" md="4">
        <v-card class="pa-4 mb-4" elevation="2" title="Histórico do AI">
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

    <v-card v-if="historico.length" class="pa-4" elevation="2">
      <v-card-title>Histórico</v-card-title>
      <v-data-table :headers="headers" :items="historico" item-key="dataHistorico">
        <template #item.dataHistorico="{ item }">
          {{ formatDate(item.dataHistorico) }}
        </template>
      </v-data-table>
    </v-card>
  </v-container>
</template>

<script setup>
import { ref } from 'vue'
import { buscarHistorico } from '../services/siscom'

const numeroAi = ref('')
const historico = ref([])
const formRef = ref(null)
const valid = ref(false)

const headers = [
  { title: 'Data', key: 'dataHistorico' },
  { title: 'Status', key: 'status' }
]

const rules = { required: v => !!v || 'Campo obrigatório' }

async function buscar() {
  if (!formRef.value?.validate()) return
  try {
    const { data } = await buscarHistorico({ numero: numeroAi.value })
    historico.value = data
  } catch (err) {
    console.error(err)
    historico.value = []
  }
}

function limpar() {
  numeroAi.value = ''
  historico.value = []
  formRef.value?.resetValidation()
}

function formatDate(ms) {
  const d = new Date(Number(ms))
  return isNaN(d) ? '' : d.toLocaleString()
}
</script>
