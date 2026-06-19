import React from 'react';
import { useTranslation } from 'react-i18next';
import type { Question, SourceLocator } from '../types';

interface Props {
  question: Question;
  sources?: SourceLocator[];
  onSubmit: (response: string) => void;
  result?: { correct: boolean } | null;
}

export const QuestionCard: React.FC<Props> = ({ question, sources, onSubmit, result }) => {
  const { t } = useTranslation();
  const [answer, setAnswer] = useState('');

  const handleSubmit = () => {
    if (answer.trim()) {
      onSubmit(answer);
    }
  };

  return (
    <div style={{
      padding: '2rem',
      maxWidth: '700px',
      margin: '0 auto',
      border: '1px solid #e0e0e0',
      borderRadius: '12px',
    }}>
      <div style={{ marginBottom: '0.5rem', fontSize: '0.8rem', color: '#888' }}>
        {question.type.toUpperCase()} | Difficulty: {question.difficulty}
      </div>

      <h2 style={{ fontSize: '1.3rem', marginBottom: '1.5rem' }}>{question.stem}</h2>

      {question.type === 'mcq' && question.options.length > 0 && (
        <div style={{ display: 'grid', gap: '0.5rem', marginBottom: '1.5rem' }}>
          {question.options.map(opt => (
            <button
              key={opt.id}
              onClick={() => setAnswer(String(opt.id))}
              style={{
                padding: '0.8rem 1rem',
                border: answer === String(opt.id) ? '2px solid #1976d2' : '1px solid #ddd',
                borderRadius: '8px',
                background: answer === String(opt.id) ? '#e3f2fd' : '#fff',
                cursor: 'pointer',
                textAlign: 'start',
              }}
            >
              {opt.text}
            </button>
          ))}
        </div>
      )}

      {(question.type === 'cloze' || question.type === 'open_text') && (
        <textarea
          value={answer}
          onChange={e => setAnswer(e.target.value)}
          placeholder={t('type_answer')}
          style={{
            width: '100%',
            minHeight: '100px',
            padding: '1rem',
            border: '1px solid #ddd',
            borderRadius: '8px',
            fontSize: '1rem',
            resize: 'vertical',
            boxSizing: 'border-box',
          }}
        />
      )}

      {result && (
        <div style={{
          padding: '1rem',
          marginTop: '1rem',
          borderRadius: '8px',
          background: result.correct ? '#e8f5e9' : '#ffebee',
          color: result.correct ? '#2e7d32' : '#c62828',
          fontWeight: 'bold',
        }}>
          {result.correct ? t('correct') : t('incorrect')}
        </div>
      )}

      {sources && sources.length > 0 && (
        <div style={{ marginTop: '1rem', padding: '1rem', background: '#f5f5f5', borderRadius: '8px' }}>
          <strong>{t('view_sources')}:</strong>
          <ul style={{ margin: '0.5rem 0 0 0', paddingLeft: '1.2rem' }}>
            {sources.map((s, i) => (
              <li key={i} style={{ fontSize: '0.85rem', marginBottom: '0.3rem' }}>
                {s.source_name} ({s.source_type})
                {s.start_offset !== undefined && ` - offset: ${s.start_offset}`}
              </li>
            ))}
          </ul>
        </div>
      )}

      {!result && (
        <button
          onClick={handleSubmit}
          disabled={!answer.trim()}
          style={{
            marginTop: '1rem',
            padding: '0.8rem 2rem',
            background: answer.trim() ? '#1976d2' : '#ccc',
            color: '#fff',
            border: 'none',
            borderRadius: '8px',
            cursor: answer.trim() ? 'pointer' : 'not-allowed',
            fontSize: '1rem',
          }}
        >
          {t('submit')}
        </button>
      )}
    </div>
  );
};

import { useState } from 'react';
