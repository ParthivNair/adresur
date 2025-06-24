import { LoginRequest, LoginResponse, User, CookProfile, MenuItem, Order, Message, ApiResponse } from '@/types/api';

const API_BASE_URL = 'http://localhost:8000';

class ApiClient {
  private token: string | null = null;

  constructor() {
    // Try to get token from localStorage on client side
    if (typeof window !== 'undefined') {
      this.token = localStorage.getItem('auth_token');
    }
  }

  setToken(token: string) {
    this.token = token;
    if (typeof window !== 'undefined') {
      localStorage.setItem('auth_token', token);
    }
  }

  clearToken() {
    this.token = null;
    if (typeof window !== 'undefined') {
      localStorage.removeItem('auth_token');
    }
  }

  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<ApiResponse<T>> {
    const url = `${API_BASE_URL}${endpoint}`;
    
    const headers: Record<string, string> = {
      'Content-Type': 'application/json',
      ...((options.headers as Record<string, string>) || {}),
    };

    if (this.token) {
      headers.Authorization = `Bearer ${this.token}`;
    }

    try {
      const response = await fetch(url, {
        ...options,
        headers,
      });

      const contentType = response.headers.get('content-type');
      let data;
      
      if (contentType && contentType.includes('application/json')) {
        data = await response.json();
      } else {
        data = await response.text();
      }

      if (!response.ok) {
        return {
          error: data.detail || data || 'Request failed',
          status: response.status,
        };
      }

      return {
        data,
        status: response.status,
      };
    } catch (error) {
      return {
        error: error instanceof Error ? error.message : 'Network error',
        status: 0,
      };
    }
  }

  // Auth endpoints
  async login(credentials: LoginRequest): Promise<ApiResponse<LoginResponse>> {
    return this.request<LoginResponse>('/auth/login', {
      method: 'POST',
      body: JSON.stringify(credentials),
    });
  }

  async register(userData: { email: string; full_name: string; password: string; role?: string }): Promise<ApiResponse<User>> {
    return this.request<User>('/auth/register', {
      method: 'POST',
      body: JSON.stringify(userData),
    });
  }

  // Cook profiles
  async getCookProfiles(): Promise<ApiResponse<CookProfile[]>> {
    return this.request<CookProfile[]>('/cooks/');
  }

  async getCookProfile(id: number): Promise<ApiResponse<CookProfile>> {
    return this.request<CookProfile>(`/cooks/${id}`);
  }

  async getMyCookProfile(): Promise<ApiResponse<CookProfile>> {
    return this.request<CookProfile>('/cooks/me/profile');
  }

  async createCookProfile(profile: { name: string; bio?: string; photo_url?: string; delivery_radius?: number }): Promise<ApiResponse<CookProfile>> {
    return this.request<CookProfile>('/cooks/', {
      method: 'POST',
      body: JSON.stringify(profile),
    });
  }

  async updateCookProfile(id: number, profile: Partial<{ name: string; bio: string; photo_url: string; delivery_radius: number }>): Promise<ApiResponse<CookProfile>> {
    return this.request<CookProfile>(`/cooks/${id}`, {
      method: 'PUT',
      body: JSON.stringify(profile),
    });
  }

  async deleteCookProfile(id: number): Promise<ApiResponse<void>> {
    return this.request<void>(`/cooks/${id}`, {
      method: 'DELETE',
    });
  }

  // Menu items
  async getMenuItems(): Promise<ApiResponse<MenuItem[]>> {
    return this.request<MenuItem[]>('/menu/');
  }

  async getMenuItem(id: number): Promise<ApiResponse<MenuItem>> {
    return this.request<MenuItem>(`/menu/${id}`);
  }

  async getCookMenuItems(cookId: number): Promise<ApiResponse<MenuItem[]>> {
    return this.request<MenuItem[]>(`/menu/cook/${cookId}`);
  }

  async createMenuItem(item: { title: string; description: string; price: number; photo_url?: string; is_available?: boolean }): Promise<ApiResponse<MenuItem>> {
    return this.request<MenuItem>('/menu/', {
      method: 'POST',
      body: JSON.stringify(item),
    });
  }

  async updateMenuItem(id: number, item: Partial<{ title: string; description: string; price: number; photo_url: string; is_available: boolean }>): Promise<ApiResponse<MenuItem>> {
    return this.request<MenuItem>(`/menu/${id}`, {
      method: 'PUT',
      body: JSON.stringify(item),
    });
  }

  async deleteMenuItem(id: number): Promise<ApiResponse<void>> {
    return this.request<void>(`/menu/${id}`, {
      method: 'DELETE',
    });
  }

  // Orders
  async getOrders(): Promise<ApiResponse<Order[]>> {
    return this.request<Order[]>('/orders/');
  }

  async getOrder(id: number): Promise<ApiResponse<Order>> {
    return this.request<Order>(`/orders/${id}`);
  }

  async createOrder(order: { menu_item_id: number; quantity?: number; special_instructions?: string }): Promise<ApiResponse<Order>> {
    return this.request<Order>('/orders/', {
      method: 'POST',
      body: JSON.stringify(order),
    });
  }

  async updateOrder(id: number, order: { status?: string; special_instructions?: string }): Promise<ApiResponse<Order>> {
    return this.request<Order>(`/orders/${id}`, {
      method: 'PUT',
      body: JSON.stringify(order),
    });
  }

  async deleteOrder(id: number): Promise<ApiResponse<void>> {
    return this.request<void>(`/orders/${id}`, {
      method: 'DELETE',
    });
  }

  // Messages
  async getMessages(orderId: number): Promise<ApiResponse<Message[]>> {
    return this.request<Message[]>(`/messages/order/${orderId}`);
  }

  async createMessage(message: { order_id: number; content: string }): Promise<ApiResponse<Message>> {
    return this.request<Message>('/messages/', {
      method: 'POST',
      body: JSON.stringify(message),
    });
  }

  // Health check
  async healthCheck(): Promise<ApiResponse<{ status: string }>> {
    return this.request<{ status: string }>('/health');
  }
}

export const apiClient = new ApiClient(); 