import './assets/main.css'

import { createRouter, createWebHistory } from 'vue-router'
import { createApp } from 'vue'
import App from './App.vue'
import ClassgroupOverview from './components/classgroupOverview/ClassgroupOverview.vue';
import ReadExcel from './components/ReadExcel.vue';
import NewClassgroup from './components/newClassgroup/NewClassgroup.vue';
import ClassroomScheduler from './components/scheduler/ClassroomScheduler.vue';
import SessionAttendanceTracker from './components/sessionAttendance/SessionAttendanceTracker.vue';
import HomePage from './components/home/HomePage.vue';

const routes = [
  { path: '/', component: HomePage },
  { path: '/classgroup', component: ClassgroupOverview },
  { path: '/classgroup/new', component: NewClassgroup },
  { path: '/schedule', component: ClassroomScheduler },
  { path: '/attendance/:sessionId', name: 'attendance', component: SessionAttendanceTracker, props: true }
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

createApp(App)
  .use(router)
  .mount('#app')

