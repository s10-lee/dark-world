import axios from "axios";
import { BASE_API_URL } from "./const";

const xhr = axios.create({
    baseURL: BASE_API_URL,
    withCredentials: true,
})

export function httpHeader() {
    let token = localStorage.getItem('t')
    if (token) {
        return { Authorization: 'Bearer ' + token }
    } else {
        return {};
    }
}

export const getApiCall = (url) => {
    return xhr.get( url, { headers: httpHeader() } )
        .then( response => response.data )
}

export const postApiCall = ( url, postData ) => {
    return xhr.post( url, { ...postData }, { headers: httpHeader() })
        .then( response => response.data )
}