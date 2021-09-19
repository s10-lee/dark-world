import axios from 'axios'

// TODO: validation ?
const xhr = axios.create({baseURL: 'http://dark.artel.works/api/', withCredentials: true})


const getLocalStorage = (key, value = null) => {
  return window.localStorage.getItem(key) || value
}

const setLocalStorage = (key, value) => {
  return window.localStorage.setItem(key, value)
}