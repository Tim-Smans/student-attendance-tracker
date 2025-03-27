<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Header -->
    <header class="bg-white shadow">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        <div class="flex justify-between items-center">
          <h1 class="text-2xl font-bold text-gray-900">Student Attendance Tracker</h1>
          <span class="px-3 py-1 bg-green-100 text-green-800 rounded-full text-sm font-medium">
            {{ todayDate }}
          </span>
        </div>
      </div>
    </header>

    <!-- Main Content -->
    <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <!-- Filters and Search -->
      <div class="mb-8 bg-white p-4 rounded-lg shadow">
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div>
            <label for="search" class="block text-sm font-medium text-gray-700 mb-1"
              >Search Student</label
            >
            <input
              type="text"
              id="search"
              v-model="searchQuery"
              placeholder="Search by name..."
              class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
            />
          </div>
          <div>
            <label for="date" class="block text-sm font-medium text-gray-700 mb-1">Date</label>
            <input
              type="date"
              id="date"
              v-model="dateFilter"
              class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
            />
          </div>
          <div>
            <label for="status" class="block text-sm font-medium text-gray-700 mb-1">Status</label>
            <select
              id="status"
              v-model="statusFilter"
              class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
            >
              <option value="">All Statuses</option>
              <option value="present">Present</option>
              <option value="absent">Absent</option>
              <option value="late">Late</option>
            </select>
          </div>
        </div>
      </div>

      <!-- Stats Cards -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <div class="bg-white overflow-hidden shadow rounded-lg">
          <div class="px-4 py-5 sm:p-6">
            <div class="flex items-center">
              <div class="flex-shrink-0 bg-green-100 rounded-md p-3">
                <svg
                  class="h-6 w-6 text-green-600"
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
              </div>
              <div class="ml-5 w-0 flex-1">
                <dl>
                  <dt class="text-sm font-medium text-gray-500 truncate">Present Today</dt>
                  <dd class="flex items-baseline">
                    <div class="text-2xl font-semibold text-gray-900">{{ presentCount }}</div>
                  </dd>
                </dl>
              </div>
            </div>
          </div>
        </div>

        <div class="bg-white overflow-hidden shadow rounded-lg">
          <div class="px-4 py-5 sm:p-6">
            <div class="flex items-center">
              <div class="flex-shrink-0 bg-red-100 rounded-md p-3">
                <svg
                  class="h-6 w-6 text-red-600"
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
              </div>
              <div class="ml-5 w-0 flex-1">
                <dl>
                  <dt class="text-sm font-medium text-gray-500 truncate">Absent Today</dt>
                  <dd class="flex items-baseline">
                    <div class="text-2xl font-semibold text-gray-900">{{ absentCount }}</div>
                  </dd>
                </dl>
              </div>
            </div>
          </div>
        </div>

        <div class="bg-white overflow-hidden shadow rounded-lg">
          <div class="px-4 py-5 sm:p-6">
            <div class="flex items-center">
              <div class="flex-shrink-0 bg-yellow-100 rounded-md p-3">
                <svg
                  class="h-6 w-6 text-yellow-600"
                  xmlns="http://www.w3.org/2000/svg"
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
              </div>
              <div class="ml-5 w-0 flex-1">
                <dl>
                  <dt class="text-sm font-medium text-gray-500 truncate">Late Today</dt>
                  <dd class="flex items-baseline">
                    <div class="text-2xl font-semibold text-gray-900">{{ lateCount }}</div>
                  </dd>
                </dl>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Attendance Table -->
      <div class="bg-white shadow overflow-hidden sm:rounded-lg">
        <div class="flex justify-between items-center px-4 py-5 sm:px-6 border-b border-gray-200">
          <h3 class="text-lg leading-6 font-medium text-gray-900">Attendance Records</h3>
          <span class="text-sm text-gray-500">{{ filteredAttendance.length }} records</span>
        </div>
        <div class="overflow-x-auto">
          <table class="min-w-full divide-y divide-gray-200">
            <thead class="bg-gray-50">
              <tr>
                <th
                  scope="col"
                  class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                >
                  Student
                </th>
                <th
                  scope="col"
                  class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                >
                  Class
                </th>
                <th
                  scope="col"
                  class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                >
                  Date
                </th>
                <th
                  scope="col"
                  class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                >
                  Time
                </th>
                <th
                  scope="col"
                  class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                >
                  Status
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
              <tr
                v-for="(record, index) in paginatedAttendance"
                :key="index"
                class="hover:bg-gray-50"
              >
                <td class="px-6 py-4 whitespace-nowrap">
                  <div class="flex items-center">
                    <div class="h-10 w-10 flex-shrink-0">
                      <img class="h-10 w-10 rounded-full" :src="record.avatar" alt="" />
                    </div>
                    <div class="ml-4">
                      <div class="text-sm font-medium text-gray-900">{{ record.name }}</div>
                      <div class="text-sm text-gray-500">{{ record.id }}</div>
                    </div>
                  </div>
                </td>
                <td class="px-6 py-4 whitespace-nowrap">
                  <div class="text-sm text-gray-900">{{ record.class }}</div>
                </td>
                <td class="px-6 py-4 whitespace-nowrap">
                  <div class="text-sm text-gray-900">{{ formatDate(record.date) }}</div>
                </td>
                <td class="px-6 py-4 whitespace-nowrap">
                  <div class="text-sm text-gray-900">{{ record.time }}</div>
                </td>
                <td class="px-6 py-4 whitespace-nowrap">
                  <span
                    :class="{
                      'px-2 py-1 inline-flex text-xs leading-5 font-semibold rounded-full': true,
                      'bg-green-100 text-green-800': record.status === 'present',
                      'bg-red-100 text-red-800': record.status === 'absent',
                      'bg-yellow-100 text-yellow-800': record.status === 'late',
                    }"
                  >
                    {{ record.status.charAt(0).toUpperCase() + record.status.slice(1) }}
                  </span>
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  <button class="text-indigo-600 hover:text-indigo-900 mr-3">Edit</button>
                  <button class="text-red-600 hover:text-red-900">Delete</button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- Pagination -->
        <div
          class="bg-white px-4 py-3 flex items-center justify-between border-t border-gray-200 sm:px-6"
        >
          <div class="hidden sm:flex-1 sm:flex sm:items-center sm:justify-between">
            <div>
              <p class="text-sm text-gray-700">
                Showing
                <span class="font-medium">{{ (currentPage - 1) * itemsPerPage + 1 }}</span>
                to
                <span class="font-medium">{{
                  Math.min(currentPage * itemsPerPage, filteredAttendance.length)
                }}</span>
                of
                <span class="font-medium">{{ filteredAttendance.length }}</span>
                results
              </p>
            </div>
            <div>
              <nav
                class="relative z-0 inline-flex rounded-md shadow-sm -space-x-px"
                aria-label="Pagination"
              >
                <button
                  @click="currentPage--"
                  :disabled="currentPage === 1"
                  class="relative inline-flex items-center px-2 py-2 rounded-l-md border border-gray-300 bg-white text-sm font-medium text-gray-500 hover:bg-gray-50"
                  :class="{ 'opacity-50 cursor-not-allowed': currentPage === 1 }"
                >
                  <span class="sr-only">Previous</span>
                  <svg
                    class="h-5 w-5"
                    xmlns="http://www.w3.org/2000/svg"
                    viewBox="0 0 20 20"
                    fill="currentColor"
                    aria-hidden="true"
                  >
                    <path
                      fill-rule="evenodd"
                      d="M12.707 5.293a1 1 0 010 1.414L9.414 10l3.293 3.293a1 1 0 01-1.414 1.414l-4-4a1 1 0 010-1.414l4-4a1 1 0 011.414 0z"
                      clip-rule="evenodd"
                    />
                  </svg>
                </button>
                <button
                  v-for="page in totalPages"
                  :key="page"
                  @click="currentPage = page"
                  :class="{
                    'relative inline-flex items-center px-4 py-2 border text-sm font-medium': true,
                    'bg-indigo-50 border-indigo-500 text-indigo-600': currentPage === page,
                    'bg-white border-gray-300 text-gray-500 hover:bg-gray-50': currentPage !== page,
                  }"
                >
                  {{ page }}
                </button>
                <button
                  @click="currentPage++"
                  :disabled="currentPage === totalPages"
                  class="relative inline-flex items-center px-2 py-2 rounded-r-md border border-gray-300 bg-white text-sm font-medium text-gray-500 hover:bg-gray-50"
                  :class="{ 'opacity-50 cursor-not-allowed': currentPage === totalPages }"
                >
                  <span class="sr-only">Next</span>
                  <svg
                    class="h-5 w-5"
                    xmlns="http://www.w3.org/2000/svg"
                    viewBox="0 0 20 20"
                    fill="currentColor"
                    aria-hidden="true"
                  >
                    <path
                      fill-rule="evenodd"
                      d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z"
                      clip-rule="evenodd"
                    />
                  </svg>
                </button>
              </nav>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script>
