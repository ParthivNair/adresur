export interface User {
  id: number;
  email: string;
  full_name: string;
  role: 'user' | 'admin';
  is_active: boolean;
  created_at: string;
}

export interface LoginRequest {
  email: string;
  password: string;
}

export interface LoginResponse {
  access_token: string;
  token_type: string;
}

export interface CookProfile {
  id: number;
  user_id: number;
  name: string;
  bio?: string;
  photo_url?: string;
  delivery_radius: number;
  created_at: string;
  updated_at: string;
}

export interface MenuItem {
  id: number;
  cook_id: number;
  title: string;
  description: string;
  price: number;
  photo_url?: string;
  is_available: boolean;
  created_at: string;
  updated_at: string;
}

export interface Order {
  id: number;
  buyer_id: number;
  cook_id: number;
  menu_item_id: number;
  quantity: number;
  status: 'pending' | 'preparing' | 'ready' | 'completed' | 'cancelled';
  total_price: number;
  special_instructions?: string;
  created_at: string;
  updated_at: string;
}

export interface Message {
  id: number;
  order_id: number;
  sender_id: number;
  content: string;
  created_at: string;
}

export interface ApiResponse<T> {
  data?: T;
  error?: string;
  status: number;
} 