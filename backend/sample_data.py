#!/usr/bin/env python3
"""
Sample Data Generator for Adresur API Testing
This script provides sample data and functions to populate the database for testing.
"""

import requests
import json
import sys
from typing import Dict, List, Optional
import time

# API base URL
BASE_URL = "http://localhost:8000"

# Sample data collections
SAMPLE_USERS = [
    {
        "email": "admin@adresur.com",
        "full_name": "Admin User",
        "password": "admin123",
        "role": "admin"
    },
    {
        "email": "maria.garcia@email.com",
        "full_name": "Maria Garcia",
        "password": "password123",
        "role": "user"
    },
    {
        "email": "john.chef@email.com",
        "full_name": "John Smith",
        "password": "password123",
        "role": "user"
    },
    {
        "email": "anna.baker@email.com",
        "full_name": "Anna Baker",
        "password": "password123",
        "role": "user"
    },
    {
        "email": "carlos.cook@email.com",
        "full_name": "Carlos Rodriguez",
        "password": "password123",
        "role": "user"
    },
    {
        "email": "sarah.customer@email.com",
        "full_name": "Sarah Johnson",
        "password": "password123",
        "role": "user"
    },
    {
        "email": "mike.buyer@email.com",
        "full_name": "Mike Wilson",
        "password": "password123",
        "role": "user"
    }
]

SAMPLE_COOK_PROFILES = [
    {
        "email": "maria.garcia@email.com",
        "name": "Maria's Kitchen",
        "bio": "Authentic Mexican cuisine made with love and traditional family recipes. Specializing in tacos, enchiladas, and homemade salsas.",
        "photo_url": "https://images.unsplash.com/photo-1583394838336-acd977736f90?w=400",
        "delivery_radius": 8.0
    },
    {
        "email": "john.chef@email.com",
        "name": "Chef John's Bistro",
        "bio": "French-inspired dishes with a modern twist. Fresh ingredients sourced locally, perfect for fine dining at home.",
        "photo_url": "https://images.unsplash.com/photo-1566554273541-37a9ca77b91b?w=400",
        "delivery_radius": 10.0
    },
    {
        "email": "anna.baker@email.com",
        "name": "Anna's Sweet Treats",
        "bio": "Homemade desserts, cakes, and pastries. From birthday cakes to daily sweet treats, everything made fresh to order.",
        "photo_url": "https://images.unsplash.com/photo-1578985545062-69928b1d9587?w=400",
        "delivery_radius": 6.0
    },
    {
        "email": "carlos.cook@email.com",
        "name": "Carlos BBQ House",
        "bio": "Slow-cooked BBQ meats with secret dry rubs and sauces. Perfect for family gatherings and meat lovers.",
        "photo_url": "https://images.unsplash.com/photo-1555939594-58d7cb561ad1?w=400",
        "delivery_radius": 12.0
    }
]

