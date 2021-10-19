import Home from "views/ws/index.vue";

export default [
    {path: '/ws', name: 'ws', component: Home, children: [
            {path: 'project', component: () => import('views/ws/project/index.vue')},
            {path: 'project/:pk', component: () => import('views/ws/project/edit.vue'), props: true},
            {path: 'request', component: () => import('views/ws/request/index.vue')},
            {path: 'request/:pk', component: () => import('views/ws/request/edit.vue'), props: true},
    ], meta: { requiresAuth: true }
    },
]
