@@ -44,66 +44,75 @@
                  @click="login"
                  :disabled="!formValid"
                >
                  Entrar
                </v-btn>

                <router-link to="/register">
                  <v-btn color="secondary" variant="text" block>
                    Criar conta
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
import { useRouter } from 'vue-router'
import { useStore } from 'vuex'
import { loginUser } from '../services/api'

const cpf = ref('')
const senha = ref('')
const formRef = ref(null)
const formValid = ref(false)
const year = new Date().getFullYear()
const router = useRouter()
const store = useStore()

const rules = {
  required: v => !!v || 'Campo obrigatório',
  cpf: v => {
    const digits = String(v || '').replace(/\D/g, '')
    return digits.length === 11 || 'CPF inválido'
  }
}

function login() {
async function login() {
  if (!formRef.value?.validate()) return
  loginUser({ username: cpf.value, password: senha.value })
    .then(() => console.log('logado'))
    .catch(err => console.error(err))
  try {
    const { data } = await loginUser({ username: cpf.value, password: senha.value })
    store.commit('setToken', data.access_token)
    await store.dispatch('fetchCurrentUser')
    router.push('/')
  } catch (err) {
    console.error(err)
  }
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
