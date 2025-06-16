<template>
  <v-app>
    <AppSidebar v-model="drawer" />
    <AppHeader
      :user="user"
      @logout="logout"
      @toggle-drawer="drawer = !drawer"
    />
    <v-main>
      <slot />
    </v-main>
    <AppFooter />
  </v-app>
</template>

<script>
import AppHeader from '../components/Header.vue';
import AppFooter from '../components/Footer.vue';
import AppSidebar from '../components/Sidebar.vue';
import { mapState } from 'vuex';

export default {
  name: 'MainLayout',
  components: { AppHeader, AppFooter, AppSidebar },
  data() {
    return {
      drawer: false
    };
  },
  computed: {
    ...mapState(['user'])
  },
  methods: {
    logout() {
      this.$store.commit('logout');
      this.$router.push('/login');
    }
  }
};
</script>
