import axios from 'axios';

const API_BASE = '/api/v1';

const api = axios.create({
  baseURL: API_BASE,
  headers: { 'Content-Type': 'application/json' },
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export const authAPI = {
  login: (email: string, password: string) =>
    api.post('/auth/login', { email, password }),
  register: (name: string, email: string, password: string, role: string = 'student') =>
    api.post('/auth/register', { name, email, password, role }),
  me: () => api.get('/auth/me'),
};

export const lessonsAPI = {
  list: () => api.get('/content/lessons'),
  get: (id: string) => api.get(`/content/lessons/${id}`),
  create: (data: any) => api.post('/content/lessons', data),
  concepts: (lessonId: string) => api.get(`/content/lessons/${lessonId}/concepts`),
};

export const questionsAPI = {
  generateBatch: (lessonId: string, conceptIds: string[], numPerConcept: number = 5) =>
    api.post('/questions/generate-batch', {
      lesson_id: lessonId,
      concept_ids: conceptIds,
      num_questions_per_concept: numPerConcept,
    }),
  get: (id: string) => api.get(`/questions/${id}`),
};

export const tutorAPI = {
  ask: (lessonId: string, query: string) =>
    api.post(`/tutor/ask?lesson_id=${lessonId}&query=${encodeURIComponent(query)}`),
  sessionStep: (studentId: string, lessonId: string, lastQuestionId?: string, lastResponse?: string) =>
    api.post('/tutor/session/step', {
      student_id: studentId,
      lesson_id: lessonId,
      last_question_id: lastQuestionId,
      last_response: lastResponse,
    }),
};

export const studentsAPI = {
  profile: (id: string) => api.get(`/students/${id}/profile`),
  summary: (id: string) => api.get(`/students/${id}/summary`),
};

export const contentAPI = {
  uploadSource: (file: File, language: string = 'en') => {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('language', language);
    return api.post('/content/sources/upload', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
  },
  index: (sourceId: string, lessonId?: string) =>
    api.post('/content/chunks/index', { source_id: sourceId, lesson_id: lessonId }),
};

export default api;
