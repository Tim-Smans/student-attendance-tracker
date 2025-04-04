<template>
  <div :class="`bg-white overflow-hidden shadow rounded-lg`">
    <div class="px-4 py-5 sm:p-6">
      <div class="flex items-center">
        <div :class="`flex-shrink-0 bg-${color}-100 rounded-md p-3`">
          <slot>
            <svg
              xmlns="http://www.w3.org/2000/svg"
              class="h-6 w-6"
              :class="`text-${color}-600`"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                v-if="color === 'green'"
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M5 13l4 4L19 7"
              />
              <path
                v-else
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M6 18L18 6M6 6l12 12"
              />
            </svg>
          </slot>
        </div>
        <div class="ml-5 w-0 flex-1">
          <dl>
            <dt class="text-sm font-medium text-gray-500 truncate">{{ title }}</dt>
            <dd>
              <div class="text-lg font-medium text-gray-900">{{ count }} ({{ percentage }}%)</div>
            </dd>
          </dl>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    color: {
      type: String,
      required: true,
    },
    title: {
      type: String,
      required: true,
    },
    count: {
      type: Number,
      required: true,
    },
    percentage: {
      type: Number,
      required: true,
    },
  },
}
</script>
