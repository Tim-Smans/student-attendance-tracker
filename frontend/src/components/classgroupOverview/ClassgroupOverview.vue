<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Header -->
    <OverviewHeader />

    <!-- Main Content -->
    <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <!-- Search -->
      <SearchBar v-model="searchQuery" />

      <!-- Loading -->
      <div v-if="loading" class="text-center text-gray-500 py-10">
        Loading classgroups and students...
      </div>

      <template v-else>
        <!-- Stats -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <StatsCard
            title="Total Classgroups"
            :value="filteredClassgroups.length"
            iconWrapperClass="bg-green-100 p-3 rounded-md"
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              class="h-6 w-6 text-green-600"
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
          </StatsCard>

          <StatsCard
            title="Total Students"
            :value="totalStudents"
            iconWrapperClass="bg-blue-100 p-3 rounded-md"
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              class="h-6 w-6 text-blue-600"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"
              />
            </svg>
          </StatsCard>

          <StatsCard
            title="Import a new classgroup"
            :value="null"
            iconWrapperClass="bg-blue-100 p-3 rounded-md"
          >
            <button class="text-indigo-600 hover:text-indigo-900">
              <router-link to="/classgroup/new" class="text-gray-700" exact>
                Import classgroup
              </router-link>
            </button>
          </StatsCard>
        </div>

        <!-- Classgroups List -->
        <div class="space-y-4">
          <div
            v-for="(classgroup, index) in filteredClassgroups"
            :key="index"
            class="bg-white shadow overflow-hidden sm:rounded-lg"
          >
            <!-- Classgroup Header -->
            <div
              @click="toggleClassgroup(classgroup.id)"
              class="px-4 py-5 sm:px-6 flex justify-between items-center cursor-pointer hover:bg-gray-50"
            >
              <div>
                <h3 class="text-lg leading-6 font-medium text-gray-900">{{ classgroup.name }}</h3>
                <p class="mt-1 max-w-2xl text-sm text-gray-500">
                  <div v-if="classgroup.students.length === 10">
                    {{ classgroup.students.length }}+ students
                  </div>
                  <div v-else>
                    {{ classgroup.students.length }} students
                  </div>
                </p>
              </div>
              <div class="flex items-center">
                <span
                  class="inline-flex items-center px-3 py-0.5 rounded-full text-sm font-medium bg-green-100 text-green-800 mr-3"
                >
                  <div v-if="classgroup.students.length === 10">
                    {{ classgroup.students.length }}+ students
                  </div>
                  <div v-else>
                    {{ classgroup.students.length }} students
                  </div>
                </span>
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  class="h-5 w-5 text-gray-400 transition-transform duration-200"
                  :class="{ 'transform rotate-180': expandedClassgroups.includes(classgroup.id) }"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M19 9l-7 7-7-7"
                  />
                </svg>
              </div>
            </div>

            <!-- Student List -->
            <div
              v-if="expandedClassgroups.includes(classgroup.id)"
              class="border-t border-gray-200"
            >
              <div class="overflow-x-auto">
                <table class="min-w-full divide-y divide-gray-200">
                  <thead class="bg-gray-50">
                    <tr>
                      <th
                        class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                      >
                        Student ID
                      </th>
                      <th
                        class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                      >
                        Name
                      </th>
                      <th
                        class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                      >
                        Email
                      </th>
                      <th
                        class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                      >
                        Degree Programme
                      </th>
                      <th
                        class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                      >
                        Actions
                      </th>
                    </tr>
                  </thead>
                  <tbody class="bg-white divide-y divide-gray-200">
                    <tr
                      v-for="student in filteredStudents(classgroup)"
                      :key="student.studentNumber"
                      class="hover:bg-gray-50"
                    >
                      <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                        {{ student.studentNumber }}
                      </td>
                      <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                        {{ student.firstName }} {{ student.lastName }}
                      </td>
                      <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                        {{ student.email }}
                      </td>
                      <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                        <span
                          class="px-2 py-1 inline-flex text-xs leading-5 font-semibold rounded-full bg-blue-100 text-blue-800"
                        >
                          {{ student.degreeProgramme }}
                        </span>
                      </td>
                      <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                        <button class="text-green-600 hover:text-green-900 mr-3">View</button>
                        <button class="text-indigo-600 hover:text-indigo-900 mr-3">Edit</button>
                      </td>
                    </tr>
                    <tr v-if="filteredStudents(classgroup).length === 10">
                      <td colspan="5" class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                        <span class="text-sm text-gray-500">+ more, see classgroup details for a full list of students.</span>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>

              <div v-if="filteredStudents(classgroup).length === 0" class="py-8 text-center">
                <p class="text-sm text-gray-500">No students match your search criteria.</p>
              </div>
            </div>
          </div>

          <!-- Empty State -->
          <div
            v-if="filteredClassgroups.length === 0"
            class="bg-white shadow overflow-hidden sm:rounded-lg py-8 text-center"
          >
            <p class="text-sm text-gray-500">No classgroups match your search criteria.</p>
          </div>
        </div>
      </template>
    </main>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import OverviewHeader from './OverviewHeader.vue'
