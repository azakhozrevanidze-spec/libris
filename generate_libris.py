#!/usr/bin/env python3
"""
Libris - Bilingual Digital Book Library
Automation script: Run this to generate the entire project structure.
Usage: python generate_libris.py
"""

import os

BASE = "libris"

FILES = {}

# ─────────────────────────────────────────
# SQL SCHEMA
# ─────────────────────────────────────────
FILES["libris_schema.sql"] = """-- Libris Database Schema
-- Run this in your Supabase SQL Editor

create extension if not exists "uuid-ossp";

create table if not exists books (
  id            uuid primary key default uuid_generate_v4(),
  title_en      text not null,
  title_ka      text not null,
  description_en text,
  description_ka text,
  category      text not null,
  author        text,
  price         numeric(10,2) default 0,
  is_free       boolean not null default true,
  cover_url     text,
  pdf_url       text,
  cloudinary_cover_id text,
  cloudinary_pdf_id   text,
  created_at    timestamptz default now(),
  updated_at    timestamptz default now()
);

-- Enable Row Level Security
alter table books enable row level security;

-- Public can read all books
create policy "Anyone can read books"
  on books for select using (true);

-- Only authenticated (admin) can insert/update/delete
create policy "Admin can insert books"
  on books for insert with check (auth.role() = 'authenticated');

create policy "Admin can update books"
  on books for update using (auth.role() = 'authenticated');

create policy "Admin can delete books"
  on books for delete using (auth.role() = 'authenticated');

-- Auto-update updated_at
create or replace function update_updated_at()
returns trigger as $$
begin
  new.updated_at = now();
  return new;
end;
$$ language plpgsql;

create trigger books_updated_at
  before update on books
  for each row execute procedure update_updated_at();
"""

# ─────────────────────────────────────────
# package.json
# ─────────────────────────────────────────
FILES["package.json"] = """{
  "name": "libris",
  "version": "1.0.0",
  "private": true,
  "dependencies": {
    "@supabase/supabase-js": "^2.39.0",
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-router-dom": "^6.21.0",
    "react-scripts": "5.0.1",
    "axios": "^1.6.2"
  },
  "scripts": {
    "start": "react-scripts start",
    "build": "react-scripts build"
  },
  "browserslist": {
    "production": [">0.2%", "not dead", "not op_mini all"],
    "development": ["last 1 chrome version", "last 1 firefox version", "last 1 safari version"]
  }
}
"""

# ─────────────────────────────────────────
# .env
# ─────────────────────────────────────────
FILES[".env"] = """REACT_APP_SUPABASE_URL=https://dkxcsvbqyczuibmcyeux.supabase.co
REACT_APP_SUPABASE_ANON_KEY=sb_publishable_vMA-sPJAAXgBAaScDBs7pQ_OjLKQ_C9
REACT_APP_CLOUDINARY_CLOUD_NAME=dompnhsjb
REACT_APP_CLOUDINARY_API_KEY=187416237257845
REACT_APP_CLOUDINARY_UPLOAD_PRESET=Libris
REACT_APP_CONTACT_EMAIL=Libris.info.aza@gmail.com
"""

# ─────────────────────────────────────────
# public/index.html
# ─────────────────────────────────────────
FILES["public/index.html"] = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <meta name="theme-color" content="#0A1628" />
  <meta name="description" content="Libris - Bilingual Digital Book Library" />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,600;0,700;1,400&family=DM+Sans:wght@300;400;500;600&display=swap" rel="stylesheet" />
  <title>Libris – Digital Book Library</title>
</head>
<body>
  <noscript>You need to enable JavaScript to run this app.</noscript>
  <div id="root"></div>
