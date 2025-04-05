<template>
    <div>
      <h3>Liste des questions</h3>
      <ul>
        <li v-for="q in questions" :key="q.id">
          {{ q.order }} - {{ q.title }} ({{ q.question_type }})
        </li>
      </ul>
    </div>
  </template>
  
  <script setup>
  import { defineProps } from 'vue';
  
  const props = defineProps({
    questions: {
      type: Array,
      required: true
    }
  });
  </script>