import axios from 'axios';
import parseJwt from './jwt'
import { API_OBTAIN_URL, API_REFRESH_URL } from "./const"



class AuthService {
    checkUserAuth () {
        return localStorage.getItem('t')
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




/*
class AuthService {
    login(username, password) {
        return axios
            .post(API_OBTAIN_URL, {
                username: username,
                password: password
            })
            .then(response => {
                if (response.data) {
                    // localStorage.setItem('t', JSON.stringify(response.data));
                }
                console.log(response.data)
                return response.data;
            })
            .catch(e => {
                throw e
            })
    }
    refresh() {

    }
    logout() {
        localStorage.removeItem('t');
    }
}

export const auth = new AuthService()*/
