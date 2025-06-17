<template>
  <v-dialog v-model="model" max-width="500">
    <v-card>
      <slot />
    </v-card>
  </v-dialog>
</template>

<script>
export default {
  name: 'AppModal',
  props: {
    modelValue: {
      type: Boolean,
      default: false
    }
  },
  computed: {
    model: {
      get() {
        return this.modelValue;
      },
      set(val) {
        this.$emit('update:modelValue', val);
      }
    }
  }
};
</script>
