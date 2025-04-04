<template>
  <div class="bg-white shadow overflow-hidden sm:rounded-lg">
    <div class="px-4 py-5 sm:px-6">
      <div class="flex flex-col sm:flex-row sm:justify-between sm:items-center">
        <div>
          <h2 class="text-lg leading-6 font-medium text-gray-900">
            {{ session.classgroup.name }}
          </h2>
          <p class="mt-1 max-w-2xl text-sm text-gray-500">
            Session on {{ formatDate(session.startTime) }}
          </p>
        </div>
        <div class="mt-3 sm:mt-0 flex items-center">
          <span
            class="inline-flex items-center px-3 py-0.5 rounded-full text-sm font-medium bg-green-100 text-green-800"
          >
            {{ formatTimeRange(session.startTime, session.endTime) }}
          </span>
        </div>
      </div>
    </div>
    <div class="border-t border-gray-200">
      <dl>
        <div class="bg-gray-50 px-4 py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
          <dt class="text-sm font-medium text-gray-500">Classroom</dt>
          <dd class="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">{{ classroom.roomName }}</dd>
        </div>
        <div class="bg-white px-4 py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
          <dt class="text-sm font-medium text-gray-500">Date</dt>
          <dd class="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">
            {{ formatDate(session.startTime) }}
          </dd>
        </div>
        <div class="bg-gray-50 px-4 py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
          <dt class="text-sm font-medium text-gray-500">Time</dt>
          <dd class="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">
            {{ formatTimeRange(session.startTime, session.endTime) }}
          </dd>
        </div>
      </dl>
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
    classgroup: {
      type: Object,
      required: true,
    },
    classroom: {
      type: Object,
      required: true,
    },
  },
  mounted() {
    console.log(this.classroom)
  },
  methods: {
    formatDate(dateString) {
      const date = new Date(dateString)
      return date.toLocaleDateString('en-US', {
        weekday: 'long',
        year: 'numeric',
        month: 'long',
        day: 'numeric',
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
  },
}
</script>
