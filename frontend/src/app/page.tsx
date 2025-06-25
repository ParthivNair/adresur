'use client';

import React, { useState, useEffect } from 'react';
import { apiClient } from '@/lib/api';
import { User } from '@/types/api';
import AuthForm from '@/components/AuthForm';
import Dashboard from '@/components/Dashboard';

export default function Home() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    checkAuthStatus();
  }, []);

  const checkAuthStatus = async () => {
    setIsLoading(true);
    const savedToken = localStorage.getItem('auth_token');
    
    if (savedToken) {
      apiClient.setToken(savedToken);
      
      // Verify token is still valid by fetching user info
      const response = await apiClient.getCurrentUser();
      
      if (response.error) {
        // Token is invalid, clear it
        apiClient.clearToken();
        setIsAuthenticated(false);
        setUser(null);
      } else if (response.data) {
        // Token is valid
        setUser(response.data);
        setIsAuthenticated(true);
      }
    }
    
    setIsLoading(false);
  };

  const handleAuthSuccess = async (token: string) => {
    // Fetch user info after successful auth
    const response = await apiClient.getCurrentUser();
    
    if (response.data) {
      setUser(response.data);
      setIsAuthenticated(true);
    }
  };

  const handleLogout = () => {
    setIsAuthenticated(false);
    setUser(null);
  };

  // Show loading spinner while checking auth status
  if (isLoading) {
    return (
      <div className="min-h-screen bg-gray-100 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading...</p>
        </div>
      </div>
    );
  }

  // Show auth form if not authenticated
  if (!isAuthenticated || !user) {
    return <AuthForm onAuthSuccess={handleAuthSuccess} />;
  }

  // Show dashboard if authenticated
  return <Dashboard user={user} onLogout={handleLogout} />;
} 