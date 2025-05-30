import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../stores/auth'

// Import components
import Login from '../components/Login.vue'
import Dashboard from '../components/Dashboard.vue'
import Authors from '../components/Authors.vue'
import Publications from '../components/Publications.vue'
import Journals from '../components/Journals.vue'

const routes = [
  {
    path: '/',
    redirect: '/dashboard'
  },
  {
    path: '/login',
    name: 'Login',
    component: Login,
    meta: { requiresGuest: true }
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: Dashboard,
    meta: { requiresAuth: true }
  },
  {
    path: '/authors',
    name: 'Authors',
    component: Authors,
    meta: { requiresAuth: true }
  },
  {
    path: '/publications',
    name: 'Publications',
    component: Publications,
    meta: { requiresAuth: true }
  },
  {
    path: '/journals',
    name: 'Journals',
    component: Journals,
    meta: { requiresAuth: true }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// Navigation guards
router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()
  
  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    next('/login')
  } else if (to.meta.requiresGuest && authStore.isAuthenticated) {
    next('/dashboard')
  } else {
    next()
  }
})

export default router