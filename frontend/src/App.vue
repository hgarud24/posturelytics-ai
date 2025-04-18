<template>
  <div id="app">
    <!-- Show Navbar only on authenticated routes -->
    <Navbar v-if="!['/login', '/signup' ].includes(route.path)" />

    <!-- Optional global navigation for testing -->
    <!-- <nav>
      <router-link to="/login">Login</router-link> |
      <router-link to="/signup">Signup</router-link> |
      <router-link to="/focus">Focus</router-link>
    </nav> -->

    <router-view />
  </div>
</template>

<script setup>
import { useRoute } from 'vue-router'  
import Navbar from './components/Navbar.vue' 

const route = useRoute()
</script>

<style>
@import url("https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600&display=swap");
* {
  padding: 0;
  margin: 0;
  box-sizing: border-box;
  font-family: "Raleway", sans-serif;
  font-weight: 400;
}

.app {
  min-height: 100vh;
  position: relative;
  background-color: #f1f1f1;
}
.container {
  padding: 0 20px;
  max-width: 1140px;
  margin: 0 auto;
}
</style>