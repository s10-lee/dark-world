import { createStore } from 'vuex'
import parseJwt from 'services/jwt'
import axios from 'axios';
import {API_OBTAIN_URL, API_REFRESH_URL} from 'services/const';

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
        login(state, payload = null) {
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
    actions: {
        checkUserAuth ({ commit, state }) {
            const now = Math.round(Date.now() / 1000)
            try {
                if (!state.user && state.token) {
                    commit('login', state.token)
                }
                const { exp = 0 } = state.user
                if (exp - now > 0) {
                    return true
                }
            } catch (e) {}

            commit('login', false)
            return false
        },
        obtainToken ( { commit }, credentials ) {
            return axios
                .post(API_OBTAIN_URL, credentials)
                .then(response => {
                    const { access_token = null } = response.data
                    commit('login', access_token)
                })
                .catch(e => {
                    throw e
                })
        },
        refreshToken ( { commit, state } ) {
            return axios
                .post(API_REFRESH_URL, {
                    refresh_token: state.token
                })
                .then(response => {
                    const { access_token = null } = response.data
                    commit('login', access_token)
                })
                .catch(e => {
                    throw e
                })
        },
        logoutToken({ commit }) {
            commit('login', null)
        }
    }
})

export default store