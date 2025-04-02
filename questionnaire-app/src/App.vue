<template>
  <div class="container">
    <h1>Gestionnaire de Questionnaires</h1>
    <!-- Formulaire pour ajouter ou modifier un questionnaire -->
    <QuestionnaireForm
      @refresh="fetchQuestionnaires"
      :selected="selectedQuestionnaire"
      @cancelEdit="handleCancelEdit"
    />
    <!-- Liste des questionnaires -->
    <QuestionnaireList
      :questionnaires="questionnaires"
      @select="handleSelectQuestionnaire"
      @refresh="fetchQuestionnaires"
    />
    <!-- Si un questionnaire est sélectionné, afficher ses questions -->
    <div v-if="selectedQuestionnaire">
      <h2>Questions du Questionnaire : {{ selectedQuestionnaire.name }}</h2>
      <QuestionList
        :questionnaire="selectedQuestionnaire"
        @refresh="fetchQuestions"
      />
    </div>
  </div>
</template>

<script>
import QuestionnaireList from './components/QuestionnaireList.vue'
import QuestionnaireForm from './components/QuestionnaireForm.vue'
import QuestionList from './components/QuestionList.vue'

export default {
  name: 'App',
  components: {
    QuestionnaireList,
    QuestionnaireForm,
    QuestionList
  },
  data() {
    return {
      questionnaires: [],
      selectedQuestionnaire: null
    }
  },
  mounted() {
    this.fetchQuestionnaires();
  },
  methods: {
    fetchQuestionnaires() {
      fetch('http://127.0.0.1:5000/questionnaires')
        .then(res => res.json())
        .then(data => {
          this.questionnaires = data;
        })
        .catch(err => console.error(err));
    },
    handleSelectQuestionnaire(q) {
      this.selectedQuestionnaire = q;
      this.fetchQuestions();
    },
    fetchQuestions() {
      // La récupération des questions s’effectuera dans le composant QuestionList,
      // mais vous pouvez ajouter ici un traitement si besoin.
    },
    handleCancelEdit() {
      this.selectedQuestionnaire = null;
    }
  }
}
</script>

<style>
.container {
  padding: 20px;
}
</style>
