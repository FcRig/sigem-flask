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
  return api.post('api/auth/register', payload);
}

export function loginUser(payload) {
  return api.post('api/auth/login', payload);
}

export function fetchCurrentUser() {
  return api.get('api/auth/me');
}

export default api;