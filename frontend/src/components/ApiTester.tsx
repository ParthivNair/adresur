'use client';

import React, { useState, useEffect } from 'react';
import { apiClient } from '@/lib/api';
import { CookProfile, MenuItem, Order, Message } from '@/types/api';

interface ApiTesterProps {
  isLoggedIn: boolean;
}

export default function ApiTester({ isLoggedIn }: ApiTesterProps) {
  const [activeTab, setActiveTab] = useState<'cooks' | 'menu' | 'orders' | 'messages'>('cooks');
  const [cookProfiles, setCookProfiles] = useState<CookProfile[]>([]);
  const [menuItems, setMenuItems] = useState<MenuItem[]>([]);
  const [orders, setOrders] = useState<Order[]>([]);
  const [messages, setMessages] = useState<Message[]>([]);
  const [loading, setLoading] = useState(false);
  const [status, setStatus] = useState<string>('');

  // Form states
  const [newCookProfile, setNewCookProfile] = useState({
    name: '',
    bio: '',
    photo_url: '',
    delivery_radius: 5
  });

  const [newMenuItem, setNewMenuItem] = useState({
    title: '',
    description: '',
    price: 0,
    photo_url: '',
    is_available: true
  });

  const [newOrder, setNewOrder] = useState({
    menu_item_id: 1,
    quantity: 1,
    special_instructions: ''
  });

  const [newMessage, setNewMessage] = useState({
    order_id: 1,
    content: ''
  });

  // Fetch functions
  const fetchCookProfiles = async () => {
    setLoading(true);
    const response = await apiClient.getCookProfiles();
    if (response.error) {
      setStatus(`Error fetching cook profiles: ${response.error}`);
    } else {
      setCookProfiles(response.data || []);
      setStatus('Cook profiles loaded successfully');
    }
    setLoading(false);
  };

  const fetchMenuItems = async () => {
    setLoading(true);
    const response = await apiClient.getMenuItems();
    if (response.error) {
      setStatus(`Error fetching menu items: ${response.error}`);
    } else {
      setMenuItems(response.data || []);
      setStatus('Menu items loaded successfully');
    }
    setLoading(false);
  };

  const fetchOrders = async () => {
    setLoading(true);
    const response = await apiClient.getOrders();
    if (response.error) {
      setStatus(`Error fetching orders: ${response.error}`);
    } else {
      setOrders(response.data || []);
      setStatus('Orders loaded successfully');
    }
    setLoading(false);
  };

  const fetchMessages = async () => {
    if (orders.length > 0) {
      setLoading(true);
      const response = await apiClient.getMessages(orders[0].id);
      if (response.error) {
        setStatus(`Error fetching messages: ${response.error}`);
      } else {
        setMessages(response.data || []);
        setStatus('Messages loaded successfully');
      }
      setLoading(false);
    }
  };

  // Create functions
  const createCookProfile = async () => {
    setLoading(true);
    const response = await apiClient.createCookProfile(newCookProfile);
    if (response.error) {
      setStatus(`Error creating cook profile: ${response.error}`);
    } else {
      setStatus('Cook profile created successfully');
      fetchCookProfiles();
      setNewCookProfile({ name: '', bio: '', photo_url: '', delivery_radius: 5 });
    }
    setLoading(false);
  };

  const createMenuItem = async () => {
    setLoading(true);
    const response = await apiClient.createMenuItem(newMenuItem);
    if (response.error) {
      setStatus(`Error creating menu item: ${response.error}`);
    } else {
      setStatus('Menu item created successfully');
      fetchMenuItems();
      setNewMenuItem({ title: '', description: '', price: 0, photo_url: '', is_available: true });
    }
    setLoading(false);
  };

  const createOrder = async () => {
    setLoading(true);
    const response = await apiClient.createOrder(newOrder);
    if (response.error) {
      setStatus(`Error creating order: ${response.error}`);
    } else {
      setStatus('Order created successfully');
      fetchOrders();
      setNewOrder({ menu_item_id: 1, quantity: 1, special_instructions: '' });
    }
    setLoading(false);
  };

  const createMessage = async () => {
    setLoading(true);
    const response = await apiClient.createMessage(newMessage);
    if (response.error) {
      setStatus(`Error creating message: ${response.error}`);
    } else {
      setStatus('Message created successfully');
      fetchMessages();
      setNewMessage({ order_id: 1, content: '' });
    }
    setLoading(false);
  };

  // Delete functions
  const deleteCookProfile = async (id: number) => {
    setLoading(true);
    const response = await apiClient.deleteCookProfile(id);
    if (response.error) {
      setStatus(`Error deleting cook profile: ${response.error}`);
    } else {
      setStatus('Cook profile deleted successfully');
      fetchCookProfiles();
    }
    setLoading(false);
  };

  const deleteMenuItem = async (id: number) => {
    setLoading(true);
    const response = await apiClient.deleteMenuItem(id);
    if (response.error) {
      setStatus(`Error deleting menu item: ${response.error}`);
    } else {
      setStatus('Menu item deleted successfully');
      fetchMenuItems();
    }
    setLoading(false);
  };

  const deleteOrder = async (id: number) => {
    setLoading(true);
    const response = await apiClient.deleteOrder(id);
    if (response.error) {
      setStatus(`Error deleting order: ${response.error}`);
    } else {
      setStatus('Order deleted successfully');
      fetchOrders();
    }
    setLoading(false);
  };

  // Load data on tab change
  useEffect(() => {
    if (!isLoggedIn) return;
    
    switch (activeTab) {
      case 'cooks':
        fetchCookProfiles();
        break;
      case 'menu':
        fetchMenuItems();
        break;
      case 'orders':
        fetchOrders();
        break;
      case 'messages':
        fetchMessages();
        break;
    }
  }, [activeTab, isLoggedIn]);

  if (!isLoggedIn) {
    return (
      <div className="bg-gray-100 p-6 rounded-lg">
        <p className="text-gray-600">Please log in to test API operations.</p>
      </div>
    );
  }

  const renderCrudButtons = () => (
    <div className="flex gap-2 mb-4">
      <button
        onClick={() => {
          switch (activeTab) {
            case 'cooks': fetchCookProfiles(); break;
            case 'menu': fetchMenuItems(); break;
            case 'orders': fetchOrders(); break;
            case 'messages': fetchMessages(); break;
          }
        }}
        className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
        disabled={loading}
      >
        GET (Fetch)
      </button>
      <button
        onClick={() => {
          switch (activeTab) {
            case 'cooks': createCookProfile(); break;
            case 'menu': createMenuItem(); break;
            case 'orders': createOrder(); break;
            case 'messages': createMessage(); break;
          }
        }}
        className="bg-green-500 text-white px-4 py-2 rounded hover:bg-green-600"
        disabled={loading}
      >
        POST (Create)
      </button>
      <button
        className="bg-yellow-500 text-white px-4 py-2 rounded hover:bg-yellow-600 opacity-50 cursor-not-allowed"
        disabled={true}
        title="PUT operations available per item"
      >
        PUT (Update)
      </button>
      <button
        className="bg-red-500 text-white px-4 py-2 rounded hover:bg-red-600 opacity-50 cursor-not-allowed"
        disabled={true}
        title="DELETE operations available per item"
      >
        DELETE (Remove)
      </button>
    </div>
  );

  const renderCreateForm = () => {
    switch (activeTab) {
      case 'cooks':
        return (
          <div className="bg-gray-50 p-4 rounded mb-4">
            <h4 className="font-medium mb-2">Create Cook Profile</h4>
            <div className="grid grid-cols-2 gap-2">
              <input
                type="text"
                placeholder="Name"
                value={newCookProfile.name}
                onChange={(e) => setNewCookProfile({ ...newCookProfile, name: e.target.value })}
                className="px-2 py-1 border rounded"
              />
              <input
                type="number"
                placeholder="Delivery Radius"
                value={newCookProfile.delivery_radius}
                onChange={(e) => setNewCookProfile({ ...newCookProfile, delivery_radius: parseFloat(e.target.value) })}
                className="px-2 py-1 border rounded"
              />
              <textarea
                placeholder="Bio"
                value={newCookProfile.bio}
                onChange={(e) => setNewCookProfile({ ...newCookProfile, bio: e.target.value })}
                className="px-2 py-1 border rounded col-span-2"
                rows={2}
              />
            </div>
          </div>
        );
      case 'menu':
        return (
          <div className="bg-gray-50 p-4 rounded mb-4">
            <h4 className="font-medium mb-2">Create Menu Item</h4>
            <div className="grid grid-cols-2 gap-2">
              <input
                type="text"
                placeholder="Title"
                value={newMenuItem.title}
                onChange={(e) => setNewMenuItem({ ...newMenuItem, title: e.target.value })}
                className="px-2 py-1 border rounded"
              />
              <input
                type="number"
                placeholder="Price"
                value={newMenuItem.price}
                onChange={(e) => setNewMenuItem({ ...newMenuItem, price: parseFloat(e.target.value) })}
                className="px-2 py-1 border rounded"
              />
              <textarea
                placeholder="Description"
                value={newMenuItem.description}
                onChange={(e) => setNewMenuItem({ ...newMenuItem, description: e.target.value })}
                className="px-2 py-1 border rounded col-span-2"
                rows={2}
              />
            </div>
          </div>
        );
      case 'orders':
        return (
          <div className="bg-gray-50 p-4 rounded mb-4">
            <h4 className="font-medium mb-2">Create Order</h4>
            <div className="grid grid-cols-3 gap-2">
              <input
                type="number"
                placeholder="Menu Item ID"
                value={newOrder.menu_item_id}
                onChange={(e) => setNewOrder({ ...newOrder, menu_item_id: parseInt(e.target.value) })}
                className="px-2 py-1 border rounded"
              />
              <input
                type="number"
                placeholder="Quantity"
                value={newOrder.quantity}
                onChange={(e) => setNewOrder({ ...newOrder, quantity: parseInt(e.target.value) })}
                className="px-2 py-1 border rounded"
              />
              <input
                type="text"
                placeholder="Special Instructions"
                value={newOrder.special_instructions}
                onChange={(e) => setNewOrder({ ...newOrder, special_instructions: e.target.value })}
                className="px-2 py-1 border rounded"
              />
            </div>
          </div>
        );
      case 'messages':
        return (
          <div className="bg-gray-50 p-4 rounded mb-4">
            <h4 className="font-medium mb-2">Create Message</h4>
            <div className="grid grid-cols-2 gap-2">
              <input
                type="number"
                placeholder="Order ID"
                value={newMessage.order_id}
                onChange={(e) => setNewMessage({ ...newMessage, order_id: parseInt(e.target.value) })}
                className="px-2 py-1 border rounded"
              />
              <input
                type="text"
                placeholder="Message Content"
                value={newMessage.content}
                onChange={(e) => setNewMessage({ ...newMessage, content: e.target.value })}
                className="px-2 py-1 border rounded"
              />
            </div>
          </div>
        );
    }
  };

  const renderDataTable = () => {
    switch (activeTab) {
      case 'cooks':
        return (
          <div className="overflow-x-auto">
            <table className="min-w-full bg-white border">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-4 py-2 border text-left">ID</th>
                  <th className="px-4 py-2 border text-left">Name</th>
                  <th className="px-4 py-2 border text-left">Bio</th>
                  <th className="px-4 py-2 border text-left">Radius</th>
                  <th className="px-4 py-2 border text-left">Actions</th>
                </tr>
              </thead>
              <tbody>
                {cookProfiles.map((profile) => (
                  <tr key={profile.id} className="hover:bg-gray-50">
                    <td className="px-4 py-2 border">{profile.id}</td>
                    <td className="px-4 py-2 border">{profile.name}</td>
                    <td className="px-4 py-2 border">{profile.bio?.substring(0, 50)}...</td>
                    <td className="px-4 py-2 border">{profile.delivery_radius}</td>
                    <td className="px-4 py-2 border">
                      <button
                        onClick={() => deleteCookProfile(profile.id)}
                        className="bg-red-500 text-white px-2 py-1 rounded text-xs hover:bg-red-600"
                      >
                        Delete
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        );
      case 'menu':
        return (
          <div className="overflow-x-auto">
            <table className="min-w-full bg-white border">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-4 py-2 border text-left">ID</th>
                  <th className="px-4 py-2 border text-left">Title</th>
                  <th className="px-4 py-2 border text-left">Price</th>
                  <th className="px-4 py-2 border text-left">Available</th>
                  <th className="px-4 py-2 border text-left">Actions</th>
                </tr>
              </thead>
              <tbody>
                {menuItems.map((item) => (
                  <tr key={item.id} className="hover:bg-gray-50">
                    <td className="px-4 py-2 border">{item.id}</td>
                    <td className="px-4 py-2 border">{item.title}</td>
                    <td className="px-4 py-2 border">${item.price}</td>
                    <td className="px-4 py-2 border">{item.is_available ? 'Yes' : 'No'}</td>
                    <td className="px-4 py-2 border">
                      <button
                        onClick={() => deleteMenuItem(item.id)}
                        className="bg-red-500 text-white px-2 py-1 rounded text-xs hover:bg-red-600"
                      >
                        Delete
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        );
      case 'orders':
        return (
          <div className="overflow-x-auto">
            <table className="min-w-full bg-white border">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-4 py-2 border text-left">ID</th>
                  <th className="px-4 py-2 border text-left">Menu Item</th>
                  <th className="px-4 py-2 border text-left">Quantity</th>
                  <th className="px-4 py-2 border text-left">Status</th>
                  <th className="px-4 py-2 border text-left">Total</th>
                  <th className="px-4 py-2 border text-left">Actions</th>
                </tr>
              </thead>
              <tbody>
                {orders.map((order) => (
                  <tr key={order.id} className="hover:bg-gray-50">
                    <td className="px-4 py-2 border">{order.id}</td>
                    <td className="px-4 py-2 border">{order.menu_item_id}</td>
                    <td className="px-4 py-2 border">{order.quantity}</td>
                    <td className="px-4 py-2 border">{order.status}</td>
                    <td className="px-4 py-2 border">${order.total_price}</td>
                    <td className="px-4 py-2 border">
                      <button
                        onClick={() => deleteOrder(order.id)}
                        className="bg-red-500 text-white px-2 py-1 rounded text-xs hover:bg-red-600"
                      >
                        Delete
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        );
      case 'messages':
        return (
          <div className="overflow-x-auto">
            <table className="min-w-full bg-white border">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-4 py-2 border text-left">ID</th>
                  <th className="px-4 py-2 border text-left">Order ID</th>
                  <th className="px-4 py-2 border text-left">Sender ID</th>
                  <th className="px-4 py-2 border text-left">Content</th>
                  <th className="px-4 py-2 border text-left">Created</th>
                </tr>
              </thead>
              <tbody>
                {messages.map((message) => (
                  <tr key={message.id} className="hover:bg-gray-50">
                    <td className="px-4 py-2 border">{message.id}</td>
                    <td className="px-4 py-2 border">{message.order_id}</td>
                    <td className="px-4 py-2 border">{message.sender_id}</td>
                    <td className="px-4 py-2 border">{message.content}</td>
                    <td className="px-4 py-2 border">{new Date(message.created_at).toLocaleString()}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        );
    }
  };

  return (
    <div className="bg-white p-6 rounded-lg shadow-md">
      <h2 className="text-xl font-bold text-gray-800 mb-4">API Operations & Data</h2>
      
      {/* Status */}
      {status && (
        <div className="mb-4 p-3 bg-blue-50 border border-blue-200 rounded">
          <p className="text-blue-800">{status}</p>
        </div>
      )}

      {/* Tabs */}
      <div className="flex space-x-1 mb-4">
        {(['cooks', 'menu', 'orders', 'messages'] as const).map((tab) => (
          <button
            key={tab}
            onClick={() => setActiveTab(tab)}
            className={`px-4 py-2 rounded ${
              activeTab === tab
                ? 'bg-blue-500 text-white'
                : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
            }`}
          >
            {tab.charAt(0).toUpperCase() + tab.slice(1)}
          </button>
        ))}
      </div>

      {/* CRUD Buttons */}
      {renderCrudButtons()}

      {/* Create Form */}
      {renderCreateForm()}

      {/* Loading indicator */}
      {loading && (
        <div className="flex items-center justify-center py-4">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
          <span className="ml-2">Loading...</span>
        </div>
      )}

      {/* Data Table */}
      {!loading && renderDataTable()}
    </div>
  );
} 