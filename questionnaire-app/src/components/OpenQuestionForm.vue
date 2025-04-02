<template>
  <div class="question-form container">
    <h3>{{ question.id ? 'Modifier' : 'Nouvelle' }} Question Ouverte</h3>
    <form @submit.prevent="save">
      <div class="form-group">
        <label>Titre :</label>
        <input v-model="formData.title" required>
      </div>
      <div class="form-group">
        <label>Ordre :</label>
        <input v-model.number="formData.ordre" type="number" min="1" required>
      </div>
      <div class="form-group">
        <label>Réponse attendue (optionnelle) :</label>
        <textarea v-model="formData.expected_answer"></textarea>
      </div>
      <div class="form-actions">
        <button type="submit">Enregistrer</button>
        <button type="button" @click="cancel">Annuler</button>
      </div>
    </form>
  </div>
</template>

<script>
export default {
  name: 'OpenQuestionForm',
  props: {
    question: {
      type: Object,
      required: true
    }
  },
  data() {
    return {
      formData: {
        title: this.question.title,
        ordre: this.question.ordre,
        question_type: 'open',
        expected_answer: this.question.expected_answer,
        questionnaire_id: this.question.quiz_id || this.question.questionnaire_id
      }
    }
  },
  methods: {
    save() {
      this.$emit('save', { ...this.formData, id: this.question.id })
    },
    cancel() {
      this.$emit('cancel')
    }
  }
}
</script>

<style scoped>
.question-form {
  margin-top: 20px;
}
.form-group {
  margin-bottom: 15px;
}
.form-group label {
  font-weight: bold;
  display: block;
  margin-bottom: 5px;
}
.form-actions {
  display: flex;
  gap: 10px;
}
</style>
