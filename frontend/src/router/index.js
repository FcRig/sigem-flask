import { createRouter, createWebHistory } from 'vue-router'
import Login from '../views/Login.vue'
import Register from '../views/Register.vue'
import Home from '../views/Home.vue'
import AdminUsers from '../views/AdminUsers.vue'
import store from '../store'

const routes = [
  { path: '/login', component: Login, meta: { layout: 'auth' } },
  { path: '/register', component: Register, meta: { layout: 'auth' } },
  { path: '/', component: Home, meta: { requiresAuth: true } },
  { path: '/admin/users', component: AdminUsers, meta: { requiresAuth: true } },
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
