<template>
  <div>
    <div class="flex items-center space-x-2">
      <!-- Present -->
      <button
        @click="updateStatus('present')"
        class="inline-flex items-center px-2.5 py-1.5 border rounded-md text-xs font-medium focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500"
        :class="[
          status === 'present'
            ? 'bg-green-100 text-green-800 border-green-200'
            : 'bg-white text-gray-700 border-gray-300 hover:bg-gray-50',
        ]"
      >
        <svg
          v-if="status === 'present'"
          xmlns="http://www.w3.org/2000/svg"
          class="-ml-0.5 mr-1.5 h-3 w-3"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M5 13l4 4L19 7"
          />
        </svg>
        Present
      </button>

      <!-- Absent -->
      <button
        @click="updateStatus('absent')"
        class="inline-flex items-center px-2.5 py-1.5 border rounded-md text-xs font-medium focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500"
        :class="[
          status === 'absent'
            ? 'bg-red-100 text-red-800 border-red-200'
            : 'bg-white text-gray-700 border-gray-300 hover:bg-gray-50',
        ]"
      >
        <svg
          v-if="status === 'absent'"
          xmlns="http://www.w3.org/2000/svg"
          class="-ml-0.5 mr-1.5 h-3 w-3"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M6 18L18 6M6 6l12 12"
          />
        </svg>
        Absent
      </button>

      <!-- Late -->
      <button
        @click="updateStatus('late')"
        class="inline-flex items-center px-2.5 py-1.5 border rounded-md text-xs font-medium focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-yellow-500"
        :class="[
          status === 'late'
            ? 'bg-yellow-100 text-yellow-800 border-yellow-200'
            : 'bg-white text-gray-700 border-gray-300 hover:bg-gray-50',
        ]"
      >
        <svg
          v-if="status === 'late'"
          xmlns="http://www.w3.org/2000/svg"
          class="-ml-0.5 mr-1.5 h-3 w-3"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"
          />
        </svg>
        Late
      </button>

      <!-- Excused -->
      <button
        @click="updateStatus('excused')"
        class="inline-flex items-center px-2.5 py-1.5 border rounded-md text-xs font-medium focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
        :class="[
          status === 'excused'
            ? 'bg-blue-100 text-blue-800 border-blue-200'
            : 'bg-white text-gray-700 border-gray-300 hover:bg-gray-50',
        ]"
      >
        <svg
          v-if="status === 'excused'"
          xmlns="http://www.w3.org/2000/svg"
          class="-ml-0.5 mr-1.5 h-3 w-3"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"
          />
        </svg>
        Excused
      </button>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    studentId: {
      type: Number,
      required: true,
    },
    status: {
      type: String,
      required: true,
      validator: (value) => ['present', 'absent', 'late', 'excused'].includes(value),
    },
  },
  methods: {
    updateStatus(newStatus) {
      if (newStatus !== this.status) {
        this.$emit('update-status', this.studentId, newStatus)
      }
    },
  },
}
</script>
