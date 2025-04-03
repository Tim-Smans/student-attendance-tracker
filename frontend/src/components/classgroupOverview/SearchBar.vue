<!-- components/SearchBar.vue -->
<template>
  <div class="mb-6">
    <div class="relative rounded-md shadow-sm max-w-md">
      <input
        type="text"
        :value="modelValue"
        @input="$emit('update:modelValue', $event.target.value)"
        class="block w-full pr-10 border-gray-300 rounded-md focus:ring-green-500 focus:border-green-500 pl-4 py-2"
        placeholder="Search classgroups or students..."
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
</template>

<script>
export default {
  name: 'SearchBar',
  props: {
    modelValue: {
      type: String,
      required: true,
    },
  },
}
</script>
