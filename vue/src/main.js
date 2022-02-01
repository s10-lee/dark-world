import { createApp, h } from 'vue'
import App from './App.vue'
import router from 'router'
import store from 'store'
import VueKinesis from 'vue-kinesis';
import {registerComponents} from 'components';
import 'scss/main.scss'

const app = createApp({
    render() {
        return h(App)
    }
}).use(router).use(store).use(VueKinesis)

registerComponents(app)

app.mount('#app')