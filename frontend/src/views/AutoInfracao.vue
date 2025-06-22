<template>
  <v-container>
    <v-card class="mb-4">
      <v-card-title>Identificação da Infração</v-card-title>
      <v-card-text>
        <p><strong>Código/Descrição da Infração:</strong> {{ data.infracao?.codigo_descricao }}</p>
        <p><strong>Amparo Legal:</strong> {{ data.infracao?.amparo_legal }}</p>
        <p><strong>Gravidade:</strong> {{ data.infracao?.gravidade }}</p>
        <p><strong>Tipo de infrator:</strong> {{ data.infracao?.tipo_infrator }}</p>
        <p><strong>Tipo de abordagem:</strong> {{ data.infracao?.tipo_abordagem }}</p>
      </v-card-text>
    </v-card>

    <v-card class="mb-4">
      <v-card-title>Identificação do veículo</v-card-title>
      <v-card-text>
        <p><strong>Emplacamento:</strong> {{ data.veiculo?.emplacamento }}</p>
        <p><strong>Placa:</strong> {{ data.veiculo?.placa }}</p>
        <p><strong>Chassi:</strong> {{ data.veiculo?.chassi }}</p>
        <p><strong>Renavam:</strong> {{ data.veiculo?.renavam }}</p>
        <p><strong>País:</strong> {{ data.veiculo?.pais }}</p>
        <p><strong>UF:</strong> {{ data.veiculo?.uf }}</p>
        <p><strong>Marca:</strong> {{ data.veiculo?.marca }}</p>
        <p><strong>Outra marca:</strong> {{ data.veiculo?.outra_marca }}</p>
        <p><strong>Modelo:</strong> {{ data.veiculo?.modelo }}</p>
        <p><strong>Cor:</strong> {{ data.veiculo?.cor }}</p>
        <p><strong>Espécie:</strong> {{ data.veiculo?.especie }}</p>
        <p><strong>Tipo do veículo:</strong> {{ data.veiculo?.tipo }}</p>
        <p><strong>Categoria:</strong> {{ data.veiculo?.categoria }}</p>
        <p><strong>Tipo do documento:</strong> {{ data.veiculo?.tipo_documento }}</p>
        <p><strong>Nº do documento:</strong> {{ data.veiculo?.numero_documento }}</p>
        <p><strong>Nome/Razão Social:</strong> {{ data.veiculo?.nome_razao_social }}</p>
        <p><strong>Tipo de composição:</strong> {{ data.veiculo?.tipo_composicao }}</p>
      </v-card-text>
    </v-card>

    <v-card>
      <v-card-title>Local da infração</v-card-title>
      <v-card-text>
        <p><strong>Código/Município/UF:</strong> {{ data.local?.codigo_municipio_uf }}</p>
      </v-card-text>
    </v-card>
  </v-container>
</template>

<script setup>
import { computed } from 'vue'
import { useStore } from 'vuex'

const store = useStore()
const data = computed(() => store.state.aiResult || {})
</script>
