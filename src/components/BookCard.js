import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useLanguage } from '../context/LanguageContext';

const PLACEHOLDER = 'https://images.unsplash.com/photo-1544947950-fa07a98d237f?w=400&q=80';

export default function BookCard({ book }) {
  const { lang, t } = useLanguage();
  const [imgError, setImgError] = useState(false);
  const [hovered, setHovered] = useState(false);
  const navigate = useNavigate();

  const title = lang === 'ka' ? (book.title_ka || book.title_en) : (book.title_en || book.title_ka);

  return (
    <div
      onClick={() => navigate(`/book/${book.id}`)}
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
        cursor: 'pointer',
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
        <div style={{ position: 'absolute', top: 12, left: 12 }}>
          <span className={book.is_free ? 'badge-free' : 'badge-paid'}>
            {book.is_free ? t.free : t.paid}
          </span>
        </div>
        <div style={{
          position: 'absolute', bottom: 0, left: 0, right: 0,
          background: 'linear-gradient(to top, rgba(10,22,40,0.85), transparent)',
          padding: '30px 12px 12px',
        }}>
          <span style={{ color: '#C9A84C', fontSize: '0.72rem', fontWeight: 600, letterSpacing: '0.08em', textTransform: 'uppercase' }}>
            {book.category}
          </span>
        </div>

        {/* Hover overlay */}
        <div style={{
          position: 'absolute', top: 0, left: 0, right: 0, bottom: 0,
          background: 'rgba(10,22,40,0.4)',
          display: 'flex', alignItems: 'center', justifyContent: 'center',
          opacity: hovered ? 1 : 0,
          transition: 'opacity 0.3s ease',
        }}>
          <div style={{
            background: '#C9A84C', color: '#0A1628',
            padding: '10px 22px', borderRadius: 30,
            fontWeight: 700, fontSize: '0.85rem',
            transform: hovered ? 'scale(1)' : 'scale(0.8)',
            transition: 'transform 0.3s ease',
          }}>
            {lang === 'ka' ? 'დეტალები →' : 'View Details →'}
          </div>
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
          <p style={{ fontSize: '0.78rem', color: '#718096', marginBottom: 4 }}>
            {t.by} {book.author}
          </p>
        )}

        <div style={{ marginTop: 'auto', paddingTop: 10 }}>
          <span style={{
            fontSize: '0.8rem', color: book.is_free ? '#059669' : '#92700A', fontWeight: 600,
          }}>
            {book.is_free ? `⬇ ${t.download}` : `🛒 ${t.buyNow}${book.price ? ` · ₾${book.price}` : ''}`}
          </span>
        </div>
      </div>
    </div>
  );
}
