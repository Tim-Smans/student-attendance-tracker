<template>
  <div class="bg-white shadow overflow-hidden sm:rounded-lg">
    <div class="px-4 py-5 sm:px-6">
      <h3 class="text-lg leading-6 font-medium text-gray-900">Attendance Summary</h3>
    </div>

    <div class="border-t border-gray-200 px-4 py-5 sm:p-6">
      <div class="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4">
        <!-- Present -->
        <SummaryCard color="green" title="Present" :count="present" :percentage="presentPercentage" />

        <!-- Absent -->
        <SummaryCard color="red" title="Absent" :count="absent" :percentage="absentPercentage" />

        <div :class="`bg-white overflow-hidden shadow rounded-lg`">
          <div class="px-4 py-5 sm:p-6">
            <div class="flex items-center">
              <div class="ml-5 w-0 flex-1">
                <dl>
                  <button @click="downloadSessionExcel"
                    class="inline-flex items-center px-4 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500">Convert
                    this session to Excel</button>
                </dl>
              </div>
            </div>
          </div>
        </div>


        <div :class="`bg-white overflow-hidden shadow rounded-lg`">
          <div class="px-4 py-5 sm:p-6">
            <div class="flex items-center">
              <div class="ml-5 w-0 flex-1">
                <dl>
                  <button @click="downloadClassgroupExcel"
                    class="inline-flex items-center px-4 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500">Convert
                    all sessions of classgroup to Excel</button>
                </dl>
              </div>
            </div>
          </div>
        </div>
      </div>


      <!-- Progress Bar -->
      <div class="mt-6">
        <div class="flex mb-2 items-center justify-between">
          <span class="text-xs font-semibold inline-block py-1 px-2 uppercase rounded-full text-green-600 bg-green-200">
            Attendance Rate
          </span>
          <span class="text-xs font-semibold inline-block text-green-600">
            {{ presentPercentage }}%
          </span>
        </div>
        <div class="overflow-hidden h-2 mb-4 text-xs flex rounded bg-gray-200">
          <div :style="{ width: presentPercentage + '%' }"
            class="shadow-none flex flex-col text-center whitespace-nowrap text-white justify-center bg-green-500 transition-all duration-500">
          </div>
          <div :style="{ width: absentPercentage + '%' }"
            class="shadow-none flex flex-col text-center whitespace-nowrap text-white justify-center bg-red-500 transition-all duration-500">
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { createWorkbook } from '@/helpers/excelHelpers'
import SummaryCard from './SummaryCard.vue'

export default {
  components: {
    SummaryCard,
  },
  props: {
    present: {
      type: Number,
      required: true,
    },
    absent: {
      type: Number,
      required: true,
    },
    session: {
      type: Object,
      required: true,
    }
  },
  computed: {
    total() {
      return this.present + this.absent
    },
    presentPercentage() {
      return this.total ? Math.round((this.present / this.total) * 100) : 0
    },
    absentPercentage() {
      return this.total ? Math.round((this.absent / this.total) * 100) : 0
    },
  },
  methods: {
    downloadSessionExcel() {
      createWorkbook([this.session])
    },
    downloadClassgroupExcel() {
      createWorkbook([this.session])
    }
  }
}
</script>
