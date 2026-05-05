# 📚 Libris – Bilingual Digital Book Library

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
