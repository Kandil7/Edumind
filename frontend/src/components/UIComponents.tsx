import React from 'react';

interface Props {
  message?: string;
  onRetry?: () => void;
}

export const LoadingSpinner: React.FC<Props> = ({ message }) => (
  <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', padding: '3rem' }}>
    <div style={{
      width: '40px',
      height: '40px',
      border: '4px solid #e0e0e0',
      borderTop: '4px solid #1976d2',
      borderRadius: '50%',
      animation: 'spin 1s linear infinite',
    }} />
    <style>{`@keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }`}</style>
    {message && <p style={{ marginTop: '1rem', color: '#666' }}>{message}</p>}
  </div>
);

export const ErrorMessage: React.FC<Props> = ({ message, onRetry }) => (
  <div style={{
    padding: '2rem',
    textAlign: 'center',
    background: '#ffebee',
    borderRadius: '12px',
    maxWidth: '500px',
    margin: '2rem auto',
  }}>
    <p style={{ color: '#c62828', fontSize: '1.1rem', marginBottom: '1rem' }}>
      {message || 'Something went wrong'}
    </p>
    {onRetry && (
      <button
        onClick={onRetry}
        style={{
          padding: '0.6rem 1.5rem',
          background: '#1976d2',
          color: '#fff',
          border: 'none',
          borderRadius: '6px',
          cursor: 'pointer',
        }}
      >
        Try Again
      </button>
    )}
  </div>
);

export const EmptyState: React.FC<{ message: string }> = ({ message }) => (
  <div style={{ padding: '3rem', textAlign: 'center', color: '#999' }}>
    <p style={{ fontSize: '1.1rem' }}>{message}</p>
  </div>
);
