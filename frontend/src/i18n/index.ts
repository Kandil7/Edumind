import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';

const resources = {
  en: {
    translation: {
      // App
      app_name: 'EduMind',
      welcome: 'Welcome to EduMind',
      loading: 'Loading',

      // Auth
      login: 'Login',
      register: 'Register',
      email: 'Email',
      password: 'Password',
      name: 'Name',
      role: 'Role',
      student: 'Student',
      teacher: 'Teacher',
      logout: 'Logout',
      already_have_account: 'Already have an account?',
      no_account: "Don't have an account?",

      // Navigation
      lessons: 'Lessons',
      start_learning: 'Start Learning',
      dashboard: 'Dashboard',
      teacher_dashboard: 'Teacher Dashboard',
      back: 'Back',

      // Student
      mastery: 'Mastery',
      gaps: 'Knowledge Gaps',
      explanations: 'Explanation',
      questions: 'Questions',
      submit: 'Submit Answer',
      next: 'Continue',
      previous: 'Previous',
      correct: 'Correct!',
      incorrect: 'Incorrect — try again',
      session_finished: 'Session Complete!',
      session_finished_desc: 'You did great! Check your dashboard for progress.',
      view_sources: 'Sources',
      type_answer: 'Type your answer here...',
      session_progress: 'Session Progress',

      // Stats
      total_attempts: 'Total Attempts',
      correct_answers: 'Correct',
      accuracy: 'Accuracy',
      mastered_skills: 'Mastered',
      needs_practice: 'Needs Practice',

      // Teacher
      upload_content: 'Upload Content',
      create_lesson: 'Create Lesson',
      existing_lessons: 'Existing Lessons',
      lesson_title: 'Lesson title',
      subject: 'Subject',
      grade_level: 'Grade level',
      description: 'Description',
      upload: 'Upload',
      uploading: 'Uploading...',
      refresh: 'Refresh',
      create: 'Create',
      overview: 'Overview',
      content: 'Content',
      students: 'Students',
      questions_count: 'Questions',
      avg_mastery: 'Avg Mastery',

      // Language
      language: 'Language',
      arabic: 'العربية',
      english: 'English',
    },
  },
  ar: {
    translation: {
      // App
      app_name: 'إدومايند',
      welcome: 'مرحباً بك في إدومايند',
      loading: 'جاري التحميل',

      // Auth
      login: 'تسجيل الدخول',
      register: 'إنشاء حساب',
      email: 'البريد الإلكتروني',
      password: 'كلمة المرور',
      name: 'الاسم',
      role: 'الدور',
      student: 'طالب',
      teacher: 'معلم',
      logout: 'تسجيل الخروج',
      already_have_account: 'لديك حساب بالفعل؟',
      no_account: 'ليس لديك حساب؟',

      // Navigation
      lessons: 'الدروس',
      start_learning: 'ابدأ التعلم',
      dashboard: 'لوحة التحكم',
      teacher_dashboard: 'لوحة تحكم المعلم',
      back: 'رجوع',

      // Student
      mastery: 'الإتقان',
      gaps: 'فجوات المعرفة',
      explanations: 'شرح',
      questions: 'الأسئلة',
      submit: 'إرسال الإجابة',
      next: 'متابعة',
      previous: 'السابق',
      correct: 'صحيح!',
      incorrect: 'خطأ — حاول مرة أخرى',
      session_finished: 'اكتملت الجلسة!',
      session_finished_desc: 'أحسنت! راجع لوحة التحكم لمتابعة تقدمك.',
      view_sources: 'المصادر',
      type_answer: 'اكتب إجابتك هنا...',
      session_progress: 'تقدم الجلسة',

      // Stats
      total_attempts: 'إجمالي المحاولات',
      correct_answers: 'صحيحة',
      accuracy: 'الدقة',
      mastered_skills: 'مُتقَنة',
      needs_practice: 'تحتاج تدريب',

      // Teacher
      upload_content: 'رفع المحتوى',
      create_lesson: 'إنشاء درس',
      existing_lessons: 'الدروس الحالية',
      lesson_title: 'عنوان الدرس',
      subject: 'المادة',
      grade_level: 'المستوى',
      description: 'الوصف',
      upload: 'رفع',
      uploading: 'جاري الرفع...',
      refresh: 'تحديث',
      create: 'إنشاء',
      overview: 'نظرة عامة',
      content: 'المحتوى',
      students: 'الطلاب',
      questions_count: 'الأسئلة',
      avg_mastery: 'متوسط الإتقان',

      // Language
      language: 'اللغة',
      arabic: 'العربية',
      english: 'English',
    },
  },
};

i18n.use(initReactI18next).init({
  resources,
  lng: 'ar',
  fallbackLng: 'en',
  interpolation: {
    escapeValue: false,
  },
});

export default i18n;
