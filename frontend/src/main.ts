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
import vue3GoogleLogin from 'vue3-google-login'
import { useAuthStore } from './stores/auth';
import Login from './components/Login.vue';
import { createPinia } from 'pinia';

const routes = [
  { path: '/login', name: 'Login', component: Login },
  { path: '/', component: HomePage, meta: { requiresAuth: true } },
  { path: '/classgroup', component: ClassgroupOverview, meta: { requiresAuth: true } },
  { path: '/classgroup/new', component: NewClassgroup, meta: { requiresAuth: true } },
  { path: '/schedule', component: ClassroomScheduler, meta: { requiresAuth: true } },
  {
    path: '/attendance/:sessionId',
    name: 'attendance',
    component: SessionAttendanceTracker,
    props: true,
    meta: { requiresAuth: true }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})


router.beforeEach((to, from, next) => {
  const auth = useAuthStore()
  if (to.meta.requiresAuth && !auth.isAuthenticated()) {
    next({ name: 'Login' })
  } else {
    next()
  }
})

const pinia = createPinia()

createApp(App)
  .use(vue3GoogleLogin, {
    clientId: import.meta.env.VITE_GOOGLE_CLIENT_ID
  })
  .use(pinia)
  .use(router)
  .mount('#app')

