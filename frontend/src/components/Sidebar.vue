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
          to="/resultado-ai"
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
          to="/resultado-ai-siscom"
        />
        <v-list-group value="siscom-cancel">
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
            to="/siscom/cancelamentos/veiculos-emergencia"
          />
          <v-list-item
            title="Duplicidade"
            prepend-icon="mdi-content-duplicate"
            to="/siscom/cancelamentos/duplicidade"
          />
        </v-list-group>
      <v-list-item
        title="Histórico"
        prepend-icon="mdi-history"
        to="/historico-siscom"
      />
    </v-list-group>

    <v-list-item
      title="Veículo"
      prepend-icon="mdi-car"
      to="/veiculo"
    />

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
        <v-list-item
          title="Criar Processo"
          prepend-icon="mdi-plus-box"
          to="/sei/criar-processo"
        />

        <v-list-item title="Criar Despacho" 
        prepend-icon="mdi-plus-box" 
        to="/sei/criar-despacho" />


      </v-list-group>
    </v-list>

      <v-dialog v-model="autoprfDialog" max-width="400">
        <v-card>
          <v-card-title>Autenticação AutoPRF</v-card-title>
          <v-card-text>
            <v-form ref="autoprfForm" v-model="autoprfValid">
              <v-text-field
                v-model="autoprfPassword"
                label="Senha AutoPRF"
                type="password"
                :rules="[rules.required]"
              />
              <v-text-field
                v-model="autoprfToken"
                label="Token AutoPRF"
                :rules="[rules.required]"
              />
            </v-form>
          </v-card-text>
          <v-card-actions>
            <v-spacer />
            <v-btn color="primary" :disabled="!autoprfValid" @click="saveAutoprf">Salvar</v-btn>
            <v-btn text @click="autoprfDialog = false; autoprfPassword = ''">Cancelar</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>



    <v-dialog v-model="siscomDialog" max-width="400">
      <v-card>
        <v-card-title>Autenticação SISCOM</v-card-title>
        <v-card-text>
            <v-form ref="siscomForm" v-model="siscomValid">
              <v-text-field v-model="siscomPassword" label="Senha SISCOM" type="password" :rules="[rules.required]" />
            </v-form>
        </v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn color="primary" :disabled="!siscomValid" @click="saveSiscom">Salvar</v-btn>
          <v-btn text @click="siscomDialog = false; siscomPassword = ''">Cancelar</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <v-dialog v-model="seiDialog" max-width="400">
      <v-card>
        <v-card-title>Autenticação SEI</v-card-title>
        <v-card-text>
            <v-form ref="seiForm" v-model="seiValid">
              <v-text-field v-model="seiUsuario" label="Usuário" :rules="[rules.required]" />
              <v-text-field
              v-model="seiPassword"
              label="Senha SEI"
              type="password"
              :rules="[rules.required]"
              />
              <v-text-field v-model="seiToken" label="Token SEI" :rules="[rules.required]" />
            </v-form>
        </v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn color="primary" :disabled="!seiValid" @click="saveSei">Salvar</v-btn>
          <v-btn text @click="seiDialog = false; seiPassword = ''">Cancelar</v-btn>
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

import { updateUser } from '../services/users'
import { autoprfLogin } from '../services/autoprf'
import { siscomLogin } from '../services/siscom'
import { seiLogin } from '../services/sei'

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

const autoprfDialog = ref(false)
const siscomDialog = ref(false)
const seiDialog = ref(false)

const autoprfToken = ref('')
const autoprfPassword = ref('')
const siscomPassword = ref('')
const seiUsuario = ref('')
const seiToken = ref('')
const seiPassword = ref('')


const autoprfForm = ref(null)
const autoprfValid = ref(false)
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
      token_autoprf: autoprfToken.value
    })
    await autoprfLogin({
      token_autoprf: autoprfToken.value,
      senha_autoprf: autoprfPassword.value
    })
    autoprfPassword.value = ''
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

async function saveSiscom() {
  if (!siscomForm.value?.validate()) return
  try {
    await siscomLogin({ senha_siscom: siscomPassword.value })
    siscomPassword.value = ''
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
      usuario_sei: seiUsuario.value,
      token_sei: seiToken.value
    })
    await seiLogin({
      usuario: seiUsuario.value,
      senha_sei: seiPassword.value,
      token_sei: seiToken.value
    })
    seiPassword.value = ''
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

