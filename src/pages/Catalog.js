import React, { useEffect, useState } from 'react';
import { supabase } from '../supabaseClient';
import { useLanguage } from '../context/LanguageContext';
import BookCard from '../components/BookCard';

export default function Catalog() {
  const { lang, t } = useLanguage();
  const [books, setBooks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');
  const [category, setCategory] = useState('');

  const catKeys = {
    en: ['All', 'Fantasy', 'Detective', 'Romance', 'Cooking', 'History', 'Science', 'Poetry', 'Children'],
    ka: ['ყველა', 'ფენტეზი', 'დეტექტივი', 'რომანტიკა', 'კულინარია', 'ისტორია', 'მეცნიერება', 'პოეზია', 'ბავშვური'],
  };
  const dbCats = ['', 'Fantasy', 'Detective', 'Romance', 'Cooking', 'History', 'Science', 'Poetry', 'Children'];

  useEffect(() => {
    setLoading(true);
    let q = supabase.from('books').select('*').order('created_at', { ascending: false });
    if (category) q = q.eq('category', category);
    q.then(({ data }) => { setBooks(data || []); setLoading(false); });
  }, [category]);

  const filtered = books.filter(b => {
    const q = search.toLowerCase();
    return (b.title_en || '').toLowerCase().includes(q) ||
      (b.title_ka || '').toLowerCase().includes(q) ||
      (b.author || '').toLowerCase().includes(q);
  });

  return (
    <div style={{ paddingTop: 72, minHeight: '100vh', background: 'var(--cream)' }}>
      {/* Header */}
      <div style={{ background: '#0A1628', padding: '60px 5% 50px' }}>
        <div style={{ maxWidth: 1200, margin: '0 auto' }}>
          <h1 style={{ fontFamily: 'Playfair Display, serif', color: '#fff', fontSize: '2.5rem', marginBottom: 8 }}>
            {t.catalog}
          </h1>
          <p style={{ color: 'rgba(255,255,255,0.55)', marginBottom: 32 }}>{t.tagline}</p>
          {/* Search */}
          <div style={{ position: 'relative', maxWidth: 520 }}>
            <span style={{ position: 'absolute', left: 16, top: '50%', transform: 'translateY(-50%)', color: '#C9A84C', fontSize: '1.1rem' }}>🔍</span>
            <input
              type="text"
              placeholder={t.search}
              value={search}
              onChange={e => setSearch(e.target.value)}
              style={{
                width: '100%', padding: '14px 16px 14px 46px',
                borderRadius: 12, border: '1px solid rgba(201,168,76,0.3)',
                background: 'rgba(255,255,255,0.08)', color: '#fff',
                fontSize: '0.95rem', outline: 'none',
                backdropFilter: 'blur(10px)',
              }}
            />
          </div>
        </div>
      </div>

      <div style={{ maxWidth: 1200, margin: '0 auto', padding: '40px 5%' }}>
        {/* Category filters */}
        <div style={{ display: 'flex', flexWrap: 'wrap', gap: 10, marginBottom: 40 }}>
          {catKeys[lang].map((label, i) => (
            <button key={i} onClick={() => setCategory(dbCats[i])} style={{
              padding: '8px 18px', borderRadius: 30, border: '1.5px solid',
              borderColor: category === dbCats[i] ? '#C9A84C' : 'rgba(201,168,76,0.2)',
              background: category === dbCats[i] ? '#C9A84C' : 'transparent',
              color: category === dbCats[i] ? '#0A1628' : '#4A5568',
              fontWeight: 600, fontSize: '0.85rem', cursor: 'pointer', transition: 'all 0.2s',
            }}>
              {label}
            </button>
          ))}
        </div>

        {/* Grid */}
        {loading ? (
          <div style={{ textAlign: 'center', padding: 80, color: '#718096' }}>Loading...</div>
        ) : filtered.length === 0 ? (
          <div style={{ textAlign: 'center', padding: 80, color: '#718096' }}>{t.noBooks}</div>
        ) : (
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(200px, 1fr))', gap: 24 }}>
            {filtered.map(b => <BookCard key={b.id} book={b} />)}
          </div>
        )}
      </div>
    </div>
  );
}
