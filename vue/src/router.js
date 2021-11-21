import {createRouter, createWebHistory} from 'vue-router'
import Home from 'views/Home'
import Profile from 'views/user/Profile'
// import Link from 'views/link/Link';
import Auth from 'views/Auth'
import NotFound from 'views/errors/NotFound';
import store from 'store';


const routes = [
    {path: '/', component: Home},
    {path: '/n00b', component: Profile, meta: { authRequired: true }},
    {path: '/sux0r', component: Auth, meta: { onlyGuest: true }},
    // {path: '/l1nk', component: Link},
    // {path: '/ws/project/:pk?', component: () => import('views/ws/Project.vue'), props: true, meta: { authRequired: true }},
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
    // instead of having to check every route record with
    // to.matched.some(record => record.meta.requiresAuth)
    const { authRequired = null, onlyGuest = null } = to.meta
    const isAuthUser = await store.dispatch('checkUserAuth')
    console.log('isAuthUser', isAuthUser)
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
