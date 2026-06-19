import React, { useState, useEffect, useCallback } from 'react';
import { useTranslation } from 'react-i18next';
import { studentsAPI } from '../api/client';
import { MasteryHeatmap } from '../components/MasteryHeatmap';
import { LoadingSpinner, ErrorMessage, EmptyState } from '../components/UIComponents';
import type { MasteryEntry } from '../types';

interface Props {
  studentId: string;
}

export const StudentDashboard: React.FC<Props> = ({ studentId }) => {
  const { t } = useTranslation();
  const [mastery, setMastery] = useState<MasteryEntry[]>([]);
  const [summary, setSummary] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const loadData = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const [profileRes, summaryRes] = await Promise.all([
        studentsAPI.profile(studentId),
        studentsAPI.summary(studentId),
      ]);
      setMastery(profileRes.data.mastery);
      setSummary(summaryRes.data);
    } catch (err: any) {
      setError(err.message || 'Failed to load dashboard');
    } finally {
      setLoading(false);
    }
  }, [studentId]);

  useEffect(() => { loadData(); }, [loadData]);

  if (loading) return <LoadingSpinner message="Loading your dashboard..." />;
  if (error) return <ErrorMessage message={error} onRetry={loadData} />;

  const lowMastery = mastery.filter(m => m.p_mastery < 0.5);
  const highMastery = mastery.filter(m => m.p_mastery >= 0.8);

  return (
    <div style={{ padding: '2rem', maxWidth: '900px', margin: '0 auto' }}>
      <h1 style={{ fontSize: '1.8rem', marginBottom: '1.5rem' }}>{t('dashboard')}</h1>

      {/* Stats Cards */}
      {summary && (
        <div style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fit, minmax(150px, 1fr))',
          gap: '1rem',
          marginBottom: '2rem',
        }}>
          <StatCard
            value={summary.total_attempts}
            label="Total Attempts"
            color="#e3f2fd"
            icon="📝"
          />
          <StatCard
            value={summary.correct_attempts}
            label="Correct"
            color="#e8f5e9"
            icon="✅"
          />
          <StatCard
            value={`${summary.accuracy_pct}%`}
            label="Accuracy"
            color="#fff3e0"
            icon="📊"
          />
          <StatCard
            value={highMastery.length}
            label="Mastered Skills"
            color="#e8f5e9"
            icon="🌟"
          />
          <StatCard
            value={lowMastery.length}
            label="Needs Practice"
            color="#ffebee"
            icon="⚠️"
          />
        </div>
      )}

      {/* Mastery Chart */}
      {mastery.length > 0 ? (
        <MasteryHeatmap mastery={mastery} />
      ) : (
        <EmptyState message="No mastery data yet. Start a learning session!" />
      )}

      {/* Low Mastery Alerts */}
      {lowMastery.length > 0 && (
        <div style={{ marginTop: '2rem' }}>
          <h3 style={{ marginBottom: '1rem', color: '#c62828' }}>⚠️ {t('gaps')}</h3>
          <div style={{ display: 'grid', gap: '0.5rem' }}>
            {lowMastery.map(m => (
              <div
                key={m.skill_id}
                style={{
                  padding: '1rem 1.5rem',
                  background: '#ffebee',
                  borderRadius: '8px',
                  display: 'flex',
                  justifyContent: 'space-between',
                  alignItems: 'center',
                  borderLeft: '4px solid #f44336',
                }}
              >
                <div>
                  <strong>{m.concept_name}</strong>
                  <span style={{ color: '#666', marginLeft: '0.5rem' }}>/ {m.skill_name}</span>
                </div>
                <span style={{
                  color: '#c62828',
                  fontWeight: 'bold',
                  fontSize: '1.1rem',
                }}>
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

const StatCard: React.FC<{ value: number | string; label: string; color: string; icon: string }> = ({
  value, label, color, icon,
}) => (
  <div style={{
    padding: '1.5rem',
    background: color,
    borderRadius: '12px',
    textAlign: 'center',
  }}>
    <div style={{ fontSize: '1.5rem', marginBottom: '0.3rem' }}>{icon}</div>
    <div style={{ fontSize: '1.8rem', fontWeight: 'bold' }}>{value}</div>
    <div style={{ color: '#666', fontSize: '0.85rem' }}>{label}</div>
  </div>
);
