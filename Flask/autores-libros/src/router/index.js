import Vue from 'vue'
import Router from 'vue-router'
import Login from '@/components/Login'
import Register from '@/components/Register'
import AutorList from '@/components/AutorList'
import LibroList from '@/components/LibroList'
import GeneroList from '@/components/GeneroList'
import GeneroForm from '@/components/GeneroForm.vue'
import LibroForm from '@/components/LibroForm.vue'
import AutorForm from '@/components/AutorForm.vue'
Vue.use(Router)

const router = new Router({
  routes: [
    {
      path: '/',
      redirect: '/login'
    },
    {
      path: '/login',
      name: 'Login',
      component: Login
    },
    {
      path: '/register',
      name: 'Register',
      component: Register
    },
    {
      path: '/autores',
      name: 'AutorList',
      component: AutorList,
      meta: { requiresAuth: true }
    },
    {
      path: '/libros',
      name: 'LibroList',
      component: LibroList,
      meta: { requiresAuth: true }
    },
    {
      path: '/generos',
      name: 'GeneroList',
      component: GeneroList,
      meta: { requiresAuth: true }
    }
  ]
})

// Guard para rutas protegidas
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token')
  
  if (to.matched.some(record => record.meta.requiresAuth)) {
    if (!token) {
      next('/login')
    } else {
      next()
    }
  } else {
    if (token && (to.path === '/login' || to.path === '/register')) {
      next('/autores')
    } else {
      next()
    }
  }
})

export default router