</body>
</html>
"""

# ─────────────────────────────────────────
# src/index.js
# ─────────────────────────────────────────
FILES["src/index.js"] = """import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(<React.StrictMode><App /></React.StrictMode>);
"""

# ─────────────────────────────────────────
# src/index.css
# ─────────────────────────────────────────
FILES["src/index.css"] = """:root {
  --deep-blue: #0A1628;
  --navy: #132240;
  --gold: #C9A84C;
  --gold-light: #E8C87A;
  --gold-pale: #F5E6C0;
  --cream: #FAF7F0;
  --text-primary: #1A1A2E;
  --text-secondary: #4A5568;
  --text-muted: #718096;
  --border: rgba(201,168,76,0.2);
  --glass: rgba(10,22,40,0.85);
}

* { box-sizing: border-box; margin: 0; padding: 0; }

body {
  font-family: 'DM Sans', sans-serif;
  background: var(--cream);
  color: var(--text-primary);
  min-height: 100vh;
}

h1, h2, h3 { font-family: 'Playfair Display', serif; }

a { text-decoration: none; color: inherit; }

::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: var(--cream); }
::-webkit-scrollbar-thumb { background: var(--gold); border-radius: 3px; }

.btn-primary {
  background: linear-gradient(135deg, var(--gold), var(--gold-light));
  color: var(--deep-blue);
  border: none;
  padding: 10px 22px;
  border-radius: 8px;
  font-family: 'DM Sans', sans-serif;
  font-weight: 600;
  font-size: 0.875rem;
  cursor: pointer;
  transition: all 0.25s ease;
  display: inline-flex;
  align-items: center;
  gap: 8px;
}
.btn-primary:hover { transform: translateY(-2px); box-shadow: 0 6px 20px rgba(201,168,76,0.35); }

.btn-outline {
  background: transparent;
  color: var(--gold);
  border: 1.5px solid var(--gold);
  padding: 10px 22px;
  border-radius: 8px;
  font-family: 'DM Sans', sans-serif;
  font-weight: 600;
  font-size: 0.875rem;
  cursor: pointer;
  transition: all 0.25s ease;
  display: inline-flex;
  align-items: center;
  gap: 8px;
}
.btn-outline:hover { background: var(--gold); color: var(--deep-blue); transform: translateY(-2px); }

.badge-free {
  background: rgba(52, 211, 153, 0.15);
  color: #059669;
  border: 1px solid rgba(52,211,153,0.3);
  padding: 3px 10px;
  border-radius: 20px;
  font-size: 0.72rem;
  font-weight: 600;
  letter-spacing: 0.05em;
  text-transform: uppercase;
}

.badge-paid {
  background: rgba(201,168,76,0.15);
  color: #92700A;
  border: 1px solid rgba(201,168,76,0.3);
  padding: 3px 10px;
  border-radius: 20px;
  font-size: 0.72rem;
  font-weight: 600;
  letter-spacing: 0.05em;
  text-transform: uppercase;
}
"""

# ─────────────────────────────────────────
# src/supabaseClient.js
# ─────────────────────────────────────────
FILES["src/supabaseClient.js"] = """import { createClient } from '@supabase/supabase-js';

const supabaseUrl = process.env.REACT_APP_SUPABASE_URL;
const supabaseAnonKey = process.env.REACT_APP_SUPABASE_ANON_KEY;

export const supabase = createClient(supabaseUrl, supabaseAnonKey);
"""

# ─────────────────────────────────────────
# src/cloudinary.js
# ─────────────────────────────────────────
FILES["src/cloudinary.js"] = """const CLOUD_NAME = process.env.REACT_APP_CLOUDINARY_CLOUD_NAME;
const UPLOAD_PRESET = process.env.REACT_APP_CLOUDINARY_UPLOAD_PRESET;

export async function uploadToCloudinary(file, folder) {
  const url = `https://api.cloudinary.com/v1_1/${CLOUD_NAME}/auto/upload`;
  const formData = new FormData();
  formData.append('file', file);
  formData.append('upload_preset', UPLOAD_PRESET);
  formData.append('folder', folder); // 'covers' or 'pdfs'

  const res = await fetch(url, { method: 'POST', body: formData });
  if (!res.ok) throw new Error('Cloudinary upload failed');
  return res.json(); // { secure_url, public_id, ... }
}
"""

# ─────────────────────────────────────────
# src/context/LanguageContext.js
# ─────────────────────────────────────────
FILES["src/context/LanguageContext.js"] = """import React, { createContext, useContext, useState } from 'react';

