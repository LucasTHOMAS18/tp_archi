<template>
  <div>
    <router-link class="button" :to="`/`">
      <span class="material-symbols-rounded ">arrow_back</span>Retour
    </router-link>

    <h2>Édition du questionnaire</h2>
    <div v-if="quiz">
      <div class="actions">
        <p>Nom :</p>
        <input v-model="quiz.name" @blur="saveQuiz" />
      </div>

      <h2>Questions</h2>
      <ul>
        <li style="margin-bottom: 10px;" class="question" v-for="q in questions" :key="q.id">
          {{ q.order }} - {{ q.title }} ({{ q.question_type }})

          <div class="actions">
            <button class="edit" @click="editQuestion(q)"><span class="material-symbols-rounded ">edit</span>Modifier</button>
            <button class="delete" @click="deleteQuestion(q.id)"><span class="material-symbols-rounded ">delete</span>Supprimer</button>
          </div>
        </li>
      </ul>

      <div>
        <h2>Ajouter une question :</h2>
        <div class="question-type-list">
          <div class="question-type-container" @click="questionType = 'open', selectedQuestion = null">
            <div class="question-type open">
              <span class="material-symbols-rounded ">question_mark</span>
            </div>

            <p>Question ouverte</p>
          </div>

          <div class="question-type-container" @click="questionType = 'mcq', selectedQuestion = null">
            <div class="question-type mcq">
              <span class="material-symbols-rounded ">select_check_box</span>
            </div>

            <p>QCM</p>
          </div>
        </div>
      </div>

      <OpenQuestionForm v-if="questionType === 'open'" :question="selectedQuestion" @submit="submitQuestion" @cancel="questionType=null"/>

      <McqQuestionForm v-if="questionType === 'mcq'" :question="selectedQuestion" @submit="submitQuestion" @cancel="questionType=null"/>
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

<style>
.question {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.selected {
  border: rgb(56, 182, 255) solid 2px;
}

.question-type-container {
  display: flex;
  align-items: center;
  justify-content: center;
  flex-direction: column;
  cursor: pointer;
}

.question-type {
  flex-grow: 0;
  width: 75px;
  aspect-ratio: 1/1;
  border-radius: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  margin-bottom: -10px;
}

.question-type span {
  font-size: 40px;
}

.open {
  background-color: #ff6105;  
  color: white;
}

.mcq {
  background-color: #0ba84a;
  color: white;
}

.question-type-list {
  display: flex;
  gap: 50px;
}
</style>