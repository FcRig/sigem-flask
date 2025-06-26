import { createRouter, createWebHistory } from 'vue-router'
import Login from '../views/Login.vue'
import Register from '../views/Register.vue'
import Home from '../views/Home.vue'
import AdminUsers from '../views/AdminUsers.vue'
import AutoInfracao from '../views/AutoInfracao.vue'
import VeiculosEmergencia from '../views/VeiculosEmergencia.vue'
import store from '../store'

const routes = [
  { path: '/login', component: Login, meta: { layout: 'auth', title: 'Login' } },
  { path: '/register', component: Register, meta: { layout: 'auth', title: 'Cadastro de Usuário' } },
  {
    path: '/',
    component: Home,
    meta: { requiresAuth: true, title: 'Bem-vindo!' }
  },
  {
    path: '/admin/users',
    component: AdminUsers,
    meta: { requiresAuth: true, title: 'Administração de Usuários' }
  },
  {
    path: '/resultado-ai',
    component: AutoInfracao,
    meta: { requiresAuth: true, title: 'Pesquisa do Auto de Infração' }
  },
  {
    path: '/cancelamentos/veiculos-emergencia',
    component: VeiculosEmergencia,
    meta: { requiresAuth: true, title: 'Veículos de Emergência' }
  },
  { path: '/:pathMatch(.*)*', redirect: '/login?error=not_found' }
]

const router = createRouter({
  history: createWebHistory(),
  routes

})

router.beforeEach((to, from, next) => {
  if (to.meta.requiresAuth && !store.state.token) {
    next('/login?error=unauthorized')
  } else {
    next()
  }
})

export default router;
