<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Header -->
    <header class="bg-white shadow">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        <h1 class="text-2xl font-bold text-gray-900">Classroom Schedule Configuration</h1>
      </div>
    </header>

    <!-- Main Content -->
    <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <!-- Classroom Selector -->
      <ClassroomSelector
        :classrooms="classrooms"
        :selectedClassroom="selectedClassroom"
        @select-classroom="selectClassroom"
        @update-sessions="sessions = $event"
      />

      <div v-if="selectedClassroom" class="mt-8">
        <div class="bg-white shadow overflow-hidden sm:rounded-lg">
          <div class="px-4 py-5 sm:px-6 flex justify-between items-center">
            <div>
              <h2 class="text-lg leading-6 font-medium text-gray-900">
                Schedule for {{ selectedClassroom.name }}
              </h2>
              <p class="mt-1 max-w-2xl text-sm text-gray-500">
                {{ selectedClassroom.location }} • Capacity:
                {{ selectedClassroom.capacity }} students
              </p>
            </div>
            <button
              @click="openSessionForm(null)"
              class="inline-flex items-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-orange-600 hover:bg-orange-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-orange-500"
            >
              <svg
                xmlns="http://www.w3.org/2000/svg"
                class="-ml-1 mr-2 h-5 w-5"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M12 6v6m0 0v6m0-6h6m-6 0H6"
                />
              </svg>
              Add Session
            </button>
          </div>
        </div>

        <!-- Schedule View Tabs -->
        <div class="mt-4 sm:mt-6">
          <div class="sm:hidden">
            <label for="view-tabs" class="sr-only">Select a view</label>
            <select
              id="view-tabs"
              v-model="activeView"
              class="block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-orange-500 focus:border-orange-500 sm:text-sm rounded-md"
            >
              <option value="calendar">Calendar View</option>
              <option value="list">List View</option>
            </select>
          </div>
          <div class="hidden sm:block">
            <div class="border-b border-gray-200">
              <nav class="-mb-px flex space-x-8" aria-label="Tabs">
                <button
                  @click="activeView = 'calendar'"
                  :class="[
                    activeView === 'calendar'
                      ? 'border-orange-500 text-orange-600'
                      : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300',
                    'whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm',
                  ]"
                >
                  Calendar View
                </button>
                <button
                  @click="activeView = 'list'"
                  :class="[
                    activeView === 'list'
                      ? 'border-orange-500 text-orange-600'
                      : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300',
                    'whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm',
                  ]"
                >
                  List View
                </button>
              </nav>
            </div>
          </div>
        </div>

        <!-- Calendar View -->
        <div v-if="activeView === 'calendar'" class="mt-6">
          <ScheduleCalendar
            :sessions="filteredSessions"
            :classgroups="classgroups"
            @edit-session="openSessionForm"
            @delete-session="confirmDeleteSession"
          />
        </div>

        <!-- List View -->
        <div v-if="activeView === 'list'" class="mt-6">
          <SessionList
            :sessions="filteredSessions"
            :classgroups="classgroups"
            :roomDevices="roomDevices"
            @edit-session="openSessionForm"
            @delete-session="confirmDeleteSession"
          />
        </div>
      </div>

      <div v-else class="mt-8 text-center py-12 bg-white shadow overflow-hidden sm:rounded-lg">
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
        <h3 class="mt-2 text-sm font-medium text-gray-900">No classroom selected</h3>
        <p class="mt-1 text-sm text-gray-500">
          Please select a classroom to configure its schedule.
        </p>
      </div>
    </main>

    <!-- Session Form Modal -->
    <SessionForm
      v-if="showSessionForm"
      :session="currentSession"
      :classgroups="classgroups"
      :roomDevices="roomDevices"
      :existingSessions="sessions"
      :selectedClassroom="selectedClassroom"
      @close="showSessionForm = false"
      @save="saveSession"
    />

    <!-- Delete Confirmation Modal -->
    <div
      v-if="showDeleteConfirmation"
      class="fixed z-10 inset-0 overflow-y-auto"
      aria-labelledby="modal-title"
      role="dialog"
      aria-modal="true"
    >
      <div
        class="flex items-end justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0"
      >
        <div
          class="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity"
          aria-hidden="true"
        ></div>
        <span class="hidden sm:inline-block sm:align-middle sm:h-screen" aria-hidden="true"
          >&#8203;</span
        >
        <div
          class="inline-block align-bottom bg-white rounded-lg px-4 pt-5 pb-4 text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-lg sm:w-full sm:p-6"
        >
          <div class="sm:flex sm:items-start">
            <div
              class="mx-auto flex-shrink-0 flex items-center justify-center h-12 w-12 rounded-full bg-red-100 sm:mx-0 sm:h-10 sm:w-10"
            >
              <svg
                class="h-6 w-6 text-red-600"
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
                aria-hidden="true"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"
                />
              </svg>
            </div>
            <div class="mt-3 text-center sm:mt-0 sm:ml-4 sm:text-left">
              <h3 class="text-lg leading-6 font-medium text-gray-900" id="modal-title">
                Delete Session
              </h3>
              <div class="mt-2">
                <p class="text-sm text-gray-500">
                  Are you sure you want to delete this session? This action cannot be undone.
                </p>
              </div>
            </div>
          </div>
          <div class="mt-5 sm:mt-4 sm:flex sm:flex-row-reverse">
            <button
              type="button"
              class="w-full inline-flex justify-center rounded-md border border-transparent shadow-sm px-4 py-2 bg-red-600 text-base font-medium text-white hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500 sm:ml-3 sm:w-auto sm:text-sm"
              @click="deleteSession"
            >
              Delete
            </button>
            <button
              type="button"
              class="mt-3 w-full inline-flex justify-center rounded-md border border-gray-300 shadow-sm px-4 py-2 bg-white text-base font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-orange-500 sm:mt-0 sm:w-auto sm:text-sm"
              @click="showDeleteConfirmation = false"
            >
              Cancel
            </button>
          </div>
        </div>
      </div>
    </div>

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
import ClassroomSelector from './ClassroomSelector.vue'
import ScheduleCalendar from './ScheduleCalendar.vue'
import SessionList from './SessionList.vue'
import SessionForm from './SessionForm.vue'
import { getDevices } from '@/helpers/deviceHelpers'
import { createSession, getSessionsOfRoomDevice } from '@/helpers/sessionHelpers'
import { getAllClassgroups } from '@/helpers/classgroupHelpers'

