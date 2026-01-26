import { createRouter, createWebHistory } from 'vue-router'
import Login from '../views/Login.vue'
import Register from '../views/Register.vue'
import Home from '../views/Home.vue'
import AdminUsers from '../views/AdminUsers.vue'
import AutoInfracao from '../views/AutoInfracao.vue'
import AutoInfracaoSiscom from '../views/AutoInfracaoSiscom.vue'
import HistoricoSiscom from '../views/HistoricoSiscom.vue'
import VeiculosEmergencia from '../views/VeiculosEmergencia.vue'
import VeiculosEmergenciaSiscom from '../views/VeiculosEmergenciaSiscom.vue'
import CancelamentoDuplicidade from '../views/CancelamentoDuplicidade.vue'
import CancelamentoDuplicidadeSiscom from '../views/CancelamentoDuplicidadeSiscom.vue'
import Veiculo from '../views/Veiculo.vue'
import CriarProcesso from '../views/CriarProcesso.vue'
import ProcurarProcesso from '../views/procurar-processo/ProcurarProcesso.vue'
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
    path: '/resultado-ai-siscom',
    component: AutoInfracaoSiscom,
    meta: { requiresAuth: true, title: 'Pesquisa AI SISCOM' }
  },
  {
    path: '/historico-siscom',
    component: HistoricoSiscom,
    meta: { requiresAuth: true, title: 'Histórico do Auto de Infração' }
  },
  {
    path: '/siscom/cancelamentos/veiculos-emergencia',
    component: VeiculosEmergenciaSiscom,
    meta: { requiresAuth: true, title: 'Veículos de Emergência SISCOM' }
  },
  {
    path: '/siscom/cancelamentos/duplicidade',
    component: CancelamentoDuplicidadeSiscom,
    meta: { requiresAuth: true, title: 'Duplicidade SISCOM' }
  },
  {
    path: '/veiculo',
    component: Veiculo,
    meta: { requiresAuth: true, title: 'Consulta de Veículo' }
  },
  {
    path: '/cancelamentos/veiculos-emergencia',
    component: VeiculosEmergencia,
    meta: { requiresAuth: true, title: 'Veículos de Emergência' }
  },
  {
    path: '/cancelamentos/duplicidade',
    component: CancelamentoDuplicidade,
    meta: { requiresAuth: true, title: 'Cancelamento por Duplicidade' }
  },
  {
    path: '/sei/criar-processo',
    component: CriarProcesso,
    meta: { requiresAuth: true, title: 'Criação de Processos SEI' }
  },
  {
    path: '/sei/procurar-processo',
    component: ProcurarProcesso,
    meta: { requiresAuth: true, title: 'Procurar Processos SEI' }
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
