import React from 'react';
import type { SourceLocator } from '../types';

interface Props {
  sources: SourceLocator[];
}

export const SourceCitation: React.FC<Props> = ({ sources }) => {
  if (!sources || sources.length === 0) return null;

  return (
    <div style={{
      padding: '1rem',
      background: '#f8f9fa',
      borderRadius: '8px',
      marginTop: '1rem',
    }}>
      <strong style={{ fontSize: '0.9rem' }}>📚 Sources:</strong>
      <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.5rem', marginTop: '0.5rem' }}>
        {sources.map((source, i) => (
          <span
            key={i}
            style={{
              padding: '0.3rem 0.7rem',
              background: '#e3f2fd',
              borderRadius: '16px',
              fontSize: '0.8rem',
              color: '#1565c0',
            }}
          >
            {source.source_name}
            {source.source_type === 'audio' && source.start_offset !== undefined && (
              <span> ({Math.floor(source.start_offset / 60)}:{String(Math.floor(source.start_offset % 60)).padStart(2, '0')})</span>
            )}
          </span>
        ))}
      </div>
    </div>
  );
};
