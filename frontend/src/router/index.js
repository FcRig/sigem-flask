import { createRouter, createWebHistory } from 'vue-router';
import Login from '../views/Login.vue';
import Register from '../views/Register.vue';
import Home from '../views/Home.vue';
import AdminUsers from '../views/AdminUsers.vue';

const routes = [
  { path: '/login', component: Login, meta: { layout: 'auth' } },
  { path: '/register', component: Register, meta: { layout: 'auth' } },
  { path: '/', component: Home },
  { path: '/admin/users', component: AdminUsers }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;
