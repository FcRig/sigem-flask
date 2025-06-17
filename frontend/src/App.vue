<template>
  <component :is="layout">
    <router-view />
  </component>
</template>

<script>
import { computed } from 'vue';
import { useRoute } from 'vue-router';
import MainLayout from './layouts/MainLayout.vue';
import AuthLayout from './layouts/AuthLayout.vue';

export default {
  name: 'App',
  components: { MainLayout, AuthLayout },
  setup() {
    const route = useRoute();
    const layout = computed(() =>
      route.meta.layout === 'auth' ? AuthLayout : MainLayout
    );
    return { layout };
  }
};
</script>
