<template>
  <v-navigation-drawer v-model="drawer" color="#f5f5f5">    
      <v-list-item dense>
        <v-list-item-content >              
          <v-list-item-title class="text-h6">
            PRF
          </v-list-item-title>
          <v-list-item-subtitle>
            NPI-RS
          </v-list-item-subtitle>
        </v-list-item-content>
      </v-list-item>
      
      <v-divider></v-divider> 
    
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
