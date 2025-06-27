import { createStore } from 'vuex'
import { setToken, fetchCurrentUser as apiFetchCurrentUser } from '../services/api'

export default createStore({
  state: {
    user: null,
    token: localStorage.getItem('token') || null,
    aiResult: null,
    loading: false,
    snackbar: { show: false, msg: '', color: 'success' }
  },
  mutations: {
    setToken(state, token) {
      state.token = token
      setToken(token)
      if (token) {
        localStorage.setItem('token', token)
      } else {
        localStorage.removeItem('token')
      }
    },
    setUser(state, user) {
      state.user = user
    },
    setAiResult(state, data) {
      state.aiResult = data
    },
    setLoading(state, value) {
      state.loading = value
    },
    showSnackbar(state, { msg, color = 'error' }) {
      state.snackbar.msg = msg
      state.snackbar.color = color
      state.snackbar.show = true
    },
    hideSnackbar(state) {
      state.snackbar.show = false
    },
    logout(state) {
      state.user = null
      state.token = null
      setToken(null)
      localStorage.removeItem('token')
    }
  },
  actions: {
    async initialize({ state, commit }) {
      if (state.token) {
        setToken(state.token)
        try {
          const { data } = await apiFetchCurrentUser()
          commit('setUser', data)
        } catch (e) {
          commit('setToken', null)
        }
      }
    },
    async fetchCurrentUser({ commit }) {
      try {
        const { data } = await apiFetchCurrentUser()
        commit('setUser', data)
      } catch (e) {
        commit('logout')
      }
    }
  },
  modules: {}
})
