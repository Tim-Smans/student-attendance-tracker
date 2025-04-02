import './assets/main.css'

import { createApp } from 'vue'
import App from './App.vue'
import type { Student } from './models/student'
import { createStudent, createStudentsFromList } from './helpers/studentHelpers'

createApp(App).mount('#app')



