<template>
  <div class="question-form container">
    <h3>{{ question.id ? 'Modifier' : 'Nouvelle' }} Question à Choix Multiples</h3>
    <form @submit.prevent="save">
      <div class="form-group">
        <label>Titre :</label>
        <input v-model="formData.title" required>
      </div>
      <div class="form-group">
        <label>Ordre :</label>
        <input v-model.number="formData.ordre" type="number" min="1" required>
      </div>
      <div class="choices-section">
        <h4>Options :</h4>
        <div v-for="(choice, index) in formData.choices" :key="index" class="choice-item">
          <input v-model="choice.text" placeholder="Texte de l'option" required>
          <label>
            <input type="checkbox" v-model="choice.is_correct">
            Correcte
          </label>
          <button type="button" @click="removeChoice(index)" class="remove-choice">×</button>
        </div>
        <button type="button" @click="addChoice" class="add-choice">Ajouter une option</button>
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
  name: 'McqQuestionForm',
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
        question_type: 'mcq',
        questionnaire_id: this.question.quiz_id || this.question.questionnaire_id,
        choices: this.question.choices ? [...this.question.choices] : [
          { text: '', is_correct: false },
          { text: '', is_correct: false }
        ]
      }
    }
  },
  methods: {
    addChoice() {
      this.formData.choices.push({ text: '', is_correct: false })
    },
    removeChoice(index) {
      if (this.formData.choices.length > 1) {
        this.formData.choices.splice(index, 1)
      } else {
        alert('Une question doit avoir au moins une option.')
      }
    },
    save() {
      const hasCorrect = this.formData.choices.some(choice => choice.is_correct)
      if (!hasCorrect) {
        alert('Veuillez sélectionner au moins une option correcte.')
        return
      }
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
.choices-section {
  margin-top: 20px;
}
.choice-item {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 10px;
}
.remove-choice {
  background-color: #e76f51;
  color: white;
  border: none;
  width: 25px;
  height: 25px;
  border-radius: 50%;
  cursor: pointer;
  font-size: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
}
.add-choice {
  background-color: var(--secondary);
  color: white;
  border: none;
  padding: 8px 12px;
  border-radius: 4px;
  cursor: pointer;
}
.form-actions {
  display: flex;
  gap: 10px;
  margin-top: 20px;
}
</style>
