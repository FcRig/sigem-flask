<template>
  <v-container class="page-title py-4">
    <h2>{{ title }}</h2>
  </v-container>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const title = computed(() => route.meta.title || '')
</script>

<style scoped>
.page-title {
  border-bottom: 1px solid #eee;
}
</style>