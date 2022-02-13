import { createStore } from 'vuex'
import parseJwt from 'services/jwt'
import axios from 'axios';
import { API_OBTAIN_URL, API_REFRESH_URL } from 'services/const';
import { SET_USER_AUTH, SET_PAGE_LOADER } from 'store/types'

const store = createStore({
    state() {
        return {
            loading: true,
            user: null,
            token: localStorage.getItem('t') || null,
        }
    },
    mutations: {
        [SET_PAGE_LOADER]( state, payload ) {
            state.loading = payload
        },
        [SET_USER_AUTH]( state, payload = null ) {
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
            if (!state.user && state.token) {
                commit(SET_USER_AUTH, state.token)
            }
            const now = Math.round(Date.now() / 1000)
            if (state.user && state.user.exp - now > 0) {
                return true
            }
            commit(SET_USER_AUTH, false)
            return false
        },
        obtainToken ({ commit }, credentials ) {
            return axios
                .post(API_OBTAIN_URL, credentials)
                .then(response => {
                    const { access_token = null } = response.data
                    commit(SET_USER_AUTH, access_token)
                })
                .catch(e => {
                    throw e
                })
        },
        refreshToken ({ commit, state }) {
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
            commit(SET_USER_AUTH, null)
        },
    }
})

export default store