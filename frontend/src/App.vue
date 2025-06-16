<template>
  <MainLayout>
    <router-view />
  </MainLayout>
</template>

<script>
import MainLayout from './layouts/MainLayout.vue';

export default {
  name: 'App',
  components: { MainLayout }
};
</script>
