# Adresur API Testing Frontend

A Next.js frontend application for testing the Adresur API with authentication and real-time data visualization.

## Features

- **Login Interface**: Test user authentication with sample users
- **Status Indicator**: Visual feedback for login success/failure
- **CRUD Operations**: Test POST, GET, PUT, and DELETE operations
- **Real-time Data Tables**: View API responses in organized tables
- **Multiple Endpoints**: Test Cook Profiles, Menu Items, Orders, and Messages

## Quick Start

1. **Install dependencies**:

   ```bash
   npm install
   ```

2. **Start the development server**:

   ```bash
   npm run dev
   ```

3. **Open your browser** and navigate to `http://localhost:3000`

## Prerequisites

- Make sure your Adresur backend API is running on `http://localhost:8000`
- Ensure you have sample data loaded in your database

## Test Users

The application includes quick login buttons for these test users:

- **Admin**: `admin@adresur.com` / `admin123`
- **Maria Garcia**: `maria.garcia@email.com` / `password123`
- **John Chef**: `john.chef@email.com` / `password123`
- **Anna Baker**: `anna.baker@email.com` / `password123`
- **Carlos Cook**: `carlos.cook@email.com` / `password123`
- **Sarah Customer**: `sarah.customer@email.com` / `password123`

## Available Operations

### Cook Profiles

- View all cook profiles
- Create new cook profiles
- Delete existing profiles

### Menu Items

- Browse menu items
- Add new menu items
- Remove menu items

### Orders

- View order history
- Create new orders
- Cancel orders

### Messages

- View messages for orders
- Send new messages

## Technology Stack

- **Next.js 15** - React framework
- **TypeScript** - Type safety
- **Tailwind CSS** - Styling
- **React Hooks** - State management

## Development

This is a simple testing interface. For production use, you would want to add:

- Form validation
- Error handling improvements
- Loading states
- Pagination for large datasets
- More sophisticated UI components
- Unit tests
