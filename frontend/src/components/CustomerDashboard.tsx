'use client';

import React, { useState } from 'react';
import { apiClient } from '@/lib/api';
import { User, CookProfile } from '@/types/api';
import MenusTab from './MenusTab';
import OrdersTab from './OrdersTab';
import MessagesTab from './MessagesTab';

interface CustomerDashboardProps {
  user: User;
  cookProfile: CookProfile | null;
  onProfileCreated: () => void;
}

export default function CustomerDashboard({ user, cookProfile, onProfileCreated }: CustomerDashboardProps) {
  const [activeTab, setActiveTab] = useState('home');

  const tabs = [
    { id: 'home', label: 'Home', icon: '🏠' },
    { id: 'menus', label: 'Browse Menus', icon: '📋' },
    { id: 'orders', label: 'My Orders', icon: '📦' },
    { id: 'messages', label: 'Messages', icon: '💬' },
  ];

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
      <div className="flex flex-col lg:flex-row gap-6">
        {/* Sidebar Navigation */}
        <div className="lg:w-64">
          <nav className="bg-white rounded-lg shadow-sm p-4">
            <ul className="space-y-2">
              {tabs.map((tab) => (
                <li key={tab.id}>
                  <button
                    onClick={() => setActiveTab(tab.id)}
                    className={`w-full flex items-center px-3 py-2 text-left rounded-md text-sm font-medium ${
                      activeTab === tab.id
                        ? 'bg-blue-100 text-blue-700'
                        : 'text-gray-600 hover:bg-gray-50 hover:text-gray-900'
                    }`}
                  >
                    <span className="mr-3">{tab.icon}</span>
                    {tab.label}
                  </button>
                </li>
              ))}
            </ul>
          </nav>
        </div>

        {/* Main Content */}
        <div className="flex-1">
          <div className="bg-white rounded-lg shadow-sm p-6">
            {activeTab === 'home' && <HomeTab user={user} cookProfile={cookProfile} onProfileCreated={onProfileCreated} />}
            {activeTab === 'menus' && <MenusTab />}
            {activeTab === 'orders' && <OrdersTab isCook={false} />}
            {activeTab === 'messages' && <MessagesTab />}
          </div>
        </div>
      </div>
    </div>
  );
}

// Home Tab Component for Customer Dashboard
function HomeTab({ user, cookProfile, onProfileCreated }: { 
  user: User; 
  cookProfile: CookProfile | null; 
  onProfileCreated: () => void;
}) {
  const [showCookForm, setShowCookForm] = useState(false);
  const [cookFormData, setCookFormData] = useState({
    name: '',
    bio: '',
    photo_url: '',
    delivery_radius: 5
  });
  const [isCreating, setIsCreating] = useState(false);

  const handleCreateCookProfile = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsCreating(true);

    try {
      const response = await apiClient.createCookProfile(cookFormData);
      if (response.error) {
        alert('Failed to create cook profile: ' + response.error);
      } else {
        setShowCookForm(false);
        onProfileCreated();
      }
    } catch (error) {
      alert('Failed to create cook profile');
    } finally {
      setIsCreating(false);
    }
  };

  return (
    <div>
      <h2 className="text-2xl font-bold text-gray-900 mb-6">Welcome to Adresur!</h2>
      
      {cookProfile ? (
        <div className="bg-green-50 border border-green-200 rounded-lg p-4 mb-6">
          <h3 className="text-lg font-semibold text-green-800 mb-2">
            🍳 Cook Profile Active
          </h3>
          <p className="text-green-700">
            <strong>{cookProfile.name}</strong>
          </p>
          {cookProfile.bio && (
            <p className="text-green-600 mt-1">{cookProfile.bio}</p>
          )}
          <p className="text-green-600 text-sm mt-2">
            Delivery radius: {cookProfile.delivery_radius} miles
          </p>
          <p className="text-green-600 text-sm mt-2">
            💡 Switch to "Cook" mode in the header to manage your kitchen!
          </p>
        </div>
      ) : (
        <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 mb-6">
          <h3 className="text-lg font-semibold text-blue-800 mb-2">
            🍳 Become a Cook
          </h3>
          <p className="text-blue-700 mb-4">
            Share your culinary skills with the community! Create a cook profile to start offering your delicious meals.
          </p>
          <button
            onClick={() => setShowCookForm(true)}
            className="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700"
          >
            Create Cook Profile
          </button>
        </div>
      )}

      {showCookForm && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-lg p-6 w-full max-w-md">
            <h3 className="text-lg font-semibold mb-4">Create Cook Profile</h3>
            <form onSubmit={handleCreateCookProfile} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Cook Name
                </label>
                <input
                  type="text"
                  value={cookFormData.name}
                  onChange={(e) => setCookFormData({ ...cookFormData, name: e.target.value })}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  required
                />
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Bio (Optional)
                </label>
                <textarea
                  value={cookFormData.bio}
                  onChange={(e) => setCookFormData({ ...cookFormData, bio: e.target.value })}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  rows={3}
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Photo URL (Optional)
                </label>
                <input
                  type="url"
                  value={cookFormData.photo_url}
                  onChange={(e) => setCookFormData({ ...cookFormData, photo_url: e.target.value })}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Delivery Radius (miles)
                </label>
                <input
                  type="number"
                  min="1"
                  max="50"
                  value={cookFormData.delivery_radius}
                  onChange={(e) => setCookFormData({ ...cookFormData, delivery_radius: Number(e.target.value) })}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>

              <div className="flex gap-3">
                <button
                  type="submit"
                  disabled={isCreating}
                  className="flex-1 bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 disabled:opacity-50"
                >
                  {isCreating ? 'Creating...' : 'Create Profile'}
                </button>
                <button
                  type="button"
                  onClick={() => setShowCookForm(false)}
                  className="flex-1 bg-gray-300 text-gray-700 py-2 px-4 rounded-md hover:bg-gray-400"
                >
                  Cancel
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="bg-gradient-to-r from-purple-50 to-pink-50 p-6 rounded-lg border">
          <h3 className="text-lg font-semibold text-gray-900 mb-2">
            🍽️ Browse Local Menus
          </h3>
          <p className="text-gray-600 mb-4">
            Discover delicious meals from local home cooks in your area.
          </p>
          <button className="text-purple-600 hover:text-purple-700 font-medium">
            Start browsing →
          </button>
        </div>

        <div className="bg-gradient-to-r from-green-50 to-blue-50 p-6 rounded-lg border">
          <h3 className="text-lg font-semibold text-gray-900 mb-2">
            📱 Stay Connected
          </h3>
          <p className="text-gray-600 mb-4">
            Message cooks directly and track your orders in real-time.
          </p>
          <button className="text-green-600 hover:text-green-700 font-medium">
            View messages →
          </button>
        </div>
      </div>
    </div>
  );
} 