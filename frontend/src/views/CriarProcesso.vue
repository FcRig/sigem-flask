<template>
  <v-container>
    <v-row>
      <v-col cols="12" md="6">
        <v-card class="pa-4 mb-4" elevation="2" title="Criação de Processos SEI">
          <v-form ref="formRef" v-model="valid">
            <v-text-field
              v-model="usuario"
              label="Usuário SEI"
              :rules="[rules.required]"
            />
            <v-text-field
              v-model="senha"
              label="Senha SEI"
              type="password"
              :rules="[rules.required]"
            />
            <v-text-field
              v-model="token"
              label="Token SEI"
              :rules="[rules.required]"
            />
            <v-select
              v-model="tipo"
              :items="tipos"
              item-title="text"
              item-value="id"
              label="Natureza do Processo"
              :rules="[rules.required]"
            />
            <v-textarea
              v-model="descricao"
              label="Descrição"
              :rules="[rules.required]"
              auto-grow
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
import { useStore } from 'vuex'
import { obterTipos, criarProcesso } from '../services/sei'

const store = useStore()

const usuario = ref(store.state.user?.usuario_sei || '')
const senha = ref('')
const token = ref(store.state.user?.token_sei || '')
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
    const { data } = await obterTipos({
      usuario: usuario.value,
      senha_sei: senha.value,
      token_sei: token.value
    })
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
      usuario: usuario.value,
      senha_sei: senha.value,
      token_sei: token.value,
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
  if (usuario.value && token.value) {
    carregarTipos()
  }
})
</script>
