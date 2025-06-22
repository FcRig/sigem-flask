<template>
  <v-container>
    <!-- Cabeçalho -->
    <v-row>
      <v-col cols="12">
        <v-card class="pa-4" elevation="2">
          <h2>
            Lavrar Auto de Infração
            <v-chip color="green" text-color="white">CTB</v-chip>
          </h2>
        </v-card>
      </v-col>
    </v-row>

    <!-- Identificação da Infração -->
    <v-card class="pa-4 mb-4" elevation="2">
      <h3>Identificação da Infração</h3>
      <v-row dense>
        <v-col cols="12" md="8">
          <v-text-field
            :model-value="ai?.infracao?.codigo_descricao"
            label="Código/Descrição da infração"
            readonly
          />
        </v-col>
        <v-col cols="12" md="4">
          <v-text-field
            :model-value="ai?.infracao?.amparo_legal"
            label="Amparo Legal"
            readonly
          />
        </v-col>
        <v-col cols="6" md="4">
          <v-text-field
            :model-value="ai?.infracao?.gravidade"
            label="Gravidade"
            readonly
          />
        </v-col>
        <v-col cols="6" md="4">
          <v-text-field
            :model-value="ai?.infracao?.tipo_infrator"
            label="Tipo de Infrator"
            readonly
          />
        </v-col>
      </v-row>

      <v-text-field
        :model-value="ai?.infracao?.tipo_abordagem"
        label="Abordagem"
        readonly
      />
    </v-card>

    <!-- Identificação do Veículo -->
    <v-card class="pa-4" elevation="2">
      <h3>Identificação do Veículo</h3>
      <v-row dense>
        <v-col cols="12" md="3">
          <v-text-field
            :model-value="ai?.veiculo?.emplacamento"
            label="Emplacamento"
            readonly
          />
        </v-col>
        <v-col cols="12" md="3">
          <v-text-field
            :model-value="ai?.veiculo?.placa"
            label="Placa"
            readonly
          />
        </v-col>
        <v-col cols="12" md="6">
          <v-text-field
            :model-value="ai?.veiculo?.chassi"
            label="Chassi"
            readonly
          />
        </v-col>
        <v-col cols="12" md="3">
          <v-text-field
            :model-value="ai?.veiculo?.renavam"
            label="Renavam"
            readonly
          />
        </v-col>
        <v-col cols="12" md="3">
          <v-text-field
            :model-value="ai?.veiculo?.pais"
            label="País"
            readonly
          />
        </v-col>
        <v-col cols="12" md="2">
          <v-text-field
            :model-value="ai?.veiculo?.uf"
            label="UF"
            readonly
          />
        </v-col>
        <v-col cols="12" md="4">
          <v-text-field
            :model-value="ai?.veiculo?.marca"
            label="Marca"
            readonly
          />
        </v-col>
        <v-col cols="12" md="2">
          <v-text-field
            :model-value="ai?.veiculo?.outra_marca"
            label="Outra Marca"
            readonly
          />
        </v-col>
        <v-col cols="12" md="6">
          <v-text-field
            :model-value="ai?.veiculo?.modelo"
            label="Modelo"
            readonly
          />
        </v-col>
        <v-col cols="6" md="3">
          <v-text-field
            :model-value="ai?.veiculo?.cor"
            label="Cor"
            readonly
          />
        </v-col>
        <v-col cols="6" md="3">
          <v-text-field
            :model-value="ai?.veiculo?.especie"
            label="Espécie"
            readonly
          />
        </v-col>
        <v-col cols="6" md="3">
          <v-text-field
            :model-value="ai?.veiculo?.tipo"
            label="Tipo do Veículo"
            readonly
          />
        </v-col>
        <v-col cols="6" md="3">
          <v-text-field
            :model-value="ai?.veiculo?.categoria"
            label="Categoria"
            readonly
          />
        </v-col>
        <v-col cols="12" md="3">
          <v-text-field
            :model-value="ai?.veiculo?.tipo_documento"
            label="Tipo Documento"
            readonly
          />
        </v-col>
        <v-col cols="12" md="3">
          <v-text-field
            :model-value="ai?.veiculo?.numero_documento"
            label="Nº Documento"
            readonly
          />
        </v-col>
        <v-col cols="12" md="6">
          <v-text-field
            :model-value="ai?.veiculo?.nome_razao_social"
            label="Nome/Razão Social"
            readonly
          />
        </v-col>
        <v-col cols="12">
          <v-text-field
            :model-value="ai?.veiculo?.tipo_composicao"
            label="Tipo de Composição"
            readonly
          />
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

const ai = computed(() => store.state.aiResult)

onMounted(() => {
  if (!ai.value) {
    router.push('/')
  }
})
</script>
