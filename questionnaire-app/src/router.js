import { createRouter, createWebHistory } from 'vue-router'
import QuizList from './components/QuizList.vue'
import QuizEditor from './components/QuizEditor.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: QuizList
  },
  {
    path: '/quiz/:id',
    name: 'QuizEditor',
    component: QuizEditor,
    props: true
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
