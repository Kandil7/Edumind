import React, { useState } from 'react';
import { useTranslation } from 'react-i18next';
import { lessonsAPI, contentAPI } from '../api/client';
import type { Lesson } from '../types';

interface Props {
  onBack: () => void;
}

export const TeacherDashboard: React.FC<Props> = ({ onBack }) => {
  const { t } = useTranslation();
  const [view, setView] = useState<'overview' | 'upload' | 'lessons'>('overview');
  const [lessons, setLessons] = useState<Lesson[]>([]);
  const [uploadFile, setUploadFile] = useState<File | null>(null);
  const [uploadLanguage, setUploadLanguage] = useState('ar');
  const [uploading, setUploading] = useState(false);
  const [newLesson, setNewLesson] = useState({
    title: '', subject: 'التفاضل والتكامل', grade_level: 'ثانوي', language: 'ar', description: '',
  });
  const [message, setMessage] = useState('');

  const loadLessons = async () => {
    try {
      const res = await lessonsAPI.list();
      setLessons(res.data);
    } catch (err) {
      console.error(err);
    }
  };

  const handleUpload = async () => {
    if (!uploadFile) return;
    setUploading(true);
    try {
      const res = await contentAPI.uploadSource(uploadFile, uploadLanguage);
      setMessage(`Uploaded: ${res.data.title} (ID: ${res.data.id})`);
      setUploadFile(null);
    } catch (err) {
      setMessage('Upload failed');
    }
    setUploading(false);
  };

  const handleCreateLesson = async () => {
    try {
      await lessonsAPI.create(newLesson);
      setMessage('Lesson created!');
      setNewLesson({ title: '', subject: 'التفاضل والتكامل', grade_level: 'ثانوي', language: 'ar', description: '' });
      loadLessons();
    } catch (err) {
      setMessage('Failed to create lesson');
    }
  };

  return (
    <div style={{ padding: '2rem', maxWidth: '900px', margin: '0 auto' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.5rem' }}>
        <h1 style={{ fontSize: '1.8rem' }}>{t('teacher_dashboard')}</h1>
        <button onClick={onBack} style={{ padding: '0.5rem 1rem', border: '1px solid #ddd', borderRadius: '6px', cursor: 'pointer' }}>
          ← Back
        </button>
      </div>

      {message && (
        <div style={{ padding: '1rem', background: '#e3f2fd', borderRadius: '8px', marginBottom: '1rem' }}>
          {message}
          <button onClick={() => setMessage('')} style={{ marginLeft: '1rem', border: 'none', background: 'none', cursor: 'pointer' }}>✕</button>
        </div>
      )}

      <div style={{ display: 'flex', gap: '0.5rem', marginBottom: '2rem' }}>
        {(['overview', 'upload', 'lessons'] as const).map(v => (
          <button
            key={v}
            onClick={() => { setView(v); if (v === 'lessons') loadLessons(); }}
            style={{
              padding: '0.6rem 1.2rem',
              background: view === v ? '#1976d2' : '#f5f5f5',
              color: view === v ? '#fff' : '#333',
              border: 'none',
              borderRadius: '6px',
              cursor: 'pointer',
            }}
          >
            {v === 'overview' ? 'Overview' : v === 'upload' ? t('upload_content') : t('lessons')}
          </button>
        ))}
      </div>

      {view === 'overview' && (
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '1rem' }}>
          <div style={{ padding: '1.5rem', background: '#e8f5e9', borderRadius: '8px', textAlign: 'center' }}>
            <div style={{ fontSize: '2rem', fontWeight: 'bold' }}>{lessons.length || '—'}</div>
            <div>Lessons</div>
          </div>
          <div style={{ padding: '1.5rem', background: '#fff3e0', borderRadius: '8px', textAlign: 'center' }}>
            <div style={{ fontSize: '2rem', fontWeight: 'bold' }}>—</div>
            <div>Students</div>
          </div>
          <div style={{ padding: '1.5rem', background: '#e3f2fd', borderRadius: '8px', textAlign: 'center' }}>
            <div style={{ fontSize: '2rem', fontWeight: 'bold' }}>—</div>
            <div>Questions</div>
          </div>
        </div>
      )}

      {view === 'upload' && (
        <div style={{ padding: '2rem', border: '2px dashed #ddd', borderRadius: '12px', textAlign: 'center' }}>
          <h3 style={{ marginBottom: '1rem' }}>{t('upload_content')}</h3>
          <input
            type="file"
            accept=".pdf,.pptx,.txt,.md,.mp3,.mp4"
            onChange={e => setUploadFile(e.target.files?.[0] || null)}
            style={{ marginBottom: '1rem' }}
          />
          <div style={{ marginBottom: '1rem' }}>
            <select value={uploadLanguage} onChange={e => setUploadLanguage(e.target.value)}>
              <option value="ar">العربية</option>
              <option value="en">English</option>
            </select>
          </div>
          <button
            onClick={handleUpload}
            disabled={!uploadFile || uploading}
            style={{
              padding: '0.8rem 2rem',
              background: uploadFile && !uploading ? '#1976d2' : '#ccc',
              color: '#fff',
              border: 'none',
              borderRadius: '8px',
              cursor: uploadFile && !uploading ? 'pointer' : 'not-allowed',
            }}
          >
            {uploading ? 'Uploading...' : 'Upload'}
          </button>
        </div>
      )}

      {view === 'lessons' && (
        <div>
          <h3 style={{ marginBottom: '1rem' }}>Create New Lesson</h3>
          <div style={{ display: 'grid', gap: '0.8rem', marginBottom: '2rem', maxWidth: '500px' }}>
            <input
              placeholder="Lesson title"
              value={newLesson.title}
              onChange={e => setNewLesson({ ...newLesson, title: e.target.value })}
              style={{ padding: '0.7rem', border: '1px solid #ddd', borderRadius: '6px' }}
            />
            <input
              placeholder="Subject"
              value={newLesson.subject}
              onChange={e => setNewLesson({ ...newLesson, subject: e.target.value })}
              style={{ padding: '0.7rem', border: '1px solid #ddd', borderRadius: '6px' }}
            />
            <input
              placeholder="Grade level"
              value={newLesson.grade_level}
              onChange={e => setNewLesson({ ...newLesson, grade_level: e.target.value })}
              style={{ padding: '0.7rem', border: '1px solid #ddd', borderRadius: '6px' }}
            />
            <textarea
              placeholder="Description"
              value={newLesson.description}
              onChange={e => setNewLesson({ ...newLesson, description: e.target.value })}
              style={{ padding: '0.7rem', border: '1px solid #ddd', borderRadius: '6px', minHeight: '80px' }}
            />
            <button
              onClick={handleCreateLesson}
              disabled={!newLesson.title}
              style={{
                padding: '0.7rem',
                background: newLesson.title ? '#4caf50' : '#ccc',
                color: '#fff',
                border: 'none',
                borderRadius: '6px',
                cursor: newLesson.title ? 'pointer' : 'not-allowed',
              }}
            >
              Create Lesson
            </button>
          </div>

          <h3 style={{ marginBottom: '1rem' }}>Existing Lessons</h3>
          <button onClick={loadLessons} style={{ marginBottom: '1rem', padding: '0.4rem 1rem', border: '1px solid #ddd', borderRadius: '4px', cursor: 'pointer' }}>
            Refresh
          </button>
          {lessons.map(l => (
            <div key={l.id} style={{ padding: '1rem', border: '1px solid #e0e0e0', borderRadius: '8px', marginBottom: '0.5rem' }}>
              <strong>{l.title}</strong>
              <span style={{ marginLeft: '1rem', color: '#666' }}>{l.subject} | {l.grade_level}</span>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};
