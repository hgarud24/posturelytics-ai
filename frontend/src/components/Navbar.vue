<template>
  <nav class="navbar">
    <div class="navbar-container">
      <!-- Logo -->
      <span class="logo">Posturelytics.AI</span>

      <!-- Links -->
      <ul class="nav-links">
        <li>
          <router-link to="/home" class="nav-link">Home</router-link>
        </li>
        <li>
          <router-link to="/focus" class="nav-link">Productivity</router-link>
        </li>
        <li>
          <button @click="logout" class="logout-button">Logout</button>
        </li>
      </ul>
    </div>
  </nav>
</template>

<script setup>
import { useRouter } from "vue-router";

const router = useRouter();

function logout() {
  localStorage.removeItem("token");
  router.push("/login");
}
</script>

<style scoped>
/* Base font */
.navbar {
  font-family: "Inter", sans-serif;
  background-color: #1f2937; /* Dark gray */
  color: white;
  padding: 12px 16px;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.2);
}

.navbar-container {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.logo {
  font-size: 1.2rem;
  font-weight: 600;
  letter-spacing: 0.5px;
  display: flex;
  align-items: center;
  gap: 6px;
}

.nav-links {
  list-style: none;
  display: flex;
  gap: 24px;
  align-items: center;
  margin: 0;
  padding: 0;
}

.nav-link {
  color: white;
  text-decoration: none;
  font-size: 0.95rem;
  transition: color 0.2s ease;
}

.nav-link:hover {
  color: #60a5fa; /* soft blue */
}

.logout-button {
  background-color: #ef4444;
  border: none;
  padding: 6px 14px;
  color: white;
  font-size: 0.85rem;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.2s ease;
}

.logout-button:hover {
  background-color: #dc2626;
}
</style>