export default {
  data() {
    return {
      searchQuery: '',
      dateFilter: '',
      statusFilter: '',
      currentPage: 1,
      itemsPerPage: 5,
      attendanceRecords: [
        {
          id: 'STU001',
          name: 'Emma Johnson',
          class: 'Mathematics 101',
          date: '2025-03-27',
          time: '09:00 AM',
          status: 'present',
          avatar: 'https://randomuser.me/api/portraits/women/1.jpg',
        },
        {
          id: 'STU002',
          name: 'Liam Smith',
          class: 'Physics 202',
          date: '2025-03-27',
          time: '10:30 AM',
          status: 'absent',
          avatar: 'https://randomuser.me/api/portraits/men/2.jpg',
        },
        {
          id: 'STU003',
          name: 'Olivia Brown',
          class: 'Chemistry 101',
          date: '2025-03-27',
          time: '01:00 PM',
          status: 'late',
          avatar: 'https://randomuser.me/api/portraits/women/3.jpg',
        },
        {
          id: 'STU004',
          name: 'Noah Wilson',
          class: 'Biology 303',
          date: '2025-03-26',
          time: '11:15 AM',
          status: 'present',
          avatar: 'https://randomuser.me/api/portraits/men/4.jpg',
        },
        {
          id: 'STU005',
          name: 'Ava Martinez',
          class: 'English Literature',
          date: '2025-03-26',
          time: '02:45 PM',
          status: 'present',
          avatar: 'https://randomuser.me/api/portraits/women/5.jpg',
        },
        {
          id: 'STU006',
          name: 'James Taylor',
          class: 'Computer Science',
          date: '2025-03-25',
          time: '09:30 AM',
          status: 'absent',
          avatar: 'https://randomuser.me/api/portraits/men/6.jpg',
        },
        {
          id: 'STU007',
          name: 'Sophia Anderson',
          class: 'History 101',
          date: '2025-03-25',
          time: '10:00 AM',
          status: 'present',
          avatar: 'https://randomuser.me/api/portraits/women/7.jpg',
        },
        {
          id: 'STU008',
          name: 'Benjamin Thomas',
          class: 'Art History',
          date: '2025-03-24',
          time: '01:30 PM',
          status: 'late',
          avatar: 'https://randomuser.me/api/portraits/men/8.jpg',
        },
        {
          id: 'STU009',
          name: 'Isabella Garcia',
          class: 'Spanish 202',
          date: '2025-03-24',
          time: '03:15 PM',
          status: 'present',
          avatar: 'https://randomuser.me/api/portraits/women/9.jpg',
        },
        {
          id: 'STU010',
          name: 'William Rodriguez',
          class: 'Physics 101',
          date: '2025-03-23',
          time: '11:45 AM',
          status: 'absent',
          avatar: 'https://randomuser.me/api/portraits/men/10.jpg',
        },
        {
          id: 'STU011',
          name: 'Mia Lewis',
          class: 'Calculus II',
          date: '2025-03-23',
          time: '09:15 AM',
          status: 'present',
          avatar: 'https://randomuser.me/api/portraits/women/11.jpg',
        },
        {
          id: 'STU012',
          name: 'Henry Walker',
          class: 'Chemistry Lab',
          date: '2025-03-22',
          time: '02:00 PM',
          status: 'late',
          avatar: 'https://randomuser.me/api/portraits/men/12.jpg',
        },
      ],
    }
  },
  computed: {
    todayDate() {
      const today = new Date()
      const options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' }
      return today.toLocaleDateString('en-US', options)
    },
    filteredAttendance() {
      return this.attendanceRecords.filter((record) => {
        const matchesSearch =
          this.searchQuery === '' ||
          record.name.toLowerCase().includes(this.searchQuery.toLowerCase()) ||
          record.id.toLowerCase().includes(this.searchQuery.toLowerCase())

        const matchesDate = this.dateFilter === '' || record.date === this.dateFilter

        const matchesStatus = this.statusFilter === '' || record.status === this.statusFilter

        return matchesSearch && matchesDate && matchesStatus
      })
    },
    paginatedAttendance() {
      const startIndex = (this.currentPage - 1) * this.itemsPerPage
      const endIndex = startIndex + this.itemsPerPage
      return this.filteredAttendance.slice(startIndex, endIndex)
    },
    totalPages() {
      return Math.ceil(this.filteredAttendance.length / this.itemsPerPage)
    },
    presentCount() {
      return this.attendanceRecords.filter(
        (record) => record.status === 'present' && this.isToday(record.date),
      ).length
    },
    absentCount() {
      return this.attendanceRecords.filter(
        (record) => record.status === 'absent' && this.isToday(record.date),
      ).length
    },
    lateCount() {
      return this.attendanceRecords.filter(
        (record) => record.status === 'late' && this.isToday(record.date),
      ).length
    },
  },
  methods: {
    formatDate(dateString) {
      const options = { year: 'numeric', month: 'short', day: 'numeric' }
      return new Date(dateString).toLocaleDateString('en-US', options)
    },
    isToday(dateString) {
      const today = new Date()
      const recordDate = new Date(dateString)
      return today.toDateString() === recordDate.toDateString()
    },
  },
}
</script>

<style>
/* Additional custom styles can be added here if needed */
</style>
