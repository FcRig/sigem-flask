<template>
  <v-app-bar color="primary" dark>
    <v-app-bar-nav-icon @click="$emit('toggle-drawer')" />
    <v-toolbar-title>Sistema de Gestão do Núcleo de Multas - SIGEM</v-toolbar-title>
    <v-spacer></v-spacer>
    <v-menu v-if="user" offset-y>
      <template #activator="{ props }">
        <v-btn v-bind="props" icon>
          <v-icon>mdi-account</v-icon>
        </v-btn>
      </template>
      <v-list>
        <v-list-item>
          <v-list-item-title>{{ user.name }}</v-list-item-title>
        </v-list-item>
        <v-list-item link>
          <v-list-item-title>Administradores</v-list-item-title>
        </v-list-item>
        <v-list-item @click="$emit('logout')">
          <v-list-item-title>Logout</v-list-item-title>
        </v-list-item>
      </v-list>
    </v-menu>
  </v-app-bar>
</template>

<script>
export default {
  name: 'AppHeader',
  props: {
    user: Object
  }
};
</script>
