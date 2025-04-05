<template>
  <div>
    <h2>Questionnaires</h2>
    <div>
      <input v-model="newName" placeholder="Nom du questionnaire" />
      <button @click="addQuiz">Ajouter</button>
    </div>
    <ul>
      <li v-for="quiz in quizzes" :key="quiz.id">
        <router-link :to="`/quiz/${quiz.id}`">{{ quiz.name }}</router-link>
        <button @click="removeQuiz(quiz.id)">Supprimer</button>
      </li>
    </ul>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import provider from '../services/provider.js';

const quizzes = ref([]);
const newName = ref('');

async function fetchData() {
  quizzes.value = await provider.getQuestionnaires();
}

async function addQuiz() {
  if (!newName.value.trim()) return;
  const created = await provider.createQuestionnaire({ name: newName.value });
  quizzes.value.push(created);
  newName.value = '';
}

async function removeQuiz(id) {
  await provider.deleteQuestionnaire(id);
  quizzes.value = quizzes.value.filter(q => q.id !== id);
}

onMounted(fetchData);
</script>