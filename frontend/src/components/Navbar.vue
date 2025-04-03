<template>
  <nav class="bg-white shadow-sm">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex justify-between h-16">
        <!-- Logo/Title -->
        <div class="flex items-center">
          <router-link to="/" class="text-xl font-semibold text-green-600 hover:text-green-800">
            Attendance Tracker
          </router-link>
        </div>

        <!-- Navigation Links -->
        <div class="flex items-center space-x-6">
          <router-link to="/" class="text-gray-700 hover:text-green-600 text-sm font-medium" exact>
            Dashboard
          </router-link>
          <router-link
            to="/classgroup"
            class="text-gray-700 hover:text-green-600 text-sm font-medium"
          >
            Classgroups
          </router-link>
          <router-link
            to="/schedule"
            class="text-gray-700 hover:text-green-600 text-sm font-medium"
          >
            Scheduler
          </router-link>
          <router-link
            to="/attendance"
            class="text-gray-700 hover:text-green-600 text-sm font-medium"
          >
            Attendance
          </router-link>
        </div>
      </div>
    </div>
  </nav>
</template>

<script setup>
// No logic needed for now
</script>
