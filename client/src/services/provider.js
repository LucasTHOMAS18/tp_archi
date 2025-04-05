const API_URL = 'http://localhost:5000/api/v1';

async function request(path, options = {}) {
  const URL = `${API_URL}${path}`;
  console.log(URL)
  const res = await fetch(`${API_URL}${path}`, options);
  if (!res.ok) throw new Error(`Erreur ${res.status}`);
  return res.status === 204 ? null : res.json();
}

export default {
  getQuestionnaires: () => request('/questionnaires'),
  createQuestionnaire: (data) => request('/questionnaires', {
    method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(data)
  }),
  updateQuestionnaire: (id, data) => request(`/questionnaires/${id}`, {
    method: 'PUT', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(data)
  }),
  deleteQuestionnaire: (id) => request(`/questionnaires/${id}`, { method: 'DELETE' }),

  getQuestions: (quizId) => request(`/questionnaires/${quizId}/questions`),
  createQuestion: (quizId, data) => request(`/questionnaires/${quizId}/questions`, {
    method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(data)
  }),
  updateQuestion: (id, data) => request(`/questions/${id}`, {
    method: 'PUT', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(data)
  }),
  deleteQuestion: (id) => request(`/questions/${id}`, { method: 'DELETE' })
};