import StatsCard from './StatsCard.vue'
import SearchBar from './SearchBar.vue'
import { getAllClassgroups, getStudentsFromClassgroup } from '@/helpers/classgroupHelpers'
import { getTotalStudentCount } from '@/helpers/studentHelpers'

export default {
  components: {
    OverviewHeader,
    StatsCard,
    SearchBar,
  },
  setup() {
    const classgroups = ref([])
    const searchQuery = ref('')
    const expandedClassgroups = ref([])
    const loading = ref(true)
    const totalStudents = ref(null)

    onMounted(async () => {
      const groups = await getAllClassgroups()

      const enrichedGroups = await Promise.all(
        groups.map(async (group) => {
          const students = await getStudentsFromClassgroup(group.id)
          return { ...group, students }
        }),
      )

      classgroups.value = enrichedGroups
      loading.value = false

      try {
        totalStudents.value = await getTotalStudentCount()
      } catch (err) {
        console.error('Failed to fetch student count:', err)
      }
    })

    const toggleClassgroup = (id) => {
      if (expandedClassgroups.value.includes(id)) {
        expandedClassgroups.value = expandedClassgroups.value.filter((groupId) => groupId !== id)
      } else {
        expandedClassgroups.value.push(id)
      }
    }

    const filteredClassgroups = computed(() => {
      if (!searchQuery.value) return classgroups.value

      const query = searchQuery.value.toLowerCase()

      return classgroups.value.filter((group) => {
        if (group.name.toLowerCase().includes(query)) return true

        return group.students.some((student) =>
          [
            student.studentNumber,
            student.firstName,
            student.lastName,
            student.email,
            student.degreeProgramme,
          ].some((field) => field.toLowerCase().includes(query)),
        )
      })
    })

    const filteredStudents = (classgroup) => {
      if (!searchQuery.value) return classgroup.students

      const query = searchQuery.value.toLowerCase()
      return classgroup.students.filter((student) =>
        [
          student.studentNumber,
          student.firstName,
          student.lastName,
          student.email,
          student.degreeProgramme,
        ].some((field) => field.toLowerCase().includes(query)),
      )
    }

    const uniqueDegreePrograms = computed(() => {
      const set = new Set()
      classgroups.value.forEach((group) => {
        group.students.forEach((student) => set.add(student.degreeProgramme))
      })
      return Array.from(set)
    })

    return {
      loading,
      searchQuery,
      classgroups,
      expandedClassgroups,
      filteredClassgroups,
      filteredStudents,
      toggleClassgroup,
      totalStudents,
      uniqueDegreePrograms,
    }
  },
}
</script>