const LanguageContext = createContext();

export const translations = {
  en: {
    siteName: 'Libris',
    tagline: 'Your bilingual digital library',
    home: 'Home',
    catalog: 'Catalog',
    contact: 'Contact',
    admin: 'Admin',
    search: 'Search books...',
    allCategories: 'All Categories',
    free: 'Free',
    paid: 'Paid',
    download: 'Download PDF',
    buyNow: 'Buy Now',
    by: 'by',
    noBooks: 'No books found.',
    footerDesc: 'A curated bilingual library for Georgian and English readers.',
    footerLinks: 'Quick Links',
    footerContact: 'Contact',
    rights: '© 2024 Libris. All rights reserved.',
    contactTitle: 'Get in Touch',
    contactDesc: 'Have questions or want to purchase a book? Reach out to us.',
    emailUs: 'Email Us',
    categories: ['All', 'Fantasy', 'Detective', 'Romance', 'Cooking', 'History', 'Science', 'Poetry', 'Children'],
    adminLogin: 'Admin Login',
    email: 'Email',
    password: 'Password',
    signIn: 'Sign In',
    dashboard: 'Dashboard',
    addBook: 'Add New Book',
    manageBooks: 'Manage Books',
    titleEn: 'Title (English)',
    titleKa: 'Title (Georgian)',
    descEn: 'Description (English)',
    descKa: 'Description (Georgian)',
    category: 'Category',
    author: 'Author',
    price: 'Price (₾)',
    isFree: 'Free Book',
    coverImage: 'Cover Image',
    pdfFile: 'PDF File',
    save: 'Save Book',
    edit: 'Edit',
    delete: 'Delete',
    uploading: 'Uploading...',
    logout: 'Logout',
    confirmDelete: 'Are you sure you want to delete this book?',
    bookAdded: 'Book added successfully!',
    bookUpdated: 'Book updated successfully!',
    bookDeleted: 'Book deleted.',
    errorOccurred: 'An error occurred. Please try again.',
    heroTitle: 'Discover Stories in Two Languages',
    heroSub: 'Browse our curated collection of Georgian and English books — free and premium.',
    exploreCatalog: 'Explore Catalog',
  },
  ka: {
    siteName: 'ლიბრისი',
    tagline: 'თქვენი ორენოვანი ციფრული ბიბლიოთეკა',
    home: 'მთავარი',
    catalog: 'კატალოგი',
    contact: 'კონტაქტი',
    admin: 'ადმინი',
    search: 'წიგნების ძიება...',
    allCategories: 'ყველა კატეგორია',
    free: 'უფასო',
    paid: 'ფასიანი',
    download: 'PDF ჩამოტვირთვა',
    buyNow: 'ყიდვა',
    by: 'ავტორი',
    noBooks: 'წიგნები ვერ მოიძებნა.',
    footerDesc: 'შერჩეული ორენოვანი ბიბლიოთეკა ქართველი და ინგლისური მკითხველებისთვის.',
    footerLinks: 'სწრაფი ბმულები',
    footerContact: 'კონტაქტი',
    rights: '© 2024 ლიბრისი. ყველა უფლება დაცულია.',
    contactTitle: 'დაგვიკავშირდით',
    contactDesc: 'გაქვთ კითხვები ან გსურთ წიგნის შეძენა? დაგვიკავშირდით.',
    emailUs: 'გამოგვიგზავნე ელ-ფოსტა',
    categories: ['ყველა', 'ფენტეზი', 'დეტექტივი', 'რომანტიკა', 'კულინარია', 'ისტორია', 'მეცნიერება', 'პოეზია', 'ბავშვური'],
    adminLogin: 'ადმინ შესვლა',
    email: 'ელ-ფოსტა',
    password: 'პაროლი',
    signIn: 'შესვლა',
    dashboard: 'პანელი',
    addBook: 'წიგნის დამატება',
    manageBooks: 'წიგნების მართვა',
    titleEn: 'სათაური (ინგლისური)',
    titleKa: 'სათაური (ქართული)',
    descEn: 'აღწერა (ინგლისური)',
    descKa: 'აღწერა (ქართული)',
    category: 'კატეგორია',
    author: 'ავტორი',
    price: 'ფასი (₾)',
    isFree: 'უფასო წიგნი',
    coverImage: 'გარეკანი',
    pdfFile: 'PDF ფაილი',
    save: 'შენახვა',
    edit: 'რედაქტირება',
    delete: 'წაშლა',
    uploading: 'იტვირთება...',
    logout: 'გამოსვლა',
    confirmDelete: 'დარწმუნებული ხართ, რომ გსურთ ამ წიგნის წაშლა?',
    bookAdded: 'წიგნი წარმატებით დაემატა!',
    bookUpdated: 'წიგნი წარმატებით განახლდა!',
    bookDeleted: 'წიგნი წაიშალა.',
    errorOccurred: 'შეცდომა მოხდა. გთხოვთ სცადოთ კვლავ.',
    heroTitle: 'აღმოაჩინე ისტორიები ორ ენაზე',
    heroSub: 'დაათვალიერე ჩვენი ქართული და ინგლისური წიგნების კოლექცია — უფასო და პრემიუმ.',
    exploreCatalog: 'კატალოგის დათვალიერება',
  }
};

