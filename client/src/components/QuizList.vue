<template>
  <div>
    <h2>Ajouter un questionnaire</h2>
    <div>
      <div class="actions">
        <input v-model="newName" placeholder="Nom du questionnaire" />
        <button class="add no-flex-grow" @click="addQuiz"><span class="material-symbols-rounded ">add</span> Ajouter</button>
      </div>
    </div>
    <h2>Liste des questionnaires</h2>
    <ul id="quizzes">
      <li v-for="quiz in quizzes" :key="quiz.id">
        <h3>{{ quiz.name }}</h3>

        <div class="actions">
          <router-link class="button edit" :to="`/quiz/${quiz.id}`"><span class="material-symbols-rounded ">edit</span>Modifier</router-link>
          <button class="delete" @click="removeQuiz(quiz.id)"><span class="material-symbols-rounded ">delete</span>Supprimer</button>
        </div>
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

<style>
#quizzes {
  width: 100%;
  padding: 0px;
}

#quizzes li {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>