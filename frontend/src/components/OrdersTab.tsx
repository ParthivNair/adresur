'use client';

import React, { useState, useEffect } from 'react';
import { apiClient } from '@/lib/api';

interface OrdersTabProps {
  isCook: boolean;
}

interface EnhancedOrder {
  id: number;
  buyer_id: number;
  cook_id: number;
  menu_item_id: number;
  quantity: number;
  status: string;
  total_price: number;
  special_instructions?: string;
  created_at: string;
  updated_at: string;
  menuItem?: {
    id: number;
    title: string;
    description: string;
    price: number;
    photo_url?: string;
  };
  cook_name?: string;
  cook_full_name?: string;
  buyer_name?: string;
  buyer_email?: string;
}

export default function OrdersTab({ isCook }: OrdersTabProps) {
  const [orders, setOrders] = useState<EnhancedOrder[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [statusFilter, setStatusFilter] = useState<string>('all');
  const [showStatusDialog, setShowStatusDialog] = useState(false);
  const [selectedOrder, setSelectedOrder] = useState<EnhancedOrder | null>(null);
  const [analytics, setAnalytics] = useState<{
    totalOrders: number;
    totalRevenue: number;
    popularItems: { [key: string]: number };
  }>({
    totalOrders: 0,
    totalRevenue: 0,
    popularItems: {}
  });

  useEffect(() => {
    loadOrders();
  }, [isCook]);

  const loadOrders = async () => {
    setIsLoading(true);
    const response = await apiClient.getOrders(isCook);
    if (response.data) {
      setOrders(response.data);
      if (isCook) {
        calculateAnalytics(response.data);
      }
    }
    setIsLoading(false);
  };

  const calculateAnalytics = (orders: EnhancedOrder[]) => {
    const completedOrders = orders.filter(order => order.status === 'completed');
    const totalRevenue = completedOrders.reduce((sum, order) => {
      const price = typeof order.total_price === 'number' ? order.total_price : parseFloat(order.total_price as string) || 0;
      return sum + price;
    }, 0);
    
    const itemCounts: { [key: string]: number } = {};
    orders.forEach(order => {
      const itemId = order.menu_item_id.toString();
      itemCounts[itemId] = (itemCounts[itemId] || 0) + order.quantity;
    });

    setAnalytics({
      totalOrders: orders.length,
      totalRevenue: totalRevenue,
      popularItems: itemCounts
    });
  };

  const updateOrderStatus = async (orderId: number, newStatus: string) => {
    const response = await apiClient.updateOrder(orderId, { status: newStatus });
    if (response.error) {
      alert('Failed to update order: ' + response.error);
    } else {
      loadOrders(); // Refresh orders
      setShowStatusDialog(false);
      setSelectedOrder(null);
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'pending':
        return 'bg-yellow-100 text-yellow-800 border-yellow-200';
      case 'preparing':
        return 'bg-blue-100 text-blue-800 border-blue-200';
      case 'ready':
        return 'bg-green-100 text-green-800 border-green-200';
      case 'completed':
        return 'bg-gray-100 text-gray-800 border-gray-200';
      case 'cancelled':
        return 'bg-red-100 text-red-800 border-red-200';
      default:
        return 'bg-gray-100 text-gray-800 border-gray-200';
    }
  };

  const getStatusEmoji = (status: string) => {
    switch (status) {
      case 'pending':
        return '⏳';
      case 'preparing':
        return '👨‍🍳';
      case 'ready':
        return '✅';
      case 'completed':
        return '🎉';
      case 'cancelled':
        return '❌';
      default:
        return '📦';
    }
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  // Utility function to safely format prices
  const formatPrice = (price: number | string): string => {
    const numPrice = typeof price === 'number' ? price : parseFloat(price as string) || 0;
    return numPrice.toFixed(2);
  };

  const filteredOrders = statusFilter === 'all' 
    ? orders 
    : orders.filter(order => order.status === statusFilter);

  const getStatusCounts = () => {
    return {
      all: orders.length,
      pending: orders.filter(o => o.status === 'pending').length,
      preparing: orders.filter(o => o.status === 'preparing').length,
      ready: orders.filter(o => o.status === 'ready').length,
      completed: orders.filter(o => o.status === 'completed').length,
      cancelled: orders.filter(o => o.status === 'cancelled').length,
    };
  };

  if (isLoading) {
    return (
      <div className="text-center py-8">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto mb-4"></div>
        <p className="text-gray-600">Loading orders...</p>
      </div>
    );
  }

  const statusCounts = getStatusCounts();

  return (
    <div>
      <h2 className="text-2xl font-bold text-gray-900 mb-6">
        {isCook ? '👨‍🍳 Cook Orders Dashboard' : '📦 My Orders'}
      </h2>

      {isCook && (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <div className="bg-blue-50 p-6 rounded-xl border border-blue-200">
            <div className="flex items-center justify-between">
              <div>
                <h3 className="font-semibold text-blue-800 mb-1">Total Orders</h3>
                <p className="text-3xl font-bold text-blue-600">{analytics.totalOrders}</p>
              </div>
              <div className="text-3xl">📊</div>
            </div>
          </div>
          <div className="bg-green-50 p-6 rounded-xl border border-green-200">
            <div className="flex items-center justify-between">
              <div>
                <h3 className="font-semibold text-green-800 mb-1">Total Revenue</h3>
                <p className="text-3xl font-bold text-green-600">
                  ${(analytics.totalRevenue || 0).toFixed(2)}
                </p>
              </div>
              <div className="text-3xl">💰</div>
            </div>
          </div>
          <div className="bg-purple-50 p-6 rounded-xl border border-purple-200">
            <div className="flex items-center justify-between">
              <div>
                <h3 className="font-semibold text-purple-800 mb-1">Active Orders</h3>
                <p className="text-3xl font-bold text-purple-600">
                  {orders.filter(o => ['pending', 'preparing', 'ready'].includes(o.status)).length}
                </p>
              </div>
              <div className="text-3xl">🔥</div>
            </div>
          </div>
        </div>
      )}

      {/* Status Filter Tabs */}
      <div className="flex flex-wrap gap-2 mb-6">
        {[
          { key: 'all', label: 'All Orders', count: statusCounts.all },
          { key: 'pending', label: 'Pending', count: statusCounts.pending, emoji: '⏳' },
          { key: 'preparing', label: 'Preparing', count: statusCounts.preparing, emoji: '👨‍🍳' },
          { key: 'ready', label: 'Ready', count: statusCounts.ready, emoji: '✅' },
          { key: 'completed', label: 'Completed', count: statusCounts.completed, emoji: '🎉' },
          { key: 'cancelled', label: 'Cancelled', count: statusCounts.cancelled, emoji: '❌' },
        ].map((filter) => (
          <button
            key={filter.key}
            onClick={() => setStatusFilter(filter.key)}
            className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
              statusFilter === filter.key
                ? 'bg-blue-600 text-white'
                : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
            }`}
          >
            {filter.emoji && <span className="mr-1">{filter.emoji}</span>}
            {filter.label} ({filter.count})
          </button>
        ))}
      </div>

      {filteredOrders.length === 0 ? (
        <div className="text-center py-12 bg-gray-50 rounded-xl">
          <div className="text-6xl mb-4">
            {statusFilter === 'all' ? '📦' : getStatusEmoji(statusFilter)}
          </div>
          <h3 className="text-xl font-semibold text-gray-700 mb-2">
            {statusFilter === 'all' 
              ? (isCook ? 'No orders received yet.' : 'You haven\'t placed any orders yet.')
              : `No ${statusFilter} orders found.`
            }
          </h3>
          <p className="text-gray-500">
            {statusFilter === 'all' && !isCook && 'Browse menus to place your first order!'}
          </p>
        </div>
      ) : (
        <div className="space-y-4">
          {filteredOrders.map((order) => (
            <div key={order.id} className="bg-white border rounded-xl p-6 hover:shadow-lg transition-shadow">
              <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-4">
                {/* Order Header */}
                <div className="flex items-start gap-4">
                  <div className="flex-shrink-0">
                    <div className={`px-3 py-2 rounded-lg text-sm font-medium border ${getStatusColor(order.status)}`}>
                      <span className="mr-1">{getStatusEmoji(order.status)}</span>
                      {order.status.charAt(0).toUpperCase() + order.status.slice(1)}
                    </div>
                  </div>
                  
                  <div className="flex-1">
                    <div className="flex items-center gap-2 mb-1">
                      <h3 className="text-lg font-semibold text-gray-900">
                        Order #{order.id}
                      </h3>
                      <span className="text-2xl font-bold text-green-600">
                        ${formatPrice(order.total_price)}
                      </span>
                    </div>
                    <p className="text-sm text-gray-500">
                      {formatDate(order.created_at)}
                    </p>
                  </div>
                </div>

                {/* Order Actions for Cooks */}
                {isCook && order.status !== 'completed' && order.status !== 'cancelled' && (
                  <div className="flex gap-2">
                    <button
                      onClick={() => {
                        setSelectedOrder(order);
                        setShowStatusDialog(true);
                      }}
                      className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 text-sm"
                    >
                      Update Status
                    </button>
                  </div>
                )}
              </div>

              {/* Order Details */}
              <div className="mt-4 pt-4 border-t border-gray-100">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <h4 className="font-medium text-gray-900 mb-2">🍽️ Menu Item</h4>
                    {order.menuItem ? (
                      <div className="bg-gray-50 p-3 rounded-lg">
                        <p className="font-semibold text-gray-900">{order.menuItem.title}</p>
                        <p className="text-sm text-gray-600">{order.menuItem.description}</p>
                        <div className="flex justify-between items-center mt-2">
                          <span className="text-sm text-gray-500">
                            ${formatPrice(order.menuItem.price)} × {order.quantity}
                          </span>
                          <span className="font-semibold text-green-600">
                            ${formatPrice((typeof order.menuItem.price === 'number' ? order.menuItem.price : parseFloat(order.menuItem.price as string) || 0) * order.quantity)}
                          </span>
                        </div>
                      </div>
                    ) : (
                      <div className="bg-gray-50 p-3 rounded-lg">
                        <p className="text-gray-500">Menu item details not available</p>
                        <p className="text-sm text-gray-500">Quantity: {order.quantity}</p>
                      </div>
                    )}
                  </div>

                  <div>
                    <div className="space-y-3">
                      <div>
                        <h4 className="font-medium text-gray-900 mb-1">
                          {isCook ? '👤 Customer' : '👨‍🍳 Cook'}
                        </h4>
                        {isCook ? (
                          <div>
                            <p className="text-sm text-gray-600">{order.buyer_name}</p>
                            <p className="text-xs text-gray-500">{order.buyer_email}</p>
                          </div>
                        ) : (
                          <div>
                            <p className="text-sm text-gray-600">{order.cook_name}</p>
                            <p className="text-xs text-gray-500">{order.cook_full_name}</p>
                          </div>
                        )}
                      </div>

                      {order.special_instructions && (
                        <div>
                          <h4 className="font-medium text-gray-900 mb-1">📝 Special Instructions</h4>
                          <div className="bg-yellow-50 border border-yellow-200 p-3 rounded-lg">
                            <p className="text-sm text-gray-700">{order.special_instructions}</p>
                          </div>
                        </div>
                      )}
                    </div>
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Status Update Dialog */}
      {showStatusDialog && selectedOrder && (
        <StatusUpdateDialog
          order={selectedOrder}
          onClose={() => {
            setShowStatusDialog(false);
            setSelectedOrder(null);
          }}
          onUpdate={updateOrderStatus}
        />
      )}
    </div>
  );
}

// Status Update Dialog Component
function StatusUpdateDialog({ 
  order, 
  onClose, 
  onUpdate 
}: { 
  order: EnhancedOrder; 
  onClose: () => void; 
  onUpdate: (orderId: number, status: string) => void;
}) {
  const statusOptions = [
    { value: 'preparing', label: '👨‍🍳 Start Preparing', color: 'bg-blue-600' },
    { value: 'ready', label: '✅ Mark as Ready', color: 'bg-green-600' },
    { value: 'completed', label: '🎉 Complete Order', color: 'bg-purple-600' },
    { value: 'cancelled', label: '❌ Cancel Order', color: 'bg-red-600' },
  ];

  const problemOptions = [
    { value: 'cancelled', label: '🔴 Out of ingredients' },
    { value: 'cancelled', label: '⏰ Taking too long' },
    { value: 'cancelled', label: '🚫 Unable to fulfill' },
    { value: 'cancelled', label: '💸 Payment issue' },
  ];

  const [showProblems, setShowProblems] = useState(false);

  const handleStatusUpdate = (newStatus: string) => {
    onUpdate(order.id, newStatus);
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
      <div className="bg-white rounded-2xl p-6 w-full max-w-md shadow-2xl">
        <div className="text-center mb-6">
          <h3 className="text-xl font-bold text-gray-900 mb-2">
            Update Order #{order.id}
          </h3>
          <p className="text-gray-600">
            Current status: <span className="font-semibold">{order.status}</span>
          </p>
        </div>

        {!showProblems ? (
          <div className="space-y-3">
            {statusOptions
              .filter(option => {
                // Show relevant options based on current status
                if (order.status === 'pending') return ['preparing', 'cancelled'].includes(option.value);
                if (order.status === 'preparing') return ['ready', 'cancelled'].includes(option.value);
                if (order.status === 'ready') return ['completed', 'cancelled'].includes(option.value);
                return option.value === 'cancelled';
              })
              .map((option) => (
                <button
                  key={option.value}
                  onClick={() => {
                    if (option.value === 'cancelled') {
                      setShowProblems(true);
                    } else {
                      handleStatusUpdate(option.value);
                    }
                  }}
                  className={`w-full ${option.color} text-white py-3 px-4 rounded-lg hover:opacity-90 transition-opacity text-left`}
                >
                  {option.label}
                </button>
              ))}

            <button
              onClick={onClose}
              className="w-full bg-gray-100 text-gray-700 py-3 px-4 rounded-lg hover:bg-gray-200 transition-colors"
            >
              Cancel
            </button>
          </div>
        ) : (
          <div className="space-y-3">
            <div className="text-center mb-4">
              <h4 className="font-semibold text-gray-900">What's the problem?</h4>
            </div>

            {problemOptions.map((option, index) => (
              <button
                key={index}
                onClick={() => handleStatusUpdate(option.value)}
                className="w-full bg-red-100 text-red-800 py-3 px-4 rounded-lg hover:bg-red-200 transition-colors text-left"
              >
                {option.label}
              </button>
            ))}

            <button
              onClick={() => setShowProblems(false)}
              className="w-full bg-gray-100 text-gray-700 py-3 px-4 rounded-lg hover:bg-gray-200 transition-colors"
            >
              ← Back
            </button>
          </div>
        )}
      </div>
    </div>
  );
} 