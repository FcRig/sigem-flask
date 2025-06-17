import axios from 'axios';
import store from '../store';

const api = axios.create({
  baseURL: 'http://localhost:8000'
});

api.interceptors.request.use(config => {
  const token = store.state.token || localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export function registerUser(payload) {
  return api.post('/auth/register', payload);
}

export function loginUser(payload) {
  return api.post('/auth/login', payload);
}

export function getCurrentUser() {
  return api.get('/auth/me');
}

export default api;
