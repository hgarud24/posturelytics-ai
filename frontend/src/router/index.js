import { createRouter, createWebHistory } from 'vue-router'
import Login from '../views/Login.vue'
import Signup from '../views/Signup.vue'
import FocusSession from '../views/FocusSession.vue'

const routes = [
  { path: '/', redirect: '/login' },
  { path: '/login', component: Login },
  { path: '/signup', component: Signup },
  { path: '/focus', component: FocusSession }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
    const publicPages = ['/login', '/signup']
    const authRequired = !publicPages.includes(to.path)
    const token = localStorage.getItem('token')
  
    if (authRequired && !token) {
      return next('/login')
    }
  
    next()
  })
  
export default router
