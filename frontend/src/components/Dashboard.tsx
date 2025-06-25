'use client';

import React, { useState, useEffect } from 'react';
import { apiClient } from '@/lib/api';
import { User, CookProfile } from '@/types/api';
import CustomerDashboard from './CustomerDashboard';
import CookDashboard from './CookDashboard';

interface DashboardProps {
  user: User;
  onLogout: () => void;
}

export default function Dashboard({ user, onLogout }: DashboardProps) {
  const [cookProfile, setCookProfile] = useState<CookProfile | null>(null);
  const [isLoadingProfile, setIsLoadingProfile] = useState(true);
  const [mode, setMode] = useState<'customer' | 'cook'>('customer');

  useEffect(() => {
    checkCookProfile();
  }, []);

  const checkCookProfile = async () => {
    setIsLoadingProfile(true);
    const response = await apiClient.checkCookProfile();
    if (response.data) {
      setCookProfile(response.data);
    }
    setIsLoadingProfile(false);
  };

  const handleLogout = () => {
    apiClient.clearToken();
    onLogout();
  };

  const switchMode = (newMode: 'customer' | 'cook') => {
    setMode(newMode);
  };

  if (isLoadingProfile) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading profile...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center space-x-4">
              <h1 className="text-xl font-bold text-gray-900">Adresur</h1>
              
              {/* Mode Toggle - Only show if user has cook profile */}
              {cookProfile && (
                <div className="flex items-center bg-gray-100 rounded-lg p-1">
                  <button
                    onClick={() => switchMode('customer')}
                    className={`px-3 py-1 rounded-md text-sm font-medium transition-colors ${
                      mode === 'customer'
                        ? 'bg-white text-blue-600 shadow-sm'
                        : 'text-gray-600 hover:text-gray-900'
                    }`}
                  >
                    🛒 Customer
                  </button>
                  <button
                    onClick={() => switchMode('cook')}
                    className={`px-3 py-1 rounded-md text-sm font-medium transition-colors ${
                      mode === 'cook'
                        ? 'bg-white text-green-600 shadow-sm'
                        : 'text-gray-600 hover:text-gray-900'
                    }`}
                  >
                    👨‍🍳 Cook
                  </button>
                </div>
              )}
            </div>
            
            <div className="flex items-center space-x-4">
              <span className="text-sm text-gray-700">
                Welcome, {user.full_name}
              </span>
              <button
                onClick={handleLogout}
                className="text-sm text-gray-500 hover:text-gray-700"
              >
                Logout
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      {mode === 'cook' && cookProfile ? (
        <CookDashboard 
          user={user} 
          cookProfile={cookProfile} 
          onProfileUpdated={checkCookProfile}
        />
      ) : (
        <CustomerDashboard 
          user={user} 
          cookProfile={cookProfile} 
          onProfileCreated={checkCookProfile}
        />
      )}
    </div>
  );
} 