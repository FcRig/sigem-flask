<template>
  <v-overlay :model-value="true" class="loading-overlay d-flex align-center justify-center">
    <v-progress-circular indeterminate size="64" color="primary" />
  </v-overlay>
</template>

<script setup>
</script>

<style scoped>
.loading-overlay {
  background-color: rgba(255, 255, 255, 0.7);
}
</style>
