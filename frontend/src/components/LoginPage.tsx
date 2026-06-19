import React, { useState } from 'react';
import { useTranslation } from 'react-i18next';
import { authAPI } from '../api/client';

interface LoginPageProps {
  onLogin: (token: string, userId: string, role: string) => void;
}

export function LoginPage({ onLogin }: LoginPageProps) {
  const { t } = useTranslation();
  const [isRegister, setIsRegister] = useState(false);
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [name, setName] = useState('');
  const [role, setRole] = useState('student');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      if (isRegister) {
        const res = await authAPI.register(name, email, password, role);
        onLogin(res.data.access_token, res.data.user_id, res.data.role);
      } else {
        const res = await authAPI.login(email, password);
        onLogin(res.data.access_token, res.data.user_id, res.data.role);
      }
    } catch (err: any) {
      setError(err.message || 'Authentication failed');
    } finally {
      setLoading(false);
    }
  };

  const containerStyle: React.CSSProperties = {
    minHeight: '100vh',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    background: 'linear-gradient(135deg, #1976d2 0%, #1565c0 100%)',
    padding: '1rem',
  };

  const cardStyle: React.CSSProperties = {
    background: '#fff',
    borderRadius: '12px',
    padding: '2.5rem',
    width: '100%',
    maxWidth: '420px',
    boxShadow: '0 8px 32px rgba(0,0,0,0.2)',
  };

  const inputStyle: React.CSSProperties = {
    width: '100%',
    padding: '0.75rem 1rem',
    border: '1px solid #ddd',
    borderRadius: '8px',
    fontSize: '1rem',
    marginBottom: '1rem',
    boxSizing: 'border-box',
    outline: 'none',
  };

  const buttonStyle: React.CSSProperties = {
    width: '100%',
    padding: '0.85rem',
    background: '#1976d2',
    color: '#fff',
    border: 'none',
    borderRadius: '8px',
    fontSize: '1rem',
    fontWeight: 600,
    cursor: loading ? 'not-allowed' : 'pointer',
    opacity: loading ? 0.7 : 1,
  };

  const labelStyle: React.CSSProperties = {
    display: 'block',
    marginBottom: '0.3rem',
    fontSize: '0.9rem',
    color: '#555',
    fontWeight: 500,
  };

  return (
    <div style={containerStyle}>
      <div style={cardStyle}>
        <h1 style={{ textAlign: 'center', marginBottom: '0.5rem', color: '#1976d2' }}>
          {t('app_name')}
        </h1>
        <p style={{ textAlign: 'center', color: '#666', marginBottom: '2rem' }}>
          {isRegister ? t('register') : t('login')}
        </p>

        {error && (
          <div style={{
            background: '#ffebee',
            color: '#c62828',
            padding: '0.75rem',
            borderRadius: '8px',
            marginBottom: '1rem',
            fontSize: '0.9rem',
          }}>
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit}>
          {isRegister && (
            <div>
              <label style={labelStyle}>{t('name')}</label>
              <input
                type="text"
                value={name}
                onChange={(e) => setName(e.target.value)}
                style={inputStyle}
                required
                placeholder={t('name')}
              />
            </div>
          )}

          <div>
            <label style={labelStyle}>{t('email')}</label>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              style={inputStyle}
              required
              placeholder="demo@edumind.com"
            />
          </div>

          <div>
            <label style={labelStyle}>{t('password')}</label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              style={inputStyle}
              required
              placeholder="••••••••"
            />
          </div>

          {isRegister && (
            <div>
              <label style={labelStyle}>{t('role')}</label>
              <select
                value={role}
                onChange={(e) => setRole(e.target.value)}
                style={{ ...inputStyle, cursor: 'pointer' }}
              >
                <option value="student">{t('student')}</option>
                <option value="teacher">{t('teacher')}</option>
              </select>
            </div>
          )}

          <button type="submit" style={buttonStyle} disabled={loading}>
            {loading ? t('loading') : isRegister ? t('register') : t('login')}
          </button>
        </form>

        <p style={{ textAlign: 'center', marginTop: '1.5rem', color: '#666' }}>
          {isRegister ? t('already_have_account') : t('no_account')}
          {' '}
          <button
            onClick={() => { setIsRegister(!isRegister); setError(''); }}
            style={{
              background: 'none',
              border: 'none',
              color: '#1976d2',
              cursor: 'pointer',
              fontWeight: 600,
              fontSize: '1rem',
              padding: 0,
            }}
          >
            {isRegister ? t('login') : t('register')}
          </button>
        </p>

        {!isRegister && (
          <div style={{
            marginTop: '1.5rem',
            padding: '0.75rem',
            background: '#e3f2fd',
            borderRadius: '8px',
            fontSize: '0.85rem',
            color: '#1565c0',
            textAlign: 'center',
          }}>
            <strong>Demo:</strong> demo@edumind.com / demo123
          </div>
        )}
      </div>
    </div>
  );
}
