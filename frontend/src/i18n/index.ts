import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';

const resources = {
  en: {
    translation: {
      app_name: 'EduMind',
      welcome: 'Welcome to EduMind',
      login: 'Login',
      register: 'Register',
      email: 'Email',
      password: 'Password',
      name: 'Name',
      lessons: 'Lessons',
      start_learning: 'Start Learning',
      dashboard: 'Dashboard',
      mastery: 'Mastery',
      gaps: 'Knowledge Gaps',
      explanations: 'Explanations',
      questions: 'Questions',
      submit: 'Submit',
      next: 'Next',
      previous: 'Previous',
      correct: 'Correct!',
      incorrect: 'Incorrect',
      session_finished: 'Session Complete',
      view_sources: 'View Sources',
      teacher_dashboard: 'Teacher Dashboard',
      upload_content: 'Upload Content',
      analytics: 'Analytics',
      language: 'Language',
    },
  },
  ar: {
    translation: {
      app_name: 'إدومايند',
      welcome: 'مرحباً بك في إدومايند',
      login: 'تسجيل الدخول',
      register: 'إنشاء حساب',
      email: 'البريد الإلكتروني',
      password: 'كلمة المرور',
      name: 'الاسم',
      lessons: 'الدروس',
      start_learning: 'ابدأ التعلم',
      dashboard: 'لوحة التحكم',
      mastery: 'الإتقان',
      gaps: 'فجوات المعرفة',
      explanations: 'الشروحات',
      questions: 'الأسئلة',
      submit: 'إرسال',
      next: 'التالي',
      previous: 'السابق',
      correct: 'صحيح!',
      incorrect: 'خطأ',
      session_finished: 'اكتملت الجلسة',
      view_sources: 'عرض المصادر',
      teacher_dashboard: 'لوحة تحكم المعلم',
      upload_content: 'رفع المحتوى',
      analytics: 'التحليلات',
      language: 'اللغة',
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
