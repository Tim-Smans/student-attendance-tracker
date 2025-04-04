<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Header -->
    <header class="bg-white shadow">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        <div class="flex flex-col sm:flex-row sm:justify-between sm:items-center">
          <h1 class="text-2xl font-bold text-gray-900">Session Attendance {{ this.sessionId }}</h1>
          <div class="mt-3 sm:mt-0">
            <button
              @click="goBack"
              class="inline-flex items-center px-4 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500"
            >
              <svg
                xmlns="http://www.w3.org/2000/svg"
                class="-ml-1 mr-2 h-5 w-5 text-gray-500"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M10 19l-7-7m0 0l7-7m-7 7h18"
                />
              </svg>
              Back
            </button>
          </div>
        </div>
      </div>
    </header>

    <!-- Main Content -->
    <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div v-if="isLoading" class="flex justify-center py-12">
        <svg
          class="animate-spin -ml-1 mr-3 h-8 w-8 text-green-500"
          xmlns="http://www.w3.org/2000/svg"
          fill="none"
          viewBox="0 0 24 24"
        >
          <circle
            class="opacity-25"
            cx="12"
            cy="12"
            r="10"
            stroke="currentColor"
            stroke-width="4"
          ></circle>
          <path
            class="opacity-75"
            fill="currentColor"
            d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
          ></path>
        </svg>
      </div>

      <div
        v-else-if="!session"
        class="text-center py-12 bg-white shadow overflow-hidden sm:rounded-lg"
      >
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
            d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
          />
        </svg>
        <h3 class="mt-2 text-sm font-medium text-gray-900">Session not found</h3>
        <p class="mt-1 text-sm text-gray-500">The requested session could not be found.</p>
      </div>

      <div v-else>
        <!-- Session Info Header -->
        <SessionInfoHeader :session="session" :classgroup="classgroup" :classroom="classroom" />

        <!-- Attendance Summary -->
        <AttendanceSummary :absent="absent" :present="present" class="mt-6" />

        <!-- Attendance Controls -->
        <div class="mt-6 bg-white shadow overflow-hidden sm:rounded-lg">
          <div class="px-4 py-5 sm:p-6">
            <div
              class="flex flex-col sm:flex-row sm:justify-between sm:items-center space-y-4 sm:space-y-0"
            >
              <!-- Search -->
              <div class="relative rounded-md shadow-sm max-w-xs w-full">
                <input
                  type="text"
                  v-model="searchQuery"
                  class="block w-full pr-10 sm:text-sm border-gray-300 rounded-md focus:ring-green-500 focus:border-green-500"
                  placeholder="Search students..."
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

              <!-- Bulk Actions -->
              <div class="flex items-center space-x-4">
                <span class="text-sm text-gray-500">Bulk action:</span>
                <div class="relative inline-block text-left">
                  <select
                    v-model="bulkAction"
                    class="block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-green-500 focus:border-green-500 sm:text-sm rounded-md"
                  >
                    <option value="" disabled>Select action</option>
                    <option value="present">Mark as Present</option>
                    <option value="absent">Mark as Absent</option>
                    <option value="late">Mark as Late</option>
                    <option value="excused">Mark as Excused</option>
                  </select>
                </div>
                <button
                  @click="applyBulkAction"
                  :disabled="!bulkAction || selectedStudents.length === 0"
                  class="inline-flex items-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-green-600 hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  Apply to {{ selectedStudents.length || 'All' }}
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- Attendance Table -->
        <AttendanceTable
          :students="filteredStudents"
          :attendedStudents="attendedStudents"
          :selectedStudents="selectedStudents"
          @toggle-select="toggleSelectStudent"
          @toggle-select-all="toggleSelectAll"
          class="mt-6"
        />
      </div>
    </main>

    <!-- Notification -->
    <div v-if="notification.show" class="fixed bottom-0 inset-x-0 pb-2 sm:pb-5">
      <div class="max-w-md mx-auto px-2 sm:px-6 lg:px-8">
        <div
          class="p-2 rounded-lg shadow-lg sm:p-3"
          :class="{
            'bg-green-500': notification.type === 'success',
            'bg-red-500': notification.type === 'error',
            'bg-blue-500': notification.type === 'info',
          }"
        >
          <div class="flex items-center justify-between flex-wrap">
            <div class="w-0 flex-1 flex items-center">
              <span
                class="flex p-2 rounded-lg"
                :class="{
                  'bg-green-600': notification.type === 'success',
                  'bg-red-600': notification.type === 'error',
                  'bg-blue-600': notification.type === 'info',
                }"
              >
                <!-- Success Icon -->
                <svg
                  v-if="notification.type === 'success'"
                  class="h-6 w-6 text-white"
                  xmlns="http://www.w3.org/2000/svg"
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

                <!-- Error Icon -->
                <svg
                  v-if="notification.type === 'error'"
                  class="h-6 w-6 text-white"
                  xmlns="http://www.w3.org/2000/svg"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"
                  />
                </svg>

                <!-- Info Icon -->
                <svg
                  v-if="notification.type === 'info'"
                  class="h-6 w-6 text-white"
                  xmlns="http://www.w3.org/2000/svg"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
                  />
                </svg>
              </span>
              <p class="ml-3 font-medium text-white truncate">
                {{ notification.message }}
              </p>
            </div>
            <div class="order-2 flex-shrink-0 sm:order-3 sm:ml-2">
              <button
                type="button"
                class="-mr-1 flex p-2 rounded-md hover:bg-opacity-20 hover:bg-black focus:outline-none"
                @click="closeNotification"
              >
                <span class="sr-only">Close</span>
                <svg
                  class="h-6 w-6 text-white"
                  xmlns="http://www.w3.org/2000/svg"
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
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import SessionInfoHeader from './SessionInfoHeader.vue'
import AttendanceSummary from './AttendanceSummary.vue'
import AttendanceTable from './AttendanceTable.vue'
import { getFullSession } from '@/helpers/sessionHelpers'
import { getStudentsFromClassgroup } from '@/helpers/classgroupHelpers'

