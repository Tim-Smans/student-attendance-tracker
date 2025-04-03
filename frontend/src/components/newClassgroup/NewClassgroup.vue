<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Header -->
    <header class="bg-white shadow">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        <h1 class="text-2xl font-bold text-gray-900">Import new Classgroup</h1>
      </div>
    </header>

    <!-- Main Content -->
    <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div class="max-w-3xl mx-auto">
        <!-- Instructions Card -->
        <Instructions />

        <!-- File Upload Area -->
        <div class="bg-white shadow sm:rounded-lg">
          <div class="px-4 py-5 sm:p-6">
            <div
              class="mt-1 flex justify-center px-6 pt-5 pb-6 border-2 border-dashed rounded-md"
              :class="[
                isDragOver ? 'border-green-500 bg-green-50' : 'border-gray-300',
                fileSelected ? 'bg-gray-50' : '',
              ]"
              @dragover.prevent="isDragOver = true"
              @dragleave.prevent="isDragOver = false"
              @drop.prevent="onFileDrop"
            >
              <div class="space-y-1 text-center">
                <div v-if="!fileSelected">
                  <svg
                    class="mx-auto h-12 w-12 text-gray-400"
                    stroke="currentColor"
                    fill="none"
                    viewBox="0 0 48 48"
                    aria-hidden="true"
                  >
                    <path
                      d="M28 8H12a4 4 0 00-4 4v20m32-12v8m0 0v8a4 4 0 01-4 4H12a4 4 0 01-4-4v-4m32-4l-3.172-3.172a4 4 0 00-5.656 0L28 28M8 32l9.172-9.172a4 4 0 015.656 0L28 28m0 0l4 4m4-24h8m-4-4v8m-12 4h.02"
                      stroke-width="2"
                      stroke-linecap="round"
                      stroke-linejoin="round"
                    />
                  </svg>
                  <div class="flex text-sm text-gray-600">
                    <label
                      for="file-upload"
                      class="relative cursor-pointer bg-white rounded-md font-medium text-green-600 hover:text-green-500 focus-within:outline-none"
                    >
                      <span>Upload a file</span>
                      <input
                        id="file-upload"
                        name="file-upload"
                        type="file"
                        class="sr-only"
                        accept=".xlsx,.xls,.csv"
                        @change="onFileChange"
                      />
                    </label>
                    <p class="pl-1">or drag it here</p>
                  </div>
                  <p class="text-xs text-gray-500">XLSX or XLS: maximum 10MB</p>
                </div>

                <!-- Selected File Info -->
                <div v-else class="w-full">
                  <div class="flex items-center justify-center">
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      class="h-8 w-8 text-green-500"
                      fill="none"
                      viewBox="0 0 24 24"
                      stroke="currentColor"
                    >
                      <path
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        stroke-width="2"
                        d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
                      />
                    </svg>
                  </div>
                  <p class="text-sm font-medium text-gray-900 mt-2">
                    {{ selectedFile.name }}
                  </p>
                  <p class="text-xs text-gray-500">
                    {{ formatFileSize(selectedFile.size) }}
                  </p>
                  <button
                    type="button"
                    class="mt-3 inline-flex items-center px-2.5 py-1.5 border border-transparent text-xs font-medium rounded text-red-700 bg-red-100 hover:bg-red-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500"
                    @click="removeFile"
                  >
                    Delete
                  </button>
                </div>
              </div>
            </div>

            <!-- Upload Progress -->
            <div v-if="isUploading" class="mt-6">
              <div class="relative pt-1">
                <div class="flex mb-2 items-center justify-between">
                  <div>
                    <span
                      class="text-xs font-semibold inline-block py-1 px-2 uppercase rounded-full text-green-600 bg-green-200"
                    >
                      Uploading file...
                    </span>
                  </div>
                  <div class="text-right">
                    <span class="text-xs font-semibold inline-block text-green-600">
                      {{ uploadProgress }}%
                    </span>
                  </div>
                </div>
                <div class="overflow-hidden h-2 mb-4 text-xs flex rounded bg-green-200">
                  <div
                    :style="{ width: uploadProgress + '%' }"
                    class="shadow-none flex flex-col text-center whitespace-nowrap text-white justify-center bg-green-500 transition-all duration-300"
                  ></div>
                </div>
              </div>
            </div>

            <!-- Submit Button -->
            <div class="mt-6">
              <button
                type="button"
                class="w-full inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-green-600 hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500 disabled:opacity-50 disabled:cursor-not-allowed"
                :disabled="!fileSelected || isUploading"
                @click="uploadFile"
              >
                <span v-if="!isUploading">Import Classgroup</span>
                <span v-else>Uploading...</span>
              </button>
            </div>
          </div>
        </div>
      </div>
    </main>

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
                <span class="sr-only">Sluiten</span>
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
import Instructions from './Instructions.vue'
import { readExcelFile } from '@/helpers/excelHelpers'
import { createClassgroup } from '@/helpers/classgroupHelpers'

