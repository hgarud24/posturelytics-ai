<template>
    <div class="auth">
      <h2>Sign Up</h2>
      <form @submit.prevent="signup">
        <input v-model="email" type="email" placeholder="Email" required />
        <input v-model="password" type="password" placeholder="Password" required />
        <button type="submit">Sign Up</button>
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
  
  async function signup() {
    try {
      const res = await axios.post('http://127.0.0.1:8000/api/auth/signup', {
        email: email.value,
        password: password.value
      })
      localStorage.setItem('token', res.data.token)
      message.value = 'Signup successful! Token stored.'
    } catch (err) {
      message.value = err.response?.data?.detail || 'Signup failed'
    }
  }
  </script>
  