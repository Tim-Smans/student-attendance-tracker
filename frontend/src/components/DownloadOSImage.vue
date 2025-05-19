<template>
  <div class="min-h-screen bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
    <div class="max-w-3xl mx-auto">
      <!-- Header -->
      <div class="text-center">
        <h1 class="text-3xl font-extrabold text-gray-900 sm:text-4xl">
          Download Our Custom OS
        </h1>
        <p class="mt-3 text-xl text-gray-500 sm:mt-4">
          Get the latest version of our custom operating system for a new device
        </p>
      </div>

      <!-- Main Content -->
      <div class="mt-10 bg-white shadow overflow-hidden rounded-lg">
        <!-- OS Version Info -->
        <div class="px-4 py-5 sm:p-6">
          <div class="flex items-center justify-between flex-wrap sm:flex-nowrap">
            <div>
              <h2 class="text-lg leading-6 font-medium text-gray-900">
                Custom OS v{{ osVersion }}
              </h2>
              <div class="mt-2 max-w-xl text-sm text-gray-500">
                <p>Released on {{ releaseDate }}</p>
                <p class="mt-1">File size: {{ fileSize }}</p>
              </div>
            </div>
            <div class="mt-5 sm:mt-0">
              <span class="inline-flex items-center px-3 py-0.5 rounded-full text-sm font-medium bg-orange-100 text-orange-800">
                Latest Version
              </span>
            </div>
          </div>

          <!-- Release Notes -->
          <div class="mt-6">
            <h3 class="text-sm font-medium text-gray-900">Release Notes:</h3>
            <div class="mt-2 text-sm text-gray-500">
              <ul class="list-disc pl-5 space-y-1">
                <li v-for="(note, index) in releaseNotes" :key="index">
                  {{ note }}
                </li>
              </ul>
            </div>
          </div>

          <!-- Download Button -->
          <div class="mt-8 flex justify-center">
            <button
              type="button"
              @click="downloadOS"
              class="inline-flex items-center px-6 py-3 border border-transparent text-base font-medium rounded-md shadow-sm text-white bg-orange-600 hover:bg-orange-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-orange-500"
              :class="{ 'opacity-75 cursor-wait': isDownloading }"
              :disabled="isDownloading"
            >
              <svg
                v-if="isDownloading"
                class="animate-spin -ml-1 mr-3 h-5 w-5 text-white"
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
              >
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              <svg
                v-else
                xmlns="http://www.w3.org/2000/svg"
                class="-ml-1 mr-3 h-5 w-5"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
              </svg>
              {{ isDownloading ? 'Downloading...' : 'Download Now' }}
            </button>
          </div>

          <!-- Additional Info -->
          <div class="mt-6 text-sm text-center text-gray-500">
            <p>Compatible with Raspberry Pi 3.</p>
            <p class="mt-1">
              Need help with installation?
              <a target="_blank" href="https://github.com/Tim-Smans/student-attendance-tracker/blob/os-image/raspberry_pi/README.md" class="font-medium text-orange-600 hover:text-orange-500">
                View installation guide
              </a>
            </p>
          </div>
        </div>
      </div>
    </div>

    <!-- Success Notification -->
    <div
      v-if="showNotification"
      class="fixed bottom-0 inset-x-0 pb-2 sm:pb-5"
    >
      <div class="max-w-md mx-auto px-2 sm:px-6 lg:px-8">
        <div class="p-2 rounded-lg shadow-lg sm:p-3 bg-orange-500">
          <div class="flex items-center justify-between flex-wrap">
            <div class="w-0 flex-1 flex items-center">
              <span class="flex p-2 rounded-lg bg-orange-600">
                <svg class="h-6 w-6 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                </svg>
              </span>
              <p class="ml-3 font-medium text-white truncate">
                {{ notificationMessage }}
              </p>
            </div>
            <div class="order-2 flex-shrink-0 sm:order-3 sm:ml-2">
              <button
                type="button"
                class="-mr-1 flex p-2 rounded-md hover:bg-orange-600 focus:outline-none"
                @click="showNotification = false"
              >
                <span class="sr-only">Dismiss</span>
                <svg class="h-6 w-6 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
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
export default {
  data() {
    return {
      osVersion: '1.0.1',
      releaseDate: 'May 10, 2025',
      fileSize: '1.5 GB',
      isDownloading: false,
      showNotification: false,
      notificationMessage: '',
      shaChecksum: 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855',
      releaseNotes: [
        'Improved system performance and stability',
        'Enhanced battery life optimization',
        'Added support for new hardware peripherals',
        'Fixed security vulnerabilities',
        'Updated core system components'
      ]
    }
  },
  methods: {
    downloadOS() {
      this.isDownloading = true;

      // Simulate download process
      setTimeout(() => {
        this.isDownloading = false;

        // In a real application, you would trigger the actual file download here
        // For example:
        window.location.href = 'https://github.com/Tim-Smans/student-attendance-tracker/releases/download/os-image/raspberry_image_v1.01.img.7z';

        // Show success notification
        this.notificationMessage = 'Download started successfully!';
        this.showNotification = true;

        // Auto-hide notification after 5 seconds
        setTimeout(() => {
          this.showNotification = false;
        }, 5000);
      }, 2000);
    },
  }
}
</script>
