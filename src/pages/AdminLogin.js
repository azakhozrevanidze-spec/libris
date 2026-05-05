import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { supabase } from '../supabaseClient';
import { useLanguage } from '../context/LanguageContext';

export default function AdminLogin() {
  const { t } = useLanguage();
  const navigate = useNavigate();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleLogin = async (e) => {
    e.preventDefault();
    setLoading(true); setError('');
    const { error: err } = await supabase.auth.signInWithPassword({ email, password });
    setLoading(false);
    if (err) { setError(err.message); return; }
    navigate('/admin/dashboard');
  };

  const inputStyle = {
    width: '100%', padding: '13px 16px', borderRadius: 10,
    border: '1.5px solid rgba(201,168,76,0.25)', background: '#f8f7f4',
    fontSize: '0.95rem', outline: 'none', color: '#1A1A2E',
    transition: 'border-color 0.2s', boxSizing: 'border-box',
  };

  return (
    <div style={{
      minHeight: '100vh', display: 'flex', alignItems: 'center', justifyContent: 'center',
      background: 'linear-gradient(135deg, #0A1628, #132240)',
      paddingTop: 72,
    }}>
      <div style={{
        background: '#fff', borderRadius: 24, padding: '48px 44px',
        width: '100%', maxWidth: 420, boxShadow: '0 40px 100px rgba(0,0,0,0.3)',
      }}>
        <div style={{ textAlign: 'center', marginBottom: 36 }}>
          <img
            src="https://res.cloudinary.com/dompnhsjb/image/upload/v1777535945/ChatGPT_Image_Apr_30_2026_11_54_26_AM_oll6ka.png"
            alt="Libris" style={{ height: 56, marginBottom: 16, borderRadius: 10 }}
          />
          <h1 style={{ fontFamily: 'Playfair Display, serif', fontSize: '1.7rem', color: '#0A1628' }}>
            {t.adminLogin}
          </h1>
        </div>

        <form onSubmit={handleLogin}>
          <div style={{ marginBottom: 18 }}>
            <label style={{ display: 'block', fontSize: '0.82rem', fontWeight: 600, color: '#4A5568', marginBottom: 6, letterSpacing: '0.04em', textTransform: 'uppercase' }}>
              {t.email}
            </label>
            <input type="email" value={email} onChange={e => setEmail(e.target.value)} style={inputStyle} required />
          </div>
          <div style={{ marginBottom: 28 }}>
            <label style={{ display: 'block', fontSize: '0.82rem', fontWeight: 600, color: '#4A5568', marginBottom: 6, letterSpacing: '0.04em', textTransform: 'uppercase' }}>
              {t.password}
            </label>
            <input type="password" value={password} onChange={e => setPassword(e.target.value)} style={inputStyle} required />
          </div>

          {error && (
            <div style={{ background: '#FEE2E2', border: '1px solid #FECACA', borderRadius: 8, padding: '10px 14px', color: '#DC2626', fontSize: '0.875rem', marginBottom: 20 }}>
              {error}
            </div>
          )}

          <button type="submit" className="btn-primary" disabled={loading}
            style={{ width: '100%', justifyContent: 'center', padding: '14px', fontSize: '1rem' }}>
            {loading ? t.uploading : t.signIn}
          </button>
        </form>
      </div>
    </div>
  );
}
