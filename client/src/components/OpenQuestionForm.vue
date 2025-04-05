<template>
  <div class="editor">
    <h3>Nouvelle question ouverte</h3>
    <input v-model="title" placeholder="Intitulé" required />
    <textarea v-model="expectedAnswer" placeholder="Réponse attendue"></textarea>
    <button class="edit" @click="save">Enregistrer</button>
  </div>
</template>

<script setup>
import { ref, watchEffect } from 'vue';
import { defineProps, defineEmits } from 'vue';

const props = defineProps({ question: Object });
const emits = defineEmits(['submit']);

const title = ref('');
const expectedAnswer = ref('');

watchEffect(() => {
  if (props.question) {
    title.value = props.question.title || '';
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
    expected_answer: expectedAnswer.value,
    question_type: 'open'
  });
}
</script>

<style>

</style>