export function LanguageProvider({ children }) {
  const [lang, setLang] = useState('en');
  const t = translations[lang];
  return (
    <LanguageContext.Provider value={{ lang, setLang, t }}>
      {children}
    </LanguageContext.Provider>
  );
}

export function useLanguage() {
  return useContext(LanguageContext);
}
"""

# ─────────────────────────────────────────
# src/App.js
# ─────────────────────────────────────────
FILES["src/App.js"] = """import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { LanguageProvider } from './context/LanguageContext';
import Navbar from './components/Navbar';
import Footer from './components/Footer';
import Home from './pages/Home';
import Catalog from './pages/Catalog';
import Contact from './pages/Contact';
import AdminLogin from './pages/AdminLogin';
import AdminDashboard from './pages/AdminDashboard';

export default function App() {
  return (
    <LanguageProvider>
      <BrowserRouter>
        <div style={{ display: 'flex', flexDirection: 'column', minHeight: '100vh' }}>
          <Navbar />
          <main style={{ flex: 1 }}>
            <Routes>
              <Route path="/" element={<Home />} />
              <Route path="/catalog" element={<Catalog />} />
              <Route path="/contact" element={<Contact />} />
              <Route path="/admin" element={<AdminLogin />} />
              <Route path="/admin/dashboard" element={<AdminDashboard />} />
            </Routes>
          </main>
          <Footer />
        </div>
      </BrowserRouter>
    </LanguageProvider>
  );
}
"""

# ─────────────────────────────────────────
# src/components/Navbar.js
# ─────────────────────────────────────────
FILES["src/components/Navbar.js"] = """import React, { useState, useEffect } from 'react';
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
"""

# ─────────────────────────────────────────
# src/components/Footer.js
# ─────────────────────────────────────────
FILES["src/components/Footer.js"] = """import React from 'react';
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
"""

# ─────────────────────────────────────────
# src/components/BookCard.js
# ─────────────────────────────────────────
FILES["src/components/BookCard.js"] = """import React, { useState } from 'react';
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
"""

# ─────────────────────────────────────────
# src/pages/Home.js
# ─────────────────────────────────────────
FILES["src/pages/Home.js"] = """import React, { useEffect, useState } from 'react';
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
"""

# ─────────────────────────────────────────
# src/pages/Catalog.js
# ─────────────────────────────────────────
FILES["src/pages/Catalog.js"] = """import React, { useEffect, useState } from 'react';
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
"""

# ─────────────────────────────────────────
# src/pages/Contact.js
# ─────────────────────────────────────────
FILES["src/pages/Contact.js"] = """import React from 'react';
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
"""

# ─────────────────────────────────────────
# src/pages/AdminLogin.js
# ─────────────────────────────────────────
FILES["src/pages/AdminLogin.js"] = """import React, { useState } from 'react';
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
"""

# ─────────────────────────────────────────
# src/pages/AdminDashboard.js
# ─────────────────────────────────────────
FILES["src/pages/AdminDashboard.js"] = """import React, { useEffect, useState } from 'react';
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
"""

# ─────────────────────────────────────────
# README.md
# ─────────────────────────────────────────
FILES["README.md"] = """# 📚 Libris – Bilingual Digital Book Library

