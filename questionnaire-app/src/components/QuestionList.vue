<template>
  <div>
    <h4>Liste des Questions</h4>
    <ul>
      <li v-for="question in questions" :key="question.id">
        {{ question.ordre }}. {{ question.title }} ({{ question.question_type }})
        <button @click="deleteQuestion(question.id)">Supprimer</button>
      </li>
    </ul>
    <!-- Formulaire pour ajouter une nouvelle question -->
    <QuestionForm :questionnaire="questionnaire" @refresh="fetchQuestions" />
  </div>
</template>

<script>
import QuestionForm from './QuestionForm.vue'

export default {
  name: 'QuestionList',
  components: { QuestionForm },
  props: {
    questionnaire: {
      type: Object,
      required: true
    }
  },
  data() {
    return {
      questions: []
    }
  },
  mounted() {
    this.fetchQuestions();
  },
  methods: {
    fetchQuestions() {
      fetch(`http://127.0.0.1:5000/questionnaires/${this.questionnaire.id}/questions`)
        .then(res => res.json())
        .then(data => {
          this.questions = data;
        })
        .catch(err => console.error(err));
    },
    deleteQuestion(id) {
      if (confirm('Supprimer cette question ?')) {
        fetch(`http://127.0.0.1:5000/questions/${id}`, {
          method: 'DELETE'
        })
          .then(() => this.fetchQuestions())
          .catch(err => console.error(err));
      }
    }
  }
}
</script>
