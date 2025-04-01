<script setup lang="ts">
import { readExcelFile } from '@/helpers/excelHelpers'
import type { ClassGroup } from '@/models/classGroup'
import { ref } from 'vue'

const fileInput = ref<HTMLInputElement | null>(null)
const files = ref()
const classGroup = ref<ClassGroup | null>(null)

function handleFileChange() {
  files.value = fileInput.value?.files || null
}

async function scanExcelFile() {
  if (!files.value || files.value.length === 0) return

  const file = files.value[0]
  classGroup.value = await readExcelFile(file)
  console.log('Gelezen klasgroep:', classGroup.value)
}
</script>

<template class="bg-red">
  <h1 class="m-10">Read excel:</h1>

  <input type="file" ref="fileInput" @change="handleFileChange" />
  <button class="mt-4 px-4 py-2 bg-blue-500 text-white rounded" @click="scanExcelFile">
    Scan Excel
  </button>

  <div v-if="classGroup">
    <div v-if="classGroup.students.length" class="mt-6">
      <h2 class="text-lg mb-2">Read students:</h2>
      <ul>
        <li v-for="(student, index) in classGroup.students" :key="index">
          {{ student.fullName }} ({{ student.studentNumber }})
        </li>
      </ul>
    </div>
  </div>
</template>

<style scoped></style>
