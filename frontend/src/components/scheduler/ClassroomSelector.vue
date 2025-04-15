<template>
  <div class="bg-white shadow overflow-hidden sm:rounded-lg">
    <div class="px-4 py-5 sm:px-6">
      <h2 class="text-lg leading-6 font-medium text-gray-900">Select a Classroom</h2>
      <p class="mt-1 max-w-2xl text-sm text-gray-500">
        Choose a classroom to configure its schedule
      </p>
    </div>
    <div class="border-t border-gray-200 px-4 py-5 sm:p-0">
      <div class="sm:px-6 py-5">
        <div class="mb-4">
          <div class="relative rounded-md shadow-sm">
            <input
              type="text"
              v-model="searchQuery"
              class="block w-full pr-10 sm:text-sm border-gray-300 rounded-md focus:ring-orange-500 focus:border-orange-500"
              placeholder="Search classrooms..."
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

        <div class="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
          <div
            v-for="classroom in filteredClassrooms"
            :key="classroom.id"
            class="relative rounded-lg border border-gray-300 bg-white px-6 py-5 shadow-sm flex items-center space-x-3 hover:border-gray-400 focus-within:ring-2 focus-within:ring-offset-2 focus-within:ring-orange-500 cursor-pointer"
            :class="{ 'ring-2 ring-orange-500 ring-offset-2': isSelected(classroom) }"
            @click="selectClassroom(classroom)"
          >
            <div class="flex-shrink-0">
              <div class="h-10 w-10 rounded-full bg-orange-100 flex items-center justify-center">
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  class="h-6 w-6 text-orange-600"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"
                  />
                </svg>
              </div>
            </div>
            <div class="flex-1 min-w-0">
              <a href="#" class="focus:outline-none">
                <span class="absolute inset-0" aria-hidden="true"></span>
                <p class="text-sm font-medium text-gray-900">Room: {{ classroom.roomName }}</p>
                <p class="text-sm text-gray-500 truncate">
                  Device Identifier: {{ classroom.deviceIdentifier }}
                </p>
              </a>
            </div>
            <div v-if="isSelected(classroom)" class="flex-shrink-0">
              <svg
                xmlns="http://www.w3.org/2000/svg"
                class="h-5 w-5 text-orange-500"
                viewBox="0 0 20 20"
                fill="currentColor"
              >
                <path
                  fill-rule="evenodd"
                  d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"
                  clip-rule="evenodd"
                />
              </svg>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { getSessionsOfRoomDevice } from '@/helpers/sessionHelpers'

export default {
  props: {
    classrooms: {
      type: Array,
      required: true,
    },
    selectedClassroom: {
      type: Object,
      default: null,
    },
  },
  data() {
    return {
      searchQuery: '',
    }
  },
  computed: {
    filteredClassrooms() {
      if (!this.searchQuery) {
        return this.classrooms
      }

      const query = this.searchQuery.toLowerCase()
      return this.classrooms.filter(
        (classroom) =>
          classroom.roomName.toLowerCase().includes(query) ||
          classroom.deviceIdentifier.toLowerCase().includes(query),
      )
    },
  },
  methods: {
    selectClassroom(classroom) {
      this.$emit('select-classroom', classroom)
      this.fetchSessions(classroom.id)
    },
    isSelected(classroom) {
      return this.selectedClassroom && this.selectedClassroom.id === classroom.id
    },
    async fetchSessions(id) {
      try {
        const sessions = await getSessionsOfRoomDevice(id)
        this.$emit('update-sessions', sessions)
      } catch (error) {
        console.error('Could not retrieve rooms:', error)
      }
    },
  },
}
</script>
