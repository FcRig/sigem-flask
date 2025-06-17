<template>
  <div class="fill-height">
    <v-container fluid>
      <v-row align="center" justify="center">
          <v-col cols="12" sm="8" md="4">
            <v-card class="pa-6 rounded-lg elevation-8">
              <div class="logo-container">
                <img
                  src="https://auto.prf.gov.br/assets/logo-PRF.8d8f70ac.svg"
                  alt="Logo PRF"
                  class="logo"
                >
              </div>

              <v-card-title class="text-h6 text-center mb-4">
                Sistema de Gestão do Núcleo de Multas – SIGEM
              </v-card-title>

              <v-form ref="formRef" v-model="formValid">
                <v-text-field
                  v-model="cpf"
                  label="CPF"
                  prepend-inner-icon="mdi-account"
                  maxlength="14"
                  outlined
                  :rules="[rules.required, rules.cpf]"
                  class="mb-4"
                ></v-text-field>

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
                  @click="register"
                  :disabled="!formValid"
                >
                  Cadastrar
                </v-btn>

                <router-link to="/login">
                  <v-btn color="secondary" variant="text" block>
                    Já possui conta? Entrar
                  </v-btn>
                </router-link>
              </v-form>

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
import { ref } from 'vue'
import { registerUser } from '../services/api'

const cpf = ref('')
const email = ref('')
const senha = ref('')
const formRef = ref(null)
const formValid = ref(false)
const year = new Date().getFullYear()

const rules = {
  required: v => !!v || 'Campo obrigatório',
  email: v => /.+@.+\..+/.test(String(v)) || 'E-mail inválido',
  cpf: v => {
    const digits = String(v || '').replace(/\D/g, '')
    return digits.length === 11 || 'CPF inválido'
  }
}

function register() {
  if (!formRef.value?.validate()) return
  registerUser({ username: cpf.value, email: email.value, password: senha.value })
    .then(() => console.log('registrado'))
    .catch(err => console.error(err))
}
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
</style>
