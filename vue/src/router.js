import {createRouter, createWebHistory} from 'vue-router'
import Auth from 'views/Auth'
import Home from 'views/Home'
import Demo from 'views/Demo'
import Landing from 'views/Landing'
import Profile from 'views/user/Profile'
import NotFound from 'views/errors/NotFound'
import store from 'store'
import { ROUTE_AUTH, ROUTE_GUEST } from 'services/const'


const routes = [
    {path: '/', component: Home},
    {path: '/land', component: Landing},
    {path: '/demo', component: Demo},
    {path: '/n00b', component: Profile, ...ROUTE_AUTH},
    {path: '/sux0r', component: Auth, ...ROUTE_GUEST},
    {path: '/m1r0/:pk?', component: () => import('views/miro/Board'), ...ROUTE_AUTH},
    {path: '/ws/project/:pk?', component: () => import('views/ws/Project.vue'), props: true, meta: { authRequired: true }},
    // {path: '/ws/request/:pk?', component: () => import('views/ws/Request.vue'), props: true, meta: { authRequired: true }},
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
