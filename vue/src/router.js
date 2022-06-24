import {createRouter, createWebHistory} from 'vue-router'
import Auth from 'views/Auth'
import Home from 'views/Home'
import Profile from 'views/user/Profile'
import Debug from 'views/Debug'

import { List, Grabber } from 'views/gallery'
import Collection from 'views/web/Collection'
import Request from 'views/web/Request'


import NotFound from 'views/errors/NotFound'
import store from 'store'
import { ROUTE_AUTH, ROUTE_GUEST } from 'services/const'
import { SET_PAGE_LOADER } from 'store/types'


const routes = [
    {path: '/', component: Home},
    {path: '/n00b', component: Profile, ...ROUTE_AUTH},

    {path: '/n00b/collection/:pk?', component: Collection, ...ROUTE_AUTH},
    {path: '/n00b/request/:pk?', component: Request, ...ROUTE_AUTH},
    {path: '/n00b/request/:pk?', component: Request, ...ROUTE_AUTH},

    {path: '/n00b/gallery', component: List, ...ROUTE_AUTH},
    {path: '/n00b/grab', component: Grabber, ...ROUTE_AUTH},
    {path: '/debug', component: Debug, ...ROUTE_AUTH},

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
    store.commit(SET_PAGE_LOADER, false)
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
