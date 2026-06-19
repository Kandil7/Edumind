import React, { useState, useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import { lessonsAPI } from '../api/client';
import type { Lesson } from '../types';

interface Props {
  onSelectLesson: (lesson: Lesson) => void;
}

export const LessonList: React.FC<Props> = ({ onSelectLesson }) => {
  const { t } = useTranslation();
  const [lessons, setLessons] = useState<Lesson[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    lessonsAPI.list()
      .then(res => setLessons(res.data))
      .catch(console.error)
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <div style={{ padding: '2rem', textAlign: 'center' }}>{t('loading')}...</div>;

  return (
    <div style={{ padding: '2rem', maxWidth: '800px', margin: '0 auto' }}>
      <h1 style={{ fontSize: '1.8rem', marginBottom: '1rem' }}>{t('lessons')}</h1>
      {lessons.length === 0 ? (
        <p style={{ color: '#666' }}>No lessons available yet.</p>
      ) : (
        <div style={{ display: 'grid', gap: '1rem' }}>
          {lessons.map(lesson => (
            <div
              key={lesson.id}
              onClick={() => onSelectLesson(lesson)}
              style={{
                padding: '1.5rem',
                border: '1px solid #e0e0e0',
                borderRadius: '8px',
                cursor: 'pointer',
                transition: 'box-shadow 0.2s',
              }}
              onMouseEnter={e => (e.currentTarget.style.boxShadow = '0 2px 8px rgba(0,0,0,0.1)')}
              onMouseLeave={e => (e.currentTarget.style.boxShadow = 'none')}
            >
              <h3 style={{ margin: '0 0 0.5rem 0' }}>{lesson.title}</h3>
              <p style={{ margin: 0, color: '#666', fontSize: '0.9rem' }}>
                {lesson.subject} | {lesson.grade_level} | {lesson.language}
              </p>
              {lesson.description && (
                <p style={{ margin: '0.5rem 0 0 0', fontSize: '0.85rem' }}>{lesson.description}</p>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
};
