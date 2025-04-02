<!-- FILE: questionnaire-app/src/components/QuestionnaireForm.vue -->
<template>
  <div>
    <h3>{{ selected ? 'Modifier' : 'Ajouter' }} un Questionnaire</h3>
    <input type="text" v-model="name" placeholder="Nom du questionnaire" />
    <button @click="submitForm">{{ selected ? 'Modifier' : 'Ajouter' }}</button>
    <button v-if="selected" @click="cancelEdit">Annuler</button>
  </div>
</template>

<script>
export default {
  name: 'QuestionnaireForm',
  props: {
    selected: {
      type: Object,
      default: null
    }
  },
  data() {
    return {
      name: this.selected ? this.selected.name : ''
    }
  },
  watch: {
    selected(newVal) {
      this.name = newVal ? newVal.name : '';
    }
  },
  methods: {
    submitForm() {
      if (this.name.trim() === '') return;
      if (this.selected) {
        // Modification d'un questionnaire existant
        fetch(`/api/questionnaires/${this.selected.id}`, {
          method: 'PUT',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ name: this.name })
        })
          .then(() => {
            this.$emit('refresh');
            this.cancelEdit();
          })
          .catch(err => console.error(err));
      } else {
        // Création d'un nouveau questionnaire
        fetch('/api/questionnaires', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ name: this.name })
        })
          .then(() => {
            this.$emit('refresh');
            this.name = '';
          })
          .catch(err => console.error(err));
      }
    },
    cancelEdit() {
      this.$emit('cancelEdit');
      this.name = '';
    }
  }
}
</script>
