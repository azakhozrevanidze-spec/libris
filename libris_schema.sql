-- Libris Database Schema
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
