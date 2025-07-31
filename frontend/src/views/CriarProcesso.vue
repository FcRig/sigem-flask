<template>
  <v-container>
    <v-row>
      <v-col cols="12" md="6">
        <v-card class="pa-4 mb-4" elevation="2" title="Criação de Processos SEI">
          <v-form ref="formRef" v-model="valid">
            <v-select
              v-model="tipo"
              :items="tipos"
              item-title="text"
              item-value="id"
              label="Natureza do Processo"
              :rules="[rules.required]"
            />
            <v-text-field
              v-model="descricao"
              label="Especificação"
              :rules="[rules.required]"
            />
            <v-btn color="primary" class="mt-2" @click="submeter" :disabled="!valid">
              SUBMETER
            </v-btn>
            <v-btn color="secondary" class="mt-2 ml-2" @click="limpar">
              LIMPAR
            </v-btn>
          </v-form>
        </v-card>
      </v-col>
    </v-row>
    <v-snackbar
      v-model="snackbar"
      :color="snackbarColor"
      location="top right"
      timeout="3000"
    >
      {{ snackbarMsg }}
    </v-snackbar>
  </v-container>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { obterTipos, criarProcesso } from '../services/sei'

const tipo = ref('')
const tipos = ref([])
const descricao = ref('')
const formRef = ref(null)
const valid = ref(false)
const snackbar = ref(false)
const snackbarMsg = ref('')
const snackbarColor = ref('success')

const rules = {
  required: v => !!v || 'Campo obrigatório'
}

async function carregarTipos() {
  try {
    const { data } = await obterTipos()
    tipos.value = data
  } catch (err) {
    snackbarMsg.value = err.response?.data?.msg || 'Erro ao carregar tipos'
    snackbarColor.value = 'error'
    snackbar.value = true
  }
}

async function submeter() {
  if (!formRef.value?.validate()) return
  try {
    await criarProcesso({
      tipo_id: tipo.value,
      tipo_nome: tipos.value.find(t => t.id === tipo.value)?.text || '',
      descricao: descricao.value
    })
    snackbarMsg.value = 'Processo criado com sucesso'
    snackbarColor.value = 'success'
    snackbar.value = true
    limpar(false)
  } catch (err) {
    snackbarMsg.value = err.response?.data?.msg || 'Erro ao criar processo'
    snackbarColor.value = 'error'
    snackbar.value = true
  }
}

function limpar(resetValidation = true) {
  if (resetValidation) formRef.value?.resetValidation()
  descricao.value = ''
  tipo.value = ''
}

onMounted(() => {
  carregarTipos()
})
</script>
