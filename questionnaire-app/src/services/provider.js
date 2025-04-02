// FILE: questionnaire-app/src/services/provider.js
const API_URL = '/api'

export default {
  getQuestionnaires() {
    return fetch(`${API_URL}/questionnaires`).then(res => res.json())
  },
  createQuestionnaire(data) {
    return fetch(`${API_URL}/questionnaires`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    }).then(res => res.json())
  },
  updateQuestionnaire(id, data) {
    return fetch(`${API_URL}/questionnaires/${id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    }).then(res => res.json())
  },
  deleteQuestionnaire(id) {
    return fetch(`${API_URL}/questionnaires/${id}`, {
      method: 'DELETE'
    })
  },
  getQuestions(quizId) {
    return fetch(`${API_URL}/questionnaires/${quizId}/questions`).then(res => res.json())
  },
  createQuestion(quizId, data) {
    return fetch(`${API_URL}/questionnaires/${quizId}/questions`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    }).then(res => res.json())
  },
  updateQuestion(id, data) {
    return fetch(`${API_URL}/questions/${id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    }).then(res => res.json())
  },
  deleteQuestion(id) {
    return fetch(`${API_URL}/questions/${id}`, {
      method: 'DELETE'
    })
  }
}
