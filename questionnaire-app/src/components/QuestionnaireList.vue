<!-- FILE: questionnaire-app/src/components/QuestionnaireList.vue -->
<template>
  <div>
    <h3>Liste des Questionnaires</h3>
    <ul>
      <li v-for="q in questionnaires" :key="q.id">
        <span @click="$emit('select', q)" style="cursor:pointer">
          {{ q.name }}
        </span>
        <button @click="deleteQuestionnaire(q.id)">Supprimer</button>
      </li>
    </ul>
  </div>
</template>

<script>
export default {
  name: 'QuestionnaireList',
  props: {
    questionnaires: {
      type: Array,
      default: () => []
    }
  },
  methods: {
    deleteQuestionnaire(id) {
      if (confirm('Supprimer ce questionnaire ?')) {
        fetch(`/api/questionnaires/${id}`, {
          method: 'DELETE'
        })
          .then(() => {
            this.$emit('refresh');
          })
          .catch(err => console.error(err));
      }
    }
  }
}
</script>
