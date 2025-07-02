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
      <v-card class="pa-4 mb-4" elevation="2">
        <h3 class="pa-4">Dados do Veículo</h3>
        <v-row dense>
          <v-col cols="12" md="4">
            <v-text-field
              :model-value="result.ano_fabricacao"
              label="Ano de Fabricação"
              readonly
            />
          </v-col>
          <v-col cols="12" md="4">
            <v-text-field
              :model-value="result.ano_modelo"
              label="Ano do Modelo"
              readonly
            />
          </v-col>
          <v-col cols="12" md="4">
            <v-text-field
              :model-value="result.ano_ultimo_licenciamento"
              label="Ano do Último Licenciamento"
              readonly
            />
          </v-col>
          <v-col cols="12" md="4">
            <v-text-field
              :model-value="result.capacidade_carga"
              label="Capacidade de Carga"
              readonly
            />
          </v-col>
          <v-col cols="12" md="4">
            <v-text-field
              :model-value="result.cmt"
              label="Capacitada Máxima de Tração (CMT)"
              readonly
            />
          </v-col>
          <v-col cols="12" md="4">
            <v-text-field
              :model-value="result.capacidade_maxima_passageiros"
              label="Capacidade Máxima de Passageiros"
              readonly
            />
          </v-col>
          <v-col cols="12" md="4">
            <v-text-field :model-value="result.categoria" label="Categoria" readonly />
          </v-col>
          <v-col cols="12" md="6">
            <v-text-field :model-value="result.chassi" label="Chassi" readonly />
          </v-col>
          <v-col cols="12" md="4">
            <v-text-field :model-value="result.cilindradas" label="Cilindradas" readonly />
          </v-col>
          <v-col cols="12" md="4">
            <v-text-field :model-value="result.cor" label="Cor" readonly />
          </v-col>
          <v-col cols="12" md="6">
            <v-text-field :model-value="result.combustivel" label="Combustível" readonly />
          </v-col>
          <v-col cols="12" md="4">
            <v-text-field
              :model-value="result.tipo_documento_proprietario"
              label="Tipo do Documento do Proprietário"
              readonly
            />
          </v-col>
          <v-col cols="12" md="6">
            <v-text-field
              :model-value="result.documento_proprietario"
              label="Documento do Proprietário"
              readonly
            />
          </v-col>
          <v-col cols="12" md="6">
            <v-text-field :model-value="result.marca_modelo" label="Marca/Modelo" readonly />
          </v-col>
          <v-col cols="12" md="6">
            <v-text-field
              :model-value="result.municipio_emplacamento"
              label="Município de Emplacamento"
              readonly
            />
          </v-col>
          <v-col cols="12" md="6">
            <v-text-field :model-value="result.proprietario" label="Proprietário(a)" readonly />
          </v-col>
          <v-col cols="12" md="4">
            <v-text-field :model-value="result.pais" label="País" readonly />
          </v-col>
          <v-col cols="12" md="4">
            <v-text-field :model-value="result.pbt" label="Peso Bruto Total (PBT)" readonly />
          </v-col>
          <v-col cols="12" md="4">
            <v-text-field :model-value="result.placa" label="Placa" readonly />
          </v-col>
          <v-col cols="12" md="4">
            <v-text-field :model-value="result.procedencia" label="Procedência" readonly />
          </v-col>
          <v-col cols="12" md="4">
            <v-text-field
              :model-value="result.quantidade_multas"
              label="Quantidade de Multas"
              readonly
            />
          </v-col>
          <v-col cols="12" md="4">
            <v-text-field :model-value="result.renavam" label="Renavam" readonly />
          </v-col>
          <v-col cols="12" md="6">
            <v-text-field :model-value="result.restricao" label="Restrição" readonly />
          </v-col>
          <v-col cols="12" md="6">
            <v-text-field :model-value="result.situacao_veiculo" label="Situação do Veículo" readonly />
          </v-col>
          <v-col cols="12" md="6">
            <v-text-field :model-value="result.tipo" label="Tipo" readonly />
          </v-col>
          <v-col cols="12" md="4">
            <v-text-field
              :model-value="result.uf_emplacamento"
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

