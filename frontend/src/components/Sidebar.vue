<template>
  <v-navigation-drawer v-model="drawer" color="#f5f5f5">
    <v-list-item dense>
      <v-list-item-content>
        <v-list-item-title class="text-h6">PRF</v-list-item-title>
        <v-list-item-subtitle>NPI-RS</v-list-item-subtitle>
      </v-list-item-content>
    </v-list-item>

    <v-divider></v-divider>

    <v-list density="compact" nav>
      <v-list-item title="Home" prepend-icon="mdi-home" to="/"></v-list-item>
      <v-list-group value="autoprf">
        <template #activator="{ props }">
          <v-list-item
            v-bind="props"
            prepend-icon="mdi-car"
            title="AutoPRF"
          />
        </template>
        <v-list-item title="Teste1" prepend-icon="mdi-file" />
        <v-list-item title="Teste2" prepend-icon="mdi-file" />
        <v-list-item title="Teste3" prepend-icon="mdi-file" />
      </v-list-group>

      <v-list-group value="siscom">
        <template #activator="{ props }">
          <v-list-item
            v-bind="props"
            prepend-icon="mdi-laptop"
            title="SISCOM"
          />
        </template>
        <v-list-item title="Teste1" prepend-icon="mdi-file" />
        <v-list-item title="Teste2" prepend-icon="mdi-file" />
        <v-list-item title="Teste3" prepend-icon="mdi-file" />
      </v-list-group>

      <v-list-group value="sei">
        <template #activator="{ props }">
          <v-list-item
            v-bind="props"
            prepend-icon="mdi-file-document"
            title="SEI"
          />
        </template>
        <v-list-item title="Teste1" prepend-icon="mdi-file" />
        <v-list-item title="Teste2" prepend-icon="mdi-file" />
        <v-list-item title="Teste3" prepend-icon="mdi-file" />
      </v-list-group>
    </v-list>
  </v-navigation-drawer>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  modelValue: {
    type: Boolean,
    required: true
  }
})
const emit = defineEmits(['update:modelValue'])

const drawer = computed({
  get: () => props.modelValue,
  set: val => emit('update:modelValue', val)
})
</script>
