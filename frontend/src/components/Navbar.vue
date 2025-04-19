<template>
  <v-container>
  <v-app-bar app class="navbar">
  <router-link to="/">
    <img src="../assets/logo.png" alt="Posturelytics Logo" class="logo" />
  </router-link>

    <v-spacer></v-spacer>
    <template v-if="isLoggedIn">
      <RouterLink to="/" custom v-slot="{ navigate }">
        <v-btn text @click="navigate">Home</v-btn>
      </RouterLink>
      <RouterLink to="/focus" custom v-slot="{ navigate }">
        <v-btn text @click="navigate">Productivity</v-btn>
      </RouterLink>
      <RouterLink to="/dashboard" custom v-slot="{ navigate }">
        <v-btn text @click="navigate">Dashboard</v-btn>
      </RouterLink>
      <v-btn text @click="logout">Logout</v-btn>
    </template>
    <template v-else>
      <RouterLink to="/" custom v-slot="{ navigate }">
        <v-btn text @click="navigate">Home</v-btn>
      </RouterLink>
      <RouterLink to="/login" custom v-slot="{ navigate }">
        <v-btn text @click="navigate">Login</v-btn>
      </RouterLink>
      <RouterLink to="/signup" custom v-slot="{ navigate }">
        <v-btn text @click="navigate">Signup</v-btn>
      </RouterLink>
    </template>
  </v-app-bar>
</v-container>
</template>

<script setup>
import { useRouter } from "vue-router";
import { computed, defineAsyncComponent, watchEffect, ref } from "vue";
import { isLoggedIn } from '@/composables/auth';


const router = useRouter();
// export const isLoggedIn = ref(!!localStorage.getItem("token"))

window.addEventListener("storage", () => {
  isLoggedIn.value = !!localStorage.getItem("token")
})

function logout() {
  localStorage.removeItem("token");
  isLoggedIn.value = false;
  router.push("/login");
}


</script>

<style scoped>
/* Base font */
.navbar {
  background-color: #1a2542 !important; /* <-- override Vuetify styles */
  color: white !important;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.2);
}
.logo{
  width: 280px;
  height: 70px;
  padding: 4px 16px;
}
/* 
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
} */

/* .nav-link {
  color: white;
  text-decoration: none;
  font-size: 0.95rem;
  transition: color 0.2s ease;
} */

/* 
.nav-link:hover {
  color: #60a5fa; 
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
} */
</style>
