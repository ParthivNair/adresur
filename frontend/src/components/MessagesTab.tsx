'use client';

import React, { useState, useEffect } from 'react';
import { apiClient } from '@/lib/api';
import { Message } from '@/types/api';

export default function MessagesTab() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);

  return (
    <div>
      <h2 className="text-2xl font-bold text-gray-900 mb-6">Messages</h2>
      
      <div className="bg-blue-50 border border-blue-200 rounded-lg p-6">
        <h3 className="text-lg font-semibold text-blue-800 mb-2">
          💬 Coming Soon
        </h3>
        <p className="text-blue-700 mb-4">
          Message functionality is under development. Soon you'll be able to:
        </p>
        <ul className="text-blue-600 space-y-2">
          <li>• Chat with cooks about your orders</li>
          <li>• Receive updates on order status</li>
          <li>• Ask questions about menu items</li>
          <li>• Get delivery notifications</li>
        </ul>
      </div>

      <div className="mt-6 text-center">
        <p className="text-gray-500">
          For now, you can contact cooks directly through their profiles or check your order status in the Orders tab.
        </p>
      </div>
    </div>
  );
} 