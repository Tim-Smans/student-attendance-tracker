<template>
  <div class="bg-white shadow overflow-hidden sm:rounded-lg">
    <div class="overflow-x-auto">
      <table class="min-w-full divide-y divide-gray-200">
        <thead class="bg-gray-50">
          <tr>
            <th
              scope="col"
              class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
            >
              <div class="flex items-center">
                <input
                  type="checkbox"
                  class="h-4 w-4 text-green-600 focus:ring-green-500 border-gray-300 rounded"
                  :checked="isAllSelected"
                  @change="toggleSelectAll"
                />
              </div>
            </th>
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
              Student ID
            </th>
            <th
              scope="col"
              class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
            >
              Status
            </th>
          </tr>
        </thead>
        <tbody class="bg-white divide-y divide-gray-200">
          <tr
            v-for="student in students"
            :key="student.studentNumber"
            :class="[
              'hover:bg-gray-50',
              hasAttended(student.studentNumber) ? 'bg-green-100' : 'bg-red-100',
            ]"
          >
            <td class="px-6 py-4 whitespace-nowrap">
              <div class="flex items-center">
                <input
                  type="checkbox"
                  class="h-4 w-4 text-green-600 focus:ring-green-500 border-gray-300 rounded"
                  :checked="isSelected(student.studentNumber)"
                  @change="toggleSelect(student.studentNumber)"
                />
              </div>
            </td>
            <td class="px-6 py-4 whitespace-nowrap">
              <div class="flex items-center">
                <div class="flex-shrink-0 h-10 w-10">
                  <div
                    class="h-10 w-10 rounded-full bg-gray-200 flex items-center justify-center text-gray-500 font-medium"
                  >
                    {{ getInitials(student.firstName, student.lastName) }}
                  </div>
                </div>
                <div class="ml-4">
                  <div class="text-sm font-medium text-gray-900">
                    {{ student.firstName }} {{ student.lastName }}
                  </div>
                  <div class="text-sm text-gray-500">
                    {{ student.email }}
                  </div>
                </div>
              </div>
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
              {{ student.studentNumber }}
            </td>
            <td class="px-6 py-4 whitespace-nowrap">
              {{ hasAttended(student.studentNumber) ? 'Present' : 'Absent' }}
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Empty State -->
    <div v-if="students.length === 0" class="py-8 text-center">
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
          d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z"
        />
      </svg>
      <h3 class="mt-2 text-sm font-medium text-gray-900">No students found</h3>
      <p class="mt-1 text-sm text-gray-500">No students match your search criteria.</p>
    </div>
  </div>
</template>

<script>
export default {
  components: {},
  props: {
    students: {
      type: Array,
      required: true,
    },
    attendedStudents: {
      type: Array,
      required: true,
    },
    selectedStudents: {
      type: Array,
      required: true,
    },
  },
  computed: {
    isAllSelected() {
      return this.students.length > 0 && this.selectedStudents.length === this.students.length
    },
  },
  methods: {
    getInitials(firstName, lastName) {
      return `${firstName.charAt(0)}${lastName.charAt(0)}`
    },
    isSelected(studentId) {
      return this.selectedStudents.includes(studentId)
    },
    hasAttended(studentId) {
      return this.attendedStudents.some((student) => student.studentNumber === studentId)
    },
    toggleSelect(studentId) {
      this.$emit('toggle-select', studentId)
    },
    toggleSelectAll(event) {
      this.$emit('toggle-select-all', event.target.checked)
    },
    formatTimestamp(timestamp) {
      if (!timestamp) return 'Never'

      const date = new Date(timestamp)
      return date.toLocaleString('en-US', {
        month: 'short',
        day: 'numeric',
        hour: 'numeric',
        minute: '2-digit',
        hour12: true,
      })
    },
  },
}
</script>
