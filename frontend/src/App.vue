<script setup lang="ts">
import MyFooter from './components/MyFooter.vue'
import Navbar from './components/Navbar.vue'
</script>

<template class="highlight">
  <Navbar />
  <router-view />
  <MyFooter />
</template>

<style scoped></style>
