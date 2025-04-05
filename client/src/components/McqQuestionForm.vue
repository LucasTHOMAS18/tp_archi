<template>
  <div>
    <h3>Nouvelle question à choix multiples</h3>
    <input v-model="title" placeholder="Intitulé" required />
    <input v-model="ordre" type="number" min="1" placeholder="Ordre" required />

    <div v-for="(choice, index) in choices" :key="index">
      <input v-model="choice.text" placeholder="Option" />
      <label>
        <input type="checkbox" v-model="choice.is_correct" /> Correcte
      </label>
      <button @click="removeChoice(index)">×</button>
    </div>

    <button @click="addChoice">Ajouter une option</button>
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
const choices = ref([
  { text: '', is_correct: false },
  { text: '', is_correct: false }
]);

watchEffect(() => {
  if (props.question) {
    title.value = props.question.title || '';
    ordre.value = props.question.ordre || 1;
    choices.value = props.question.choices?.map(c => ({ ...c })) || [
      { text: '', is_correct: false },
      { text: '', is_correct: false }
    ];
  }
});

function addChoice() {
  choices.value.push({ text: '', is_correct: false });
}

function removeChoice(index) {
  if (choices.value.length > 1) choices.value.splice(index, 1);
}

function save() {
  if (!title.value.trim()) {
    alert('Le titre est obligatoire.');
    return;
  }

  const hasCorrect = choices.value.some(c => c.is_correct);
  if (!hasCorrect) {
    alert('Au moins une option correcte est requise.');
    return;
  }

  emits('submit', {
    id: props.question?.id,
    title: title.value,
    ordre: ordre.value,
    question_type: 'mcq',
    choices: choices.value
  });
}
</script>