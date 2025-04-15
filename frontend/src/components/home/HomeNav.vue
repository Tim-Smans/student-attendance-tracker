<template>
  <!-- Navigation Cards -->
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
    <h2 class="text-2xl font-bold text-gray-900 mb-6">Quick Navigation</h2>

    <div class="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
      <!-- Classgroups Card -->
      <div
        class="bg-white overflow-hidden shadow rounded-lg transition-all duration-300 hover:shadow-xl transform hover:-translate-y-1"
      >
        <div class="px-4 py-5 sm:p-6">
          <div
            class="flex items-center justify-center h-16 w-16 rounded-md bg-green-100 text-green-600 mx-auto"
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              class="h-8 w-8"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"
              />
            </svg>
          </div>
          <div class="mt-5 text-center">
            <h3 class="text-lg font-medium text-gray-900">Classgroups</h3>
            <p class="mt-2 text-sm text-gray-500">
              Manage your classgroups, view student lists, and organize your teaching groups.
            </p>
            <div class="mt-4">
              <a
                href="#"
                class="inline-flex items-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-green-600 hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500"
              >
                View Classgroups
              </a>
            </div>
          </div>
        </div>
        <div class="bg-gray-50 px-4 py-4 sm:px-6">
          <div class="text-sm">
            <span class="font-medium text-green-600 hover:text-green-500">
              12 active classgroups
            </span>
          </div>
        </div>
      </div>

      <!-- Schedule Card -->
      <div
        class="bg-white overflow-hidden shadow rounded-lg transition-all duration-300 hover:shadow-xl transform hover:-translate-y-1"
      >
        <div class="px-4 py-5 sm:p-6">
          <div
            class="flex items-center justify-center h-16 w-16 rounded-md bg-blue-100 text-blue-600 mx-auto"
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              class="h-8 w-8"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"
              />
            </svg>
          </div>
          <div class="mt-5 text-center">
            <h3 class="text-lg font-medium text-gray-900">Schedule</h3>
            <p class="mt-2 text-sm text-gray-500">
              View and manage your teaching schedule, classroom assignments, and session times.
            </p>
            <div class="mt-4">
              <a
                href="#"
                class="inline-flex items-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
              >
                View Schedule
              </a>
            </div>
          </div>
        </div>
        <div class="bg-gray-50 px-4 py-4 sm:px-6">
          <div class="text-sm">
            <span class="font-medium text-blue-600 hover:text-blue-500"> 3 sessions today </span>
          </div>
        </div>
      </div>

      <!-- Attendance Card -->
      <div
        class="bg-white overflow-hidden shadow rounded-lg transition-all duration-300 hover:shadow-xl transform hover:-translate-y-1"
      >
        <div class="px-4 py-5 sm:p-6">
          <div
            class="flex items-center justify-center h-16 w-16 rounded-md bg-purple-100 text-purple-600 mx-auto"
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              class="h-8 w-8"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M9 16h.01"
              />
            </svg>
          </div>
          <div class="mt-5 text-center">
            <h3 class="text-lg font-medium text-gray-900">Attendance</h3>
            <p class="mt-2 text-sm text-gray-500">
              Track and manage student attendance for your sessions and view attendance reports.
            </p>
            <div class="mt-4">
              <a
                href="#"
                class="inline-flex items-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-purple-600 hover:bg-purple-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-purple-500"
              >
                Track Attendance
              </a>
            </div>
          </div>
        </div>
        <div class="bg-gray-50 px-4 py-4 sm:px-6">
          <div class="text-sm">
            <span class="font-medium text-purple-600 hover:text-purple-500">
              87% average attendance rate
            </span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
