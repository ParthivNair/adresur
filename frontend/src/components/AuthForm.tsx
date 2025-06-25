'use client';

import React, { useState } from 'react';
import { apiClient } from '@/lib/api';
import { LoginRequest } from '@/types/api';

interface AuthFormProps {
  onAuthSuccess: (token: string) => void;
}

export default function AuthForm({ onAuthSuccess }: AuthFormProps) {
  const [isLogin, setIsLogin] = useState(true);
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    full_name: '',
    confirmPassword: ''
  });
  const [status, setStatus] = useState<{
    type: 'idle' | 'loading' | 'success' | 'error';
    message: string;
  }>({ type: 'idle', message: '' });

  // Sample test users for quick login
  const testUsers = [
    { email: 'admin@adresur.com', password: 'admin123', role: 'admin' },
    { email: 'maria.garcia@email.com', password: 'password123', role: 'user' },
    { email: 'john.chef@email.com', password: 'password123', role: 'user' },
    { email: 'anna.baker@email.com', password: 'password123', role: 'user' },
    { email: 'carlos.cook@email.com', password: 'password123', role: 'user' },
    { email: 'sarah.customer@email.com', password: 'password123', role: 'user' },
  ];

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setStatus({ type: 'loading', message: isLogin ? 'Logging in...' : 'Creating account...' });

    try {
      if (isLogin) {
        const response = await apiClient.login({
          email: formData.email,
          password: formData.password
        });
        
        if (response.error) {
          setStatus({ type: 'error', message: response.error });
        } else if (response.data) {
          apiClient.setToken(response.data.access_token);
          setStatus({ type: 'success', message: 'Login successful!' });
          onAuthSuccess(response.data.access_token);
        }
      } else {
        // Registration
        if (formData.password !== formData.confirmPassword) {
          setStatus({ type: 'error', message: 'Passwords do not match' });
          return;
        }

        const registerResponse = await apiClient.register({
          email: formData.email,
          full_name: formData.full_name,
          password: formData.password
        });

        if (registerResponse.error) {
          setStatus({ type: 'error', message: registerResponse.error });
        } else {
          // Auto-login after successful registration
          const loginResponse = await apiClient.login({
            email: formData.email,
            password: formData.password
          });

          if (loginResponse.error) {
            setStatus({ type: 'error', message: 'Account created but login failed. Please try logging in manually.' });
          } else if (loginResponse.data) {
            apiClient.setToken(loginResponse.data.access_token);
            setStatus({ type: 'success', message: 'Account created successfully!' });
            onAuthSuccess(loginResponse.data.access_token);
          }
        }
      }
    } catch (error) {
      setStatus({ 
        type: 'error', 
        message: error instanceof Error ? error.message : 'Operation failed' 
      });
    }
  };

  const handleQuickLogin = (user: typeof testUsers[0]) => {
    setFormData(prev => ({ ...prev, email: user.email, password: user.password }));
  };

  const resetForm = () => {
    setFormData({ email: '', password: '', full_name: '', confirmPassword: '' });
    setStatus({ type: 'idle', message: '' });
  };

  const toggleMode = () => {
    setIsLogin(!isLogin);
    resetForm();
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center p-4">
      <div className="max-w-md w-full space-y-8">
        <div className="text-center">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">
            Welcome to Adresur
          </h1>
          <p className="text-gray-600">
            {isLogin ? 'Sign in to your account' : 'Create your account'}
          </p>
        </div>

        <div className="bg-white p-8 rounded-lg shadow-md">
          <form onSubmit={handleSubmit} className="space-y-4">
            {!isLogin && (
              <div>
                <label htmlFor="full_name" className="block text-sm font-medium text-gray-700 mb-1">
                  Full Name
                </label>
                <input
                  type="text"
                  id="full_name"
                  value={formData.full_name}
                  onChange={(e) => setFormData({ ...formData, full_name: e.target.value })}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  required={!isLogin}
                />
              </div>
            )}

            <div>
              <label htmlFor="email" className="block text-sm font-medium text-gray-700 mb-1">
                Email
              </label>
              <input
                type="email"
                id="email"
                value={formData.email}
                onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                required
              />
            </div>

            <div>
              <label htmlFor="password" className="block text-sm font-medium text-gray-700 mb-1">
                Password
              </label>
              <input
                type="password"
                id="password"
                value={formData.password}
                onChange={(e) => setFormData({ ...formData, password: e.target.value })}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                required
              />
            </div>

            {!isLogin && (
              <div>
                <label htmlFor="confirmPassword" className="block text-sm font-medium text-gray-700 mb-1">
                  Confirm Password
                </label>
                <input
                  type="password"
                  id="confirmPassword"
                  value={formData.confirmPassword}
                  onChange={(e) => setFormData({ ...formData, confirmPassword: e.target.value })}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  required={!isLogin}
                />
              </div>
            )}

            {status.message && (
              <div className={`p-3 rounded-md text-sm ${
                status.type === 'error' ? 'bg-red-50 text-red-600' : 
                status.type === 'success' ? 'bg-green-50 text-green-600' : 
                'bg-blue-50 text-blue-600'
              }`}>
                {status.message}
              </div>
            )}

            <button
              type="submit"
              disabled={status.type === 'loading'}
              className="w-full bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {status.type === 'loading' 
                ? (isLogin ? 'Signing in...' : 'Creating account...') 
                : (isLogin ? 'Sign In' : 'Create Account')
              }
            </button>
          </form>

          <div className="mt-6 text-center">
            <button
              type="button"
              onClick={toggleMode}
              className="text-blue-600 hover:text-blue-500 text-sm"
            >
              {isLogin 
                ? "Don't have an account? Sign up" 
                : "Already have an account? Sign in"
              }
            </button>
          </div>

          {isLogin && (
            <div className="mt-6">
              <h3 className="text-sm font-medium text-gray-700 mb-2">Quick Login (Test Users):</h3>
              <div className="grid grid-cols-2 gap-2">
                {testUsers.map((user, index) => (
                  <button
                    key={index}
                    onClick={() => handleQuickLogin(user)}
                    className="text-xs bg-gray-100 hover:bg-gray-200 px-2 py-1 rounded border text-left"
                  >
                    <div className="font-medium truncate">{user.email}</div>
                    <div className="text-gray-600">{user.role}</div>
                  </button>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
} 