A full-featured bilingual (Georgian + English) digital book library built with React, Supabase, and Cloudinary.

## 🚀 Quick Start

### 1. Database Setup
Run `libris_schema.sql` in your **Supabase SQL Editor** to create the `books` table.

### 2. Install Dependencies
```bash
npm install
```

### 3. Configure Environment
The `.env` file is pre-configured. Verify your credentials are correct.

### 4. Start Development Server
```bash
npm start
```
Opens at **http://localhost:3000**

---

## 🔐 Admin Panel

**URL:** `/admin`

Login with your Supabase Auth credentials. Create an admin user in:
> Supabase Dashboard → Authentication → Users → Add user

### Admin Features:
- Add/Edit/Delete books
- Upload cover images → saved to Cloudinary `/covers`
- Upload PDF files → saved to Cloudinary `/pdfs`
- Toggle Free vs Paid
- Bilingual title & description support

---

## 📁 Project Structure

```
libris/
├── public/
│   └── index.html
├── src/
│   ├── components/
│   │   ├── Navbar.js
│   │   ├── Footer.js
│   │   └── BookCard.js
│   ├── context/
│   │   └── LanguageContext.js
│   ├── pages/
│   │   ├── Home.js
│   │   ├── Catalog.js
│   │   ├── Contact.js
│   │   ├── AdminLogin.js
│   │   └── AdminDashboard.js
│   ├── App.js
│   ├── index.js
│   ├── index.css
│   ├── supabaseClient.js
│   └── cloudinary.js
├── .env
├── package.json
├── libris_schema.sql
└── README.md
```

---

## 🎨 Design System

| Token       | Value    |
|-------------|----------|
| Deep Blue   | #0A1628  |
| Gold        | #C9A84C  |
| Gold Light  | #E8C87A  |
| Cream BG    | #FAF7F0  |

**Fonts:** Playfair Display (headings) + DM Sans (body)

---

## 💳 Monetization

- **Free books** → "Download PDF" button links to Cloudinary PDF
- **Paid books** → "Buy Now" button opens `mailto:Libris.info.aza@gmail.com` with book title pre-filled

---

## 🌐 Languages

Full UI in **English** and **Georgian (ქართული)** with language switcher in navbar.

---

## 📦 Tech Stack

- **React 18** + React Router v6
- **Tailwind CSS** (via global CSS variables)
- **Supabase** (PostgreSQL + Auth + RLS)
- **Cloudinary** (images & PDFs with signed upload preset)
"""

# ─────────────────────────────────────────
# WRITE ALL FILES
# ─────────────────────────────────────────
def write_files():
    for rel_path, content in FILES.items():
        full_path = os.path.join(BASE, rel_path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"  ✓  {full_path}")

if __name__ == "__main__":
    print("\n🚀 Generating Libris project...\n")
    write_files()
    print(f"\n✅ Done! Project created in ./{BASE}/")
    print("\nNext steps:")
    print(f"  1. cd {BASE}")
    print("  2. Run libris_schema.sql in Supabase SQL Editor")
    print("  3. npm install")
    print("  4. npm start\n")
