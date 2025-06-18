<template>
  <v-dialog v-model="model" max-width="500">
    <v-card>
      <slot />
    </v-card>
  </v-dialog>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  modelValue: {
    type: Boolean,
    default: false
  }
})
const emit = defineEmits(['update:modelValue'])

const model = computed({
  get: () => props.modelValue,
  set: val => emit('update:modelValue', val)
})
</script>
