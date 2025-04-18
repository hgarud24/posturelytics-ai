<template>
    <div class="auth">
      <h2>Log In</h2>
      <form @submit.prevent="login">
        <input v-model="email" type="email" placeholder="Email" required />
        <input v-model="password" type="password" placeholder="Password" required />
        <button type="submit">Log In</button>
      </form>
      <p>{{ message }}</p>
    </div>
  </template>
  
  <script setup>
  import { ref } from 'vue'
  import axios from 'axios'
  
  const email = ref('')
  const password = ref('')
  const message = ref('')
  
  async function login() {
    try {
      const res = await axios.post('http://127.0.0.1:8000/api/auth/login', {
        email: email.value,
        password: password.value
      })
      localStorage.setItem('token', res.data.token)
      message.value = 'Login successful! Token stored.'
    } catch (err) {
      message.value = err.response?.data?.detail || 'Login failed'
    }
  }
  </script>
  