SAMPLE_MENU_ITEMS = [
    # Maria's Kitchen items
    {
        "cook_email": "maria.garcia@email.com",
        "title": "Authentic Chicken Tacos (3 pack)",
        "description": "Three soft corn tortillas filled with seasoned grilled chicken, onions, cilantro, and lime. Served with homemade salsa verde.",
        "price": 12.99,
        "photo_url": "https://images.unsplash.com/photo-1565299624946-b28f40a0ca4b?w=400",
        "is_available": True
    },
    {
        "cook_email": "maria.garcia@email.com",
        "title": "Beef Enchiladas Rojas",
        "description": "Three corn tortillas filled with seasoned ground beef, topped with red enchilada sauce and melted cheese. Served with rice and beans.",
        "price": 15.50,
        "photo_url": "https://images.unsplash.com/photo-1599974579688-8dbdd335c77f?w=400",
        "is_available": True
    },
    {
        "cook_email": "maria.garcia@email.com",
        "title": "Vegetarian Quesadilla",
        "description": "Large flour tortilla filled with mixed vegetables, cheese, and black beans. Served with sour cream and guacamole.",
        "price": 10.99,
        "photo_url": "https://images.unsplash.com/photo-1618040996337-56904b7850b9?w=400",
        "is_available": True
    },
    
    # Chef John's Bistro items
    {
        "cook_email": "john.chef@email.com",
        "title": "Coq au Vin",
        "description": "Classic French braised chicken in red wine sauce with mushrooms, pearl onions, and herbs. Served with mashed potatoes.",
        "price": 24.99,
        "photo_url": "https://images.unsplash.com/photo-1604503468506-a8da13d82791?w=400",
        "is_available": True
    },
    {
        "cook_email": "john.chef@email.com",
        "title": "Pan-Seared Salmon",
        "description": "Fresh Atlantic salmon with lemon butter sauce, roasted vegetables, and wild rice pilaf.",
        "price": 22.50,
        "photo_url": "https://images.unsplash.com/photo-1467003909585-2f8a72700288?w=400",
        "is_available": True
    },
    {
        "cook_email": "john.chef@email.com",
        "title": "Beef Bourguignon",
        "description": "Tender beef braised in red wine with carrots, onions, and mushrooms. A French classic served with crusty bread.",
        "price": 26.99,
        "photo_url": "https://images.unsplash.com/photo-1574484284002-952d92456975?w=400",
        "is_available": False  # Currently not available
    },
    
    # Anna's Sweet Treats items
    {
        "cook_email": "anna.baker@email.com",
        "title": "Chocolate Chip Cookies (dozen)",
        "description": "Freshly baked chocolate chip cookies made with premium chocolate chips and vanilla. Soft and chewy texture.",
        "price": 8.99,
        "photo_url": "https://images.unsplash.com/photo-1499636136210-6f4ee915583e?w=400",
        "is_available": True
    },
    {
        "cook_email": "anna.baker@email.com",
        "title": "Red Velvet Cake Slice",
        "description": "Rich red velvet cake with cream cheese frosting. Moist, fluffy, and perfectly sweet.",
        "price": 6.50,
        "photo_url": "https://images.unsplash.com/photo-1586985289688-ca3cf47d3e6e?w=400",
        "is_available": True
    },
    {
        "cook_email": "anna.baker@email.com",
        "title": "Custom Birthday Cake (8 inch)",
        "description": "Custom decorated birthday cake. Choose your flavor and design. 24-hour advance notice required.",
        "price": 35.99,
        "photo_url": "https://images.unsplash.com/photo-1558618047-3c8c76ca7d13?w=400",
        "is_available": True
    },
    
    # Carlos BBQ House items
    {
        "cook_email": "carlos.cook@email.com",
        "title": "BBQ Ribs Full Rack",
        "description": "Full rack of baby back ribs with our signature dry rub, slow-smoked for 6 hours. Served with coleslaw and baked beans.",
        "price": 28.99,
        "photo_url": "https://images.unsplash.com/photo-1544025162-d76694265947?w=400",
        "is_available": True
    },
    {
        "cook_email": "carlos.cook@email.com",
        "title": "Pulled Pork Sandwich",
        "description": "Slow-cooked pulled pork with BBQ sauce on a brioche bun. Served with crispy fries and pickle.",
        "price": 13.99,
        "photo_url": "https://images.unsplash.com/photo-1606728035253-49e8a23146de?w=400",
        "is_available": True
    },
    {
        "cook_email": "carlos.cook@email.com",
        "title": "Brisket Platter",
        "description": "Tender smoked brisket sliced thick, served with mac and cheese, cornbread, and your choice of BBQ sauce.",
        "price": 19.99,
        "photo_url": "https://images.unsplash.com/photo-1544025162-d76694265947?w=400",
        "is_available": True
    }
]

SAMPLE_ORDERS = [
    {
        "buyer_email": "sarah.customer@email.com",
        "menu_item_title": "Authentic Chicken Tacos (3 pack)",
        "quantity": 2,
        "special_instructions": "Extra spicy salsa please!",
        "status": "completed"
    },
    {
        "buyer_email": "mike.buyer@email.com",
        "menu_item_title": "Pan-Seared Salmon",
        "quantity": 1,
        "special_instructions": "No vegetables, extra rice please",
        "status": "ready"
    },
    {
        "buyer_email": "sarah.customer@email.com",
        "menu_item_title": "Chocolate Chip Cookies (dozen)",
        "quantity": 1,
        "special_instructions": None,
        "status": "preparing"
    },
    {
        "buyer_email": "mike.buyer@email.com",
        "menu_item_title": "BBQ Ribs Full Rack",
        "quantity": 1,
        "special_instructions": "Medium sauce on the side",
        "status": "pending"
    }
]

