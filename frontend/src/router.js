import { createRouter, createWebHistory } from 'vue-router'
import HomePage from './pages/HomePage.vue'
import JobsPage from './pages/JobsPage.vue'
import CandidatesPage from './pages/CandidatesPage.vue'

const routes = [
  { path: '/', name: 'home', component: HomePage },
  { path: '/vagas', name: 'jobs', component: JobsPage },
  { path: '/candidatos', name: 'candidates', component: CandidatesPage },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior: () => ({ top: 0 }),
})

export default router
