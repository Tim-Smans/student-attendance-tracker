<template>
  <div class="bg-white shadow overflow-hidden sm:rounded-lg">
    <!-- Calendar Header -->
    <div class="px-4 py-5 sm:px-6 flex justify-between items-center">
      <div class="flex items-center">
        <button @click="previousWeek" class="mr-2 p-1 rounded-full hover:bg-gray-100">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            class="h-5 w-5 text-gray-600"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M15 19l-7-7 7-7"
            />
          </svg>
        </button>
        <h3 class="text-lg leading-6 font-medium text-gray-900">
          {{ formatDateRange(weekStart, weekEnd) }}
        </h3>
        <button @click="nextWeek" class="ml-2 p-1 rounded-full hover:bg-gray-100">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            class="h-5 w-5 text-gray-600"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M9 5l7 7-7 7"
            />
          </svg>
        </button>
      </div>
      <button
        @click="today"
        class="inline-flex items-center px-3 py-1 border border-gray-300 shadow-sm text-sm leading-4 font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500"
      >
        Today
      </button>
    </div>

    <!-- Calendar Grid -->
    <div class="overflow-x-auto">
      <div class="min-w-full">
        <!-- Days of Week Header -->
        <div class="grid grid-cols-8 border-b border-gray-200">
          <div
            class="py-3 text-center text-xs font-medium text-gray-500 uppercase tracking-wider border-r border-gray-200 bg-gray-50"
          >
            Time
          </div>
          <div
            v-for="(day, index) in daysOfWeek"
            :key="index"
            class="py-3 text-center text-xs font-medium text-gray-500 uppercase tracking-wider border-r border-gray-200 bg-gray-50"
            :class="{ 'bg-green-50': isToday(day.date) }"
          >
            <div>{{ day.name }}</div>
            <div class="text-sm text-gray-700">{{ formatDayDate(day.date) }}</div>
          </div>
        </div>

        <!-- Time Slots -->
        <div>
          <div v-for="hour in hours" :key="hour" class="grid grid-cols-8 border-b border-gray-200">
            <!-- Time Column -->
            <div class="py-2 text-center text-xs text-gray-500 border-r border-gray-200 bg-gray-50">
              {{ formatHour(hour) }}
            </div>

            <!-- Day Columns -->
            <div
              v-for="(day, dayIndex) in daysOfWeek"
              :key="`${hour}-${dayIndex}`"
              class="relative py-2 border-r border-gray-200 h-16"
              :class="{ 'bg-green-50': isToday(day.date) }"
            >
              <!-- Sessions that start in this time slot -->
              <div
                v-for="session in getSessionsForTimeSlot(day.date, hour)"
                :key="session.id"
                class="absolute left-0 right-0 mx-1 rounded-md px-2 py-1 text-xs font-medium text-white overflow-hidden cursor-pointer"
                :class="getSessionColor(session.classgroupId)"
                :style="getSessionStyle(session, hour)"
                @click="handleClick(session)"
                @dblclick="handleDoubleClick(session)"
              >
                <div class="font-bold truncate">{{ getClassgroupName(session.classgroupId) }}</div>
                <div class="truncate">{{ formatSessionTime(session) }}</div>
              </div>
            </div>
          </div>
        </div>
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
  },
  data() {
    return {
      weekStart: this.getWeekStart(new Date()),
      hours: Array.from({ length: 14 }, (_, i) => i + 8), // 8 AM to 9 PM
      colors: [
        'bg-blue-500',
        'bg-green-500',
        'bg-purple-500',
        'bg-yellow-500',
        'bg-pink-500',
        'bg-indigo-500',
        'bg-red-500',
        'bg-teal-500',
      ],
    }
  },
  computed: {
    weekEnd() {
      const end = new Date(this.weekStart)
      end.setDate(end.getDate() + 6)
      return end
    },
    daysOfWeek() {
      return Array.from({ length: 7 }, (_, i) => {
        const date = new Date(this.weekStart)
        date.setDate(date.getDate() + i)
        return {
          name: this.getDayName(date),
          date: new Date(date),
        }
      })
    },
  },
  methods: {
    getWeekStart(date) {
      const result = new Date(date)
      const day = result.getDay()
      result.setDate(result.getDate() - day + (day === 0 ? -6 : 1)) // Adjust to Monday
      result.setHours(0, 0, 0, 0)
      return result
    },
    getDayName(date) {
      return date.toLocaleDateString('en-US', { weekday: 'short' })
    },
    formatDayDate(date) {
      return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' })
    },
    formatDateRange(start, end) {
      const startMonth = start.toLocaleDateString('en-US', { month: 'short' })
      const endMonth = end.toLocaleDateString('en-US', { month: 'short' })
      const startDay = start.getDate()
      const endDay = end.getDate()
      const year = start.getFullYear()

      if (startMonth === endMonth) {
        return `${startMonth} ${startDay} - ${endDay}, ${year}`
      }
      return `${startMonth} ${startDay} - ${endMonth} ${endDay}, ${year}`
    },
    formatHour(hour) {
      return `${hour % 12 || 12} ${hour < 12 ? 'AM' : 'PM'}`
    },
    formatSessionTime(session) {
      const start = new Date(session.startTime)
      const end = new Date(session.endTime)
      return `${start.getHours() % 12 || 12}:${start.getMinutes().toString().padStart(2, '0')} - ${end.getHours() % 12 || 12}:${end.getMinutes().toString().padStart(2, '0')} ${end.getHours() < 12 ? 'AM' : 'PM'}`
    },
    isToday(date) {
      const today = new Date()
      return (
        date.getDate() === today.getDate() &&
        date.getMonth() === today.getMonth() &&
        date.getFullYear() === today.getFullYear()
      )
    },
    isSameDay(date1, date2) {
      return (
        date1.getDate() === date2.getDate() &&
        date1.getMonth() === date2.getMonth() &&
        date1.getFullYear() === date2.getFullYear()
      )
    },
    getSessionsForTimeSlot(day, hour) {
      return this.sessions.filter((session) => {
        const start = new Date(session.startTime)
        return this.isSameDay(start, day) && start.getHours() === hour
      })
    },
    getSessionStyle(session, hour) {
      const start = new Date(session.startTime)
      const end = new Date(session.endTime)

      // Calculate height based on duration
      const durationHours = (end - start) / (1000 * 60 * 60)
      const height = durationHours * 64 // 64px per hour (16px base height * 4)
      const topOffset = (start.getMinutes() / 60) * 64

      return {
        height: `${height}px`,
        top: `${topOffset}px`,
        zIndex: 10,
      }
    },
    getSessionColor(classgroupId) {
      if (!classgroupId) return 'bg-gray-500'

      // Hash string to number
      let hash = 0
      for (let i = 0; i < classgroupId.length; i++) {
        hash = classgroupId.charCodeAt(i) + ((hash << 5) - hash)
      }

      const colorIndex = Math.abs(hash) % this.colors.length
      return this.colors[colorIndex]
    },
    getClassgroupName(classgroupId) {
      const classgroup = this.classgroups.find((cg) => cg.id === classgroupId)
      return classgroup ? classgroup.name : 'Unknown Classgroup'
    },
    previousWeek() {
      const newStart = new Date(this.weekStart)
      newStart.setDate(newStart.getDate() - 7)
      this.weekStart = newStart
    },
    nextWeek() {
      const newStart = new Date(this.weekStart)
      newStart.setDate(newStart.getDate() + 7)
      this.weekStart = newStart
    },
    today() {
      this.weekStart = this.getWeekStart(new Date())
    },
    editSession(session) {
      this.$emit('edit-session', session)
    },
    deleteSession(session) {
      this.$emit('delete-session', session)
    },
    openAttendance(session) {
      if (!session || !session.id) {
        console.error('Invalid session object', session)
        return
      }
      this.$router.replace({ name: 'attendance', params: { sessionId: session.id } })
    },
    handleClick(session) {
      if (this.clickTimeout) {
        clearTimeout(this.clickTimeout)
        this.clickTimeout = null
      }
      this.clickTimeout = setTimeout(() => {
        this.editSession(session)
        this.clickTimeout = null
      }, 250)
    },
    handleDoubleClick(session) {
      if (this.clickTimeout) {
        clearTimeout(this.clickTimeout)
        this.clickTimeout = null
      }
      this.openAttendance(session)
    },
  },
}
</script>
