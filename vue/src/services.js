import axios from 'axios'
// const isProd = process.env.NODE_ENV === 'production';
const baseApiUrl = '/api/v1'

// TODO: validation ?
export const xhr = axios.create({baseURL: baseApiUrl, withCredentials: true})

// const getLocalStorage = (key, value = null) => {
//   return window.localStorage.getItem(key) || value
// }
//
// const setLocalStorage = (key, value) => {
//   return window.localStorage.setItem(key, value)
// }