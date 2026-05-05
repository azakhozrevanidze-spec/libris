import React from 'react';
import { useLanguage } from '../context/LanguageContext';

const EMAIL = process.env.REACT_APP_CONTACT_EMAIL || 'Libris.info.aza@gmail.com';

export default function Contact() {
  const { t } = useLanguage();

  return (
    <div style={{ paddingTop: 72, minHeight: '100vh', background: 'var(--cream)' }}>
      <div style={{ background: '#0A1628', padding: '80px 5%' }}>
        <div style={{ maxWidth: 700, margin: '0 auto', textAlign: 'center' }}>
          <h1 style={{ fontFamily: 'Playfair Display, serif', color: '#fff', fontSize: '2.8rem', marginBottom: 16 }}>
            {t.contactTitle}
          </h1>
          <p style={{ color: 'rgba(255,255,255,0.6)', fontSize: '1.1rem', lineHeight: 1.7, marginBottom: 40 }}>
            {t.contactDesc}
          </p>

          <div style={{
            background: 'rgba(255,255,255,0.06)', border: '1px solid rgba(201,168,76,0.2)',
            borderRadius: 20, padding: '40px 48px', display: 'inline-block',
            backdropFilter: 'blur(10px)',
          }}>
            <div style={{ fontSize: '2.5rem', marginBottom: 16 }}>✉️</div>
            <p style={{ color: 'rgba(255,255,255,0.6)', fontSize: '0.9rem', marginBottom: 12, textTransform: 'uppercase', letterSpacing: '0.08em' }}>
              {t.emailUs}
            </p>
            <a
              href={`mailto:${EMAIL}`}
              style={{
                color: '#C9A84C', fontSize: '1.15rem', fontWeight: 600,
                transition: 'opacity 0.2s',
              }}
              onMouseEnter={e => e.target.style.opacity = '0.75'}
              onMouseLeave={e => e.target.style.opacity = '1'}
            >
              {EMAIL}
            </a>
          </div>
        </div>
      </div>
    </div>
  );
}
