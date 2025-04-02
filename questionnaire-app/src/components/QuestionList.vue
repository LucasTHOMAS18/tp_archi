<template>
  <div class="question-list">
    <h3>Liste des Questions</h3>
    <div v-if="questions.length === 0" class="no-questions">
      Aucune question dans ce questionnaire.
    </div>
    <ul v-else class="questions">
      <li v-for="question in sortedQuestions" :key="question.id" class="question-item">
        <div class="question-content" @click="$emit('select-question', question)">
          <span class="order">{{ question.ordre }}.</span>
          <span class="title">{{ question.title }}</span>
          <span class="type">
            {{ question.question_type === 'open' ? '(Question Ouverte)' : '(QCM)' }}
          </span>
        </div>
        <button @click.stop="$emit('delete-question', question.id)" class="delete-btn">
          Supprimer
        </button>
      </li>
    </ul>
    <button @click="$emit('add-question')" class="add-btn">
      Ajouter une question
    </button>
  </div>
</template>

<script>
export default {
  name: 'QuestionList',
  props: {
    questions: {
      type: Array,
      required: true
    }
  },
  computed: {
    sortedQuestions() {
      return [...this.questions].sort((a, b) => a.ordre - b.ordre)
    }
  }
}
</script>

<style scoped>
.question-list {
  margin: 20px 0;
}
.no-questions {
  color: #777;
  font-style: italic;
  margin: 10px 0;
}
.questions {
  list-style: none;
  padding: 0;
}
.question-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px;
  border-bottom: 1px solid #ddd;
}
.question-item:hover {
  background-color: #f7f7f7;
}
.delete-btn {
  background-color: #e76f51;
}
.add-btn {
  background-color: var(--secondary);
  margin-top: 10px;
}
</style>
