<template>
  <v-app>
    <AppHeader />
    <v-main>
      <slot />
    </v-main>
    <AppFooter />
    <AppModal v-model="showModal">
      <slot name="modal" />
    </AppModal>
  </v-app>
</template>

<script setup>
import { ref } from 'vue'
import AppHeader from '../components/Header.vue'
import AppFooter from '../components/Footer.vue'
import AppModal from '../components/AppModal.vue'

const showModal = ref(false)
</script>
