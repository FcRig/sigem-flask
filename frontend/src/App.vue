<template>
<component :is="layout">
  <router-view />
</component>
<LoadingOverlay v-if="loading" />
<v-snackbar v-model="snackbar.show" :color="snackbar.color" location="top right" timeout="3000" @update:model-value="val => { if (!val) store.commit('hideSnackbar') }">
  {{ snackbar.msg }}
</v-snackbar>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import { useStore } from 'vuex'
import MainLayout from './layouts/MainLayout.vue'
import AuthLayout from './layouts/AuthLayout.vue'
import LoadingOverlay from './components/LoadingOverlay.vue'

const store = useStore()
const route = useRoute()
const layout = computed(() =>
  route.meta.layout === 'auth' ? AuthLayout : MainLayout
)
const loading = computed(() => store.state.loading)
const snackbar = computed(() => store.state.snackbar)
</script>
