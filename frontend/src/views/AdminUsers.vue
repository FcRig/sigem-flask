<template>
  <v-container>
    <v-card>
      <v-card-title>Usuários cadastrados</v-card-title>
      <v-data-table :items="users" :headers="headers" item-key="id">
        <template #item.administrador="{ item }">
          {{ item.administrador ? 'Sim' : 'Não' }}
        </template>
        <template #item.actions="{ item }">
          <v-btn icon="mdi-pencil" size="small" @click="openEdit(item)" />
          <v-btn icon="mdi-delete" size="small" color="red" @click="removeUser(item)" />
        </template>
      </v-data-table>
    </v-card>

    <v-dialog v-model="editDialog" max-width="400">
      <v-card>
        <v-card-title>Editar usuário</v-card-title>
        <v-card-text>
          <v-form ref="formRef" v-model="formValid">
            <v-text-field
              v-model="editUser.username"
              label="Usuário"
              :rules="[rules.required]"
            ></v-text-field>
            <v-text-field
              v-model="editUser.email"
              label="Email"
              :rules="[rules.required, rules.email]"
            ></v-text-field>
            <v-checkbox
              v-model="editUser.administrador"
              label="Administrador"
            ></v-checkbox>
            <v-text-field
              v-model="editUser.password"
              label="Senha"
              type="password"
            ></v-text-field>
          </v-form>
        </v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn text @click="editDialog = false">Cancelar</v-btn>
          <v-btn color="primary" :disabled="!formValid" @click="saveEdit">Salvar</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <v-dialog v-model="deleteDialog" max-width="400">
      <v-card>
        <v-card-title>Remover usuário</v-card-title>
        <v-card-text>Confirma remover este usuário?</v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn text @click="deleteDialog = false">Cancelar</v-btn>
          <v-btn color="red" @click="confirmDelete">Remover</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { fetchUsers, updateUser, deleteUser } from '../services/api'

const users = ref([])
const editDialog = ref(false)
const deleteDialog = ref(false)
const deleteId = ref(null)
const editUser = ref({ id: null, username: '', email: '', administrador: false, password: '' })
const formRef = ref(null)
const formValid = ref(false)

const headers = [
  { title: 'ID', key: 'id' },
  { title: 'Usuário', key: 'username' },
  { title: 'Email', key: 'email' },
  { title: 'Administrador', key: 'administrador' },
  { title: 'Ações', key: 'actions', sortable: false },
]

const rules = {
  required: v => !!v || 'Campo obrigatório',
  email: v => /.+@.+\..+/.test(String(v)) || 'E-mail inválido',
}

async function loadUsers() {
  const { data } = await fetchUsers()
  users.value = data
}

function openEdit(item) {
  editUser.value = { id: item.id, username: item.username, email: item.email, administrador: item.administrador, password: '' }
  editDialog.value = true
}

async function saveEdit() {
  if (!formRef.value?.validate()) return
  const payload = { username: editUser.value.username, email: editUser.value.email }
  payload.administrador = editUser.value.administrador
  if (editUser.value.password) payload.password = editUser.value.password
  await updateUser(editUser.value.id, payload)
  editDialog.value = false
  await loadUsers()
}

function removeUser(item) {
  deleteId.value = item.id
  deleteDialog.value = true
}

async function confirmDelete() {
  await deleteUser(deleteId.value)
  deleteDialog.value = false
  await loadUsers()
}

onMounted(loadUsers)
</script>