export default {
  components: {
    SessionInfoHeader,
    AttendanceSummary,
    AttendanceTable,
  },
  props: {
    sessionId: {
      type: String,
      required: true,
    },
  },
  data() {
    return {
      isLoading: true,
      session: null,
      classgroup: null,
      classroom: null,
      students: [],
      attendanceRecords: [],
      attendedStudents: [],
      searchQuery: '',
      absent: 0,
      present: 0,
      bulkAction: '',
      selectedStudents: [],
      notification: {
        show: false,
        type: 'success',
        message: '',
        timeout: null,
      },
    }
  },
  computed: {
    filteredStudents() {
      if (!this.searchQuery) {
        return this.students
      }

      const query = this.searchQuery.toLowerCase()
      return this.students.filter(
        (student) =>
          student.studentNumber.toLowerCase().includes(query) ||
          student.firstName.toLowerCase().includes(query) ||
          student.lastName.toLowerCase().includes(query) ||
          student.email.toLowerCase().includes(query),
      )
    },
    hasChanges() {
      if (!this.originalAttendanceRecords.length) return false

      return (
        JSON.stringify(this.attendanceRecords) !== JSON.stringify(this.originalAttendanceRecords)
      )
    },
  },
  created() {
    this.fetchSessionData()
  },
  methods: {
    async fetchStudents() {
      this.students = await getStudentsFromClassgroup(this.session.classgroup.id)
    },
    async fetchSessionData() {
      this.session = await getFullSession(this.sessionId)
      this.classgroup = this.session.classgroup
      this.classroom = this.session.roomDevice
      this.attendanceRecords = this.session.attendances
      await this.fetchStudents()

      const allStudents = await getStudentsFromClassgroup(this.session.classgroup.id)

      const attendedStudentIds = this.attendanceRecords.map((record) => record.studentId)

      this.attendedStudents = allStudents.filter((student) =>
        attendedStudentIds.includes(student.studentNumber),
      )

      this.present = this.attendedStudents.length
      this.absent = this.students.length - this.present

      this.isLoading = false
    },
    toggleSelectStudent(studentId) {
      const index = this.selectedStudents.indexOf(studentId)
      if (index === -1) {
        this.selectedStudents.push(studentId)
      } else {
        this.selectedStudents.splice(index, 1)
      }
    },
    toggleSelectAll(isSelected) {
      if (isSelected) {
        this.selectedStudents = this.filteredStudents.map((student) => student.id)
      } else {
        this.selectedStudents = []
      }
    },

    goBack() {
      this.$router.go(-1)
    },
    showNotification(type, message) {
      // Clear any existing timeout
      if (this.notification.timeout) {
        clearTimeout(this.notification.timeout)
      }

      // Set notification
      this.notification.type = type
      this.notification.message = message
      this.notification.show = true

      // Auto-hide after 5 seconds
      this.notification.timeout = setTimeout(() => {
        this.closeNotification()
      }, 5000)
    },
    closeNotification() {
      this.notification.show = false
    },
  },
}
</script>
