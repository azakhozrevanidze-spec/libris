import React, { useState } from 'react';
import { useLanguage } from '../context/LanguageContext';

const EMAIL = process.env.REACT_APP_CONTACT_EMAIL || 'Libris.info.aza@gmail.com';
const PLACEHOLDER = 'https://images.unsplash.com/photo-1544947950-fa07a98d237f?w=400&q=80';

export default function BookCard({ book }) {
  const { lang, t } = useLanguage();
  const [imgError, setImgError] = useState(false);
  const [hovered, setHovered] = useState(false);

  const title = lang === 'ka' ? (book.title_ka || book.title_en) : (book.title_en || book.title_ka);
  const desc = lang === 'ka' ? (book.description_ka || book.description_en) : (book.description_en || book.description_ka);

  const handleBuy = () => {
    const subject = encodeURIComponent(`Purchase Request: ${book.title_en}`);
    window.location.href = `mailto:${EMAIL}?subject=${subject}&body=Hello%2C%20I%20would%20like%20to%20purchase%20the%20book%20%22${encodeURIComponent(book.title_en)}%22.`;
  };

  return (
    <div
      onMouseEnter={() => setHovered(true)}
      onMouseLeave={() => setHovered(false)}
      style={{
        background: '#fff',
        borderRadius: 16,
        overflow: 'hidden',
        boxShadow: hovered ? '0 20px 60px rgba(10,22,40,0.15)' : '0 4px 20px rgba(10,22,40,0.07)',
        transition: 'all 0.35s cubic-bezier(0.34,1.56,0.64,1)',
        transform: hovered ? 'translateY(-8px)' : 'translateY(0)',
        border: '1px solid rgba(201,168,76,0.12)',
        display: 'flex',
        flexDirection: 'column',
      }}
    >
      {/* Cover */}
      <div style={{ position: 'relative', paddingTop: '140%', overflow: 'hidden' }}>
        <img
          src={imgError ? PLACEHOLDER : (book.cover_url || PLACEHOLDER)}
          alt={title}
          onError={() => setImgError(true)}
          style={{
            position: 'absolute', top: 0, left: 0, width: '100%', height: '100%',
            objectFit: 'cover',
            transition: 'transform 0.5s ease',
            transform: hovered ? 'scale(1.06)' : 'scale(1)',
          }}
        />
        {/* Badge overlay */}
        <div style={{ position: 'absolute', top: 12, left: 12 }}>
          <span className={book.is_free ? 'badge-free' : 'badge-paid'}>
            {book.is_free ? t.free : t.paid}
          </span>
        </div>
        {/* Category */}
        <div style={{
          position: 'absolute', bottom: 0, left: 0, right: 0,
          background: 'linear-gradient(to top, rgba(10,22,40,0.85), transparent)',
          padding: '30px 12px 12px',
        }}>
          <span style={{ color: '#C9A84C', fontSize: '0.72rem', fontWeight: 600, letterSpacing: '0.08em', textTransform: 'uppercase' }}>
            {book.category}
          </span>
        </div>
      </div>

      {/* Content */}
      <div style={{ padding: '16px', flex: 1, display: 'flex', flexDirection: 'column' }}>
        <h3 style={{
          fontFamily: 'Playfair Display, serif', fontSize: '1rem',
          fontWeight: 700, lineHeight: 1.35, color: '#0A1628',
          marginBottom: 6, display: '-webkit-box', WebkitLineClamp: 2,
          WebkitBoxOrient: 'vertical', overflow: 'hidden',
        }}>{title}</h3>

        {book.author && (
          <p style={{ fontSize: '0.78rem', color: '#718096', marginBottom: 8 }}>
            {t.by} {book.author}
          </p>
        )}

        {desc && (
          <p style={{
            fontSize: '0.82rem', color: '#4A5568', lineHeight: 1.6,
            display: '-webkit-box', WebkitLineClamp: 3, WebkitBoxOrient: 'vertical',
            overflow: 'hidden', flex: 1, marginBottom: 12,
          }}>{desc}</p>
        )}

        <div style={{ marginTop: 'auto', paddingTop: 12, borderTop: '1px solid rgba(201,168,76,0.1)' }}>
          {book.is_free ? (
            <a
              href={book.pdf_url || '#'}
              target="_blank"
              rel="noopener noreferrer"
              className="btn-primary"
              style={{ width: '100%', justifyContent: 'center' }}
            >
              ⬇ {t.download}
            </a>
          ) : (
            <button
              onClick={handleBuy}
              className="btn-primary"
              style={{ width: '100%', justifyContent: 'center' }}
            >
              🛒 {t.buyNow} {book.price ? `· ₾${book.price}` : ''}
            </button>
          )}
        </div>
      </div>
    </div>
  );
}
