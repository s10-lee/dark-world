import { createRouter, createWebHistory } from 'vue-router'
import Home from './views/Home.vue'
import Project from './views/compose/Project'
import Request from './views/compose/Request'
import Profile from './views/user/Profile'
import Link from "./views/link/Link";
import NotFound from "./views/errors/NotFound";

import store from "./store";

const routes = [
  {path: '/', component: Home},
  {path: '/n00b', component: Profile},
  {path: '/l1nk', component: Link},
  {path: '/ws/request', component: Request},
  {path: '/project', component: Project, props: true},
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


export default router
