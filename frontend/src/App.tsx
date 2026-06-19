import { useState, useEffect, useCallback } from 'react';
import { useTranslation } from 'react-i18next';
import { LoginPage } from './components/LoginPage';
import { LessonList } from './components/LessonList';
import { StudentSession } from './pages/StudentSession';
import { StudentDashboard } from './pages/StudentDashboard';
import { TeacherDashboard } from './pages/TeacherDashboard';
import { authAPI } from './api/client';
import type { Lesson, AuthState } from './types';

type View = 'lessons' | 'session' | 'dashboard' | 'teacher';

function App() {
  const { t, i18n } = useTranslation();
  const [auth, setAuth] = useState<AuthState>({
    user: null,
    token: null,
    isAuthenticated: false,
    isLoading: true,
  });
  const [view, setView] = useState<View>('lessons');
  const [selectedLesson, setSelectedLesson] = useState<Lesson | null>(null);

  // Check for existing token on mount
  useEffect(() => {
    const token = localStorage.getItem('token');
    if (token) {
      authAPI.me()
        .then(res => {
          setAuth({
            user: res.data,
            token,
            isAuthenticated: true,
            isLoading: false,
          });
        })
        .catch(() => {
          localStorage.removeItem('token');
          setAuth({ user: null, token: null, isAuthenticated: false, isLoading: false });
        });
    } else {
      setAuth(prev => ({ ...prev, isLoading: false }));
    }
  }, []);

  const handleLogin = useCallback((token: string, userId: string, role: string) => {
    localStorage.setItem('token', token);
    setAuth({
      user: { user_id: userId, email: '', role: role as any },
      token,
      isAuthenticated: true,
      isLoading: false,
    });
  }, []);

  const handleLogout = useCallback(() => {
    localStorage.removeItem('token');
    setAuth({ user: null, token: null, isAuthenticated: false, isLoading: false });
    setView('lessons');
  }, []);

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

  // Loading state
  if (auth.isLoading) {
    return (
      <div style={{ minHeight: '100vh', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
        <p style={{ fontSize: '1.2rem', color: '#666' }}>{t('loading')}...</p>
      </div>
    );
  }

  // Not authenticated - show login
  if (!auth.isAuthenticated) {
    return <LoginPage onLogin={handleLogin} />;
  }

  // Authenticated - show app
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
          {auth.user?.role === 'teacher' && (
            <button
              onClick={() => setView('teacher')}
              style={{ background: 'none', border: 'none', color: '#fff', cursor: 'pointer' }}
            >
              {t('teacher_dashboard')}
            </button>
          )}
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
          <button
            onClick={handleLogout}
            style={{
              padding: '0.4rem 0.8rem',
              background: 'rgba(255,255,255,0.1)',
              border: '1px solid rgba(255,255,255,0.2)',
              borderRadius: '4px',
              color: '#fff',
              cursor: 'pointer',
            }}
          >
            {t('logout')}
          </button>
        </div>
      </nav>

      <main>
        {view === 'lessons' && <LessonList onSelectLesson={handleSelectLesson} />}
        {view === 'session' && selectedLesson && (
          <StudentSession
            lesson={selectedLesson}
            studentId={auth.user?.user_id || ''}
            onFinish={handleSessionFinish}
          />
        )}
        {view === 'dashboard' && <StudentDashboard studentId={auth.user?.user_id || ''} />}
        {view === 'teacher' && <TeacherDashboard onBack={() => setView('lessons')} />}
      </main>
    </div>
  );
}

export default App;
