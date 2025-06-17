import { createStore } from 'vuex';

export default createStore({
  state: {
    user: null
    user: null,
    token: localStorage.getItem('token')
  },
  mutations: {
    setUser(state, user) {
      state.user = user;
    },
    setToken(state, token) {
      state.token = token;
      if (token) {
        localStorage.setItem('token', token);
      } else {
        localStorage.removeItem('token');
      }
    },
    logout(state) {
      state.user = null;
      state.token = null;
      localStorage.removeItem('token');
    }
  },
  actions: {},
  modules: {}
});