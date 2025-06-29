<template>
  <v-container>
    <v-row>
      <v-col cols="12">
        <v-card class="pa-4" elevation="2">
          <h2>Auto de Infração SISCOM</h2>
        </v-card>
      </v-col>
    </v-row>
    <v-row class="my-2">
      <v-col cols="12" class="text-right">
        <v-btn color="primary" @click="limparConsulta">Limpar</v-btn>
      </v-col>
    </v-row>

    <v-card class="pa-4 mb-4" elevation="2">
      <v-row dense>
        <v-col cols="12" md="3">
          <v-text-field :model-value="ai?.numeroAuto" label="Número AI" readonly />
        </v-col>
        <v-col cols="12" md="3">
          <v-text-field :model-value="ai?.codigoInfracao" label="Código" readonly />
        </v-col>
        <v-col cols="12" md="6">
          <v-text-field :model-value="ai?.descAbreviadaInfracao" label="Descrição" readonly />
        </v-col>
        <v-col cols="12" md="3">
          <v-text-field :model-value="ai?.placa" label="Placa" readonly />
        </v-col>
        <v-col cols="12" md="3">
          <v-text-field :model-value="ai?.renavam" label="Renavam" readonly />
        </v-col>
        <v-col cols="12" md="3">
          <v-text-field :model-value="ai?.kmInfracao" label="Km" readonly />
        </v-col>
        <v-col cols="12" md="3">
          <v-text-field :model-value="ai?.municipioInfracao?.nome" label="Município" readonly />
        </v-col>
        <v-col cols="12" md="3">
          <v-text-field :model-value="ai?.valorInfracao" label="Valor" readonly />
        </v-col>
      </v-row>
    </v-card>
  </v-container>
</template>

<script setup>
import { computed, onMounted } from 'vue'
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'

const store = useStore()
const router = useRouter()

const ai = computed(() => store.state.siscomAiResult)

onMounted(() => {
  if (!ai.value) {
    router.push('/')
  }
})

function limparConsulta() {
  store.commit('setSiscomAiResult', null)
  router.push('/')
}
</script>
