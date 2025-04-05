import { createRouter, createWebHistory } from 'vue-router';
import QuizEditor from './components/QuizEditor.vue';
import QuizList from './components/QuizList.vue';

const routes = [
  { path: '/', name: 'home', component: QuizList },
  { path: '/quiz/:id', name: 'quiz-editor', component: QuizEditor, props: true },
];

export default createRouter({
  history: createWebHistory(),
  routes
});