<template>
  <v-navigation-drawer v-model="drawer" color="#f5f5f5" class="app-sidebar">
    <v-list-item dense>
      <v-list-item-content>
        <v-list-item-title class="text-h6">PRF</v-list-item-title>
        <v-list-item-subtitle>NPI-RS</v-list-item-subtitle>
      </v-list-item-content>
    </v-list-item>

    <v-divider></v-divider>

    <v-list density="compact" nav>
      <v-list-item title="Home" prepend-icon="mdi-home" to="/"></v-list-item>
      <v-list-group value="autoprf">
        <template #activator="{ props }">
          <v-list-item
            v-bind="props"
            prepend-icon="mdi-car"
            title="AutoPRF"
          />
        </template>
        <v-list-item
          title="Autenticação"
          prepend-icon="mdi-lock"
          @click="autoprfDialog = true"
        />
        <v-list-item
          title="Pesquisar AI"
          prepend-icon="mdi-magnify"
          @click="autoprfPesquisaDialog = true"
        />
        <v-list-group value="autoprf-cancel">
          <template #activator="{ props }">
            <v-list-item
              v-bind="props"
              prepend-icon="mdi-cancel"
              title="Cancelamentos"
            />
          </template>
          <v-list-item
            title="Veículos de Emergência"
            prepend-icon="mdi-ambulance"
            to="/cancelamentos/veiculos-emergencia"
          />
          <v-list-item
            title="Duplicidade"
            prepend-icon="mdi-content-duplicate"
            to="/cancelamentos/duplicidade"
          />
        </v-list-group>
      </v-list-group>

      <v-list-group value="siscom">
        <template #activator="{ props }">
          <v-list-item
            v-bind="props"
            prepend-icon="mdi-laptop"
            title="SISCOM"
          />
        </template>
        <v-list-item
          title="Autenticação"
          prepend-icon="mdi-lock"
          @click="siscomDialog = true"
        />
        <v-list-item
          title="Pesquisar AI"
          prepend-icon="mdi-magnify"
          @click="siscomPesquisaDialog = true"
        />
      </v-list-group>

      <v-list-group value="sei">
        <template #activator="{ props }">
          <v-list-item
            v-bind="props"
            prepend-icon="mdi-file-document"
            title="SEI"
          />
        </template>
        <v-list-item
          title="Autenticação"
          prepend-icon="mdi-lock"
          @click="seiDialog = true"
        />
      </v-list-group>
    </v-list>

      <v-dialog v-model="autoprfDialog" max-width="400">
        <v-card>
          <v-card-title>Autenticação AutoPRF</v-card-title>
          <v-card-text>
            <v-form ref="autoprfForm" v-model="autoprfValid">
              <v-text-field v-model="autoprfSenha" label="Senha AutoPRF" type="password" :rules="[rules.required]" />
              <v-text-field v-model="autoprfToken" label="Token AutoPRF" />
            </v-form>
          </v-card-text>
          <v-card-actions>
            <v-spacer />
            <v-btn text @click="autoprfDialog = false">Cancelar</v-btn>
            <v-btn color="primary" :disabled="!autoprfValid" @click="saveAutoprf">Salvar</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>

      <v-dialog v-model="autoprfPesquisaDialog" max-width="400">
        <v-card>
          <v-card-title>Pesquisar Auto de Infração</v-card-title>
          <v-card-text>
            <v-form ref="autoprfPesquisaForm" v-model="autoprfPesquisaValid">
              <v-text-field v-model="autoInfracao" label="Número do AI" :rules="[rules.required]" />
            </v-form>
          </v-card-text>
          <v-card-actions>
            <v-spacer />
            <v-btn text @click="autoprfPesquisaDialog = false">Cancelar</v-btn>
            <v-btn color="primary" :disabled="!autoprfPesquisaValid" @click="pesquisarAI">Pesquisar</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>

      <v-dialog v-model="siscomPesquisaDialog" max-width="400">
        <v-card>
          <v-card-title>Pesquisar Auto de Infração</v-card-title>
          <v-card-text>
            <v-form ref="siscomPesquisaForm" v-model="siscomPesquisaValid">
              <v-text-field v-model="siscomNumeroAi" label="Número do AI" :rules="[rules.required]" />
            </v-form>
          </v-card-text>
          <v-card-actions>
            <v-spacer />
            <v-btn text @click="siscomPesquisaDialog = false">Cancelar</v-btn>
            <v-btn color="primary" :disabled="!siscomPesquisaValid" @click="pesquisarSiscomAi">Pesquisar</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>

    <v-dialog v-model="siscomDialog" max-width="400">
      <v-card>
        <v-card-title>Autenticação SISCOM</v-card-title>
        <v-card-text>
          <v-form ref="siscomForm" v-model="siscomValid">
            <v-text-field v-model="siscomSenha" label="Senha SISCOM" type="password" :rules="[rules.required]" />
          </v-form>
        </v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn text @click="siscomDialog = false">Cancelar</v-btn>
          <v-btn color="primary" :disabled="!siscomValid" @click="saveSiscom">Salvar</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <v-dialog v-model="seiDialog" max-width="400">
      <v-card>
        <v-card-title>Autenticação SEI</v-card-title>
        <v-card-text>
          <v-form ref="seiForm" v-model="seiValid">
            <v-text-field v-model="seiSenha" label="Senha SEI" type="password" :rules="[rules.required]" />
            <v-text-field v-model="seiToken" label="Token SEI" />
          </v-form>
        </v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn text @click="seiDialog = false">Cancelar</v-btn>
          <v-btn color="primary" :disabled="!seiValid" @click="saveSei">Salvar</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <v-snackbar
      v-model="snackbar"
      :color="snackbarColor"
      location="top right"
      timeout="1500"
    >
      {{ snackbarMsg }}
    </v-snackbar>
  </v-navigation-drawer>
