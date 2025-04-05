<template>
  <div class="editor">
    <h3>Nouvelle question à choix multiples</h3>
    <input v-model="title" placeholder="Intitulé" required />

    <div v-for="(choice, index) in choices" :key="index" class="actions">
      <input v-model="choice.text" placeholder="Option"/>
      <label>
        <input type="checkbox" v-model="choice.is_correct" /> Correcte
      </label>
      <button class="delete no-flex-grow" @click="removeChoice(index)"><span class="material-symbols-rounded ">delete</span></button>
    </div>

    <button @click="addChoice">Ajouter une option</button>
    <button class="edit" @click="save">Enregistrer</button>
  </div>
</template>

<script setup>
import { ref, watchEffect } from 'vue';
import { defineProps, defineEmits } from 'vue';

const props = defineProps({ question: Object });
const emits = defineEmits(['submit']);

const title = ref('');
const choices = ref([
  { text: '', is_correct: false },
  { text: '', is_correct: false }
]);

watchEffect(() => {
  if (props.question) {
    title.value = props.question.title || '';
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
    question_type: 'mcq',
    choices: choices.value
  });
}
</script>

<style>
label {
  display: flex;
  align-items: center;
  justify-content: center;
}
</style>