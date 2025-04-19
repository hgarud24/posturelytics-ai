<template>
  <!-- <v-container class="fill-height fill-width d-flex align-center justify-center"> -->
  <div class="signup-wrapper">
    <div class="logo-wrapper">
      <img src="@/assets/logo.png" alt="Posturelytics Logo" class="logo" />
    </div>
    <v-card class="pa-6 signup-card" elevation="12" max-width="500">
      <v-card-title class="signup-title">
        Create a new account
      </v-card-title>
      <v-card-subtitle class="text-center mb-4"
        >It’s quick and easy.</v-card-subtitle
      >
      <v-form @submit.prevent="signup">
        <v-row dense>
          <v-col cols="12" md="6">
            <v-text-field v-model="firstName" label="First Name" required />
          </v-col>
          <v-col cols="12" md="6">
            <v-text-field v-model="lastName" label="Last Name" required />
          </v-col>
          <v-col cols="12">
            <v-text-field v-model="email" label="Email" type="email" required />
          </v-col>
          <v-col cols="12">
            <v-text-field
              v-model="password"
              label="Password"
              type="password"
              required
            />
          </v-col>
          <v-col cols="12">
            <v-text-field
              v-model="birthday"
              label="Birthday (YYYY-MM-DD)"
              type="date"
              required
            />
          </v-col>
          <v-col cols="12">
            <v-radio-group v-model="gender" label="Gender" row>
              <v-radio label="Female" value="female" />
              <v-radio label="Male" value="male" />
            </v-radio-group>
          </v-col>
          <v-col cols="12" class="text-center">
            <v-btn class="signup-button" color="primary" type="submit" block>Sign Up</v-btn>
          </v-col>
        </v-row>
      </v-form>

      <v-alert v-if="message" class="mt-4" type="info" :text="message" />
    </v-card>
  </div>
</template>

<script setup>
import { ref } from "vue";
import axios from "axios";
import { useRouter } from "vue-router";

const router = useRouter();

const firstName = ref("");
const lastName = ref("");
const email = ref("");
const password = ref("");
const birthday = ref("");
const gender = ref("");
const message = ref("");

async function signup() {
  try {
    const res = await axios.post("http://127.0.0.1:8000/api/auth/signup", {
      first_name: firstName.value,
      last_name: lastName.value,
      email: email.value,
      password: password.value,
      birthday: birthday.value,
      gender: gender.value,
    });

    localStorage.setItem("token", res.data.token);
    message.value = "Signup successful! Redirecting...";
    setTimeout(() => router.push("/login"), 1000);
  } catch (err) {
    message.value = err.response?.data?.detail || "Signup failed";
  }
}
</script>

<style scoped>
.signup-wrapper {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-color: #010d2d;
  flex-direction: column;
}
.signup-title{
  text-align: center;
  margin-bottom: 20px;
  font-size: 20px;
  font-weight: 600;
  color: #1c1e21;
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
.signup-card{
  max-height: 80vh; /* Optional: prevent from becoming too tall */
  background-color: #e9eef2;
  border-radius: 10px;
  
}

.signup-button {
  color: white;
  font-weight: bold;
}

</style>
