'use client';

import React, { useState, useEffect } from 'react';
import { apiClient } from '@/lib/api';
import { User, CookProfile, MenuItem, Order } from '@/types/api';
import OrdersTab from './OrdersTab';

interface CookDashboardProps {
  user: User;
  cookProfile: CookProfile;
  onProfileUpdated: () => void;
}

export default function CookDashboard({ user, cookProfile, onProfileUpdated }: CookDashboardProps) {
  const [activeTab, setActiveTab] = useState('overview');

  const tabs = [
    { id: 'overview', label: 'Overview', icon: '📊' },
    { id: 'menu', label: 'My Menu', icon: '🍽️' },
    { id: 'orders', label: 'Orders', icon: '📦' },
    { id: 'profile', label: 'Profile', icon: '👨‍🍳' },
  ];

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
      {/* Cook Mode Header */}
      <div className="bg-green-50 border border-green-200 rounded-lg p-4 mb-6">
        <div className="flex items-center justify-between">
          <div className="flex items-center">
            <span className="text-2xl mr-3">👨‍🍳</span>
            <div>
              <h2 className="text-lg font-semibold text-green-800">
                Cook Mode: {cookProfile.name}
              </h2>
              <p className="text-green-600 text-sm">
                Manage your kitchen, menu, and orders
              </p>
            </div>
          </div>
          <div className="text-right">
            <p className="text-sm text-green-600">
              Delivery radius: {cookProfile.delivery_radius} miles
            </p>
          </div>
        </div>
      </div>

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
                        ? 'bg-green-100 text-green-700'
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
            {activeTab === 'overview' && <OverviewTab cookProfile={cookProfile} />}
            {activeTab === 'menu' && <MenuTab cookProfile={cookProfile} />}
            {activeTab === 'orders' && <CookOrdersTab cookProfile={cookProfile} />}
            {activeTab === 'profile' && <ProfileTab cookProfile={cookProfile} onProfileUpdated={onProfileUpdated} />}
          </div>
        </div>
      </div>
    </div>
  );
}

// Overview Tab - Dashboard with analytics
function OverviewTab({ cookProfile }: { cookProfile: CookProfile }) {
  const [stats, setStats] = useState({
    totalMenuItems: 0,
    activeOrders: 0,
    totalRevenue: 0,
    completedOrders: 0
  });

  return (
    <div>
      <h2 className="text-2xl font-bold text-gray-900 mb-6">Dashboard Overview</h2>
      
      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <div className="bg-blue-50 p-6 rounded-lg border border-blue-200">
          <h3 className="font-semibold text-blue-800 mb-2">Menu Items</h3>
          <p className="text-3xl font-bold text-blue-600">{stats.totalMenuItems}</p>
        </div>
        <div className="bg-yellow-50 p-6 rounded-lg border border-yellow-200">
          <h3 className="font-semibold text-yellow-800 mb-2">Active Orders</h3>
          <p className="text-3xl font-bold text-yellow-600">{stats.activeOrders}</p>
        </div>
        <div className="bg-green-50 p-6 rounded-lg border border-green-200">
          <h3 className="font-semibold text-green-800 mb-2">Total Revenue</h3>
          <p className="text-3xl font-bold text-green-600">${stats.totalRevenue.toFixed(2)}</p>
        </div>
        <div className="bg-purple-50 p-6 rounded-lg border border-purple-200">
          <h3 className="font-semibold text-purple-800 mb-2">Completed Orders</h3>
          <p className="text-3xl font-bold text-purple-600">{stats.completedOrders}</p>
        </div>
      </div>

      <div className="bg-blue-50 border border-blue-200 rounded-lg p-6">
        <h3 className="text-lg font-semibold text-blue-800 mb-2">
          🚀 Welcome to Cook Mode!
        </h3>
        <p className="text-blue-700">
          This is your dedicated space to manage your cooking business. Add menu items, track orders, and grow your customer base.
        </p>
      </div>
    </div>
  );
}

