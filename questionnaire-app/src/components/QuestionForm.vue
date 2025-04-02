<!-- FILE: questionnaire-app/src/components/QuestionForm.vue -->
<template>
  <div>
    <h4>Ajouter une Question Ouverte</h4>
    <input type="text" v-model="title" placeholder="Titre de la question" />
    <input type="number" v-model.number="ordre" placeholder="Ordre" min="1" />
    <textarea
      v-model="expected_answer"
      placeholder="Réponse attendue (optionnelle)"
    ></textarea>
    <button @click="submitQuestion">Ajouter Question</button>
  </div>
</template>

<script>
export default {
  name: 'QuestionForm',
  props: {
    questionnaire: {
      type: Object,
      required: true
    }
  },
  data() {
    return {
      title: '',
      ordre: 1,
      expected_answer: ''
    }
  },
  methods: {
    submitQuestion() {
      if (this.title.trim() === '') return;
      const question = {
        title: this.title,
        ordre: this.ordre,
        question_type: 'open',
        expected_answer: this.expected_answer
      };
      fetch(`/api/questionnaires/${this.questionnaire.id}/questions`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(question)
      })
        .then(() => {
          this.$emit('refresh');
          this.title = '';
          this.ordre = 1;
          this.expected_answer = '';
        })
        .catch(err => console.error(err));
    }
  }
}
</script>
