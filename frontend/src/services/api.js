import axios from 'axios';

const api = axios.create({
  // Base URL points to the Flask backend. Adjust the port if needed.
  baseURL: 'http://localhost:5000/api'
});

export function registerUser(payload) {
  return api.post('/auth/register', payload);
}

export function loginUser(payload) {
  return api.post('/auth/login', payload);
}

export default api;
