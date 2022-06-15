import { createStore } from 'vuex'
import parseJwt from 'services/jwt'
import axios from 'axios';
import { API_OBTAIN_URL, API_REFRESH_URL } from 'services/const';
import { SET_USER, SET_TOKEN, SET_PAGE_LOADER, SET_NAVBAR_DISPLAY, ADD_NOTIFICATION, POP_NOTIFICATION } from 'store/types'

const store = createStore({
    state() {
        return {
            navbar: true,
            loading: true,
            user: null,
            token: localStorage.getItem('t') || null,
            notifications: [],
        }
    },
    mutations: {
        [SET_NAVBAR_DISPLAY]( state, payload ) {
            state.navbar = payload
        },
        [SET_PAGE_LOADER]( state, payload ) {
            state.loading = payload
        },
        [SET_USER] ( state, payload = null ) {
            state.user = payload
        },
        [SET_TOKEN] ( state, payload = null ) {
            if (payload) {
                state.token = payload
                localStorage.setItem('t', payload)
            } else {
                state.token = null
                localStorage.removeItem('t')
            }
        },
        [ADD_NOTIFICATION] ( state, payload ) {
            state.notifications.push(payload)
        },
        [POP_NOTIFICATION] ( state ) {
            state.notifications.splice(0, 1)
        }
    },
    actions: {
        setTokenFromResponse({ commit, state, dispatch }, data) {
            const { access_token = null } = data
            const user = parseJwt(access_token)

            commit(SET_USER, user)
            commit(SET_TOKEN, access_token)

            const now = Math.ceil(Date.now() / 1000)
            const timeout = (user.exp - now) * 1000
            setTimeout(() => dispatch('refreshToken'), timeout)
            return true
        },
        checkUserAuth ({ commit, state }) {
            if (!state.user && state.token) {
                commit(SET_USER, parseJwt(state.token))
            }
            const now = Math.ceil(Date.now() / 1000)

            if (state.user && state.user.exp - now > 0) {
                // console.log('checkUserAuth = ', state.user.exp - now)
                return true
            }
            commit(SET_USER, null)
            commit(SET_TOKEN, null)
            return false
        },
        obtainToken ({ state, dispatch }, credentials ) {
            return axios
                .post(API_OBTAIN_URL, credentials)
                .then(response => dispatch('setTokenFromResponse', response.data))
                .catch(e => {
                    throw e
                })
        },
        refreshToken ({ state, dispatch }) {
            return axios
                .post(API_REFRESH_URL, {refresh_token: state.token})
                .then(response => dispatch('setTokenFromResponse', response.data))
                .catch(e => {
                    throw e
                })
        },
        logoutToken({ commit }) {
            commit(SET_USER, null)
            commit(SET_TOKEN, null)
        },
        notify({ commit, state }, message ) {
            commit(ADD_NOTIFICATION, message)
            if (message.duration) {
                setTimeout(() => commit(POP_NOTIFICATION), message.duration)
            }
        }
    }
})

export default store