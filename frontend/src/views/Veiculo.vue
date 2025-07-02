<template>
  <v-container>
    <v-row>
      <v-col cols="12" md="4">
        <v-card class="pa-4 mb-4" elevation="2" title="Consulta de Veículo">
          <v-form ref="formRef" v-model="valid">
            <v-text-field
              v-model="placa"
              label="Placa"
              prepend-icon="mdi-car"
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

    <template v-if="result">
      <v-card
        v-for="(group, name) in result"
        :key="name"
        class="pa-4 mb-4"
        elevation="2"
      >
        <h3 class="pa-4">{{ formatLabel(name) }}</h3>
        <v-row dense>
          <template v-if="typeof group === 'object' && group !== null && !Array.isArray(group)">
            <v-col
              v-for="(value, key) in group"
              :key="key"
              cols="12"
              md="4"
            >
              <v-text-field :model-value="value" :label="formatLabel(key)" readonly />
            </v-col>
          </template>
          <template v-else>
            <v-col cols="12">
              <v-text-field :model-value="group" :label="formatLabel(name)" readonly />
            </v-col>
          </template>
        </v-row>
      </v-card>
    </template>
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

function formatLabel(key) {
  return (key || '')
    .replace(/_/g, ' ')
    .replace(/(?:^|\s)\w/g, l => l.toUpperCase())
}

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

