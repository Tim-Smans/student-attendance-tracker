<template>
  <div class="min-h-screen bg-gray-50">
    <HomeHero />
    <HomeStats
      :classgroupsAmmount="classgroupCount"
      :sessionsAmmount="sessionCount"
      :studentsAmmount="studentCount"
    />
    <HomeNav />
  </div>
</template>

<script>
import { getClassgroupCount } from '@/helpers/classgroupHelpers'
import HomeHero from './HomeHero.vue'
import HomeNav from './HomeNav.vue'
import HomeStats from './HomeStats.vue'
import { getSessionsCount } from '@/helpers/sessionHelpers'
import { getTotalStudentCount } from '@/helpers/studentHelpers'

export default {
  components: {
    HomeHero,
    HomeStats,
    HomeNav,
  },
  data() {
    return {
      classgroupCount: 0,
      sessionCount: 0,
      studentCount: 0,
    }
  },
  created() {
    this.fetchClassgroupCount()
    this.fetchSessionsCount()
    this.fetchStudentsCount()
  },
  methods: {
    async fetchClassgroupCount() {
      try {
        this.classgroupCount = await getClassgroupCount()
      } catch (error) {
        console.error('Could not retrieve classgroup count:', error)
      }
    },
    async fetchSessionsCount() {
      try {
        this.sessionCount = await getSessionsCount()
      } catch (error) {
        console.error('Could not retrieve session count:', error)
      }
    },
    async fetchStudentsCount() {
      try {
        this.studentCount = await getTotalStudentCount()
      } catch (error) {
        console.error('Could not retrieve student count:', error)
      }
    },
  },
}
</script>
