export interface User {
  user_id: string;
  email: string;
  role: 'student' | 'teacher' | 'admin';
}

export interface AuthState {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  isLoading: boolean;
}

export interface Lesson {
  id: string;
  title: string;
  subject: string;
  grade_level: string;
  language: string;
  description: string;
  is_active: boolean;
  created_at: string;
}

export interface Concept {
  id: string;
  lesson_id: string;
  name: string;
  description: string;
  difficulty_level: number;
}

export interface Question {
  id: string;
  type: 'cloze' | 'mcq' | 'open_text' | 'vqa' | 'table_qa' | 'oral';
  lesson_id: string;
  concept_id: string;
  skill_id: string;
  stem: string;
  options: { id: number; text: string }[];
  difficulty: number;
}

export interface SourceLocator {
  source_id: string;
  source_name: string;
  source_type: string;
  start_offset?: number;
  end_offset?: number;
}

export interface RAGAnswer {
  answer: string;
  sources: SourceLocator[];
}

export interface MasteryEntry {
  skill_id: string;
  skill_name: string;
  concept_name: string;
  p_mastery: number;
  num_attempts: number;
}

export interface StudentProfile {
  student_id: string;
  mastery: MasteryEntry[];
}

export interface TutorStepResponse {
  action: 'EXPLAIN' | 'QUESTION' | 'FINISHED';
  skill_id?: string;
  explanation?: string;
  sources?: SourceLocator[];
  question?: Question;
}

export interface Misconception {
  misconception_id: string;
  description: string;
  num_occurrences: number;
  first_seen: string;
  last_seen: string;
}

export interface LessonOverview {
  lesson_id: string;
  title: string;
  subject: string;
  grade_level: string;
  concept_count: number;
  chunk_count: number;
  question_count: number;
  student_count: number;
  avg_mastery_pct: number;
}

export interface SkillStats {
  skill_id: string;
  skill_name: string;
  avg_mastery_pct: number;
  student_count: number;
  total_attempts: number;
  accuracy_pct: number;
}

export interface ConceptStats {
  concept_id: string;
  concept_name: string;
  difficulty_level: number;
  skills: SkillStats[];
}

export interface LessonAnalytics {
  lesson_id: string;
  title: string;
  concepts: ConceptStats[];
  top_misconceptions: Misconception[];
}

export interface StudentGap {
  misconception_id: string;
  description: string;
  num_occurrences: number;
  first_seen: string;
  last_seen: string;
}
