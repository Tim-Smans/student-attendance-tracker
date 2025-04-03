import './assets/main.css'

import { createMemoryHistory, createRouter, createWebHistory } from 'vue-router'
import { createApp } from 'vue'
import App from './App.vue'
import ClassgroupOverview from './components/classgroupOverview/ClassgroupOverview.vue';
import ReadExcel from './components/ReadExcel.vue';
import NewClassgroup from './components/newClassgroup/NewClassgroup.vue';
import ClassroomScheduler from './components/scheduler/ClassroomScheduler.vue';
import SessionAttendanceTracker from './components/sessionAttendance/SessionAttendanceTracker.vue';

const routes = [
  { path: '/', component: ReadExcel },
  { path: '/classgroup', component: ClassgroupOverview },
  { path: '/classgroup/new', component: NewClassgroup },
  { path: '/schedule', component: ClassroomScheduler },
  { path: '/attendance/:sessionId', component: SessionAttendanceTracker, props: true },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

createApp(App)
  .use(router)
  .mount('#app')

