'use client';

import React, { useState, useEffect } from 'react';
import { apiClient } from '@/lib/api';
import { CookProfile, MenuItem } from '@/types/api';

interface CartItem {
  menuItem: MenuItem;
  quantity: number;
  specialInstructions: string;
}

export default function MenusTab() {
  const [cooks, setCooks] = useState<CookProfile[]>([]);
  const [menuItems, setMenuItems] = useState<MenuItem[]>([]);
  const [selectedCook, setSelectedCook] = useState<CookProfile | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [isLoadingMenu, setIsLoadingMenu] = useState(false);
  const [cart, setCart] = useState<CartItem[]>([]);
  const [showCart, setShowCart] = useState(false);
  const [showOrderDialog, setShowOrderDialog] = useState(false);
  const [selectedMenuItem, setSelectedMenuItem] = useState<MenuItem | null>(null);

  useEffect(() => {
    loadCooks();
  }, []);

  const loadCooks = async () => {
    setIsLoading(true);
    const response = await apiClient.getCookProfiles();
    if (response.data) {
      setCooks(response.data);
    }
    setIsLoading(false);
  };

  const loadCookMenu = async (cook: CookProfile) => {
    setSelectedCook(cook);
    setIsLoadingMenu(true);
    const response = await apiClient.getCookMenuItems(cook.id);
    if (response.data) {
      setMenuItems(response.data);
    } else {
      setMenuItems([]);
    }
    setIsLoadingMenu(false);
  };

  const addToCart = (menuItem: MenuItem, quantity: number, specialInstructions: string) => {
    // Check if cart is empty or if item is from the same cook as existing items
    if (cart.length > 0) {
      const currentCookId = cart[0].menuItem.cook_id;
      if (menuItem.cook_id !== currentCookId) {
        const currentCookName = selectedCook?.name || 'this cook';
        alert(`🛒 You can only order from one cook at a time. Your cart currently contains items from ${currentCookName}. Please complete that order first or clear your cart.`);
        return;
      }
    }
    
    const existingItemIndex = cart.findIndex(item => item.menuItem.id === menuItem.id);
    
    if (existingItemIndex >= 0) {
      const updatedCart = [...cart];
      updatedCart[existingItemIndex].quantity += quantity;
      if (specialInstructions) {
        updatedCart[existingItemIndex].specialInstructions = specialInstructions;
      }
      setCart(updatedCart);
    } else {
      setCart([...cart, { menuItem, quantity, specialInstructions }]);
    }
    setShowOrderDialog(false);
    setSelectedMenuItem(null);
  };

  const removeFromCart = (menuItemId: number) => {
    setCart(cart.filter(item => item.menuItem.id !== menuItemId));
  };

  const updateCartQuantity = (menuItemId: number, newQuantity: number) => {
    if (newQuantity <= 0) {
      removeFromCart(menuItemId);
      return;
    }
    
    setCart(cart.map(item => 
      item.menuItem.id === menuItemId 
        ? { ...item, quantity: newQuantity }
        : item
    ));
  };

  const getCartTotal = () => {
    return cart.reduce((total, item) => {
      const price = typeof item.menuItem.price === 'number' ? item.menuItem.price : parseFloat(item.menuItem.price as string) || 0;
      return total + (price * item.quantity);
    }, 0);
  };

  const placeOrder = async () => {
    if (cart.length === 0) return;

    const orderItems = cart.map(item => ({
      menu_item_id: item.menuItem.id,
      quantity: item.quantity,
      special_instructions: item.specialInstructions || undefined
    }));

    try {
      const response = await apiClient.createBatchOrder(orderItems);
      
      if (response.error) {
        alert(`Failed to place order: ${response.error}`);
      } else {
        alert('🎉 Order placed successfully!');
        setCart([]);
        setShowCart(false);
      }
    } catch (error) {
      alert('Failed to place order');
    }
  };

  if (isLoading) {
    return (
      <div className="text-center py-8">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto mb-4"></div>
        <p className="text-gray-600">Loading cooks...</p>
      </div>
    );
  }

  return (
    <div className="relative">
      {/* Shopping Cart Button */}
      {cart.length > 0 && (
        <div className="fixed top-4 right-4 z-40 flex flex-col gap-2">
          <button
            onClick={() => setShowCart(true)}
            className="bg-blue-600 text-white p-3 rounded-full shadow-lg hover:bg-blue-700 transition-colors relative"
          >
            🛒
            <span className="absolute -top-2 -right-2 bg-red-500 text-white text-xs w-6 h-6 rounded-full flex items-center justify-center">
              {cart.reduce((sum, item) => sum + item.quantity, 0)}
            </span>
          </button>
          <button
            onClick={() => {
              if (confirm('Are you sure you want to clear your cart?')) {
                setCart([]);
              }
            }}
            className="bg-red-500 text-white px-3 py-1 rounded-lg text-xs hover:bg-red-600 transition-colors shadow-lg"
          >
            Clear Cart
          </button>
        </div>
      )}

      <h2 className="text-2xl font-bold text-gray-900 mb-6">Browse Local Menus</h2>
      
      {!selectedCook ? (
        <div>
          <p className="text-gray-600 mb-6">
            Discover delicious meals from local home cooks in your area.
          </p>
          
          {cooks.length === 0 ? (
            <div className="text-center py-12">
              <div className="text-6xl mb-4">🍳</div>
              <p className="text-gray-500">No cooks available yet. Be the first to create a cook profile!</p>
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {cooks.map((cook) => (
                <div key={cook.id} className="bg-white border rounded-xl p-6 hover:shadow-lg transition-shadow">
                  <div className="flex items-center mb-4">
                    {cook.photo_url ? (
                      <img 
                        src={cook.photo_url} 
                        alt={cook.name}
                        className="w-12 h-12 rounded-full object-cover mr-4"
                      />
                    ) : (
                      <div className="w-12 h-12 rounded-full bg-gray-200 flex items-center justify-center mr-4">
                        <span className="text-gray-600 text-lg">👨‍🍳</span>
                      </div>
                    )}
                    <div>
                      <h3 className="text-lg font-semibold text-gray-900">{cook.name}</h3>
                      <p className="text-sm text-gray-500">
                        Delivers within {cook.delivery_radius} miles
                      </p>
                    </div>
                  </div>
                  
                  {cook.bio && (
                    <p className="text-gray-600 mb-4 text-sm">{cook.bio}</p>
                  )}
                  
                  <button
                    onClick={() => loadCookMenu(cook)}
                    className="w-full bg-blue-600 text-white py-2 px-4 rounded-lg hover:bg-blue-700 transition-colors"
                  >
                    View Menu
                  </button>
                </div>
              ))}
            </div>
          )}
        </div>
      ) : (
        <div>
          <div className="flex items-center justify-between mb-6">
            <div className="flex items-center">
              <button
                onClick={() => {
                  setSelectedCook(null);
                  setMenuItems([]);
                }}
                className="mr-4 text-blue-600 hover:text-blue-700 flex items-center gap-1"
              >
                ← Back to Cooks
              </button>
              <div className="flex items-center">
                {selectedCook.photo_url ? (
                  <img 
                    src={selectedCook.photo_url} 
                    alt={selectedCook.name}
                    className="w-10 h-10 rounded-full object-cover mr-3"
                  />
                ) : (
                  <div className="w-10 h-10 rounded-full bg-gray-200 flex items-center justify-center mr-3">
                    <span className="text-gray-600">👨‍🍳</span>
                  </div>
                )}
                <div>
                  <h3 className="text-xl font-bold text-gray-900">{selectedCook.name}</h3>
                  <p className="text-sm text-gray-500">
                    Delivers within {selectedCook.delivery_radius} miles
                  </p>
                </div>
              </div>
            </div>
          </div>

          {isLoadingMenu ? (
            <div className="text-center py-8">
              <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto mb-4"></div>
              <p className="text-gray-600">Loading menu...</p>
            </div>
          ) : menuItems.length === 0 ? (
            <div className="text-center py-12">
              <div className="text-6xl mb-4">🍽️</div>
              <p className="text-gray-500">This cook hasn't added any menu items yet.</p>
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {menuItems.map((item) => (
                <div key={item.id} className="bg-white border rounded-xl overflow-hidden hover:shadow-lg transition-shadow">
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
                      
                      <button
                        onClick={() => {
                          setSelectedMenuItem(item);
                          setShowOrderDialog(true);
                        }}
                        disabled={!item.is_available}
                        className="bg-blue-600 text-white py-2 px-4 rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                      >
                        Add to Cart
                      </button>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      )}

      {/* Order Dialog */}
      {showOrderDialog && selectedMenuItem && (
        <OrderDialog
          menuItem={selectedMenuItem}
          onClose={() => {
            setShowOrderDialog(false);
            setSelectedMenuItem(null);
          }}
          onAddToCart={addToCart}
        />
      )}

      {/* Shopping Cart */}
      {showCart && (
        <ShoppingCart
          cart={cart}
          onClose={() => setShowCart(false)}
          onUpdateQuantity={updateCartQuantity}
          onRemoveItem={removeFromCart}
          onPlaceOrders={placeOrder}
          total={getCartTotal()}
          cookName={selectedCook?.name || (cart.length > 0 ? `Cook ID ${cart[0].menuItem.cook_id}` : '')}
        />
      )}
    </div>
  );
}

// Order Dialog Component
function OrderDialog({ 
  menuItem, 
  onClose, 
  onAddToCart 
}: { 
  menuItem: MenuItem; 
  onClose: () => void; 
  onAddToCart: (menuItem: MenuItem, quantity: number, specialInstructions: string) => void;
}) {
  const [quantity, setQuantity] = useState(1);
  const [specialInstructions, setSpecialInstructions] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onAddToCart(menuItem, quantity, specialInstructions);
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
      <div className="bg-white rounded-2xl p-6 w-full max-w-md shadow-2xl">
        <div className="text-center mb-4">
          <h3 className="text-xl font-bold text-gray-900">{menuItem.title}</h3>
          <p className="text-2xl font-bold text-green-600">${(typeof menuItem.price === 'number' ? menuItem.price : parseFloat(menuItem.price as string) || 0).toFixed(2)}</p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Quantity
            </label>
            <div className="flex items-center gap-3">
              <button
                type="button"
                onClick={() => setQuantity(Math.max(1, quantity - 1))}
                className="w-8 h-8 rounded-full bg-gray-200 flex items-center justify-center hover:bg-gray-300"
              >
                -
              </button>
              <span className="text-lg font-semibold w-8 text-center">{quantity}</span>
              <button
                type="button"
                onClick={() => setQuantity(quantity + 1)}
                className="w-8 h-8 rounded-full bg-gray-200 flex items-center justify-center hover:bg-gray-300"
              >
                +
              </button>
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Special Instructions (Optional)
            </label>
            <textarea
              value={specialInstructions}
              onChange={(e) => setSpecialInstructions(e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              rows={3}
              placeholder="Any special requests or dietary notes..."
            />
          </div>

          <div className="bg-gray-50 p-3 rounded-lg">
            <div className="flex justify-between items-center">
              <span className="font-medium">Subtotal:</span>
              <span className="text-lg font-bold text-green-600">
                ${((typeof menuItem.price === 'number' ? menuItem.price : parseFloat(menuItem.price as string) || 0) * quantity).toFixed(2)}
              </span>
            </div>
          </div>

          <div className="flex gap-3">
            <button
              type="button"
              onClick={onClose}
              className="flex-1 bg-gray-100 text-gray-700 py-2 px-4 rounded-lg hover:bg-gray-200"
            >
              Cancel
            </button>
            <button
              type="submit"
              className="flex-1 bg-blue-600 text-white py-2 px-4 rounded-lg hover:bg-blue-700"
            >
              Add to Cart
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}

// Shopping Cart Component
function ShoppingCart({
  cart,
  onClose,
  onUpdateQuantity,
  onRemoveItem,
  onPlaceOrders,
  total,
  cookName
}: {
  cart: CartItem[];
  onClose: () => void;
  onUpdateQuantity: (menuItemId: number, newQuantity: number) => void;
  onRemoveItem: (menuItemId: number) => void;
  onPlaceOrders: () => void;
  total: number;
  cookName: string;
}) {
  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
      <div className="bg-white rounded-2xl p-6 w-full max-w-2xl max-h-[90vh] overflow-y-auto shadow-2xl">
        <div className="flex justify-between items-center mb-6">
          <div>
            <h3 className="text-2xl font-bold text-gray-900">🛒 Your Cart</h3>
            {cart.length > 0 && cookName && (
              <p className="text-sm text-gray-600 mt-1">
                Ordering from: <span className="font-semibold">{cookName}</span>
              </p>
            )}
          </div>
          <button
            onClick={onClose}
            className="text-gray-500 hover:text-gray-700 text-2xl"
          >
            ×
          </button>
        </div>

        {cart.length === 0 ? (
          <div className="text-center py-8">
            <div className="text-6xl mb-4">🛒</div>
            <p className="text-gray-500">Your cart is empty</p>
          </div>
        ) : (
          <>
            <div className="space-y-4 mb-6">
              {cart.map((item) => (
                <div key={item.menuItem.id} className="border rounded-lg p-4">
                  <div className="flex justify-between items-start mb-2">
                    <div>
                      <h4 className="font-semibold text-gray-900">{item.menuItem.title}</h4>
                      <p className="text-sm text-gray-600">${(typeof item.menuItem.price === 'number' ? item.menuItem.price : parseFloat(item.menuItem.price as string) || 0).toFixed(2)} each</p>
                    </div>
                    <button
                      onClick={() => onRemoveItem(item.menuItem.id)}
                      className="text-red-500 hover:text-red-700"
                    >
                      🗑️
                    </button>
                  </div>

                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-3">
                      <button
                        onClick={() => onUpdateQuantity(item.menuItem.id, item.quantity - 1)}
                        className="w-8 h-8 rounded-full bg-gray-200 flex items-center justify-center hover:bg-gray-300"
                      >
                        -
                      </button>
                      <span className="font-semibold w-8 text-center">{item.quantity}</span>
                      <button
                        onClick={() => onUpdateQuantity(item.menuItem.id, item.quantity + 1)}
                        className="w-8 h-8 rounded-full bg-gray-200 flex items-center justify-center hover:bg-gray-300"
                      >
                        +
                      </button>
                    </div>
                    <span className="font-bold text-green-600">
                      ${((typeof item.menuItem.price === 'number' ? item.menuItem.price : parseFloat(item.menuItem.price as string) || 0) * item.quantity).toFixed(2)}
                    </span>
                  </div>

                  {item.specialInstructions && (
                    <div className="mt-2 p-2 bg-yellow-50 rounded text-sm">
                      <strong>Special instructions:</strong> {item.specialInstructions}
                    </div>
                  )}
                </div>
              ))}
            </div>

            <div className="border-t pt-4">
              <div className="flex justify-between items-center mb-4">
                <span className="text-xl font-bold">Total:</span>
                <span className="text-2xl font-bold text-green-600">
                  ${total.toFixed(2)}
                </span>
              </div>

              <div className="flex gap-3">
                <button
                  onClick={onClose}
                  className="flex-1 bg-gray-100 text-gray-700 py-3 px-4 rounded-lg hover:bg-gray-200"
                >
                  Continue Shopping
                </button>
                <button
                  onClick={onPlaceOrders}
                  className="flex-1 bg-green-600 text-white py-3 px-4 rounded-lg hover:bg-green-700 font-semibold"
                >
                  🚀 Place Order
                </button>
              </div>
            </div>
          </>
        )}
      </div>
    </div>
  );
} 