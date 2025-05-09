<script setup lang="ts">
import { GoogleLogin } from 'vue3-google-login';
import MyFooter from './components/MyFooter.vue'
import Navbar from './components/Navbar.vue'
</script>

<template class="highlight">
  <Navbar />
  <router-view />
  <MyFooter />
</template>

<style scoped></style>
