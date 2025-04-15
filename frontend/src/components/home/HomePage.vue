<template>
  <div class="min-h-screen bg-gray-50">
    <HomeHero />
    <HomeStats :classgroupsAmmount="classgroupCount" />
    <HomeNav />
  </div>
</template>

<script>
import { getClassgroupCount } from '@/helpers/classgroupHelpers'
import HomeHero from './HomeHero.vue'
import HomeNav from './HomeNav.vue'
import HomeStats from './HomeStats.vue'

export default {
  components: {
    HomeHero,
    HomeStats,
    HomeNav,
  },
  data() {
    return {
      classgroupCount: 0,
    }
  },
  created() {
    this.fetchClassgroupCount()
  },
  methods: {
    async fetchClassgroupCount() {
      try {
        this.classgroupCount = await getClassgroupCount()
      } catch (error) {
        console.error('Could not retrieve classgroups:', error)
      }
    },
  },
}
</script>
