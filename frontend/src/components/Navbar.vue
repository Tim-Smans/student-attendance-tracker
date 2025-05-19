<template>
  <nav class="bg-white shadow-sm">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex justify-between h-16">
        <!-- Logo/Title -->
        <div class="flex items-center">
          <router-link to="/" class="text-xl font-semibold text-orange-600 hover:text-orange-800">
            Attendance Tracker
          </router-link>
        </div>

        <!-- Navigation Links -->
        <div class="flex items-center space-x-6">
          <router-link to="/" class="text-gray-700 hover:text-orange-600 text-sm font-medium" exact>
            Dashboard
          </router-link>
          <router-link
            to="/classgroup"
            class="text-gray-700 hover:text-orange-600 text-sm font-medium"
          >
            Classgroups
          </router-link>
          <router-link
            to="/schedule"
            class="text-gray-700 hover:text-orange-600 text-sm font-medium"
          >
            Scheduler
          </router-link>
          <router-link
            to="/new-device"
            class="text-gray-700 hover:text-orange-600 text-sm font-medium"
          >
            Set up new classroom
          </router-link>

          <div v-if="auth.user" class="flex items-center space-x-4">
            <img :src="auth.user.picture" class="w-6 h-6 rounded-full" />
            <span>{{ auth.user.given_name }}</span>
            <button @click="logout" class="text-sm text-red-500 hover:underline">Logout</button>
          </div>
        </div>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'

const auth = useAuthStore()
const router = useRouter()

const logout = () => {
  auth.logout()
  router.push('/login')
}
</script>
