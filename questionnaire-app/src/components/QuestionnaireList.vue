<template>
  <div>
    <h3>Liste des Questionnaires</h3>
    <ul>
      <li v-for="q in questionnaires" :key="q.id">
        <!-- En cliquant sur le nom, on sélectionne le questionnaire -->
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
        fetch(`http://127.0.0.1:5000/questionnaires/${id}`, {
          method: 'DELETE'
        })
          .then(() => {
            // Informer le parent de rafraîchir la liste
            this.$emit('refresh');
          })
          .catch(err => console.error(err));
      }
    }
  }
}
</script>