// Menu Tab - Manage menu items
function MenuTab({ cookProfile }: { cookProfile: CookProfile }) {
  const [menuItems, setMenuItems] = useState<MenuItem[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [showAddForm, setShowAddForm] = useState(false);

  useEffect(() => {
    loadMenuItems();
  }, []);

  const loadMenuItems = async () => {
    setIsLoading(true);
    const response = await apiClient.getCookMenuItems(cookProfile.id);
    if (response.data) {
      setMenuItems(response.data);
    }
    setIsLoading(false);
  };

  if (isLoading) {
    return (
      <div className="text-center py-8">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-green-600 mx-auto mb-4"></div>
        <p className="text-gray-600">Loading menu...</p>
      </div>
    );
  }

  return (
    <div>
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-2xl font-bold text-gray-900">My Menu</h2>
        <button
          onClick={() => setShowAddForm(true)}
          className="bg-gradient-to-r from-green-500 to-green-600 text-white px-6 py-3 rounded-lg hover:from-green-600 hover:to-green-700 shadow-lg transform hover:scale-105 transition-all duration-200 flex items-center gap-2"
        >
          <span className="text-xl">✨</span>
          Add New Dish
        </button>
      </div>

      {menuItems.length === 0 ? (
        <div className="text-center py-12 bg-gradient-to-br from-gray-50 to-gray-100 rounded-xl">
          <div className="text-6xl mb-4">🍽️</div>
          <h3 className="text-xl font-semibold text-gray-700 mb-2">Your menu is empty!</h3>
          <p className="text-gray-500 mb-6">Add your first delicious dish to get started</p>
          <button
            onClick={() => setShowAddForm(true)}
            className="bg-green-600 text-white px-6 py-2 rounded-lg hover:bg-green-700"
          >
            Create Your First Dish
          </button>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {menuItems.map((item) => (
            <div key={item.id} className="border rounded-xl overflow-hidden hover:shadow-lg transition-shadow bg-white">
              {item.photo_url && (
                <img 
                  src={item.photo_url} 
                  alt={item.title}
                  className="w-full h-48 object-cover"
                />
              )}
              <div className="p-4">
                <div className="flex justify-between items-start mb-2">
                  <h4 className="text-lg font-semibold text-gray-900">{item.title}</h4>
                  <span className="text-lg font-bold text-green-600">
                    ${(typeof item.price === 'number' ? item.price : parseFloat(item.price as string) || 0).toFixed(2)}
                  </span>
                </div>
                
                <p className="text-gray-600 mb-4">{item.description}</p>
                
                <div className="flex justify-between items-center">
                  <span className={`px-3 py-1 rounded-full text-sm font-medium ${
                    item.is_available 
                      ? 'bg-green-100 text-green-800' 
                      : 'bg-red-100 text-red-800'
                  }`}>
                    {item.is_available ? '✅ Available' : '❌ Unavailable'}
                  </span>
                  <div className="flex gap-2">
                    <button className="text-blue-600 hover:text-blue-700 text-sm">
                      Edit
                    </button>
                    <button className="text-red-600 hover:text-red-700 text-sm">
                      Delete
                    </button>
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Add Menu Item Dialog */}
      {showAddForm && (
        <AddMenuItemDialog 
          onClose={() => setShowAddForm(false)}
          onSuccess={() => {
            setShowAddForm(false);
            loadMenuItems();
          }}
        />
      )}
    </div>
  );
}

// Add Menu Item Dialog Component
function AddMenuItemDialog({ onClose, onSuccess }: { onClose: () => void; onSuccess: () => void }) {
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    price: '',
    photo_url: '',
    is_available: true
  });
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [errors, setErrors] = useState<{ [key: string]: string }>({});

  const validateForm = () => {
    const newErrors: { [key: string]: string } = {};
    
    if (!formData.title.trim()) {
      newErrors.title = 'Dish name is required';
    }
    if (!formData.description.trim()) {
      newErrors.description = 'Description is required';
    }
    if (!formData.price || isNaN(Number(formData.price)) || Number(formData.price) <= 0) {
      newErrors.price = 'Please enter a valid price';
    }
    
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!validateForm()) {
      return;
    }

    setIsSubmitting(true);
    
    try {
      const response = await apiClient.createMenuItem({
        title: formData.title,
        description: formData.description,
        price: Number(formData.price),
        photo_url: formData.photo_url || undefined,
        is_available: formData.is_available
      });

      if (response.error) {
        alert('Failed to create menu item: ' + response.error);
      } else {
        onSuccess();
      }
    } catch (error) {
      alert('Failed to create menu item');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
      <div className="bg-white rounded-2xl p-8 w-full max-w-md max-h-[90vh] overflow-y-auto shadow-2xl">
        <div className="text-center mb-6">
          <div className="text-4xl mb-2">🍳</div>
          <h3 className="text-2xl font-bold text-gray-900">Add New Dish</h3>
          <p className="text-gray-600">Share your culinary creation with the world!</p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-5">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              🍽️ Dish Name *
            </label>
            <input
              type="text"
              value={formData.title}
              onChange={(e) => setFormData({ ...formData, title: e.target.value })}
              className={`w-full px-4 py-3 border rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500 transition-colors ${
                errors.title ? 'border-red-300' : 'border-gray-300'
              }`}
              placeholder="e.g., Grandma's Secret Lasagna"
            />
            {errors.title && <p className="text-red-500 text-sm mt-1">{errors.title}</p>}
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              📝 Description *
            </label>
            <textarea
              value={formData.description}
              onChange={(e) => setFormData({ ...formData, description: e.target.value })}
              className={`w-full px-4 py-3 border rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500 transition-colors ${
                errors.description ? 'border-red-300' : 'border-gray-300'
              }`}
              rows={3}
              placeholder="Tell customers what makes this dish special..."
            />
            {errors.description && <p className="text-red-500 text-sm mt-1">{errors.description}</p>}
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              💰 Price *
            </label>
            <div className="relative">
              <span className="absolute left-3 top-3 text-gray-500">$</span>
              <input
                type="number"
                step="0.01"
                min="0"
                value={formData.price}
                onChange={(e) => setFormData({ ...formData, price: e.target.value })}
                className={`w-full pl-8 pr-4 py-3 border rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500 transition-colors ${
                  errors.price ? 'border-red-300' : 'border-gray-300'
                }`}
                placeholder="0.00"
              />
            </div>
            {errors.price && <p className="text-red-500 text-sm mt-1">{errors.price}</p>}
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              📸 Photo URL (Optional)
            </label>
            <input
              type="url"
              value={formData.photo_url}
              onChange={(e) => setFormData({ ...formData, photo_url: e.target.value })}
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500 transition-colors"
              placeholder="https://example.com/your-dish-photo.jpg"
            />
          </div>

          <div className="flex items-center gap-3">
            <input
              type="checkbox"
              id="available"
              checked={formData.is_available}
              onChange={(e) => setFormData({ ...formData, is_available: e.target.checked })}
              className="w-4 h-4 text-green-600 focus:ring-green-500 border-gray-300 rounded"
            />
            <label htmlFor="available" className="text-sm font-medium text-gray-700">
              ✅ Available for ordering
            </label>
          </div>

          <div className="flex gap-3 pt-4">
            <button
              type="button"
              onClick={onClose}
              className="flex-1 bg-gray-100 text-gray-700 py-3 px-4 rounded-lg hover:bg-gray-200 transition-colors"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={isSubmitting}
              className="flex-1 bg-gradient-to-r from-green-500 to-green-600 text-white py-3 px-4 rounded-lg hover:from-green-600 hover:to-green-700 disabled:opacity-50 transition-all transform hover:scale-105"
            >
              {isSubmitting ? (
                <div className="flex items-center justify-center gap-2">
                  <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
                  Creating...
                </div>
              ) : (
                '🚀 Add Dish'
              )}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}

// Cook Orders Tab - Manage incoming orders
function CookOrdersTab({ cookProfile }: { cookProfile: CookProfile }) {
  return <OrdersTab isCook={true} />;
}

// Profile Tab - Manage cook profile
function ProfileTab({ cookProfile, onProfileUpdated }: { 
  cookProfile: CookProfile; 
  onProfileUpdated: () => void;
}) {
  return (
    <div>
      <h2 className="text-2xl font-bold text-gray-900 mb-6">Cook Profile</h2>
      
      <div className="bg-white border rounded-lg p-6">
        <div className="flex items-center mb-6">
          {cookProfile.photo_url ? (
            <img 
              src={cookProfile.photo_url} 
              alt={cookProfile.name}
              className="w-16 h-16 rounded-full object-cover mr-4"
            />
          ) : (
            <div className="w-16 h-16 rounded-full bg-gray-200 flex items-center justify-center mr-4">
              <span className="text-gray-600 text-2xl">👨‍🍳</span>
            </div>
          )}
          <div>
            <h3 className="text-xl font-semibold text-gray-900">{cookProfile.name}</h3>
            <p className="text-gray-600">Cook since {new Date(cookProfile.created_at).toLocaleDateString()}</p>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <h4 className="font-semibold text-gray-900 mb-2">Bio</h4>
            <p className="text-gray-600">{cookProfile.bio || 'No bio provided'}</p>
          </div>
          
          <div>
            <h4 className="font-semibold text-gray-900 mb-2">Delivery Information</h4>
            <p className="text-gray-600">
              Delivery radius: {cookProfile.delivery_radius} miles
            </p>
          </div>
        </div>

        <div className="mt-6">
          <button className="bg-green-600 text-white px-4 py-2 rounded-md hover:bg-green-700">
            Edit Profile
          </button>
        </div>
      </div>
    </div>
  );
} 