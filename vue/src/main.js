import { createApp, h } from 'vue'
import App from './App.vue'
import router from 'router'
import store from 'store'

import BLink from 'components/BLink'
import BLoading from 'components/BLoading'
import BNavbar from 'components/BNavbar'
import 'scss/dark.scss'

const app = createApp({
    render() {
        return h(App)
    }
}).use(router).use(store)


app.component('b-link', BLink)
app.component('b-loading', BLoading)
app.component('b-navbar', BNavbar)

app.mount('#app')
