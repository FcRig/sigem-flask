<template>
  <div class="fill-height">
    <v-container fluid>
      <v-row align="center" justify="center">
        <v-col cols="12" sm="8" md="4">
          <v-card class="pa-6 rounded-lg elevation-8">
            <div class="logo-container">
              <img
                src="@/assets/prf_logo.png"
                alt="Logo PRF"
                class="logo"
              />
            </div>

            <v-card-title class="text-h6 text-center mb-4">
              <p>Sistema de Gestão do Núcleo de Multas <br>SIGEM</p>
            </v-card-title>

            <v-form ref="formRef" v-model="formValid">
              <v-text-field
                v-model="email"
                label="Email"
                prepend-inner-icon="mdi-email"
                outlined
                :rules="[rules.required, rules.email]"
                class="mb-4"
              ></v-text-field>

              <v-text-field
                v-model="senha"
                label="Senha"
                prepend-inner-icon="mdi-lock"
                type="password"
                outlined
                :rules="[rules.required]"
                class="mb-6"
              ></v-text-field>

              <v-btn
                color="primary"
                block
                class="mb-2"
                @click="login"
                :disabled="!formValid"
              >
                Entrar
              </v-btn>

              <router-link to="/register" class="registrar">
                <v-btn color="secondary" variant="text" block >
                  Criar conta
                </v-btn>
              </router-link>
            </v-form>

            <v-snackbar
              v-model="successSnackbar"
              color="success"
              location="top right"
              timeout="1500"
              @update:model-value="val => { if (!val) router.push('/') }"
            >
              {{ successMsg }}
            </v-snackbar>

            <v-snackbar
              v-model="errorSnackbar"
              color="error"
              location="top right"
              timeout="3000"
            >
              {{ errorMsg }}
            </v-snackbar>

            <v-card-subtitle class="text-center mt-6 caption">
              © {{ year }} Polícia Rodoviária Federal
            </v-card-subtitle>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useStore } from 'vuex'
import { loginUser } from '../services/api'

const email = ref('')
const senha = ref('')
const formRef = ref(null)
const formValid = ref(false)
const year = new Date().getFullYear()
const router = useRouter()
const route = useRoute()
const store = useStore()
const successSnackbar = ref(false)
const successMsg = ref('')
const errorSnackbar = ref(false)
const errorMsg = ref('')

const rules = {
  required: v => !!v || 'Campo obrigatório',
  email: v => /.+@.+\..+/.test(String(v)) || 'E-mail inválido'
}

async function login() {
  if (!formRef.value?.validate()) return
  try {
    const { data } = await loginUser({ email: email.value, password: senha.value })
    store.commit('setToken', data.access_token)
    await store.dispatch('fetchCurrentUser')
    successMsg.value = 'Login realizado com sucesso'
    successSnackbar.value = true
  } catch (err) {
    errorMsg.value = err.response?.data?.msg || 'Erro ao fazer login'
    errorSnackbar.value = true
    console.error(err)
  }
}

function handleQueryError(error) {
  if (error === 'unauthorized') {
    errorMsg.value = 'Faça login para continuar'
  } else if (error === 'not_found') {
    errorMsg.value = 'Página não encontrada'
  } else {
    errorMsg.value = 'Erro desconhecido'
  }
  errorSnackbar.value = true
}

onMounted(() => {
  if (route.query.error) {
    handleQueryError(route.query.error)
  }
})

watch(
  () => route.query.error,
  val => {
    if (val) handleQueryError(val)
  }
)
</script>

<style scoped>
.fill-height {
  min-height: 100vh;
  background: #e4e5e6;
}

.logo-container {
  display: flex;
  justify-content: center;
  margin-bottom: 24px;
}

.logo {
  width: 140px;
  height: auto;
}

.registrar {
  text-decoration: none;
}
</style>