export default {
  components: {
    Instructions,
  },
  data() {
    return {
      selectedFile: null,
      fileSelected: false,
      isDragOver: false,
      isUploading: false,
      uploadProgress: 0,
      notification: {
        show: false,
        type: 'success', // 'success', 'error', 'info'
        message: '',
        timeout: null,
      },
    }
  },
  methods: {
    onFileChange(event) {
      const file = event.target.files[0]
      if (file) {
        this.validateAndSetFile(file)
      }
    },

    onFileDrop(event) {
      this.isDragOver = false
      const file = event.dataTransfer.files[0]
      if (file) {
        this.validateAndSetFile(file)
      }
    },

    validateAndSetFile(file) {
      // Check file type
      const validTypes = [
        'application/vnd.ms-excel',
        'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        'text/csv',
      ]

      const fileExtension = file.name.split('.').pop().toLowerCase()
      const isValidExtension = ['xlsx', 'xls', 'csv'].includes(fileExtension)

      if (!validTypes.includes(file.type) && !isValidExtension) {
        this.showNotification('error', 'Ongeldig bestandsformaat. Upload een Excel of CSV bestand.')
        return
      }

      // Check file size (10MB max)
      if (file.size > 10 * 1024 * 1024) {
        this.showNotification('error', 'Bestand is te groot. Maximale grootte is 10MB.')
        return
      }

      this.selectedFile = file
      this.fileSelected = true
    },

    removeFile() {
      this.selectedFile = null
      this.fileSelected = false
      // Reset file input
      const fileInput = document.getElementById('file-upload')
      if (fileInput) {
        fileInput.value = ''
      }
    },

    formatFileSize(bytes) {
      if (bytes === 0) return '0 Bytes'

      const k = 1024
      const sizes = ['Bytes', 'KB', 'MB', 'GB']
      const i = Math.floor(Math.log(bytes) / Math.log(k))

      return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
    },

    async uploadFile() {
      if (!this.selectedFile) return

      this.isUploading = true
      this.uploadProgress = 0

      try {
        this.uploadProgress = 30

        // Read the excel file
        const classGroupData = await readExcelFile(this.selectedFile)

        this.uploadProgress = 60

        // Create the classgroup using the API
        const classGroupInput = { ...classGroupData }
        const result = await createClassgroup(classGroupInput)

        this.uploadProgress = 100

        // Check the result
        if (result) {
          this.showNotification('success', 'Klasgroep succesvol geïmporteerd!')
        } else {
          this.showNotification('error', 'Importeren mislukt. Geen geldige klasgroep aangemaakt.')
        }

        this.removeFile()
      } catch (error) {
        console.error('Upload error:', error)
        this.showNotification(
          'error',
          'Er is een fout opgetreden bij het verwerken van het bestand.',
        )
      } finally {
        this.isUploading = false
      }
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
