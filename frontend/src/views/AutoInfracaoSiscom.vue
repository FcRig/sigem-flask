<template>
  <v-container>
    <!-- Cabeçalho -->
    <v-row>
      <v-col cols="12">
        <v-card class="pa-4" elevation="2">
          <h2>
            Auto de Infração
            <v-chip color="blue" text-color="white">SISCOM</v-chip>
          </h2>
        </v-card>
      </v-col>
    </v-row>
    <v-row class="my-2">
      <v-col cols="12" class="text-right">
        <v-btn color="primary" @click="limparConsulta">Limpar</v-btn>
      </v-col>
    </v-row>

    <!-- Identificação da Infração -->
    <v-card class="pa-4 mb-4" elevation="2">
      <h3 class="pa-4">Identificação da Infração</h3>
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
        <v-col cols="6" md="4">
          <v-text-field
            :model-value="ai?.infracao?.tipo_abordagem"
            label="Abordagem"
            readonly
          />
        </v-col>
      </v-row>
    </v-card>

    <!-- Identificação do Veículo -->
    <v-card class="pa-4" elevation="2">
      <h3 class="pa-4">Identificação do Veículo</h3>
      <v-row dense>
        <v-col cols="12" md="3">
          <v-text-field
            :model-value="ai?.veiculo?.emplacamento"
            label="Emplacamento"
            readonly
          />
        </v-col>
        <v-col cols="12" md="3">
          <v-text-field :model-value="ai?.veiculo?.placa" label="Placa" readonly />
        </v-col>
        <v-col cols="12" md="6">
          <v-text-field :model-value="ai?.veiculo?.chassi" label="Chassi" readonly />
        </v-col>
        <v-col cols="12" md="3">
          <v-text-field :model-value="ai?.veiculo?.renavam" label="Renavam" readonly />
        </v-col>
        <v-col cols="12" md="3">
          <v-text-field :model-value="ai?.veiculo?.pais" label="País" readonly />
        </v-col>
        <v-col cols="12" md="2">
          <v-text-field :model-value="ai?.veiculo?.uf" label="UF" readonly />
        </v-col>
        <v-col cols="12" md="4">
          <v-text-field :model-value="ai?.veiculo?.marca" label="Marca" readonly />
        </v-col>
        <v-col cols="12" md="2">
          <v-text-field :model-value="ai?.veiculo?.outra_marca" label="Outra Marca" readonly />
        </v-col>
        <v-col cols="12" md="6">
          <v-text-field :model-value="ai?.veiculo?.modelo" label="Modelo" readonly />
        </v-col>
        <v-col cols="6" md="3">
          <v-text-field :model-value="ai?.veiculo?.cor" label="Cor" readonly />
        </v-col>
        <v-col cols="6" md="3">
          <v-text-field :model-value="ai?.veiculo?.especie" label="Espécie" readonly />
        </v-col>
        <v-col cols="6" md="3">
          <v-text-field :model-value="ai?.veiculo?.tipo" label="Tipo do Veículo" readonly />
        </v-col>
        <v-col cols="6" md="3">
          <v-text-field :model-value="ai?.veiculo?.categoria" label="Categoria" readonly />
        </v-col>
        <v-col cols="6" md="3">
          <v-text-field :model-value="ai?.veiculo?.tipo_documento" label="Tipo Documento" readonly />
        </v-col>
        <v-col cols="12" md="3">
          <v-text-field :model-value="ai?.veiculo?.numero_documento" label="Nº Documento" readonly />
        </v-col>
        <v-col cols="12" md="6">
          <v-text-field :model-value="ai?.veiculo?.nome_razao_social" label="Nome/Razão Social" readonly />
        </v-col>
        <v-col cols="6" md="3">
          <v-text-field :model-value="ai?.veiculo?.tipo_composicao" label="Tipo de Composição" readonly />
        </v-col>
      </v-row>
    </v-card>

    <!-- Local da Infração -->
    <v-card class="pa-4 mb-4" elevation="2">
      <h3 class="pa-4">Local da Infração</h3>
      <v-row dense>
        <v-col cols="12" md="6">
          <v-text-field
            :model-value="ai?.local?.codigo_municipio_uf"
            label="Código/Município/UF"
            readonly
          />
        </v-col>
        <v-col cols="6" md="3">
          <v-text-field :model-value="ai?.local?.rodovia" label="BR" readonly />
        </v-col>
        <v-col cols="6" md="3">
          <v-text-field :model-value="ai?.local?.km" label="Km" readonly />
        </v-col>
        <v-col cols="6" md="3">
          <v-text-field :model-value="ai?.local?.sentido" label="sentido" readonly />
        </v-col>
        <v-col cols="6" md="3">
          <v-text-field :model-value="ai?.local?.data_hora" label="Data/Hora" readonly />
        </v-col>
      </v-row>
    </v-card>

    <!-- Medições -->
    <v-card class="pa-4 mb-4" elevation="2">
      <h3 class="pa-4">Medições</h3>
      <v-row dense>
        <v-col cols="6" md="3">
          <v-text-field :model-value="ai?.medicoes?.tipo" label="Tipo de medição" readonly />
        </v-col>
        <v-col cols="6" md="3">
          <v-text-field :model-value="ai?.medicoes?.comprovacao" label="Comprovado por" readonly />
        </v-col>
      </v-row>
      <v-row dense>
        <v-col cols="6" md="3">
          <v-text-field :model-value="ai?.medicoes?.realizada" label="Medição realizada" readonly />
        </v-col>
        <v-col cols="6" md="3">
          <v-text-field :model-value="ai?.medicoes?.considerada" label="Valor considerado" readonly />
        </v-col>
        <v-col cols="3" md="3">
          <v-text-field :model-value="ai?.medicoes?.limite" label="Limite regulamentado" readonly />
        </v-col>
        <v-col cols="6" md="3">
          <v-text-field :model-value="ai?.medicoes?.excesso" label="Excesso verificado" readonly />
        </v-col>
      </v-row>
    </v-card>

    <!-- Equipamento -->
    <v-card class="pa-4 mb-4" elevation="2">
      <h3 class="pa-4">Equipamento/Instrumento de aferição utilizado</h3>
      <v-row dense>
        <v-col cols="3" >
          <v-text-field :model-value="ai?.equipamento?.numero" label="Número de série" readonly />
        </v-col>
        <v-col cols="3" >
          <v-text-field :model-value="ai?.equipamento?.descricao" label="Descrição" readonly />
        </v-col>
        <v-col cols="3" >
          <v-text-field :model-value="ai?.equipamento?.marca" label="Marca" readonly />
        </v-col>
        <v-col cols="3" >
          <v-text-field :model-value="ai?.equipamento?.modelo" label="Valor considerado" readonly />
        </v-col>
      </v-row>
    </v-card>

    <!-- Observações -->
    <v-card class="pa-4 mb-4" elevation="2">
      <h3 class="pa-4">Observações</h3>
      <v-row dense>
        <v-col cols="12" >
          <v-textarea :model-value="ai?.observacoes" label="Observações" readonly />
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
