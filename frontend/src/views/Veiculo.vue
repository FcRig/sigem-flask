<template>
  <v-container>
    <v-row>
      <v-col cols="12" md="4">
        <v-card class="pa-4 mb-4" elevation="2" title="Consulta de Veículo">
          <v-form ref="formRef" v-model="valid">
            <v-text-field
              v-model="placa"
              label="Placa"
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

    <v-card v-if="result" class="pa-4" elevation="2">
      <v-card-title>Resultado</v-card-title>
      <v-card-text>
        <pre>{{ result }}</pre>
      </v-card-text>
    </v-card>
  </v-container>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useStore } from 'vuex'

const store = useStore()

const placa = ref('')
const formRef = ref(null)
const valid = ref(false)

const result = computed(() => store.state.veiculoResult)

const rules = { required: v => !!v || 'Campo obrigatório' }

async function buscar() {
  if (!formRef.value?.validate()) return
  try {
    await store.dispatch('consultarPlaca', { placa: placa.value })
  } catch (err) {
    store.commit('showSnackbar', {
      msg: err.response?.data?.msg || 'Erro ao consultar placa'
    })
    store.commit('setVeiculoResult', null)
  }
}

function limpar() {
  placa.value = ''
  store.commit('setVeiculoResult', null)
  formRef.value?.resetValidation()
}
</script>

