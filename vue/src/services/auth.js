import axios from 'axios';
import parseJwt from 'services/jwt'
import { API_OBTAIN_URL, API_REFRESH_URL } from "./const"


class AuthService {
    checkUserAuth () {
        const now = Math.round(Date.now() / 1000)
        try {
            const { exp } = parseJwt( localStorage.getItem('t') )
            return exp - now > 0
        } catch (e) {
            localStorage.removeItem('t')
        }
        return false
    }
    obtainToken ( username, password ) {
        return axios
            .post(API_OBTAIN_URL, {
                username: username,
                password: password
            })
            .then(response => {
                return response.data.access_token
            })
            .catch(e => {
                throw e
            })
    }
}

const auth = new AuthService()

export default auth