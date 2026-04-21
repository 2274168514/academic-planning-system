import { createStore } from 'vuex'

export default createStore({
  state: {
    token: localStorage.getItem('token') || '',
    user: JSON.parse(localStorage.getItem('user')) || null
  },
  getters: {
    isLoggedIn: state => !!state.token,
    currentUser: state => state.user
  },
  mutations: {
    SET_TOKEN(state, token) {
      state.token = token
    },
    SET_USER(state, user) {
      state.user = user
    },
    LOGOUT(state) {
      state.token = ''
      state.user = null
    }
  },
  actions: {
    login({ commit }, { token, user }) {
      localStorage.setItem('token', token)
      localStorage.setItem('user', JSON.stringify(user))
      commit('SET_TOKEN', token)
      commit('SET_USER', user)
    },
    logout({ commit }) {
      localStorage.removeItem('token')
      localStorage.removeItem('user')
      commit('LOGOUT')
    }
  },
  modules: {}
})
