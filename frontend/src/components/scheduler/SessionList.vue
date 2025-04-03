<template>
  <div class="bg-white shadow overflow-hidden sm:rounded-lg">
    <div class="px-4 py-5 sm:px-6 flex justify-between items-center">
      <h3 class="text-lg leading-6 font-medium text-gray-900">Sessions List</h3>
      <div class="flex items-center">
        <div class="relative rounded-md shadow-sm max-w-xs">
          <input
            type="text"
            v-model="searchQuery"
            class="block w-full pr-10 sm:text-sm border-gray-300 rounded-md focus:ring-green-500 focus:border-green-500"
            placeholder="Search sessions..."
          />
          <div class="absolute inset-y-0 right-0 pr-3 flex items-center pointer-events-none">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              class="h-5 w-5 text-gray-400"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
              />
            </svg>
          </div>
        </div>
      </div>
    </div>
    <div class="border-t border-gray-200">
      <div class="overflow-x-auto">
        <table class="min-w-full divide-y divide-gray-200">
          <thead class="bg-gray-50">
            <tr>
              <th
                scope="col"
                class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
              >
                Date & Time
              </th>
              <th
                scope="col"
                class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
              >
                Classgroup
              </th>
              <th
                scope="col"
                class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
              >
                Room
              </th>
              <th
                scope="col"
                class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
              >
                Duration
              </th>
              <th
                scope="col"
                class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
              >
                Actions
              </th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-200">
            <tr v-for="session in filteredSessions" :key="session.id" class="hover:bg-gray-50">
              <td class="px-6 py-4 whitespace-nowrap">
                <div class="text-sm text-gray-900">{{ formatDate(session.startTime) }}</div>
                <div class="text-sm text-gray-500">
                  {{ formatTimeRange(session.startTime, session.endTime) }}
                </div>
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                <span
                  class="px-2 py-1 inline-flex text-xs leading-5 font-semibold rounded-full"
                  :class="getClassgroupColor(session.classgroupId)"
                >
                  {{ getClassgroupName(session.classgroupId) }}
                </span>
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                {{ getRoomDeviceName(session.roomDeviceId) }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                {{ calculateDuration(session.startTime, session.endTime) }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm font-medium">
                <button
                  @click="editSession(session)"
                  class="text-green-600 hover:text-green-900 mr-3"
                >
                  Edit
                </button>
                <button @click="deleteSession(session)" class="text-red-600 hover:text-red-900">
                  Delete
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Empty State -->
      <div v-if="filteredSessions.length === 0" class="py-8 text-center">
        <svg
          xmlns="http://www.w3.org/2000/svg"
          class="mx-auto h-12 w-12 text-gray-400"
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
        <h3 class="mt-2 text-sm font-medium text-gray-900">No sessions found</h3>
        <p class="mt-1 text-sm text-gray-500">
          {{
            searchQuery
              ? 'No sessions match your search criteria.'
              : 'Get started by creating a new session.'
          }}
        </p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    sessions: {
      type: Array,
      required: true,
    },
    classgroups: {
      type: Array,
      required: true,
    },
    roomDevices: {
      type: Array,
      required: true,
    },
  },
  data() {
    return {
      searchQuery: '',
      colors: [
        'bg-blue-100 text-blue-800',
        'bg-green-100 text-green-800',
        'bg-purple-100 text-purple-800',
        'bg-yellow-100 text-yellow-800',
        'bg-pink-100 text-pink-800',
        'bg-indigo-100 text-indigo-800',
        'bg-red-100 text-red-800',
        'bg-teal-100 text-teal-800',
      ],
    }
  },
  computed: {
    filteredSessions() {
      if (!this.searchQuery) {
        return this.sessions
      }

      const query = this.searchQuery.toLowerCase()
      return this.sessions.filter((session) => {
        const classgroup = this.getClassgroupName(session.classgroupId).toLowerCase()
        const device = this.getRoomDeviceName(session.roomDeviceId).toLowerCase()
        const date = this.formatDate(session.startTime).toLowerCase()

        return classgroup.includes(query) || device.includes(query) || date.includes(query)
      })
    },
  },
  methods: {
    formatDate(dateString) {
      const date = new Date(dateString)
      return date.toLocaleDateString('en-US', {
        weekday: 'short',
        month: 'short',
        day: 'numeric',
        year: 'numeric',
      })
    },
    formatTimeRange(startString, endString) {
      const start = new Date(startString)
      const end = new Date(endString)

      const formatTime = (date) => {
        return date.toLocaleTimeString('en-US', {
          hour: 'numeric',
          minute: '2-digit',
          hour12: true,
        })
      }

      return `${formatTime(start)} - ${formatTime(end)}`
    },
    calculateDuration(startString, endString) {
      const start = new Date(startString)
      const end = new Date(endString)

      const durationMs = end - start
      const durationMinutes = Math.floor(durationMs / (1000 * 60))

      if (durationMinutes < 60) {
        return `${durationMinutes} minutes`
      }

      const hours = Math.floor(durationMinutes / 60)
      const minutes = durationMinutes % 60

      if (minutes === 0) {
        return `${hours} hour${hours > 1 ? 's' : ''}`
      }

      return `${hours} hour${hours > 1 ? 's' : ''} ${minutes} minute${minutes > 1 ? 's' : ''}`
    },
    getClassgroupName(classgroupId) {
      const classgroup = this.classgroups.find((c) => c.id === classgroupId)

      if (!classgroup) {
        console.warn('Classgroup not found for ID:', classgroupId)
        return 'Unknown Classgroup'
      }

      return classgroup.name
    },
    getRoomDeviceName(deviceId) {
      const device = this.roomDevices.find((d) => d.id === deviceId)
      return device ? device.roomName : 'Unknown Device'
    },
    getClassgroupColor(classgroupId) {
      // Use consistent colors for classgroups
      const colorIndex = classgroupId % this.colors.length
      return this.colors[colorIndex]
    },
    editSession(session) {
      this.$emit('edit-session', session)
    },
    deleteSession(session) {
      this.$emit('delete-session', session)
    },
  },
}
</script>
