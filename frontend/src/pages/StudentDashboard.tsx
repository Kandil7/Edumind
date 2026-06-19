import React, { useState, useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import { studentsAPI } from '../api/client';
import { MasteryHeatmap } from '../components/MasteryHeatmap';
import type { MasteryEntry } from '../types';

interface Props {
  studentId: string;
}

export const StudentDashboard: React.FC<Props> = ({ studentId }) => {
  const { t } = useTranslation();
  const [mastery, setMastery] = useState<MasteryEntry[]>([]);
  const [summary, setSummary] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([
      studentsAPI.profile(studentId),
      studentsAPI.summary(studentId),
    ])
      .then(([profileRes, summaryRes]) => {
        setMastery(profileRes.data.mastery);
        setSummary(summaryRes.data);
      })
      .catch(console.error)
      .finally(() => setLoading(false));
  }, [studentId]);

  if (loading) return <div style={{ padding: '2rem', textAlign: 'center' }}>{t('loading')}...</div>;

  return (
    <div style={{ padding: '2rem', maxWidth: '900px', margin: '0 auto' }}>
      <h1 style={{ fontSize: '1.8rem', marginBottom: '1.5rem' }}>{t('dashboard')}</h1>

      {summary && (
        <div style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(3, 1fr)',
          gap: '1rem',
          marginBottom: '2rem',
        }}>
          <div style={{ padding: '1.5rem', background: '#e3f2fd', borderRadius: '8px', textAlign: 'center' }}>
            <div style={{ fontSize: '2rem', fontWeight: 'bold' }}>{summary.total_attempts}</div>
            <div style={{ color: '#666' }}>Total Attempts</div>
          </div>
          <div style={{ padding: '1.5rem', background: '#e8f5e9', borderRadius: '8px', textAlign: 'center' }}>
            <div style={{ fontSize: '2rem', fontWeight: 'bold' }}>{summary.correct_attempts}</div>
            <div style={{ color: '#666' }}>Correct</div>
          </div>
          <div style={{ padding: '1.5rem', background: '#fff3e0', borderRadius: '8px', textAlign: 'center' }}>
            <div style={{ fontSize: '2rem', fontWeight: 'bold' }}>{summary.accuracy_pct}%</div>
            <div style={{ color: '#666' }}>Accuracy</div>
          </div>
        </div>
      )}

      <MasteryHeatmap mastery={mastery} />

      {mastery.length > 0 && (
        <div style={{ marginTop: '2rem' }}>
          <h3>{t('gaps')}</h3>
          <div style={{ display: 'grid', gap: '0.5rem' }}>
            {mastery
              .filter(m => m.p_mastery < 0.5)
              .map(m => (
                <div
                  key={m.skill_id}
                  style={{
                    padding: '1rem',
                    background: '#ffebee',
                    borderRadius: '8px',
                    display: 'flex',
                    justifyContent: 'space-between',
                  }}
                >
                  <span>{m.concept_name} / {m.skill_name}</span>
                  <span style={{ color: '#c62828', fontWeight: 'bold' }}>
                    {Math.round(m.p_mastery * 100)}%
                  </span>
                </div>
              ))}
          </div>
        </div>
      )}
    </div>
  );
};
