# Adresur Context File

This document captures the foundational steps and feature roadmap for **Adresur**, a platform for home-cooked meals shared within local communities. It also provides high-level guidance on development priorities, helping maintain consistency and alignment throughout the project.

---

## 🥘 Mission & Core Idea

Adresur aims to connect home cooks with local families and individuals, offering affordable, fresh, home-cooked meals while reducing food waste. The platform focuses on authentic, small-batch cooking and community-driven sharing.

---

## 🏗️ Foundational Steps & Features

### Step 1: Core Idea & Legal Foundations

- **Mission clarity**: Adresur is a hyper-local meal-sharing app for home-cooked meals.
- **Licensing**: All code is proprietary ("All Rights Reserved").
- **Entity**: Brand named “Adresur” (not formally incorporated yet).

---

### Step 2: MVP (Minimum Viable Product) Core Features

- **User Registration**: Users can create accounts and log in securely.
- **Cook Profile**: Cooks create profiles with bios, photos, and delivery radius.
- **Menu Listings**: Cooks upload dish details (title, description, price, photo).
- **Order Placement**: Buyers can browse, select, and order dishes.
- **Order Status Tracking**: Orders move through clear status stages.
- **Payment Processing**: Integrated secure payments (e.g., Stripe/PayPal).
- **Basic Messaging**: Cooks and buyers can leave notes on orders.
- **Admin Dashboard**: View and manage all users, orders, and earnings.

---

### Step 3: Initial Safety & Compliance

- **Photo Evidence**: Cooks upload kitchen and dish prep photos for trust.
- **Cook Verification**: Manual or automated verification.
- **Terms/Privacy Policies**: Clear policies for legal compliance and user protection.

---

### Step 4: Delivery Logistics

- **Delivery Radius / Zip Codes**: Let cooks define delivery zones.
- **Delivery Coordination**: Manual or driver-based delivery support.
- **Delivery Status**: Real-time tracking for drivers.

---

### Step 5: Community & Reviews

- **Ratings & Reviews**: Buyers leave reviews for dishes and cooks.
- **Featured Cooks / Dishes**: Highlight popular cooks or dishes.

---

### Step 6: Business & Regulatory Support

- **Compliance Resource Center**: In-app guides for cottage food laws and safety.
- **Verification Reminders**: Automated alerts to update cook compliance info.

---

### Step 7: Scaling & Growth Features

- **Promotions & Discounts**: Allow cooks to offer discounts.
- **Subscription / Meal Plans**: Families can subscribe to meals from favorite cooks.
- **Referral / Loyalty Programs**: Encourage word-of-mouth growth.
- **Analytics Dashboard**: Insights for admins and cooks.

---

### Step 8: Automation & Support

- **Automated Messaging**: Order confirmations and delivery updates.
- **Help Center / Chatbot**: In-app help for common questions.

---

### Step 9: Future Innovations

- **AI Compliance Checks**: AI to verify kitchen cleanliness.
- **Community Events**: In-app events like local food fairs.
- **Partnerships**: Collaboration with local farms and delivery co-ops.

---

## 🔥 Initial Development Stack & Flow

- **Backend-first** development approach for stability.
- **Supabase** for free-tier relational database storage (Postgres-based).
- **FastAPI** (or similar Python-based framework) for backend APIs.
- **Frontend** to follow backend, using React and TailwindCSS.
- **Cursor** for fast iteration — context file always open for clear AI guidance.

---

## ✏️ Additional Notes

- All features listed here are **modular** — prioritize core flow first.
- “Context-first” approach: Cursor’s AI suggestions will be guided by this file.
- Future updates will extend this file as new features are defined or adjusted.

---

**Adresur** — Connecting kitchens, sharing stories.
