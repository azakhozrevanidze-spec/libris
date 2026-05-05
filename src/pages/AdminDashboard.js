import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { supabase } from '../supabaseClient';
import { uploadToCloudinary } from '../cloudinary';
import { useLanguage } from '../context/LanguageContext';

const CATEGORIES = ['Fantasy', 'Detective', 'Romance', 'Cooking', 'History', 'Science', 'Poetry', 'Children', 'Other'];
const EMPTY_FORM = { title_en: '', title_ka: '', description_en: '', description_ka: '', category: 'Fantasy', author: '', price: '', is_free: true };

export default function AdminDashboard() {
  const { t } = useLanguage();
  const navigate = useNavigate();
  const [books, setBooks] = useState([]);
  const [form, setForm] = useState(EMPTY_FORM);
  const [editId, setEditId] = useState(null);
  const [coverFile, setCoverFile] = useState(null);
  const [pdfFile, setPdfFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [msg, setMsg] = useState('');
  const [tab, setTab] = useState('add');

  useEffect(() => {
    checkAuth();
    fetchBooks();
  }, []);

  const checkAuth = async () => {
    const { data: { user } } = await supabase.auth.getUser();
    if (!user) navigate('/admin');
  };

  const fetchBooks = async () => {
    const { data } = await supabase.from('books').select('*').order('created_at', { ascending: false });
    setBooks(data || []);
  };

  const handleLogout = async () => {
    await supabase.auth.signOut();
    navigate('/admin');
  };

  const showMsg = (m) => { setMsg(m); setTimeout(() => setMsg(''), 3000); };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      let payload = { ...form, price: form.is_free ? 0 : parseFloat(form.price) || 0 };

      if (coverFile) {
        const res = await uploadToCloudinary(coverFile, 'covers');
        payload.cover_url = res.secure_url;
        payload.cloudinary_cover_id = res.public_id;
      }
      if (pdfFile) {
        const res = await uploadToCloudinary(pdfFile, 'pdfs');
        payload.pdf_url = res.secure_url;
        payload.cloudinary_pdf_id = res.public_id;
      }

      if (editId) {
        await supabase.from('books').update(payload).eq('id', editId);
        showMsg(t.bookUpdated);
        setEditId(null);
      } else {
        await supabase.from('books').insert(payload);
        showMsg(t.bookAdded);
      }

      setForm(EMPTY_FORM); setCoverFile(null); setPdfFile(null);
      fetchBooks(); setTab('manage');
    } catch (err) {
      showMsg(t.errorOccurred);
    }
    setLoading(false);
  };

  const handleEdit = (book) => {
    setForm({
      title_en: book.title_en || '', title_ka: book.title_ka || '',
      description_en: book.description_en || '', description_ka: book.description_ka || '',
      category: book.category || 'Fantasy', author: book.author || '',
      price: book.price || '', is_free: book.is_free,
    });
    setEditId(book.id); setTab('add');
    window.scrollTo(0, 0);
  };

  const handleDelete = async (id) => {
    if (!window.confirm(t.confirmDelete)) return;
    await supabase.from('books').delete().eq('id', id);
    showMsg(t.bookDeleted);
    fetchBooks();
  };

  const inputStyle = {
    width: '100%', padding: '11px 14px', borderRadius: 8,
    border: '1.5px solid rgba(201,168,76,0.2)', background: '#f8f7f4',
    fontSize: '0.9rem', color: '#1A1A2E', outline: 'none', boxSizing: 'border-box',
  };
  const labelStyle = { display: 'block', fontSize: '0.78rem', fontWeight: 600, color: '#4A5568', marginBottom: 6, textTransform: 'uppercase', letterSpacing: '0.04em' };
  const fieldStyle = { marginBottom: 16 };

  return (
    <div style={{ paddingTop: 72, minHeight: '100vh', background: '#f0ede8' }}>
      {/* Top bar */}
      <div style={{ background: '#0A1628', padding: '16px 5%', display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 16 }}>
          <img src="https://res.cloudinary.com/dompnhsjb/image/upload/v1777535945/ChatGPT_Image_Apr_30_2026_11_54_26_AM_oll6ka.png" alt="Libris" style={{ height: 36, borderRadius: 6 }} />
          <span style={{ color: '#fff', fontFamily: 'Playfair Display, serif', fontSize: '1.1rem' }}>{t.dashboard}</span>
        </div>
        <button onClick={handleLogout} className="btn-outline" style={{ fontSize: '0.8rem', padding: '8px 18px' }}>
          {t.logout}
        </button>
      </div>

      {/* Tabs */}
      <div style={{ background: '#fff', borderBottom: '1px solid rgba(201,168,76,0.15)', padding: '0 5%' }}>
        <div style={{ maxWidth: 1100, margin: '0 auto', display: 'flex', gap: 0 }}>
          {[{ key: 'add', label: editId ? '✏ Edit Book' : `+ ${t.addBook}` }, { key: 'manage', label: `📚 ${t.manageBooks} (${books.length})` }].map(tb => (
            <button key={tb.key} onClick={() => setTab(tb.key)} style={{
              padding: '18px 28px', border: 'none', background: 'transparent', cursor: 'pointer',
              fontWeight: 600, fontSize: '0.88rem', transition: 'all 0.2s',
              borderBottom: tab === tb.key ? '3px solid #C9A84C' : '3px solid transparent',
              color: tab === tb.key ? '#0A1628' : '#718096',
            }}>
              {tb.label}
            </button>
          ))}
        </div>
      </div>

      {msg && (
        <div style={{ background: '#D1FAE5', border: '1px solid #6EE7B7', padding: '12px 5%', color: '#065F46', fontWeight: 500, fontSize: '0.9rem' }}>
          ✓ {msg}
        </div>
      )}

      <div style={{ maxWidth: 1100, margin: '0 auto', padding: '40px 5%' }}>
        {/* ADD / EDIT TAB */}
        {tab === 'add' && (
          <div style={{ background: '#fff', borderRadius: 20, padding: '40px', boxShadow: '0 4px 30px rgba(10,22,40,0.07)', border: '1px solid rgba(201,168,76,0.1)' }}>
            <h2 style={{ fontFamily: 'Playfair Display, serif', fontSize: '1.6rem', marginBottom: 32, color: '#0A1628' }}>
              {editId ? `✏ ${t.edit}` : t.addBook}
            </h2>
            <form onSubmit={handleSubmit}>
              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 20 }}>
                <div style={fieldStyle}>
                  <label style={labelStyle}>{t.titleEn}</label>
                  <input style={inputStyle} value={form.title_en} onChange={e => setForm({...form, title_en: e.target.value})} required />
                </div>
                <div style={fieldStyle}>
                  <label style={labelStyle}>{t.titleKa}</label>
                  <input style={inputStyle} value={form.title_ka} onChange={e => setForm({...form, title_ka: e.target.value})} required />
                </div>
                <div style={fieldStyle}>
                  <label style={labelStyle}>{t.descEn}</label>
                  <textarea rows={3} style={{...inputStyle, resize: 'vertical'}} value={form.description_en} onChange={e => setForm({...form, description_en: e.target.value})} />
                </div>
                <div style={fieldStyle}>
                  <label style={labelStyle}>{t.descKa}</label>
                  <textarea rows={3} style={{...inputStyle, resize: 'vertical'}} value={form.description_ka} onChange={e => setForm({...form, description_ka: e.target.value})} />
                </div>
                <div style={fieldStyle}>
                  <label style={labelStyle}>{t.author}</label>
                  <input style={inputStyle} value={form.author} onChange={e => setForm({...form, author: e.target.value})} />
                </div>
                <div style={fieldStyle}>
                  <label style={labelStyle}>{t.category}</label>
                  <select style={inputStyle} value={form.category} onChange={e => setForm({...form, category: e.target.value})}>
                    {CATEGORIES.map(c => <option key={c} value={c}>{c}</option>)}
                  </select>
                </div>
              </div>

              {/* Free/Paid Toggle */}
              <div style={{ background: '#f8f7f4', borderRadius: 12, padding: '20px', marginBottom: 20, border: '1px solid rgba(201,168,76,0.15)', display: 'flex', alignItems: 'center', gap: 20, flexWrap: 'wrap' }}>
                <div>
                  <p style={{ fontWeight: 700, marginBottom: 4, color: '#0A1628' }}>Monetization</p>
                  <p style={{ fontSize: '0.82rem', color: '#718096' }}>Toggle between free download or paid purchase</p>
                </div>
                <div style={{ display: 'flex', gap: 12, marginLeft: 'auto' }}>
                  <button type="button" onClick={() => setForm({...form, is_free: true})} style={{
                    padding: '10px 24px', borderRadius: 8, border: '2px solid',
                    borderColor: form.is_free ? '#059669' : 'rgba(201,168,76,0.2)',
                    background: form.is_free ? 'rgba(52,211,153,0.1)' : 'transparent',
                    color: form.is_free ? '#059669' : '#718096', fontWeight: 700, cursor: 'pointer', transition: 'all 0.2s',
                  }}>✓ Free</button>
                  <button type="button" onClick={() => setForm({...form, is_free: false})} style={{
                    padding: '10px 24px', borderRadius: 8, border: '2px solid',
                    borderColor: !form.is_free ? '#C9A84C' : 'rgba(201,168,76,0.2)',
                    background: !form.is_free ? 'rgba(201,168,76,0.1)' : 'transparent',
                    color: !form.is_free ? '#92700A' : '#718096', fontWeight: 700, cursor: 'pointer', transition: 'all 0.2s',
                  }}>$ Paid</button>
                </div>
                {!form.is_free && (
                  <div style={{ width: '100%' }}>
                    <label style={labelStyle}>{t.price}</label>
                    <input type="number" step="0.01" min="0" style={{...inputStyle, maxWidth: 180}}
                      value={form.price} onChange={e => setForm({...form, price: e.target.value})} />
                  </div>
                )}
              </div>

              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 20, marginBottom: 28 }}>
                <div style={fieldStyle}>
                  <label style={labelStyle}>{t.coverImage}</label>
                  <input type="file" accept="image/*" onChange={e => setCoverFile(e.target.files[0])} style={{ ...inputStyle, padding: '8px' }} />
                </div>
                <div style={fieldStyle}>
                  <label style={labelStyle}>{t.pdfFile}</label>
                  <input type="file" accept=".pdf" onChange={e => setPdfFile(e.target.files[0])} style={{ ...inputStyle, padding: '8px' }} />
                </div>
              </div>

              <div style={{ display: 'flex', gap: 12 }}>
                <button type="submit" className="btn-primary" disabled={loading} style={{ padding: '13px 32px', fontSize: '0.95rem' }}>
                  {loading ? t.uploading : t.save}
                </button>
                {editId && (
                  <button type="button" className="btn-outline" onClick={() => { setEditId(null); setForm(EMPTY_FORM); setTab('manage'); }}>
                    Cancel
                  </button>
                )}
              </div>
            </form>
          </div>
        )}

        {/* MANAGE TAB */}
        {tab === 'manage' && (
          <div>
            <h2 style={{ fontFamily: 'Playfair Display, serif', fontSize: '1.6rem', marginBottom: 28, color: '#0A1628' }}>
              {t.manageBooks}
            </h2>
            <div style={{ display: 'grid', gap: 16 }}>
              {books.map(book => (
                <div key={book.id} style={{
                  background: '#fff', borderRadius: 14, padding: '20px 24px',
                  display: 'flex', alignItems: 'center', gap: 20,
                  boxShadow: '0 2px 12px rgba(10,22,40,0.06)',
                  border: '1px solid rgba(201,168,76,0.1)',
                }}>
                  {book.cover_url && (
                    <img src={book.cover_url} alt={book.title_en}
                      style={{ width: 56, height: 72, objectFit: 'cover', borderRadius: 8, flexShrink: 0 }} />
                  )}
                  <div style={{ flex: 1, minWidth: 0 }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: 10, marginBottom: 4, flexWrap: 'wrap' }}>
                      <h3 style={{ fontFamily: 'Playfair Display, serif', fontSize: '1rem', color: '#0A1628' }}>
                        {book.title_en}
                      </h3>
                      <span className={book.is_free ? 'badge-free' : 'badge-paid'}>
                        {book.is_free ? 'Free' : `Paid · ₾${book.price}`}
                      </span>
                    </div>
                    <p style={{ fontSize: '0.8rem', color: '#718096' }}>{book.title_ka} · {book.category}{book.author ? ` · ${book.author}` : ''}</p>
                  </div>
                  <div style={{ display: 'flex', gap: 10, flexShrink: 0 }}>
                    <button onClick={() => handleEdit(book)} className="btn-outline" style={{ padding: '8px 16px', fontSize: '0.82rem' }}>
                      ✏ {t.edit}
                    </button>
                    <button onClick={() => handleDelete(book.id)} style={{
                      padding: '8px 16px', borderRadius: 8, border: '1.5px solid #FECACA',
                      background: 'transparent', color: '#DC2626', fontWeight: 600,
                      fontSize: '0.82rem', cursor: 'pointer', transition: 'all 0.2s',
                    }}
                      onMouseEnter={e => { e.target.style.background = '#FEE2E2'; }}
                      onMouseLeave={e => { e.target.style.background = 'transparent'; }}
                    >
                      🗑 {t.delete}
                    </button>
                  </div>
                </div>
              ))}
              {books.length === 0 && (
                <div style={{ textAlign: 'center', padding: 60, color: '#718096' }}>No books yet. Add your first book!</div>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
