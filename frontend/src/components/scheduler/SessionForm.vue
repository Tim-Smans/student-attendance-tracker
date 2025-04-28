
<template>
  <div
    class="fixed inset-0 z-10 overflow-y-auto"
    aria-labelledby="modal-title"
    role="dialog"
    aria-modal="true"
  >
    <div class="flex items-center justify-center min-h-screen px-4 text-center relative">
      <!-- Overlay -->
      <div class="absolute inset-0 bg-gray-500 bg-opacity-75 transition-opacity" aria-hidden="true"></div>

      <!-- Modal content -->
      <span class="hidden sm:inline-block sm:align-middle sm:h-screen" aria-hidden="true">&#8203;</span>

      <div
        class="inline-block align-bottom bg-white rounded-lg px-4 pt-5 pb-4 text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-lg sm:w-full sm:p-6 relative"
      >
      <div class="mt-3 text-center sm:mt-0 sm:text-left">
            <h3 class="text-lg leading-6 font-medium text-gray-900" id="modal-title">
              {{ session?.id ? 'Edit Session' : 'Add New Session' }}
            </h3>
            <div class="mt-2">
              <p class="text-sm text-gray-500">
                {{
                  session.id
                    ? 'Update the details for this session.'
                    : 'Fill in the details to create a new session.'
                }}
              </p>
            </div>
          </div>
        <form @submit.prevent="saveSession" class="mt-5 space-y-6">
          <!-- Date -->
          <div>
            <label for="session-date" class="block text-sm font-medium text-gray-700">Date</label>
            <div class="mt-1">
              <input
                type="date"
                id="session-date"
                v-model="formData.date"
                required
                class="shadow-sm focus:ring-green-500 focus:border-green-500 block w-full sm:text-sm border-gray-300 rounded-md"
              />
            </div>
          </div>

          <!-- Time Range -->
          <div class="grid grid-cols-1 gap-4 sm:grid-cols-2">
            <div>
              <label for="start-time" class="block text-sm font-medium text-gray-700"
                >Start Time</label
              >
              <div class="mt-1">
                <input
                  type="time"
                  id="start-time"
                  v-model="formData.startTime"
                  required
                  class="shadow-sm focus:ring-green-500 focus:border-green-500 block w-full sm:text-sm border-gray-300 rounded-md"
                />
              </div>
            </div>
            <div>
              <label for="end-time" class="block text-sm font-medium text-gray-700">End Time</label>
              <div class="mt-1">
                <input
                  type="time"
                  id="end-time"
                  v-model="formData.endTime"
                  required
                  class="shadow-sm focus:ring-green-500 focus:border-green-500 block w-full sm:text-sm border-gray-300 rounded-md"
                />
              </div>
              <p v-if="timeError" class="mt-1 text-sm text-red-600">{{ timeError }}</p>
            </div>
          </div>

          <!-- Classgroup -->
          <div>
            <label for="classgroup" class="block text-sm font-medium text-gray-700"
              >Classgroup</label
            >
            <div class="mt-1">
              <select
                id="classgroup"
                v-model="formData.classgroupId"
                required
                class="shadow-sm focus:ring-green-500 focus:border-green-500 block w-full sm:text-sm border-gray-300 rounded-md"
              >
                <option value="" disabled>Select a classgroup</option>
                <option
                  v-for="classgroup in classgroups"
                  :key="classgroup.id"
                  :value="classgroup.id"
                >
                  {{ classgroup.name }}
                </option>
              </select>
            </div>
          </div>

          <!-- Room Device -->
          <div>
            <label for="room-device" class="block text-sm font-medium text-gray-700"
              >Room Device</label
            >
            <div class="mt-1">
              <select
                id="room-device"
                v-model="formData.roomDeviceId"
                required
                class="shadow-sm focus:ring-green-500 focus:border-green-500 block w-full sm:text-sm border-gray-300 rounded-md"
              >
                <option value="" disabled>Select a device</option>
                <option v-for="device in roomDevices" :key="device.id" :value="device.id">
                  {{ device.roomName }} ({{ device.deviceIdentifier }})
                </option>
              </select>
            </div>
          </div>

          <!-- Conflict Warning -->
          <div v-if="conflictWarning" class="rounded-md bg-yellow-50 p-4">
            <div class="flex">
              <div class="flex-shrink-0">
                <svg
                  class="h-5 w-5 text-yellow-400"
                  xmlns="http://www.w3.org/2000/svg"
                  viewBox="0 0 20 20"
                  fill="currentColor"
                  aria-hidden="true"
                >
                  <path
                    fill-rule="evenodd"
                    d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z"
                    clip-rule="evenodd"
                  />
                </svg>
              </div>
              <div class="ml-3">
                <h3 class="text-sm font-medium text-yellow-800">Scheduling Conflict</h3>
                <div class="mt-2 text-sm text-yellow-700">
                  <p>{{ conflictWarning }}</p>
                </div>
              </div>
            </div>
          </div>

          <div class="mt-5 sm:mt-6 sm:grid sm:grid-cols-2 sm:gap-3 sm:grid-flow-row-dense">
            <button
              type="submit"
              :disabled="!!timeError || isSubmitting"
              class="w-full inline-flex justify-center rounded-md border border-transparent shadow-sm px-4 py-2 bg-green-600 text-base font-medium text-white hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500 sm:col-start-2 sm:text-sm disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {{ isSubmitting ? 'Saving...' : session.id ? 'Update Session' : 'Create Session' }}
            </button>
            <button
              type="button"
              class="mt-3 w-full inline-flex justify-center rounded-md border border-gray-300 shadow-sm px-4 py-2 bg-white text-base font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500 sm:mt-0 sm:col-start-1 sm:text-sm"
              @click="$emit('close')"
              :disabled="isSubmitting"
            >
              Cancel
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>


