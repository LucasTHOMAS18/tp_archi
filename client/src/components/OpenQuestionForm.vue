<template>
  <div>
    <h3>Nouvelle question ouverte</h3>
    <input v-model="title" placeholder="Intitulé" required />
    <input v-model="ordre" type="number" min="1" placeholder="Ordre" required />
    <textarea v-model="expectedAnswer" placeholder="Réponse attendue"></textarea>
    <button @click="save">Enregistrer</button>
  </div>
</template>

<script setup>
import { ref, watchEffect } from 'vue';
import { defineProps, defineEmits } from 'vue';

const props = defineProps({ question: Object });
const emits = defineEmits(['submit']);

const title = ref('');
const ordre = ref(1);
const expectedAnswer = ref('');

watchEffect(() => {
  if (props.question) {
    title.value = props.question.title || '';
    ordre.value = props.question.ordre || 1;
    expectedAnswer.value = props.question.expected_answer || '';
  }
});

function save() {
  if (!title.value.trim()) {
    alert('Le titre est obligatoire.');
    return;
  }

  emits('submit', {
    id: props.question?.id,
    title: title.value,
    ordre: ordre.value,
    expected_answer: expectedAnswer.value,
    question_type: 'open'
  });
}
</script>