import React from 'react';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell } from 'recharts';
import type { MasteryEntry } from '../types';

interface Props {
  mastery: MasteryEntry[];
}

const getColor = (p: number): string => {
  if (p >= 0.8) return '#4caf50';
  if (p >= 0.6) return '#ff9800';
  if (p >= 0.4) return '#ff5722';
  return '#f44336';
};

export const MasteryHeatmap: React.FC<Props> = ({ mastery }) => {
  if (mastery.length === 0) {
    return <p style={{ color: '#666' }}>No mastery data yet. Start a learning session!</p>;
  }

  const data = mastery.map(m => ({
    name: m.concept_name.substring(0, 20),
    mastery: Math.round(m.p_mastery * 100),
    attempts: m.num_attempts,
  }));

  return (
    <div style={{ padding: '1rem' }}>
      <h3 style={{ marginBottom: '1rem' }}>Mastery per Concept</h3>
      <ResponsiveContainer width="100%" height={300}>
        <BarChart data={data} margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
          <XAxis dataKey="name" tick={{ fontSize: 11 }} />
          <YAxis domain={[0, 100]} tick={{ fontSize: 11 }} />
          <Tooltip formatter={(value: number) => [`${value}%`, 'Mastery']} />
          <Bar dataKey="mastery" radius={[4, 4, 0, 0]}>
            {data.map((entry, i) => (
              <Cell key={i} fill={getColor(entry.mastery / 100)} />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
};
