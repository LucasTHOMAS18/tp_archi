const API_URL = 'http://localhost:5000/api/v1';

async function request(path, options = {}) {
  const URL = `${API_URL}${path}`;
  console.log(URL)
  const res = await fetch(`${API_URL}${path}`, options);
  if (!res.ok) throw new Error(`Erreur ${res.status}`);
  return res.status === 204 ? null : res.json();
}

export default {
  getQuestionnaires: () => request('/quizzes'),
  createQuestionnaire: (data) => request('/quizzes', {
    method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(data)
  }),
  updateQuestionnaire: (id, data) => request(`/quizzes/${id}`, {
    method: 'PUT', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(data)
  }),
  deleteQuestionnaire: (id) => request(`/quizzes/${id}`, { method: 'DELETE' }),

  getQuestions: (quizId) => request(`/quizzes/${quizId}/questions`),
  createQuestion: (quizId, data) => request(`/quizzes/${quizId}/questions`, {
    method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(data)
  }),
  updateQuestion: (id, data) => request(`/questions/${id}`, {
    method: 'PUT', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(data)
  }),
  deleteQuestion: (id) => request(`/questions/${id}`, { method: 'DELETE' })
};
