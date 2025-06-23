-- Manual Password Fix for Adresur Sample Users
-- Run this SQL directly in your Supabase SQL Editor

-- First, let's generate the correct password hashes
-- These hashes are generated using bcrypt with the same settings as your app

-- Update admin user with correct password hash for "admin123"
INSERT INTO users (email, full_name, role, hashed_password, is_active, created_at)
VALUES ('admin@adresur.com', 'Admin User', 'admin', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewIBxLaKK.YjNhHm', true, NOW())
ON CONFLICT (email) 
DO UPDATE SET 
    hashed_password = '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewIBxLaKK.YjNhHm',
    updated_at = NOW();

-- Update regular user with correct password hash for "user123"
INSERT INTO users (email, full_name, role, hashed_password, is_active, created_at)
VALUES ('user@example.com', 'Test User', 'user', '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW', true, NOW())
ON CONFLICT (email) 
DO UPDATE SET 
    hashed_password = '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW',
    updated_at = NOW();

-- Verify the users were created/updated
SELECT email, full_name, role, is_active, created_at 
FROM users 
WHERE email IN ('admin@adresur.com', 'user@example.com')
ORDER BY email; 