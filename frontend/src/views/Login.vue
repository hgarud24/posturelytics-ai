<template>
  <div class="login-wrapper">
    <div class="logo-wrapper">
      <img src="@/assets/logo.png" alt="Posturelytics Logo" class="logo" />
    </div>
    <v-card class="login-card">
      <!-- Heading -->
      <h2 class="login-title">Log Into Posturelytics.AI</h2>

      <!-- Login Form -->
      <v-form @submit.prevent="login" class="login-form">
        <v-text-field
          v-model="email"
          type="email"
          placeholder="Email or phone number"
          outlined
          dense
          hide-details
          required
        />
        <v-text-field
          v-model="password"
          type="password"
          placeholder="Password"
          outlined
          dense
          hide-details
          required
        />
        <v-btn class="login-button" color="primary" block type="submit">
          Log In
        </v-btn>
        <div class="divider">or</div>
        <v-btn to="/signup" color="success" class="create-account" block>
          Create new account
        </v-btn>
      </v-form>
    </v-card>

    <p class="message">{{ message }}</p>
  </div>
</template>

<script setup>
import { ref } from "vue";
import axios from "axios";
import { useRouter } from "vue-router";
import { isLoggedIn } from '@/composables/auth';

const router = useRouter();
const email = ref("");
const password = ref("");
const message = ref("");

async function login() {
  try {
    const res = await axios.post("http://127.0.0.1:8000/api/auth/login", {
      email: email.value,
      password: password.value,
    });
    localStorage.setItem("token", res.data.token);
    message.value = "Login successful! Token stored.";
    isLoggedIn.value = true;
    setTimeout(() => router.push("/focus"), 1000);
  } catch (err) {
    message.value = err.response?.data?.detail || "Login failed";
  }
}
</script>

<style scoped>
.login-wrapper {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-color: #010d2d;
  flex-direction: column;
}

.login-card {
  width: 400px;
  padding: 32px;
  border-radius: 10px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
  background-color: #e9eef2;
}

.logo-wrapper {
  display: flex;
  justify-content: center;
  margin-bottom: 12px;
}

.logo {
  height: 60px;
  object-fit: contain;
}

.login-title {
  font-family: "Inter", sans-serif;
  text-align: center;
  margin-bottom: 20px;
  font-size: 20px;
  font-weight: 600;
  color: #1c1e21;
}

.login-form {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.login-button {
  color: white;
  font-weight: bold;
}

.forgot-link {
  text-align: center;
  margin-top: 10px;
  color: #1877f2;
  cursor: pointer;
  font-size: 14px;
}

.divider {
  text-align: center;
  margin: 8px 0;
  color: #aaa;
  font-size: 14px;
}

.create-account {
  background-color: #42b72a;
  color: white;
  font-weight: bold;
}

.message {
  margin-top: 20px;
  text-align: center;
  color: #d93025;
}
</style>
