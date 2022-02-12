import {createRouter, createWebHistory} from 'vue-router'
import Auth from 'views/Auth'
import Home from 'views/Home'
import Profile from 'views/user/Profile'
import Gallery from 'views/gallery/Index'
import Upload from "views/gallery/Upload";
import NotFound from 'views/errors/NotFound'
import store from 'store'
import { ROUTE_AUTH, ROUTE_GUEST } from 'services/const'


const routes = [
    {path: '/', component: Home},
    {path: '/n00b', component: Profile, ...ROUTE_AUTH},
    {path: '/n00b/gallery', component: Gallery, ...ROUTE_AUTH},
    {path: '/n00b/upload', component: Upload, ...ROUTE_AUTH},
    {path: '/sux0r', component: Auth, ...ROUTE_GUEST},

    {path: '/:pathMatch(.*)*', name: 'NotFound', component: NotFound, props: true},
]

const router = createRouter({
    history: createWebHistory(),
    linkExactActiveClass: 'active',
    linkActiveClass: 'active',
    routes
})

router.afterEach(() => {
    store.commit('loaded')
})


router.beforeEach(async (to, from) => {
    const { authRequired = null, onlyGuest = null } = to.meta
    const isAuthUser = await store.dispatch('checkUserAuth')

    if (authRequired && !isAuthUser) {
        // this route requires auth, check if logged in
        // if not, redirect to login page.
        return {
            path: '/sux0r',
            // save the location we were at to come back later
            // query: { redirect: to.fullPath },
        }
    } else if (onlyGuest && isAuthUser) {
        return {path: '/'}
    }

})

export default router
