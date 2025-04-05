<template>
    <div>
      <h2>Édition du questionnaire</h2>
      <div v-if="quiz">
        <input v-model="quiz.name" @blur="saveQuiz" />
  
        <ul>
          <li v-for="q in questions" :key="q.id">
            {{ q.ordre }} - {{ q.title }} ({{ q.question_type }})
            <button @click="editQuestion(q)">Modifier</button>
            <button @click="deleteQuestion(q.id)">Supprimer</button>
          </li>
        </ul>
  
        <div>
          <p>Ajouter une question :</p>
          <button @click="questionType = 'open'; selectedQuestion = null">Question ouverte</button>
          <button @click="questionType = 'mcq'; selectedQuestion = null">QCM</button>
        </div>
  
        <OpenQuestionForm
          v-if="questionType === 'open'"
          :question="selectedQuestion"
          @submit="submitQuestion"
        />
  
        <McqQuestionForm
          v-if="questionType === 'mcq'"
          :question="selectedQuestion"
          @submit="submitQuestion"
        />
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted, watch } from 'vue';
  import { useRoute } from 'vue-router';
  import provider from '../services/provider.js';
  import OpenQuestionForm from './OpenQuestionForm.vue';
  import McqQuestionForm from './McqQuestionForm.vue';
  
  const route = useRoute();
  const id = route.params.id;
  
  const quiz = ref(null);
  const questions = ref([]);
  const questionType = ref(null);
  const selectedQuestion = ref(null);
  
  async function loadQuiz() {
    const all = await provider.getQuestionnaires();
    quiz.value = all.find(q => q.id == id);
    questions.value = await provider.getQuestions(id);
  }
  
  async function saveQuiz() {
    await provider.updateQuestionnaire(id, { name: quiz.value.name });
  }
  
  async function submitQuestion(data) {
    if (data.id) {
      await provider.updateQuestion(data.id, data);
    } else {
      await provider.createQuestion(id, data);
    }
    await loadQuiz();
    questionType.value = null;
    selectedQuestion.value = null;
  }
  
  function editQuestion(question) {
    selectedQuestion.value = question;
    questionType.value = question.question_type;
  }
  
  async function deleteQuestion(qid) {
    await provider.deleteQuestion(qid);
    await loadQuiz();
  }
  
  onMounted(loadQuiz);
  watch(() => route.params.id, loadQuiz);
  </script>
  