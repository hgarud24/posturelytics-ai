<template>
    <nav class="navbar">
      <router-link to="/focus">🏠 Home</router-link>
      <button @click="logout">Logout</button>
    </nav>
  </template>
  
  <script setup>
  import { useRouter } from 'vue-router'
  
  const router = useRouter()
  
  function logout() {
    localStorage.removeItem('token')
    router.push('/login')
  }
  </script>
  
  <style scoped>
  .navbar {
    display: flex;
    justify-content: space-between;
    padding: 1rem;
    background-color: #eee;
  }
  </style>
  