<script>
export default {
  props: {
    session: {
      type: Object,
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
    existingSessions: {
      type: Array,
      required: true,
    },
    selectedClassroom: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      formData: {
        date: '',
        startTime: '',
        endTime: '',
        classgroupId: '',
        roomDeviceId: '',
      },
      isSubmitting: false,
      timeError: '',
      conflictWarning: '',
    }
  },
  created() {
    this.initializeForm()
  },
  methods: {
    /**
     * Populate the form with data from the session if in edit mode, otherwise
     * set default values.
     *
     * If in edit mode, the form is populated with the existing values from the
     * session. If in create mode, the form is populated with default values.
     * The default values are set to the current date and the current time rounded
     * down to the nearest hour, with the end time set to one hour later.
     *
     * The form data is set to a new object with the following properties:
     * - date: The date of the session in ISO format (YYYY-MM-DD)
     * - startTime: The start time of the session in ISO format (HH:mm)
     * - endTime: The end time of the session in ISO format (HH:mm)
     * - classgroupId: The ID of the classgroup
     * - roomDeviceId: The ID of the room device
     */
    initializeForm() {
      if (this.session.id) {
        // Edit mode - populate form with existing data
        const startDate = new Date(this.session.startTime)
        const endDate = new Date(this.session.endTime)

        this.formData = {
          date: this.formatDateForInput(startDate),
          startTime: this.formatTimeForInput(startDate),
          endTime: this.formatTimeForInput(endDate),
          classgroupId: this.session.classgroupId,
          roomDeviceId: this.session.roomDeviceId,
        }
      } else {
        // Create mode - set default values
        const now = new Date()
        const roundedHour = new Date(now.setMinutes(0, 0, 0))
        const oneHourLater = new Date(roundedHour)
        oneHourLater.setHours(oneHourLater.getHours() + 1)

        this.formData = {
          date: this.formatDateForInput(now),
          startTime: this.formatTimeForInput(roundedHour),
          endTime: this.formatTimeForInput(oneHourLater),
          classgroupId: '',
          roomDeviceId: '',
        }
      }
    },
    formatDateForInput(date) {
      return date.toISOString().split('T')[0]
    },
    formatTimeForInput(date) {
      return date.toTimeString().substring(0, 5)
    },
    validateTimes() {
      if (!this.formData.startTime || !this.formData.endTime) {
        return false
      }

      const [startHours, startMinutes] = this.formData.startTime.split(':').map(Number)
      const [endHours, endMinutes] = this.formData.endTime.split(':').map(Number)

      if (endHours < startHours || (endHours === startHours && endMinutes <= startMinutes)) {
        this.timeError = 'End time must be after start time'
        return false
      }

      this.timeError = ''
      return true
    },
    checkForConflicts() {
      if (!this.formData.date || !this.formData.startTime || !this.formData.endTime) {
        return
      }

      const newSessionStart = new Date(`${this.formData.date}T${this.formData.startTime}`)
      const newSessionEnd = new Date(`${this.formData.date}T${this.formData.endTime}`)

      // Check for conflicts with existing sessions
      const conflicts = this.existingSessions.filter((existingSession) => {
        // Skip the current session when editing
        if (this.session.id && existingSession.id === this.session.id) {
          return false
        }

        const existingStart = new Date(existingSession.startTime)
        const existingEnd = new Date(existingSession.endTime)

        // Check if dates are the same
        if (existingStart.toDateString() !== newSessionStart.toDateString()) {
          return false
        }

        // Check for time overlap
        return (
          (newSessionStart >= existingStart && newSessionStart < existingEnd) ||
          (newSessionEnd > existingStart && newSessionEnd <= existingEnd) ||
          (newSessionStart <= existingStart && newSessionEnd >= existingEnd)
        )
      })

      if (conflicts.length > 0) {
        const conflictClassgroup = this.classgroups.find(
          (cg) => cg.id === conflicts[0].classgroupId,
        )
        const conflictStart = new Date(conflicts[0].startTime)
        const conflictEnd = new Date(conflicts[0].endTime)

        this.conflictWarning = `This time slot conflicts with "${conflictClassgroup?.name || 'Unknown'}" scheduled from ${this.formatTime(conflictStart)} to ${this.formatTime(conflictEnd)}.`
      } else {
        this.conflictWarning = ''
      }
    },
    formatTime(date) {
      return date.toLocaleTimeString('en-US', {
        hour: 'numeric',
        minute: '2-digit',
        hour12: true,
      })
    },
    saveSession() {
      if (!this.validateTimes()) {
        return
      }

      this.isSubmitting = true

      // Construct ISO datetime strings
      const startDateTime = `${this.formData.date}T${this.formData.startTime}:00`
      const endDateTime = `${this.formData.date}T${this.formData.endTime}:00`

      // Prepare session data
      const sessionData = {
        id: this.session.id,
        startTime: startDateTime,
        endTime: endDateTime,
        classgroupId: this.formData.classgroupId,
        roomDeviceId: this.formData.roomDeviceId,
      }

      // Emit the save event with the session data
      this.$emit('save', sessionData)
      this.isSubmitting = false
    },
  },
  watch: {
    'formData.startTime': function () {
      this.validateTimes()
      this.checkForConflicts()
    },
    'formData.endTime': function () {
      this.validateTimes()
      this.checkForConflicts()
    },
    'formData.date': function () {
      this.checkForConflicts()
    },
  },
}
</script>
