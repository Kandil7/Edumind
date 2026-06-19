import React, { useState, useEffect, useCallback } from 'react';
import { useTranslation } from 'react-i18next';
import { tutorAPI } from '../api/client';
import { QuestionCard } from '../components/QuestionCard';
import { SourceCitation } from '../components/SourceCitation';
import { LoadingSpinner, ErrorMessage } from '../components/UIComponents';
import type { Lesson, TutorStepResponse } from '../types';

interface Props {
  lesson: Lesson;
  studentId: string;
  onFinish: () => void;
}

export const StudentSession: React.FC<Props> = ({ lesson, studentId, onFinish }) => {
  const { t } = useTranslation();
  const [step, setStep] = useState<TutorStepResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [lastQuestionId, setLastQuestionId] = useState<string | undefined>();
  const [lastResponse, setLastResponse] = useState<string | undefined>();
  const [stepCount, setStepCount] = useState(0);
  const [sessionHistory, setSessionHistory] = useState<{ question: string; correct: boolean }[]>([]);

  const loadStep = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await tutorAPI.sessionStep(studentId, lesson.id, lastQuestionId, lastResponse);
      setStep(res.data);
      setStepCount(prev => prev + 1);

      if (res.data.question) {
        setLastQuestionId(res.data.question.id);
      }
    } catch (err: any) {
      setError(err.message || 'Failed to load step');
    } finally {
      setLoading(false);
    }
  }, [studentId, lesson.id, lastQuestionId, lastResponse]);

  useEffect(() => { loadStep(); }, []);

  const handleSubmitAnswer = async (response: string) => {
    setLastResponse(response);
    await loadStep();
  };

  if (loading && !step) {
    return <LoadingSpinner message="Preparing your learning session..." />;
  }

  if (error) {
    return <ErrorMessage message={error} onRetry={loadStep} />;
  }

  if (step?.action === 'FINISHED' || stepCount > 15) {
    return (
      <div style={{ padding: '3rem', textAlign: 'center', maxWidth: '500px', margin: '0 auto' }}>
        <div style={{ fontSize: '4rem', marginBottom: '1rem' }}>🎉</div>
        <h2 style={{ marginBottom: '1rem' }}>{t('session_finished')}</h2>
        <p style={{ color: '#666', marginBottom: '0.5rem' }}>
          You completed {stepCount - 1} steps in this session.
        </p>
        <p style={{ color: '#666', marginBottom: '2rem' }}>
          Keep practicing to improve your mastery!
        </p>
        <button
          onClick={onFinish}
          style={{
            padding: '0.8rem 2rem',
            background: '#1976d2',
            color: '#fff',
            border: 'none',
            borderRadius: '8px',
            cursor: 'pointer',
            fontSize: '1rem',
          }}
        >
          {t('dashboard')}
        </button>
      </div>
    );
  }

  return (
    <div style={{ padding: '1rem' }}>
      <div style={{
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        marginBottom: '1.5rem',
        padding: '0.8rem 1.2rem',
        background: '#f5f5f5',
        borderRadius: '8px',
      }}>
        <span style={{ fontSize: '0.9rem', color: '#333' }}>
          📖 {lesson.title}
        </span>
        <span style={{ fontSize: '0.85rem', color: '#666' }}>
          Step {stepCount} / 15
        </span>
      </div>

      {step?.action === 'EXPLAIN' && step.explanation && (
        <div style={{
          padding: '2rem',
          maxWidth: '700px',
          margin: '0 auto',
          background: '#e8f5e9',
          borderRadius: '12px',
          border: '1px solid #c8e6c9',
        }}>
          <h2 style={{ marginBottom: '1rem', color: '#2e7d32' }}>💡 {t('explanations')}</h2>
          <p style={{ lineHeight: 1.8, whiteSpace: 'pre-wrap', fontSize: '1rem' }}>
            {step.explanation}
          </p>
          {step.sources && <SourceCitation sources={step.sources} />}
          <button
            onClick={() => loadStep()}
            style={{
              marginTop: '1.5rem',
              padding: '0.8rem 2rem',
              background: '#1976d2',
              color: '#fff',
              border: 'none',
              borderRadius: '8px',
              cursor: 'pointer',
              fontSize: '1rem',
            }}
          >
            {t('next')} →
          </button>
        </div>
      )}

      {step?.action === 'QUESTION' && step.question && (
        <QuestionCard
          question={step.question}
          sources={step.sources || undefined}
          onSubmit={handleSubmitAnswer}
        />
      )}

      {sessionHistory.length > 0 && (
        <div style={{ marginTop: '2rem', maxWidth: '700px', margin: '2rem auto 0' }}>
          <h4 style={{ marginBottom: '0.5rem', color: '#666' }}>Session Progress</h4>
          <div style={{ display: 'flex', gap: '0.3rem', flexWrap: 'wrap' }}>
            {sessionHistory.map((h, i) => (
              <div
                key={i}
                style={{
                  width: '24px',
                  height: '24px',
                  borderRadius: '4px',
                  background: h.correct ? '#4caf50' : '#f44336',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  fontSize: '0.7rem',
                  color: '#fff',
                }}
                title={h.question}
              >
                {i + 1}
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};
