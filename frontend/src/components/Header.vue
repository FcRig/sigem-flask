<template>
  <v-app-bar color="#150958" dense>
    <v-app-bar-nav-icon v-if="user" @click="$emit('toggle-drawer')" />
    <v-card class="pa-6 rounded-lg elevation-8" color="#150958" to="/">
      <div class="logo-container">
        <img
          src="@/assets/prf.png"
          alt="PRF"
          class="logo"
        />
      </div>
    </v-card>
    <v-toolbar-title class="text-h5">Sistema de Gestão do Núcleo de Multas - SIGEM</v-toolbar-title>    
    <v-menu v-if="user" offset-y>
      <template #activator="{ props }">
        <v-btn v-bind="props" class="d-flex align-center" variant="text">
          <v-icon class="mr-2">mdi-account-circle</v-icon>
          <span>{{ user.username }}</span>
        </v-btn>
      </template>
      <v-list>        
        <v-list-item v-if="user.administrador" link :to="'/admin/users'">
          <v-list-item-title>Administração</v-list-item-title>
        </v-list-item>
        <v-list-item @click="$emit('logout')">
          <v-list-item-title>Logout</v-list-item-title>
        </v-list-item>
      </v-list>
    </v-menu>
  </v-app-bar>
</template>

<script setup>
defineProps({
  user: Object
})

defineEmits(['toggle-drawer', 'logout'])
</script>

<style>
.logo-container {
  display: flex;
  justify-content: center; 
}

.logo {
  width: 100px;
  height: auto;
}</style>
