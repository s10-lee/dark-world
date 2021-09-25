import {createStore} from 'vuex'

// Create a new store instance.
const store = createStore({
  state() {
    return {
      count: 0,
      loading: true,
      user: null,
    }
  },
  mutations: {
    increment(state) {
      state.count++
    },
    loaded(state) {
      state.loading = false
    },
    auth(state, payload) {
      if (!payload) {
        state.user = null
      } else {
        state.user = payload

      }
    }
  }
})

export default store