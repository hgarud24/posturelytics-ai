import { createRouter, createWebHistory } from "vue-router";
import Login from "../views/Login.vue";
import Signup from "../views/Signup.vue";
import FocusSession from "../views/FocusSession.vue";
import Dashboard from "../views/Dashboard.vue";
import Home from "../views/Home.vue";

const routes = [
  { path: "/", name: "Home", component: Home },
  { path: "/login", name: "Login", component: Login },
  { path: "/signup", name: "Signup", component: Signup },
  { path: "/focus", name: "Focus", component: FocusSession },
  { path: "/dashboard", name: "Dashboard", component: Dashboard },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

// router.beforeEach((to, from, next) => {
//     const publicPages = ['/login', '/signup' , '/home']
//     const authRequired = !publicPages.includes(to.path)
//     const token = localStorage.getItem('token')

//     if (authRequired && !token) {
//       return next('/login')
//     }
//     next()
//   })

export default router;
