<template>
  <v-app>
    <AppHeader />
    <v-main>
      <slot />
    </v-main>
    <AppFooter />
    <AppModal v-model="showModal">
      <slot name="modal" />
    </AppModal>
  </v-app>
</template>

<script>
import AppHeader from '../components/Header.vue';
import AppFooter from '../components/Footer.vue';
import AppModal from '../components/AppModal.vue';

export default {
  name: 'AuthLayout',
  components: { AppHeader, AppFooter, AppModal },
  data() {
    return {
      showModal: false
    };
  }
};
</script>
