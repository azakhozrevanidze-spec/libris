import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { supabase } from '../supabaseClient';
import { useLanguage } from '../context/LanguageContext';

const EMAIL = process.env.REACT_APP_CONTACT_EMAIL || 'Libris.info.aza@gmail.com';
const PLACEHOLDER = 'https://images.unsplash.com/photo-1544947950-fa07a98d237f?w=400&q=80';

export default function BookDetail() {
  const { id } = useParams();
  const { lang, t } = useLanguage();
  const navigate = useNavigate();
  const [book, setBook] = useState(null);
  const [loading, setLoading] = useState(true);
  const [imgError, setImgError] = useState(false);

  useEffect(() => {
    supabase.from('books').select('*').eq('id', id).single()
      .then(({ data }) => { setBook(data); setLoading(false); });
  }, [id]);

  if (loading) return (
    <div style={{
      minHeight: '100vh', display: 'flex', alignItems: 'center', justifyContent: 'center',
      background: 'var(--cream)', paddingTop: 72,
    }}>
      <style>{`@keyframes spin { to { transform: rotate(360deg); } }`}</style>
      <div style={{ textAlign: 'center' }}>
        <div style={{
          width: 48, height: 48, border: '3px solid rgba(201,168,76,0.2)',
          borderTop: '3px solid #C9A84C', borderRadius: '50%',
          animation: 'spin 0.8s linear infinite', margin: '0 auto 16px',
        }} />
        <p style={{ color: '#718096', fontFamily: 'DM Sans, sans-serif' }}>
          {lang === 'ka' ? 'იტვირთება...' : 'Loading...'}
        </p>
      </div>
    </div>
  );

  if (!book) return (
    <div style={{ minHeight: '100vh', display: 'flex', alignItems: 'center', justifyContent: 'center', paddingTop: 72 }}>
      <div style={{ textAlign: 'center' }}>
        <p style={{ fontSize: '1.2rem', color: '#718096' }}>წიგნი ვერ მოიძებნა</p>
        <button onClick={() => navigate('/catalog')} className="btn-primary" style={{ marginTop: 20 }}>
          ← {t.catalog}
        </button>
      </div>
    </div>
  );

  const title = lang === 'ka' ? (book.title_ka || book.title_en) : (book.title_en || book.title_ka);
  const desc = lang === 'ka' ? (book.description_ka || book.description_en) : (book.description_en || book.description_ka);

  const handleBuy = () => {
    const subject = encodeURIComponent(`Purchase Request: ${book.title_en}`);
    const body = encodeURIComponent(`Hello, I would like to purchase the book "${book.title_en}".`);
    window.location.href = `mailto:${EMAIL}?subject=${subject}&body=${body}`;
  };

  return (
    <div style={{ minHeight: '100vh', background: 'var(--cream)', paddingTop: 72 }}>
      <style>{`@keyframes spin { to { transform: rotate(360deg); } }`}</style>

      {/* Hero */}
      <div style={{
        background: 'linear-gradient(135deg, #0A1628 0%, #132240 100%)',
        padding: '60px 5%',
        position: 'relative', overflow: 'hidden',
      }}>
        <div style={{
          position: 'absolute', top: -100, right: -100, width: 400, height: 400,
          borderRadius: '50%', border: '1px solid rgba(201,168,76,0.08)', pointerEvents: 'none',
        }} />

        <div style={{ maxWidth: 1100, margin: '0 auto' }}>
          {/* Back button */}
          <button
            onClick={() => navigate(-1)}
            style={{
              background: 'rgba(255,255,255,0.08)', border: '1px solid rgba(255,255,255,0.15)',
              color: 'rgba(255,255,255,0.7)', padding: '8px 18px', borderRadius: 8,
              cursor: 'pointer', fontSize: '0.85rem', marginBottom: 40,
              display: 'flex', alignItems: 'center', gap: 6, transition: 'all 0.2s',
            }}
            onMouseEnter={e => e.currentTarget.style.background = 'rgba(255,255,255,0.15)'}
            onMouseLeave={e => e.currentTarget.style.background = 'rgba(255,255,255,0.08)'}
          >
            ← {lang === 'ka' ? 'უკან' : 'Back'}
          </button>

          <div style={{ display: 'grid', gridTemplateColumns: 'auto 1fr', gap: 60, alignItems: 'start' }}>
            {/* Cover */}
            <div style={{ flexShrink: 0 }}>
              <div style={{
                width: 220, borderRadius: 16, overflow: 'hidden',
                boxShadow: '0 30px 80px rgba(0,0,0,0.5)',
                border: '1px solid rgba(201,168,76,0.2)',
              }}>
                <img
                  src={imgError ? PLACEHOLDER : (book.cover_url || PLACEHOLDER)}
                  alt={title}
                  onError={() => setImgError(true)}
                  style={{ width: '100%', display: 'block', aspectRatio: '2/3', objectFit: 'cover' }}
                />
              </div>
            </div>

            {/* Info */}
            <div>
              <div style={{ display: 'flex', alignItems: 'center', gap: 12, marginBottom: 16, flexWrap: 'wrap' }}>
                <span className={book.is_free ? 'badge-free' : 'badge-paid'}>
                  {book.is_free ? t.free : t.paid}
                </span>
                <span style={{
                  background: 'rgba(201,168,76,0.12)', color: '#C9A84C',
                  border: '1px solid rgba(201,168,76,0.25)',
                  padding: '3px 12px', borderRadius: 20,
                  fontSize: '0.72rem', fontWeight: 600, letterSpacing: '0.06em', textTransform: 'uppercase',
                }}>
                  {book.category}
                </span>
              </div>

              <h1 style={{
                fontFamily: 'Playfair Display, serif', color: '#fff',
                fontSize: 'clamp(1.8rem, 3.5vw, 2.8rem)', lineHeight: 1.2,
                marginBottom: 8, fontWeight: 700,
              }}>
                {title}
              </h1>

              {book.author && (
                <p style={{ color: '#C9A84C', fontSize: '1rem', marginBottom: 24, fontWeight: 500 }}>
                  {t.by} {book.author}
                </p>
              )}

              {!book.is_free && book.price > 0 && (
                <div style={{
                  display: 'inline-block', background: 'rgba(201,168,76,0.12)',
                  border: '1px solid rgba(201,168,76,0.3)', borderRadius: 10,
                  padding: '8px 20px', marginBottom: 28,
                }}>
                  <span style={{ color: '#C9A84C', fontSize: '1.4rem', fontWeight: 700 }}>₾{book.price}</span>
                </div>
              )}

              {/* Action buttons */}
              <div style={{ display: 'flex', gap: 14, flexWrap: 'wrap', marginTop: 8 }}>
                {book.is_free ? (
                  book.pdf_url ? (
                    <a
                      href={book.pdf_url}
                      download
                      target="_blank"
                      rel="noopener noreferrer"
                      className="btn-primary"
                      style={{ fontSize: '1rem', padding: '14px 32px' }}
                    >
                      ⬇ {t.download}
                    </a>
                  ) : (
                    <div style={{
                      padding: '14px 32px', borderRadius: 8,
                      background: 'rgba(255,255,255,0.06)',
                      border: '1px solid rgba(255,255,255,0.1)',
                      color: 'rgba(255,255,255,0.4)', fontSize: '0.9rem',
                      display: 'flex', alignItems: 'center', gap: 10,
                    }}>
                      <div style={{
                        width: 16, height: 16, border: '2px solid rgba(201,168,76,0.3)',
                        borderTop: '2px solid #C9A84C', borderRadius: '50%',
                        animation: 'spin 0.8s linear infinite', flexShrink: 0,
                      }} />
                      {lang === 'ka' ? 'PDF იტვირთება...' : 'PDF uploading...'}
                    </div>
                  )
                ) : (
                  <button
                    onClick={handleBuy}
                    className="btn-primary"
                    style={{ fontSize: '1rem', padding: '14px 32px' }}
                  >
                    🛒 {t.buyNow}
                  </button>
                )}

                <button
                  onClick={() => navigate('/catalog')}
                  className="btn-outline"
                  style={{ fontSize: '1rem', padding: '14px 28px' }}
                >
                  {t.catalog}
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Description */}
      {desc && (
        <div style={{ maxWidth: 1100, margin: '0 auto', padding: '60px 5%' }}>
          <div style={{
            background: '#fff', borderRadius: 20, padding: '40px 48px',
            boxShadow: '0 4px 30px rgba(10,22,40,0.07)',
            border: '1px solid rgba(201,168,76,0.1)',
          }}>
            <h2 style={{
              fontFamily: 'Playfair Display, serif', fontSize: '1.4rem',
              color: '#0A1628', marginBottom: 20,
              paddingBottom: 16, borderBottom: '2px solid rgba(201,168,76,0.15)',
            }}>
              {lang === 'ka' ? 'აღწერა' : 'Description'}
            </h2>
            <p style={{
              color: '#4A5568', lineHeight: 1.9, fontSize: '1rem',
              fontFamily: 'DM Sans, sans-serif',
            }}>
              {desc}
            </p>

            {book.description_en && book.description_ka && (
              <div style={{
                marginTop: 32, paddingTop: 24,
                borderTop: '1px solid rgba(201,168,76,0.1)',
                display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 32,
              }}>
                <div>
                  <p style={{ fontSize: '0.75rem', fontWeight: 700, color: '#C9A84C', letterSpacing: '0.08em', textTransform: 'uppercase', marginBottom: 10 }}>
                    English
                  </p>
                  <p style={{ color: '#718096', lineHeight: 1.7, fontSize: '0.9rem' }}>{book.description_en}</p>
                </div>
                <div>
                  <p style={{ fontSize: '0.75rem', fontWeight: 700, color: '#C9A84C', letterSpacing: '0.08em', textTransform: 'uppercase', marginBottom: 10 }}>
                    ქართული
                  </p>
                  <p style={{ color: '#718096', lineHeight: 1.7, fontSize: '0.9rem' }}>{book.description_ka}</p>
                </div>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
