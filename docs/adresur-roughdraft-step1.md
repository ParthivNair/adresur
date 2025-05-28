# Step 1: Rough Draft Backend Plan (Adresur)

This document outlines the first development milestone for Adresur: building a **rough draft backend** with mock data structures and core logic. The goal is to create a functional prototype of the core classes and relationships **without worrying about APIs or databases yet**.

---

## 🎯 Goals

✅ **Create basic class structures** for Users, CookProfiles, Dishes, and Orders.  
✅ **Establish clear relationships** between these classes (like dishes belonging to cooks, orders tied to buyers and cooks).  
✅ **Implement CRUD-like methods** in plain Python (create, read, update, delete).  
✅ **Test with mock data** — no real database or API calls.

---

## 🛠️ Core Classes & Fields

### `User`
- `id` (int or UUID)
- `name` (string)
- `email` (string)
- `role` (enum: buyer, cook, admin)
- `profile_picture` (optional string)
- `created_at` (timestamp)

### `CookProfile`
- `id` (int or UUID)
- `user_id` (link to User)
- `bio` (text)
- `kitchen_photos` (list of strings)
- `delivery_radius` (int)
- `is_verified` (boolean)
- `created_at` (timestamp)

### `Dish`
- `id` (int or UUID)
- `cook_id` (link to CookProfile)
- `title` (string)
- `description` (text)
- `price` (decimal)
- `available` (boolean)
- `photo_url` (string)

### `Order`
- `id` (int or UUID)
- `buyer_id` (link to User)
- `cook_id` (link to CookProfile)
- `status` (enum: pending, accepted, preparing, out_for_delivery, completed, cancelled)
- `total_price` (decimal)
- `delivery_address` (string)
- `delivery_instructions` (text)
- `placed_at` (timestamp)

---

## 🚦 Development Plan for Flight

✅ **Hour 1**: Draft all core classes as Python classes with relationships.  
✅ **Hour 2**: Implement create, read, update, delete methods.  
✅ **Hour 3**: Test with mock data and print outputs to validate relationships.

---

## 📝 Next Steps After Flight

- Move core logic to API endpoints (FastAPI or similar).  
- Integrate Supabase or Postgres for persistent storage.  
- Build minimal frontend to consume these APIs.

---

**Adresur’s first step: laying the foundation for everything to come.**

