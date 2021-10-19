import {createStore} from 'vuex'
import parseJwt from 'services/jwt'

const USER_TOKEN = 'USER_TOKEN'

const store = createStore({
    state() {
        return {
            loading: true,
            user: null,
            token: localStorage.getItem('t') || null,
        }
    },
    mutations: {
        loaded(state) {
            state.loading = false
        },
        login(state, payload) {
            if (payload) {
                state.token = payload
                state.user = parseJwt(payload)
                localStorage.setItem('t', payload)
            } else {
                state.token = null
                state.user = null
                localStorage.removeItem('t')
            }
        },

    },
    actions: {}
})

export default store