export default {
  components: {
    ClassroomSelector,
    ScheduleCalendar,
    SessionList,
    SessionForm,
  },
  data() {
    return {
      classrooms: [],
      selectedClassroom: null,
      sessions: [],
      classgroups: [],
      roomDevices: [],
      activeView: 'calendar',
      showSessionForm: false,
      currentSession: null,
      showDeleteConfirmation: false,
      sessionToDelete: null,
      notification: {
        show: false,
        type: 'success',
        message: '',
        timeout: null,
      },
    }
  },

  /**
   * Lifecycle hook called when the component is created.
   * Initializes the component by fetching data for classrooms (devices), classgroups, and room devices.
   */
  created() {
    this.fetchClassrooms()
    this.fetchClassgroups()
    this.fetchRoomDevices()
  },
  computed: {
    filteredSessions() {
      if (!this.selectedClassroom) return []
      return this.sessions.filter((session) => session.roomDeviceId === this.selectedClassroom.id)
    },
  },
  methods: {
    async fetchClassrooms() {
      try {
        this.classrooms = await getDevices()
      } catch (error) {
        console.error('Could not retrieve rooms:', error)
      }
    },
    async fetchClassgroups() {
      try {
        this.classgroups = await getAllClassgroups()
      } catch (error) {
        console.error('Could not retrieve classgroups:', error)
      }
    },
    async fetchRoomDevices() {
      try {
        this.roomDevices = await getDevices()
      } catch (error) {
        console.error('Could not retrieve rooms devices:', error)
      }
    },
    async fetchSessions() {
      if (!this.selectedClassroom) return
      try {
        const sessions = await getSessionsOfRoomDevice(this.selectedClassroom.id)
        console.log(sessions)
        this.sessions = sessions
      } catch (error) {
        console.error('Could not retrieve sessions:', error)
        this.showNotification('error', 'Failed to fetch sessions')
      }
    },
    selectClassroom(classroom) {
      this.selectedClassroom = classroom
      this.fetchSessions()
    },
    openSessionForm(session) {
      this.currentSession = session
        ? { ...session }
        : {
            id: null,
            startTime: '',
            endTime: '',
            classgroupId: '',
            roomDeviceId: '',
          }
      this.showSessionForm = true
    },
    /**
     * Save a session by either creating a new one or updating an existing one.
     * If the sessionData has an id, it will be updated, otherwise a new session is created.
     * @param {Object} sessionData - Session data to be saved, with the following properties:
     *  - id: The id of the session to update, if null a new session is created
     *  - startTime: The start time of the session
     *  - endTime: The end time of the session
     *  - classgroupId: The id of the classgroup
     *  - roomDeviceId: The id of the room device
     */
    async saveSession(sessionData) {
      if (sessionData.id) {
        // Update existing session
        const index = this.sessions.findIndex((s) => s.id === sessionData.id)
        if (index !== -1) {
          const sessionRequest = {
            classgroup_id: sessionData.classgroupId,
            room_device_id: sessionData.roomDeviceId,
            start_time: sessionData.startTime,
            end_time: sessionData.endTime,
          }

          //Add update here
          this.showNotification('success', 'Session updated successfully')
        }
      } else {
        const sessionRequest = {
          classgroup_id: sessionData.classgroupId,
          room_device_id: sessionData.roomDeviceId,
          start_time: sessionData.startTime,
          end_time: sessionData.endTime,
        }

        // Add new session
        await createSession(sessionRequest)
        await this.fetchSessions()
        this.showNotification('success', 'New session added successfully')
      }
      this.showSessionForm = false
    },
    confirmDeleteSession(session) {
      this.sessionToDelete = session
      this.showDeleteConfirmation = true
    },
    deleteSession() {
      if (this.sessionToDelete) {
        const index = this.sessions.findIndex((s) => s.id === this.sessionToDelete.id)
        if (index !== -1) {
          this.sessions.splice(index, 1)
          this.showNotification('success', 'Session deleted successfully')
        }
      }
      this.showDeleteConfirmation = false
      this.sessionToDelete = null
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
