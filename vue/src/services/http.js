import axios from 'axios';
import { BASE_API_URL } from 'services/const'

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

export const requestApiCall = ( method, url, payload = null, formData = null) => {
    const data = payload || formData
    const additionalHeaders = formData ? {'Content-Type': 'multipart/form-data'} : {}
    return xhr.request({
        method: method,
        url: url,
        data: data,
        headers: {
            ...httpHeader(),
            ...additionalHeaders,
        },
    }).then( response => response.data )
}

export const getApiCall = (url) => {
    return xhr.get( url, { headers: httpHeader() } )
        .then( response => response.data )
}

export const postApiCall = ( url, payloadData ) => {
    return xhr.post( url, { ...payloadData }, { headers: httpHeader() })
        .then( response => response.data )
}

export const putApiCall = ( url, payloadData ) => {
    return xhr.put( url, { ...payloadData }, { headers: httpHeader() })
        .then( response => response.data )
}

export const deleteApiCall = ( url ) => {
    return xhr.delete( url, { headers: httpHeader() })
        .then( response => response.data )
}

export const uploadApiCall = ( url, formData ) => {
    return xhr.post( url, formData, {
        headers: {
            ...httpHeader(),
            'Content-Type': 'multipart/form-data'
        }})
        .then( response => response.data )
}
