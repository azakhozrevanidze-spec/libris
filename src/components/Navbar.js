import React, { useState, useEffect } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { useLanguage } from '../context/LanguageContext';

export default function Navbar() {
  const { lang, setLang, t } = useLanguage();
  const [scrolled, setScrolled] = useState(false);
  const [menuOpen, setMenuOpen] = useState(false);
  const location = useLocation();

  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 20);
    window.addEventListener('scroll', onScroll);
    return () => window.removeEventListener('scroll', onScroll);
  }, []);

  const navStyle = {
    position: 'fixed', top: 0, left: 0, right: 0, zIndex: 1000,
    background: scrolled ? 'rgba(10,22,40,0.97)' : 'rgba(10,22,40,0.85)',
    backdropFilter: 'blur(16px)',
    borderBottom: scrolled ? '1px solid rgba(201,168,76,0.25)' : '1px solid transparent',
    transition: 'all 0.3s ease',
    padding: '0 5%',
  };

  const links = [
    { to: '/', label: t.home },
    { to: '/catalog', label: t.catalog },
    { to: '/contact', label: t.contact },
  ];

  const isActive = (path) => location.pathname === path;

  return (
    <nav style={navStyle}>
      <div style={{ maxWidth: 1200, margin: '0 auto', display: 'flex', alignItems: 'center', justifyContent: 'space-between', height: 72 }}>
        {/* Logo */}
        <Link to="/" style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
          <img
            src="https://res.cloudinary.com/dompnhsjb/image/upload/v1777535945/ChatGPT_Image_Apr_30_2026_11_54_26_AM_oll6ka.png"
            alt="Libris"
            style={{ height: 44, width: 44, objectFit: 'contain', borderRadius: 8 }}
          />
          <span style={{ fontFamily: 'Playfair Display, serif', fontSize: '1.4rem', color: '#fff', fontWeight: 700, letterSpacing: '0.02em' }}>
            Libris
          </span>
        </Link>

        {/* Desktop Nav */}
        <div style={{ display: 'flex', alignItems: 'center', gap: 32 }} className="desktop-nav">
          {links.map(l => (
            <Link key={l.to} to={l.to} style={{
              color: isActive(l.to) ? '#C9A84C' : 'rgba(255,255,255,0.75)',
              fontWeight: 500, fontSize: '0.9rem', letterSpacing: '0.02em',
              transition: 'color 0.2s', padding: '4px 0',
              borderBottom: isActive(l.to) ? '2px solid #C9A84C' : '2px solid transparent',
            }}>
              {l.label}
            </Link>
          ))}
        </div>

        {/* Right side */}
        <div style={{ display: 'flex', alignItems: 'center', gap: 16 }}>
          {/* Language Toggle */}
          <div style={{
            display: 'flex', background: 'rgba(255,255,255,0.08)', borderRadius: 8,
            padding: 3, border: '1px solid rgba(201,168,76,0.2)'
          }}>
            {['en', 'ka'].map(l => (
              <button key={l} onClick={() => setLang(l)} style={{
                padding: '5px 12px', borderRadius: 6, border: 'none', cursor: 'pointer',
                background: lang === l ? '#C9A84C' : 'transparent',
                color: lang === l ? '#0A1628' : 'rgba(255,255,255,0.6)',
                fontWeight: 600, fontSize: '0.78rem', letterSpacing: '0.05em',
                textTransform: 'uppercase', transition: 'all 0.2s',
              }}>
                {l}
              </button>
            ))}
          </div>

          <Link to="/admin" style={{
            color: 'rgba(255,255,255,0.5)', fontSize: '0.8rem', fontWeight: 500,
            letterSpacing: '0.05em', textTransform: 'uppercase', transition: 'color 0.2s',
          }}
            onMouseEnter={e => e.target.style.color = '#C9A84C'}
            onMouseLeave={e => e.target.style.color = 'rgba(255,255,255,0.5)'}
          >
            {t.admin}
          </Link>
        </div>
      </div>
    </nav>
  );
}
