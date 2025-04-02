<template>
  <div class="quiz-editor container">
    <div v-if="loading" class="loading">Chargement...</div>
    <div v-else>
      <div class="quiz-header">
        <h2>Éditeur : {{ quiz.name }}</h2>
        <div class="quiz-actions">
          <input v-model="quiz.name" @change="updateQuiz">
          <button @click="deleteQuiz" class="delete-btn">Supprimer le questionnaire</button>
        </div>
      </div>
      <QuestionList 
        :questions="questions" 
        @select-question="selectQuestion"
        @delete-question="deleteQuestion"
        @add-question="showQuestionTypeSelector = true"
      />
      <div v-if="showQuestionTypeSelector" class="question-type-selector">
        <h3>Ajouter une question</h3>
        <button @click="addQuestion('open')">Question Ouverte</button>
        <button @click="addQuestion('mcq')">Question à Choix Multiples</button>
        <button @click="cancelAddQuestion">Annuler</button>
      </div>
      <OpenQuestionForm 
        v-if="selectedQuestionType === 'open' && selectedQuestion" 
        :question="selectedQuestion"
        @save="saveQuestion"
        @cancel="deselectQuestion"
      />
      <McqQuestionForm 
        v-if="selectedQuestionType === 'mcq' && selectedQuestion" 
        :question="selectedQuestion"
        @save="saveQuestion"
        @cancel="deselectQuestion"
      />
    </div>
  </div>
</template>

<script>
import provider from '../services/provider'
import QuestionList from './QuestionList.vue'
import OpenQuestionForm from './OpenQuestionForm.vue'
import McqQuestionForm from './McqQuestionForm.vue'

export default {
  name: 'QuizEditor',
  components: { QuestionList, OpenQuestionForm, McqQuestionForm },
  props: {
    id: {
      type: [String, Number],
      required: true
    }
  },
  data() {
    return {
      loading: true,
      quiz: {},
      questions: [],
      showQuestionTypeSelector: false,
      selectedQuestion: null,
      selectedQuestionType: null
    }
  },
  created() {
    this.fetchData()
  },
  methods: {
    fetchData() {
      this.loading = true
      provider.getQuestionnaires()
        .then(data => {
          this.quiz = data.find(q => q.id == this.id) || {}
        })
        .then(() => provider.getQuestions(this.id))
        .then(qs => {
          this.questions = qs
        })
        .finally(() => {
          this.loading = false
        })
    },
    updateQuiz() {
      provider.updateQuestionnaire(this.id, { name: this.quiz.name })
        .catch(err => {
          console.error('Error updating quiz:', err)
          this.fetchData()
        })
    },
    deleteQuiz() {
      if (confirm('Êtes-vous sûr de vouloir supprimer ce questionnaire ?')) {
        provider.deleteQuestionnaire(this.id)
          .then(() => {
            this.$router.push('/')
          })
          .catch(err => console.error('Error deleting quiz:', err))
      }
    },
    addQuestion(type) {
      this.showQuestionTypeSelector = false
      this.selectedQuestionType = type
      if (type === 'open') {
        this.selectedQuestion = {
          title: '',
          ordre: this.questions.length + 1,
          question_type: 'open',
          quiz_id: this.id,
          expected_answer: ''
        }
      } else {
        this.selectedQuestion = {
          title: '',
          ordre: this.questions.length + 1,
          question_type: 'mcq',
          quiz_id: this.id,
          choices: [
            { text: '', is_correct: false },
            { text: '', is_correct: false }
          ]
        }
      }
    },
    cancelAddQuestion() {
      this.showQuestionTypeSelector = false
    },
    selectQuestion(question) {
      this.selectedQuestion = { ...question }
      this.selectedQuestionType = question.question_type
      if (question.question_type === 'mcq' && !question.choices) {
        this.selectedQuestion.choices = []
      }
    },
    deselectQuestion() {
      this.selectedQuestion = null
      this.selectedQuestionType = null
    },
    saveQuestion(questionData) {
      const isNew = !questionData.id
      const savePromise = isNew
        ? provider.createQuestion(this.id, questionData)
        : provider.updateQuestion(questionData.id, questionData)
      savePromise
        .then(() => {
          this.fetchData()
          this.deselectQuestion()
        })
        .catch(err => {
          console.error('Error saving question:', err)
        })
    },
    deleteQuestion(id) {
      if (confirm('Êtes-vous sûr de vouloir supprimer cette question ?')) {
        provider.deleteQuestion(id)
          .then(() => {
            this.fetchData()
            this.deselectQuestion()
          })
          .catch(err => console.error('Error deleting question:', err))
      }
    }
  },
  watch: {
    id() {
      this.fetchData()
    }
  }
}
</script>

<style scoped>
.quiz-editor {
  margin-top: 20px;
}
.quiz-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.quiz-actions input {
  padding: 5px;
  border: 1px solid var(--primary);
  border-radius: 4px;
}
.question-type-selector {
  margin: 20px 0;
  padding: 15px;
  border: 1px solid #ccc;
  border-radius: 5px;
}
.delete-btn {
  background-color: #e76f51;
}
</style>
