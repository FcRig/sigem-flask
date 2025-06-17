import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000'
});

export function setToken(token) {
  if (token) {
    api.defaults.headers.common['Authorization'] = `Bearer ${token}`;
  } else {
    delete api.defaults.headers.common['Authorization'];
  }
}

export function registerUser(payload) {
  return api.post('/auth/register', payload);
}

export function loginUser(payload) {
  return api.post('/auth/login', payload);
}

export function fetchCurrentUser() {
  return api.get('/auth/me');
}

export default api;
