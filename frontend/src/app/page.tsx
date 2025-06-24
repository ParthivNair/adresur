'use client';

import React, { useState, useEffect } from 'react';
import LoginForm from '@/components/LoginForm';
import ApiTester from '@/components/ApiTester';

export default function Home() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [token, setToken] = useState<string | null>(null);

  useEffect(() => {
    // Check if user is already logged in
    const savedToken = localStorage.getItem('auth_token');
    if (savedToken) {
      setToken(savedToken);
      setIsLoggedIn(true);
    }
  }, []);

  const handleLoginSuccess = (accessToken: string) => {
    setToken(accessToken);
    setIsLoggedIn(true);
  };

  return (
    <main className="min-h-screen bg-gray-100 py-8">
      <div className="container mx-auto px-4 max-w-6xl">
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-gray-800 mb-2">
            Adresur API Testing Interface
          </h1>
          <p className="text-gray-600">
            Test your API endpoints with authentication and real-time data visualization
          </p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Login Section */}
          <div className="lg:col-span-1">
            <LoginForm onLoginSuccess={handleLoginSuccess} />
          </div>

          {/* API Testing Section */}
          <div className="lg:col-span-2">
            <ApiTester isLoggedIn={isLoggedIn} />
          </div>
        </div>

        {/* Footer */}
        <div className="mt-8 text-center text-gray-500 text-sm">
          <p>
            Make sure your backend API is running on{' '}
            <code className="bg-gray-200 px-1 rounded">http://localhost:8000</code>
          </p>
        </div>
      </div>
    </main>
  );
} 