import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000'
});

export function registerUser(payload) {
  return api.post('/auth/register', payload);
}

export function loginUser(payload) {
  return api.post('/auth/login', payload);
}

export default api;
