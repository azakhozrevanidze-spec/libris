import React from 'react';
import { Link } from 'react-router-dom';
import { useLanguage } from '../context/LanguageContext';

const EMAIL = process.env.REACT_APP_CONTACT_EMAIL || 'Libris.info.aza@gmail.com';

export default function Footer() {
  const { t } = useLanguage();
  return (
    <footer style={{
      background: '#0A1628',
      borderTop: '1px solid rgba(201,168,76,0.15)',
      padding: '60px 5% 32px',
      color: 'rgba(255,255,255,0.65)',
    }}>
      <div style={{ maxWidth: 1200, margin: '0 auto' }}>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))', gap: 48, marginBottom: 48 }}>
          {/* Brand */}
          <div>
            <div style={{ display: 'flex', alignItems: 'center', gap: 10, marginBottom: 16 }}>
              <img
                src="https://res.cloudinary.com/dompnhsjb/image/upload/v1777535945/ChatGPT_Image_Apr_30_2026_11_54_26_AM_oll6ka.png"
                alt="Libris"
                style={{ height: 36, width: 36, objectFit: 'contain', borderRadius: 6 }}
              />
              <span style={{ fontFamily: 'Playfair Display, serif', color: '#fff', fontSize: '1.2rem', fontWeight: 700 }}>
                Libris
              </span>
            </div>
            <p style={{ fontSize: '0.875rem', lineHeight: 1.7 }}>{t.footerDesc}</p>
          </div>

          {/* Links */}
          <div>
            <h4 style={{ color: '#C9A84C', fontFamily: 'Playfair Display, serif', marginBottom: 16, fontSize: '1rem' }}>
              {t.footerLinks}
            </h4>
            {[{ to: '/', label: t.home }, { to: '/catalog', label: t.catalog }, { to: '/contact', label: t.contact }].map(l => (
              <div key={l.to} style={{ marginBottom: 10 }}>
                <Link to={l.to} style={{ color: 'rgba(255,255,255,0.6)', fontSize: '0.875rem', transition: 'color 0.2s' }}
                  onMouseEnter={e => e.target.style.color = '#C9A84C'}
                  onMouseLeave={e => e.target.style.color = 'rgba(255,255,255,0.6)'}
                >{l.label}</Link>
              </div>
            ))}
          </div>

          {/* Contact */}
          <div>
            <h4 style={{ color: '#C9A84C', fontFamily: 'Playfair Display, serif', marginBottom: 16, fontSize: '1rem' }}>
              {t.footerContact}
            </h4>
            <a href={`mailto:${EMAIL}`} style={{
              color: 'rgba(255,255,255,0.6)', fontSize: '0.875rem',
              display: 'flex', alignItems: 'center', gap: 8, transition: 'color 0.2s'
            }}
              onMouseEnter={e => e.target.style.color = '#C9A84C'}
              onMouseLeave={e => e.target.style.color = 'rgba(255,255,255,0.6)'}
            >
              ✉ {EMAIL}
            </a>
          </div>
        </div>

        <div style={{ borderTop: '1px solid rgba(255,255,255,0.08)', paddingTop: 24, textAlign: 'center', fontSize: '0.8rem' }}>
          {t.rights}
        </div>
      </div>
    </footer>
  );
}
