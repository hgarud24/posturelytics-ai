<template>
  <div id="app">
    <!-- Show Navbar only on authenticated routes -->
    <Navbar v-if="!['/login', '/signup'].includes(route.path)" />

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
import { useRoute } from 'vue-router'  // ✅ This is required
import Navbar from './components/Navbar.vue' // ✅ Import the navbar

const route = useRoute()
</script>
