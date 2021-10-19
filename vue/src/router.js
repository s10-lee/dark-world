import {createRouter, createWebHistory} from 'vue-router'
import Home from 'views/Home.vue'
import Profile from 'views/user/Profile'
import Link from 'views/link/Link';
import Auth from 'views/Auth'
import NotFound from 'views/errors/NotFound';
import auth from 'services/auth'
import wsRoutes from 'views/ws/index.js'
import store from './store';


const routes = [
    {path: '/', component: Home},
    {path: '/n00b', component: Profile, meta: { requiresAuth: true }},
    {path: '/l1nk', component: Link},
    {path: '/sux0r', component: Auth},
    ...wsRoutes,
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


router.beforeEach((to, from) => {
    // instead of having to check every route record with
    // to.matched.some(record => record.meta.requiresAuth)
    if (to.meta.requiresAuth && !auth.checkUserAuth()) {
        // this route requires auth, check if logged in
        // if not, redirect to login page.
        return {
            path: '/sux0r',
            // save the location we were at to come back later
            // query: { redirect: to.fullPath },
        }
    }
})

export default router
