<template>
  <v-app>
    <AppSidebar v-if="user" v-model="drawer" />
    <AppHeader
      :user="user"
      @logout="logout"
      @toggle-drawer="drawer = !drawer"
    />
    <v-main>
      <PageTitle />
      <slot />
    </v-main>
    <AppFooter />
  </v-app>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useStore } from 'vuex'
import AppHeader from '../components/Header.vue'
import AppFooter from '../components/Footer.vue'
import AppSidebar from '../components/Sidebar.vue'
import PageTitle from '../components/PageTitle.vue'

const store = useStore()
const router = useRouter()

const drawer = ref(true)
const user = computed(() => store.state.user)

function logout() {
  store.commit('logout')
  router.push('/login')
}
</script>
