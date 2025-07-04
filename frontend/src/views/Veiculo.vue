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

    <template v-if="result">
      <v-card class="pa-4 mb-4" elevation="2">
        <h3 class="pa-4">Dados do Veículo</h3>
        <v-row dense>
          <v-col cols="12" md="3">
            <v-text-field
              :model-value="result.anoFabricacao"
              label="Ano de Fabricação"
              readonly
            />
          </v-col>
          <v-col cols="12" md="3">
            <v-text-field
              :model-value="result.anoModelo"
              label="Ano do Modelo"
              readonly
            />
          </v-col>         
          <v-col cols="12" md="3">
            <v-text-field
              :model-value="result.capacidadeMaximaDeTracao"
              label="Capacitada Máxima de Tração (CMT)"
              readonly
            />
          </v-col>
          <v-col cols="12" md="3">
            <v-text-field
              :model-value="result.capacidadePassageiros"
              label="Capacidade Máxima de Passageiros"
              readonly
            />
          </v-col>
          <v-col cols="12" md="3">
            <v-text-field :model-value="result.categoria" label="Categoria" readonly />
          </v-col>
          <v-col cols="12" md="3">
            <v-text-field :model-value="result.chassi" label="Chassi" readonly />
          </v-col>
          <v-col cols="12" md="3">
            <v-text-field :model-value="result.cilindradas" label="Cilindradas" readonly />
          </v-col>
          <v-col cols="12" md="3">
            <v-text-field :model-value="result.cor" label="Cor" readonly />
          </v-col>
          <v-col cols="12" md="3">
            <v-text-field :model-value="result.combustivel" label="Combustível" readonly />
          </v-col>          
          <v-col cols="12" md="3">
            <v-text-field
              :model-value="tipoDocumentoProprietario"
              label="Tipo de Documento do Proprietário"
              readonly
            />
          </v-col>
          <v-col cols="12" md="3">
            <v-text-field
              :model-value="documentoProprietario"
              label="Documento do Proprietário"
              readonly
            />
          </v-col>
          <v-col cols="12" md="3">
            <v-text-field :model-value="result.marcaModelo" label="Marca/Modelo" readonly />
          </v-col>
          <v-col cols="12" md="3">
            <v-text-field
              :model-value="result.municipioEmplacamento"
              label="Município de Emplacamento"
              readonly
            />
          </v-col>
          <v-col cols="12" md="9">
            <v-text-field :model-value="result.nomeProprietario" label="Proprietário(a)" readonly />
          </v-col>
          <v-col cols="12" md="3">
            <v-text-field :model-value="result.pais" label="País" readonly />
          </v-col>
          <v-col cols="12" md="3">
            <v-text-field :model-value="result.pesoBrutoTotal" label="Peso Bruto Total (PBT)" readonly />
          </v-col>
          <v-col cols="12" md="3">
            <v-text-field :model-value="result.placa" label="Placa" readonly />
          </v-col>
          <v-col cols="12" md="3">
            <v-text-field :model-value="result.procedenciaVeiculo" label="Procedência" readonly />
          </v-col>
          
          <v-col cols="12" md="6">
            <v-text-field :model-value="restricao1" label="Restrição" readonly />
          </v-col>
          <v-col cols="12" md="6">
            <v-text-field :model-value="restricao2" label="Restrição" readonly />
          </v-col>
          <v-col cols="12" md="6">
            <v-text-field :model-value="restricao3" label="Restrição" readonly />
          </v-col>
          <v-col cols="12" md="6">
            <v-text-field :model-value="restricao4" label="Restrição" readonly />
          </v-col>
          <v-col cols="12" md="3">
            <v-text-field :model-value="result.renavam" label="Renavam" readonly />
          </v-col>
          <v-col cols="12" md="3">
            <v-text-field :model-value="situacaoVeiculo" label="Situação do Veículo" readonly />
          </v-col>
          <v-col cols="12" md="3">
            <v-text-field :model-value="result.tipo" label="Tipo" readonly />
          </v-col>
          <v-col cols="12" md="3">
            <v-text-field
              :model-value="result.ufEmplacamento"
              label="UF de Emplacamento"
              readonly
            />
          </v-col>
        </v-row>
      </v-card>
    </template>
  </v-container>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useVeiculoFormatter } from '../mixins/useVeiculoFormatter'
import { useStore } from 'vuex'
import { onBeforeRouteLeave } from 'vue-router'

const store = useStore()

const placa = ref('')
const formRef = ref(null)
const valid = ref(false)

const result = computed(() => store.state.veiculoResult)

const {
  tipoDocumentoProprietario,
  documentoProprietario,
  situacaoVeiculo,
  restricao1,
  restricao2,
  restricao3,
  restricao4,
} = useVeiculoFormatter(result)

const rules = { required: v => !!v || 'Campo obrigatório' }

function formatLabel(key) {
  return (key || '')
    .replace(/_/g, ' ')
    .replace(/(?:^|\s)\w/g, l => l.toUpperCase())
}

async function buscar() {
  if (!formRef.value?.validate()) return
  try {
    await store.dispatch('consultarPlaca', { placa: placa.value.trim() })
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

onBeforeRouteLeave(() => {
  limpar()
})
</script>