</template>

<script setup>
import { computed, ref } from 'vue'
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'
import { updateUser } from '../services/users'
import { autoprfLogin, pesquisarAutoInfracao } from '../services/autoprf'
import { pesquisarAi as pesquisarSiscom } from '../services/siscom'

const props = defineProps({
  modelValue: {
    type: Boolean,
    required: true
  }
})
const emit = defineEmits(['update:modelValue'])

const drawer = computed({
  get: () => props.modelValue,
  set: val => emit('update:modelValue', val)
})

const store = useStore()
const router = useRouter()

const autoprfDialog = ref(false)
const autoprfPesquisaDialog = ref(false)
const siscomPesquisaDialog = ref(false)
const siscomDialog = ref(false)
const seiDialog = ref(false)

const autoprfSenha = ref('')
const autoprfToken = ref('')
const siscomSenha = ref('')
const seiSenha = ref('')
const seiToken = ref('')
const autoInfracao = ref('')
const siscomNumeroAi = ref('')

const autoprfForm = ref(null)
const autoprfValid = ref(false)
const autoprfPesquisaForm = ref(null)
const autoprfPesquisaValid = ref(false)
const siscomPesquisaForm = ref(null)
const siscomPesquisaValid = ref(false)
const siscomForm = ref(null)
const siscomValid = ref(false)
const seiForm = ref(null)
const seiValid = ref(false)

const snackbar = ref(false)
const snackbarMsg = ref('')
const snackbarColor = ref('success')

const rules = {
  required: v => !!v || 'Campo obrigatório'
}

async function saveAutoprf() {
  if (!autoprfForm.value?.validate()) return
  try {
    await updateUser(store.state.user.id, {
      senha_autoprf: autoprfSenha.value,
      token_autoprf: autoprfToken.value
    })
    await autoprfLogin({
      senha_autoprf: autoprfSenha.value,
      token_autoprf: autoprfToken.value
    })
    snackbarMsg.value = 'Dados AutoPRF salvos com sucesso'
    snackbarColor.value = 'success'
    snackbar.value = true
    autoprfDialog.value = false
  } catch (err) {
    snackbarMsg.value = err.response?.data?.msg || 'Erro ao salvar dados AutoPRF'
    snackbarColor.value = 'error'
    snackbar.value = true
  }
}

async function pesquisarAI() {
  if (!autoprfPesquisaForm.value?.validate()) return
  try {
    const { data } = await pesquisarAutoInfracao({ auto_infracao: autoInfracao.value })
    store.commit('setAiResult', data)
    snackbarMsg.value = 'Pesquisa enviada com sucesso'
    snackbarColor.value = 'success'
    snackbar.value = true
    autoprfPesquisaDialog.value = false
    autoInfracao.value = ''
    router.push('/resultado-ai')
  } catch (err) {
    snackbarMsg.value = err.response?.data?.msg || 'Erro ao pesquisar AI'
    snackbarColor.value = 'error'
    snackbar.value = true
  }
}

async function pesquisarSiscomAi() {
  if (!siscomPesquisaForm.value?.validate()) return
  try {
    const { data } = await pesquisarSiscom({ numero: siscomNumeroAi.value })
    store.commit('setSiscomAiResult', data)
    snackbarMsg.value = 'Pesquisa enviada com sucesso'
    snackbarColor.value = 'success'
    snackbar.value = true
    siscomPesquisaDialog.value = false
    siscomNumeroAi.value = ''
    router.push('/resultado-ai-siscom')
  } catch (err) {
    snackbarMsg.value = err.response?.data?.msg || 'Erro ao pesquisar AI'
    snackbarColor.value = 'error'
    snackbar.value = true
  }
}

async function saveSiscom() {
  if (!siscomForm.value?.validate()) return
  try {
    await updateUser(store.state.user.id, {
      senha_siscom: siscomSenha.value
    })
    snackbarMsg.value = 'Dados SISCOM salvos com sucesso'
    snackbarColor.value = 'success'
    snackbar.value = true
    siscomDialog.value = false
  } catch (err) {
    snackbarMsg.value = err.response?.data?.msg || 'Erro ao salvar dados SISCOM'
    snackbarColor.value = 'error'
    snackbar.value = true
  }
}

async function saveSei() {
  if (!seiForm.value?.validate()) return
  try {
    await updateUser(store.state.user.id, {
      senha_sei: seiSenha.value,
      token_sei: seiToken.value
    })
    snackbarMsg.value = 'Dados SEI salvos com sucesso'
    snackbarColor.value = 'success'
    snackbar.value = true
    seiDialog.value = false
  } catch (err) {
    snackbarMsg.value = err.response?.data?.msg || 'Erro ao salvar dados SEI'
    snackbarColor.value = 'error'
    snackbar.value = true
  }
}
</script>

<style scoped>
  .app-sidebar .v-list-group__items .v-list-item {
    padding-inline-start: 18px !important;
  }

  .app-sidebar .v-list-group__items .v-list-item__prepend {
    margin-inline-start: 0 !important;
    margin-inline-end: 8px !important;
  }
</style>

