'use client';

import React, { useState } from 'react';
import { apiClient } from '@/lib/api';
import { LoginRequest } from '@/types/api';

interface LoginFormProps {
  onLoginSuccess: (token: string) => void;
}

export default function LoginForm({ onLoginSuccess }: LoginFormProps) {
  const [credentials, setCredentials] = useState<LoginRequest>({
    email: '',
    password: '',
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
    setStatus({ type: 'loading', message: 'Logging in...' });

    try {
      const response = await apiClient.login(credentials);
      
      if (response.error) {
        setStatus({ type: 'error', message: response.error });
      } else if (response.data) {
        apiClient.setToken(response.data.access_token);
        setStatus({ type: 'success', message: 'Login successful!' });
        onLoginSuccess(response.data.access_token);
      }
    } catch (error) {
      setStatus({ 
        type: 'error', 
        message: error instanceof Error ? error.message : 'Login failed' 
      });
    }
  };

  const handleQuickLogin = (user: typeof testUsers[0]) => {
    setCredentials({ email: user.email, password: user.password });
  };

  const handleLogout = () => {
    apiClient.clearToken();
    setCredentials({ email: '', password: '' });
    setStatus({ type: 'idle', message: '' });
  };

  const getStatusIcon = () => {
    switch (status.type) {
      case 'loading':
        return (
          <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-blue-600"></div>
        );
      case 'success':
        return (
          <div className="rounded-full h-4 w-4 bg-green-500 flex items-center justify-center">
            <svg className="h-3 w-3 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
            </svg>
          </div>
        );
      case 'error':
        return (
          <div className="rounded-full h-4 w-4 bg-red-500 flex items-center justify-center">
            <svg className="h-3 w-3 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
          </div>
        );
      default:
        return (
          <div className="rounded-full h-4 w-4 bg-gray-300"></div>
        );
    }
  };

  return (
    <div className="bg-white p-6 rounded-lg shadow-md">
      <div className="flex items-center gap-3 mb-4">
        <h2 className="text-xl font-bold text-gray-800">Login</h2>
        {getStatusIcon()}
        {status.message && (
          <span className={`text-sm ${
            status.type === 'error' ? 'text-red-600' : 
            status.type === 'success' ? 'text-green-600' : 
            'text-blue-600'
          }`}>
            {status.message}
          </span>
        )}
      </div>

      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label htmlFor="email" className="block text-sm font-medium text-gray-700 mb-1">
            Email
          </label>
          <input
            type="email"
            id="email"
            value={credentials.email}
            onChange={(e) => setCredentials({ ...credentials, email: e.target.value })}
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
            value={credentials.password}
            onChange={(e) => setCredentials({ ...credentials, password: e.target.value })}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            required
          />
        </div>

        <div className="flex gap-2">
          <button
            type="submit"
            disabled={status.type === 'loading'}
            className="flex-1 bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {status.type === 'loading' ? 'Logging in...' : 'Login'}
          </button>
          
          {status.type === 'success' && (
            <button
              type="button"
              onClick={handleLogout}
              className="bg-gray-600 text-white py-2 px-4 rounded-md hover:bg-gray-700"
            >
              Logout
            </button>
          )}
        </div>
      </form>

      <div className="mt-6">
        <h3 className="text-sm font-medium text-gray-700 mb-2">Quick Login (Test Users):</h3>
        <div className="grid grid-cols-2 gap-2">
          {testUsers.map((user, index) => (
            <button
              key={index}
              onClick={() => handleQuickLogin(user)}
              className="text-xs bg-gray-100 hover:bg-gray-200 px-2 py-1 rounded border text-left"
            >
              <div className="font-medium">{user.email}</div>
              <div className="text-gray-600">{user.role}</div>
            </button>
          ))}
        </div>
      </div>
    </div>
  );
} 