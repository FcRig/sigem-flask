import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:5000'
});

export function setToken(token) {
  if (token) {
    api.defaults.headers.common['Authorization'] = `Bearer ${token}`;
  } else {
    delete api.defaults.headers.common['Authorization'];
  }
}

export function registerUser(payload) {
  return api.post('/api/auth/register', payload);
}

export function loginUser(payload) {
  return api.post('/api/auth/login', payload);
}

export function fetchCurrentUser() {
  return api.get('/api/auth/me');
}

export function fetchUsers() {
  return api.get('/api/auth/users');
}

export function createUser(payload) {
  return api.post('/api/auth/users', payload);
}

export function fetchUser(id) {
  return api.get(`/api/auth/users/${id}`);
}

export function updateUser(id, payload) {
  return api.put(`/api/auth/users/${id}`, payload);
}

export function deleteUser(id) {
  return api.delete(`/api/auth/users/${id}`);
}

export function autoprfLogin(payload) {
  return api.post('/api/autoprf/login', payload);
}

export function pesquisarAutoInfracao(payload) {
  return api.post('/api/autoprf/pesquisar_ai', payload);
}

export function setupLoadingInterceptors(store) {
  api.interceptors.request.use(
    config => {
      store.commit('setLoading', true);
      return config;
    },
    error => {
      store.commit('setLoading', false);
      return Promise.reject(error);
    }
  );

  api.interceptors.response.use(
    response => {
      store.commit('setLoading', false);
      return response;
    },
    error => {
      store.commit('setLoading', false);
      return Promise.reject(error);
    }
  );
}

export default api;
