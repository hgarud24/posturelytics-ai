import { createRouter, createWebHistory } from 'vue-router'
import Login from '../views/Login.vue'
import Signup from '../views/Signup.vue'
import FocusSession from '../views/FocusSession.vue'
import Home from '../views/Home.vue'

const routes = [
  { path: '/', redirect: '/home' },
  { path: '/login', component: Login },
  { path: '/signup', component: Signup },
  { path: '/focus', component: FocusSession },
  { path: '/home', component: Home }

]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
    const publicPages = ['/login', '/signup' , '/home']
    const authRequired = !publicPages.includes(to.path)
    const token = localStorage.getItem('token')
  
    if (authRequired && !token) {
      return next('/login')
    }
  
    next()
  })
  
export default router
