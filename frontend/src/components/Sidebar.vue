<template>
  <v-navigation-drawer v-model="drawer">
    <v-list nav>
      <v-list-item link to="/">
        <v-list-item-title>Home</v-list-item-title>
      </v-list-item>
    </v-list>
  </v-navigation-drawer>
</template>

<script>
export default {
  name: 'AppSidebar',
  props: {
    modelValue: {
      type: Boolean,
      required: true
    }
  },
  computed: {
    drawer: {
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
