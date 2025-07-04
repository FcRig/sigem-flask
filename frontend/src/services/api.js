import axios from 'axios'
import router from '../router'

const api = axios.create({
  baseURL: 'http://localhost:5000'
})

export function setToken(token) {
  if (token) {
    api.defaults.headers.common['Authorization'] = `Bearer ${token}`;
  } else {
    delete api.defaults.headers.common['Authorization'];
  }
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
      if (error.response) {
        const status = error.response.status;
        const msg = error.response.data?.msg || error.response.data?.message || '';

        if ([401, 422].includes(status) && /token has expired/i.test(msg)) {
          store.commit('logout');
          store.commit('showSnackbar', { msg: 'Sessão expirada' });
          router.push('/');
        }

        if ((status === 401 || status === 400) &&
            (/Sessão AutoPRF expirada/i.test(msg) || /Sessão não iniciada/i.test(msg))) {
          store.commit('showSnackbar', { msg: 'Faça login no AutoPRF' });
        }
      }
      return Promise.reject(error);
    }
  );
}

export default api;