SAMPLE_MESSAGES = [
    {
        "order_buyer_email": "sarah.customer@email.com",
        "order_menu_item": "Authentic Chicken Tacos (3 pack)",
        "sender_email": "sarah.customer@email.com",
        "content": "Hi! Can you make the salsa extra spicy? Thanks!"
    },
    {
        "order_buyer_email": "sarah.customer@email.com",
        "order_menu_item": "Authentic Chicken Tacos (3 pack)",
        "sender_email": "maria.garcia@email.com",
        "content": "Of course! I'll make sure to add extra jalapeños to your salsa. Your order will be ready in 20 minutes."
    },
    {
        "order_buyer_email": "mike.buyer@email.com",
        "order_menu_item": "Pan-Seared Salmon",
        "sender_email": "john.chef@email.com",
        "content": "Your salmon is ready for pickup! It's perfectly cooked and the rice portion has been doubled as requested."
    }
]

class SampleDataGenerator:
    def __init__(self, base_url: str = BASE_URL):
        self.base_url = base_url
        self.tokens = {}  # Store user tokens
        self.users = {}   # Store user data
        self.cook_profiles = {}  # Store cook profile data
        self.menu_items = {}     # Store menu item data
        self.orders = {}         # Store order data

    def check_api_health(self) -> bool:
        """Check if the API is running"""
        try:
            response = requests.get(f"{self.base_url}/health")
            return response.status_code == 200
        except requests.exceptions.ConnectionError:
            return False

    def register_users(self) -> bool:
        """Register all sample users"""
        print("📝 Registering sample users...")
        success_count = 0
        
        for user_data in SAMPLE_USERS:
            try:
                response = requests.post(f"{self.base_url}/auth/register", json=user_data)
                if response.status_code == 200:
                    user_info = response.json()
                    self.users[user_data["email"]] = user_info
                    print(f"✅ Registered: {user_data['full_name']} ({user_data['email']})")
                    success_count += 1
                elif response.status_code == 400 and "already registered" in response.json().get("detail", ""):
                    print(f"ℹ️  Already exists: {user_data['full_name']} ({user_data['email']})")
                    success_count += 1
                else:
                    print(f"❌ Failed to register {user_data['email']}: {response.status_code}")
            except Exception as e:
                print(f"❌ Error registering {user_data['email']}: {e}")
        
        print(f"📊 Registered {success_count}/{len(SAMPLE_USERS)} users")
        return success_count > 0

    def login_users(self) -> bool:
        """Login all users and store tokens"""
        print("\n🔐 Logging in users...")
        success_count = 0
        
        for user_data in SAMPLE_USERS:
            try:
                login_data = {
                    "email": user_data["email"],
                    "password": user_data["password"]
                }
                response = requests.post(f"{self.base_url}/auth/login", json=login_data)
                if response.status_code == 200:
                    token = response.json().get("access_token")
                    self.tokens[user_data["email"]] = token
                    print(f"✅ Logged in: {user_data['email']}")
                    success_count += 1
                else:
                    print(f"❌ Failed to login {user_data['email']}: {response.status_code}")
            except Exception as e:
                print(f"❌ Error logging in {user_data['email']}: {e}")
        
        print(f"📊 Logged in {success_count}/{len(SAMPLE_USERS)} users")
        return success_count > 0

    def create_cook_profiles(self) -> bool:
        """Create cook profiles for designated users"""
        print("\n👨‍🍳 Creating cook profiles...")
        success_count = 0
        
        for profile_data in SAMPLE_COOK_PROFILES:
            email = profile_data["email"]
            if email not in self.tokens:
                print(f"❌ No token for {email}, skipping cook profile")
                continue
                
            headers = {"Authorization": f"Bearer {self.tokens[email]}"}
            cook_data = {
                "name": profile_data["name"],
                "bio": profile_data["bio"],
                "photo_url": profile_data["photo_url"],
                "delivery_radius": profile_data["delivery_radius"]
            }
            
            try:
                response = requests.post(f"{self.base_url}/cooks/", json=cook_data, headers=headers)
                if response.status_code == 200:
                    profile_info = response.json()
                    self.cook_profiles[email] = profile_info
                    print(f"✅ Created cook profile: {profile_data['name']}")
                    success_count += 1
                elif response.status_code == 400 and "already exists" in response.json().get("detail", ""):
                    print(f"ℹ️  Cook profile already exists: {profile_data['name']}")
                    success_count += 1
                else:
                    print(f"❌ Failed to create cook profile for {email}: {response.status_code}")
            except Exception as e:
                print(f"❌ Error creating cook profile for {email}: {e}")
        
        print(f"📊 Created {success_count}/{len(SAMPLE_COOK_PROFILES)} cook profiles")
        return success_count > 0

    def create_menu_items(self) -> bool:
        """Create menu items for cooks"""
        print("\n🍽️  Creating menu items...")
        success_count = 0
        
        # First, get cook profiles to map emails to cook IDs
        cook_email_to_id = {}
        for email in self.tokens:
            headers = {"Authorization": f"Bearer {self.tokens[email]}"}
            try:
                response = requests.get(f"{self.base_url}/cooks/me/profile", headers=headers)
                if response.status_code == 200:
                    profile = response.json()
                    cook_email_to_id[email] = profile["id"]
            except:
                pass  # Not a cook
        
        for item_data in SAMPLE_MENU_ITEMS:
            cook_email = item_data["cook_email"]
            if cook_email not in self.tokens:
                print(f"❌ No token for cook {cook_email}, skipping menu item")
                continue
                
            headers = {"Authorization": f"Bearer {self.tokens[cook_email]}"}
            menu_data = {
                "title": item_data["title"],
                "description": item_data["description"],
                "price": item_data["price"],
                "photo_url": item_data["photo_url"],
                "is_available": item_data["is_available"]
            }
            
            try:
                response = requests.post(f"{self.base_url}/menu/", json=menu_data, headers=headers)
                if response.status_code == 200:
                    menu_info = response.json()
                    self.menu_items[item_data["title"]] = menu_info
                    print(f"✅ Created menu item: {item_data['title']}")
                    success_count += 1
                else:
                    print(f"❌ Failed to create menu item '{item_data['title']}': {response.status_code}")
            except Exception as e:
                print(f"❌ Error creating menu item '{item_data['title']}': {e}")
        
        print(f"📊 Created {success_count}/{len(SAMPLE_MENU_ITEMS)} menu items")
        return success_count > 0

    def generate_all_data(self) -> bool:
        """Generate all sample data"""
        print("🚀 Starting sample data generation for Adresur API\n")
        
        # Check API health
        if not self.check_api_health():
            print("❌ API is not running. Please start the server first.")
            return False
        
        print("✅ API is running\n")
        
        # Step 1: Register users
        if not self.register_users():
            print("❌ Failed to register users")
            return False
        
        # Step 2: Login users
        if not self.login_users():
            print("❌ Failed to login users")
            return False
        
        # Step 3: Create cook profiles
        if not self.create_cook_profiles():
            print("❌ Failed to create cook profiles")
            return False
        
        # Step 4: Create menu items
        if not self.create_menu_items():
            print("❌ Failed to create menu items")
            return False
        
        print("\n🎉 Sample data generation completed successfully!")
        print(f"📚 Visit {self.base_url}/docs for interactive API documentation")
        print(f"🔍 Use the following credentials to test:")
        print("   Admin: admin@adresur.com / admin123")
        print("   Cook: maria.garcia@email.com / password123")
        print("   Customer: sarah.customer@email.com / password123")
        
        return True

    def print_summary(self):
        """Print a summary of created data"""
        print("\n📋 Data Summary:")
        print(f"👥 Users: {len(SAMPLE_USERS)}")
        print(f"👨‍🍳 Cook Profiles: {len(SAMPLE_COOK_PROFILES)}")
        print(f"🍽️  Menu Items: {len(SAMPLE_MENU_ITEMS)}")
        print(f"📦 Sample Orders: {len(SAMPLE_ORDERS)}")
        print(f"💬 Sample Messages: {len(SAMPLE_MESSAGES)}")

def main():
    """Main function to run the sample data generator"""
    generator = SampleDataGenerator()
    
    if len(sys.argv) > 1 and sys.argv[1] == "--summary":
        generator.print_summary()
        return
    
    success = generator.generate_all_data()
    if not success:
        sys.exit(1)

if __name__ == "__main__":
    main() 