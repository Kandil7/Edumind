import React, { useState, useEffect, useCallback } from 'react';
import { useTranslation } from 'react-i18next';
import { lessonsAPI } from '../api/client';
import { LoadingSpinner, ErrorMessage, EmptyState } from './UIComponents';
import type { Lesson } from '../types';

interface Props {
  onSelectLesson: (lesson: Lesson) => void;
}

export const LessonList: React.FC<Props> = ({ onSelectLesson }) => {
  const { t } = useTranslation();
  const [lessons, setLessons] = useState<Lesson[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const loadLessons = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await lessonsAPI.list();
      setLessons(res.data);
    } catch (err: any) {
      setError(err.message || 'Failed to load lessons');
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => { loadLessons(); }, [loadLessons]);

  if (loading) return <LoadingSpinner message={t('loading')} />;
  if (error) return <ErrorMessage message={error} onRetry={loadLessons} />;

  return (
    <div style={{ padding: '2rem', maxWidth: '800px', margin: '0 auto' }}>
      <h1 style={{ fontSize: '1.8rem', marginBottom: '1.5rem' }}>{t('lessons')}</h1>
      {lessons.length === 0 ? (
        <EmptyState message="No lessons available yet. Ask a teacher to upload content!" />
      ) : (
        <div style={{ display: 'grid', gap: '1rem' }}>
          {lessons.map(lesson => (
            <div
              key={lesson.id}
              onClick={() => onSelectLesson(lesson)}
              style={{
                padding: '1.5rem',
                border: '1px solid #e0e0e0',
                borderRadius: '12px',
                cursor: 'pointer',
                transition: 'all 0.2s',
                background: '#fff',
              }}
              onMouseEnter={e => {
                e.currentTarget.style.boxShadow = '0 4px 12px rgba(0,0,0,0.1)';
                e.currentTarget.style.borderColor = '#1976d2';
              }}
              onMouseLeave={e => {
                e.currentTarget.style.boxShadow = 'none';
                e.currentTarget.style.borderColor = '#e0e0e0';
              }}
            >
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'start' }}>
                <div>
                  <h3 style={{ margin: '0 0 0.5rem 0', fontSize: '1.2rem' }}>{lesson.title}</h3>
                  <p style={{ margin: 0, color: '#666', fontSize: '0.9rem' }}>
                    {lesson.subject} | {lesson.grade_level} | {lesson.language === 'ar' ? 'عربي' : 'English'}
                  </p>
                </div>
                <span style={{
                  padding: '0.3rem 0.8rem',
                  background: lesson.is_active ? '#e8f5e9' : '#ffebee',
                  color: lesson.is_active ? '#2e7d32' : '#c62828',
                  borderRadius: '12px',
                  fontSize: '0.75rem',
                }}>
                  {lesson.is_active ? 'Active' : 'Inactive'}
                </span>
              </div>
              {lesson.description && (
                <p style={{ margin: '0.8rem 0 0 0', fontSize: '0.85rem', color: '#555' }}>
                  {lesson.description}
                </p>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
};
