<template>
  <v-container>
    <v-card class="pa-4 mb-4" elevation="2">
      <v-form ref="formRef" v-model="valid">
        <v-text-field
          v-model="numeroAi"
          label="Número do Auto de Infração"
          :rules="[rules.required]"
        />
        <v-btn color="primary" class="mt-2" @click="buscar" :disabled="!valid">
          Pesquisar
        </v-btn>
      </v-form>
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
import { pesquisarAutoInfracao, obterEnvolvidos } from '../services/api'

const numeroAi = ref('')
const envolvidos = ref([])
const formRef = ref(null)
const valid = ref(false)

const rules = { required: v => !!v || 'Campo obrigatório' }

async function buscar() {
  if (!formRef.value?.validate()) return
  try {
    const { data } = await pesquisarAutoInfracao({ auto_infracao: numeroAi.value })
    if (data.id) {
      const res = await obterEnvolvidos(data.id)
      envolvidos.value = res.data
    } else {
      envolvidos.value = []
    }
  } catch (err) {
    console.error(err)
    envolvidos.value = []
  }
}
</script>
