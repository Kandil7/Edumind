import React, { useState, useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import { tutorAPI } from '../api/client';
import { QuestionCard } from '../components/QuestionCard';
import { SourceCitation } from '../components/SourceCitation';
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
  const [lastQuestionId, setLastQuestionId] = useState<string | undefined>();
  const [lastResponse, setLastResponse] = useState<string | undefined>();
  const [stepCount, setStepCount] = useState(0);

  const loadStep = async () => {
    setLoading(true);
    try {
      const res = await tutorAPI.sessionStep(studentId, lesson.id, lastQuestionId, lastResponse);
      setStep(res.data);
      setStepCount(prev => prev + 1);

      if (res.data.question) {
        setLastQuestionId(res.data.question.id);
      }
    } catch (err) {
      console.error('Session step error:', err);
    }
    setLoading(false);
  };

  useEffect(() => {
    loadStep();
  }, []);

  const handleSubmitAnswer = async (response: string) => {
    setLastResponse(response);
    await loadStep();
  };

  if (loading && !step) {
    return (
      <div style={{ padding: '3rem', textAlign: 'center' }}>
        <p>{t('loading')}...</p>
      </div>
    );
  }

  if (step?.action === 'FINISHED' || stepCount > 15) {
    return (
      <div style={{ padding: '3rem', textAlign: 'center' }}>
        <h2>{t('session_finished')}</h2>
        <p>You completed {stepCount - 1} questions.</p>
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
            marginTop: '1rem',
          }}
        >
          {t('dashboard')}
        </button>
      </div>
    );
  }

  return (
    <div style={{ padding: '1rem' }}>
      <div style={{ marginBottom: '1rem', fontSize: '0.85rem', color: '#666' }}>
        {lesson.title} | Step {stepCount}
      </div>

      {step?.action === 'EXPLAIN' && step.explanation && (
        <div style={{
          padding: '2rem',
          maxWidth: '700px',
          margin: '0 auto',
          background: '#e8f5e9',
          borderRadius: '12px',
        }}>
          <h2 style={{ marginBottom: '1rem' }}>{t('explanations')}</h2>
          <p style={{ lineHeight: 1.8, whiteSpace: 'pre-wrap' }}>{step.explanation}</p>
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
            {t('next')}
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
    </div>
  );
};
