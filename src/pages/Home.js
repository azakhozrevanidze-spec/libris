import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { supabase } from '../supabaseClient';
import { useLanguage } from '../context/LanguageContext';
import BookCard from '../components/BookCard';

export default function Home() {
  const { t } = useLanguage();
  const [books, setBooks] = useState([]);

  useEffect(() => {
    supabase.from('books').select('*').order('created_at', { ascending: false }).limit(6)
      .then(({ data }) => setBooks(data || []));
  }, []);

  return (
    <div>
      {/* Hero */}
      <section style={{
        background: 'linear-gradient(135deg, #0A1628 0%, #132240 60%, #1a3060 100%)',
        minHeight: '92vh', display: 'flex', alignItems: 'center',
        padding: '100px 5% 60px',
        position: 'relative', overflow: 'hidden',
      }}>
        {/* Decorative circles */}
        <div style={{
          position: 'absolute', top: -80, right: -80, width: 500, height: 500,
          borderRadius: '50%', border: '1px solid rgba(201,168,76,0.1)',
          pointerEvents: 'none',
        }} />
        <div style={{
          position: 'absolute', top: 40, right: 40, width: 300, height: 300,
          borderRadius: '50%', border: '1px solid rgba(201,168,76,0.07)',
          pointerEvents: 'none',
        }} />
        <div style={{
          position: 'absolute', bottom: -100, left: -60, width: 400, height: 400,
          borderRadius: '50%', background: 'radial-gradient(circle, rgba(201,168,76,0.05) 0%, transparent 70%)',
          pointerEvents: 'none',
        }} />

        <div style={{ maxWidth: 1200, margin: '0 auto', width: '100%', display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 80, alignItems: 'center' }}>
          <div>
            <div style={{
              display: 'inline-block', background: 'rgba(201,168,76,0.12)',
              border: '1px solid rgba(201,168,76,0.25)', borderRadius: 30,
              padding: '6px 18px', marginBottom: 24,
              color: '#C9A84C', fontSize: '0.8rem', fontWeight: 600, letterSpacing: '0.08em',
            }}>
              📚 Georgian & English Library
            </div>
            <h1 style={{
              fontFamily: 'Playfair Display, serif', fontSize: 'clamp(2.2rem, 4vw, 3.5rem)',
              color: '#fff', lineHeight: 1.15, fontWeight: 700, marginBottom: 24,
            }}>
              {t.heroTitle}
            </h1>
            <p style={{ color: 'rgba(255,255,255,0.65)', fontSize: '1.1rem', lineHeight: 1.7, marginBottom: 40, maxWidth: 480 }}>
              {t.heroSub}
            </p>
            <Link to="/catalog" className="btn-primary" style={{ fontSize: '1rem', padding: '14px 32px' }}>
              {t.exploreCatalog} →
            </Link>
          </div>

          {/* Logo display */}
          <div style={{ display: 'flex', justifyContent: 'center' }}>
            <div style={{
              width: 280, height: 280, borderRadius: 32,
              background: 'rgba(255,255,255,0.05)',
              border: '1px solid rgba(201,168,76,0.2)',
              display: 'flex', alignItems: 'center', justifyContent: 'center',
              boxShadow: '0 40px 100px rgba(0,0,0,0.3)',
            }}>
              <img
                src="https://res.cloudinary.com/dompnhsjb/image/upload/v1777535945/ChatGPT_Image_Apr_30_2026_11_54_26_AM_oll6ka.png"
                alt="Libris"
                style={{ width: 200, height: 200, objectFit: 'contain', borderRadius: 16 }}
              />
            </div>
          </div>
        </div>
      </section>

      {/* Featured Books */}
      {books.length > 0 && (
        <section style={{ padding: '80px 5%', background: 'var(--cream)' }}>
          <div style={{ maxWidth: 1200, margin: '0 auto' }}>
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: 48 }}>
              <h2 style={{ fontFamily: 'Playfair Display, serif', fontSize: '2rem', color: '#0A1628' }}>
                Latest Books
              </h2>
              <Link to="/catalog" className="btn-outline">{t.catalog} →</Link>
            </div>
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(200px, 1fr))', gap: 24 }}>
              {books.map(b => <BookCard key={b.id} book={b} />)}
            </div>
          </div>
        </section>
      )}
    </div>
  );
}
