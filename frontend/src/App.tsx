import React, { useState } from 'react';
import { useTranslation } from 'react-i18next';
import { LessonList } from './components/LessonList';
import { StudentSession } from './pages/StudentSession';
import { StudentDashboard } from './pages/StudentDashboard';
import type { Lesson } from './types';

type View = 'lessons' | 'session' | 'dashboard';

const STUDENT_ID = '00000000-0000-0000-0000-000000000001';

function App() {
  const { t, i18n } = useTranslation();
  const [view, setView] = useState<View>('lessons');
  const [selectedLesson, setSelectedLesson] = useState<Lesson | null>(null);

  const handleSelectLesson = (lesson: Lesson) => {
    setSelectedLesson(lesson);
    setView('session');
  };

  const handleSessionFinish = () => {
    setView('dashboard');
  };

  const toggleLanguage = () => {
    i18n.changeLanguage(i18n.language === 'ar' ? 'en' : 'ar');
  };

  return (
    <div
      dir={i18n.language === 'ar' ? 'rtl' : 'ltr'}
      style={{
        minHeight: '100vh',
        fontFamily: i18n.language === 'ar' ? 'Arial, sans-serif' : 'Arial, sans-serif',
      }}
    >
      <nav style={{
        padding: '1rem 2rem',
        background: '#1976d2',
        color: '#fff',
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
      }}>
        <h1 style={{ margin: 0, fontSize: '1.3rem', cursor: 'pointer' }} onClick={() => setView('lessons')}>
          {t('app_name')}
        </h1>
        <div style={{ display: 'flex', gap: '1rem', alignItems: 'center' }}>
          <button
            onClick={() => setView('lessons')}
            style={{ background: 'none', border: 'none', color: '#fff', cursor: 'pointer' }}
          >
            {t('lessons')}
          </button>
          <button
            onClick={() => setView('dashboard')}
            style={{ background: 'none', border: 'none', color: '#fff', cursor: 'pointer' }}
          >
            {t('dashboard')}
          </button>
          <button
            onClick={toggleLanguage}
            style={{
              padding: '0.4rem 0.8rem',
              background: 'rgba(255,255,255,0.2)',
              border: '1px solid rgba(255,255,255,0.3)',
              borderRadius: '4px',
              color: '#fff',
              cursor: 'pointer',
            }}
          >
            {i18n.language === 'ar' ? 'EN' : 'عربي'}
          </button>
        </div>
      </nav>

      <main>
        {view === 'lessons' && <LessonList onSelectLesson={handleSelectLesson} />}
        {view === 'session' && selectedLesson && (
          <StudentSession
            lesson={selectedLesson}
            studentId={STUDENT_ID}
            onFinish={handleSessionFinish}
          />
        )}
        {view === 'dashboard' && <StudentDashboard studentId={STUDENT_ID} />}
      </main>
    </div>
  );
}

export default App;
