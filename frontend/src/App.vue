<template>
  <v-app>
    <Navbar  />
    <router-view class="router-view"/>
  </v-app>
</template>

<script setup>
import { useRoute } from 'vue-router'  
import Navbar from './components/Navbar.vue' 

const route = useRoute()
</script>

<style>
.router-view{
  background-color: #212531;
}

</style>