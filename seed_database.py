"""
Database Seeder for WebMents (Python Version)
Author: Anuj Singla (2210991317)
Institution: Chitkara University, Rajpura, Punjab

This script populates the database with sample data for demonstration
"""

import json
from datetime import datetime
from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient('mongodb://127.0.0.1:27017/')
db = client['webments']

def seed_database():
    """Seed the database with sample data"""
    
    print("\n" + "=" * 60)
    print("🌱 WebMents Database Seeder (Python)")
    print("=" * 60)
    print()

    try:
        # Load sample data
        with open('sample_data.json', 'r', encoding='utf-8') as f:
            sample_data = json.load(f)

        # Clear existing data
        print("🗑️  Clearing existing data...")
        db.users.delete_many({})
        db.products.delete_many({})
        db.orders.delete_many({})
        print("✅ Existing data cleared\n")

        # Seed Users
        print("👥 Seeding users...")
        users = []
        for user in sample_data['users']:
            user['createdAt'] = datetime.utcnow()
            user['updatedAt'] = datetime.utcnow()
            users.append(user)
        
        db.users.insert_many(users)
        manufacturers = [u for u in users if u['role'] == 'manufacturer']
        buyers = [u for u in users if u['role'] == 'buyer']
        
        print(f"✅ {len(users)} users added")
        print(f"   - {len(manufacturers)} Manufacturers")
        print(f"   - {len(buyers)} Buyers\n")

        # Seed Products
        print("📦 Seeding products...")
        products = []
        for product in sample_data['products']:
            product['image'] = 'sample-product.jpg'  # Placeholder
            product['createdAt'] = datetime.utcnow()
            product['updatedAt'] = datetime.utcnow()
            products.append(product)
        
        db.products.insert_many(products)
        print(f"✅ {len(products)} products added")
        
        # Count by category
        categories = {}
        for p in products:
            cat = p['category']
            categories[cat] = categories.get(cat, 0) + 1
        
        for cat, count in categories.items():
            print(f"   - {cat}: {count} products")
        print()

        # Seed Orders
        print("📋 Seeding orders...")
        orders = []
        for order in sample_data['orders']:
            order['orderDate'] = datetime.strptime(order['orderDate'], '%Y-%m-%d')
            order['expectedDelivery'] = datetime.strptime(order['expectedDelivery'], '%Y-%m-%d')
            if 'deliveredDate' in order:
                order['deliveredDate'] = datetime.strptime(order['deliveredDate'], '%Y-%m-%d')
            order['createdAt'] = datetime.utcnow()
            order['updatedAt'] = datetime.utcnow()
            orders.append(order)
        
        db.orders.insert_many(orders)
        total_revenue = sum(order['total'] for order in orders)
        
        print(f"✅ {len(orders)} orders added")
        print(f"   - Total Revenue: ₹{total_revenue:,}\n")

        # Display statistics
        print("=" * 60)
        print("📊 Database Statistics")
        print("=" * 60)
        print(f"Total Users:         {db.users.count_documents({})}")
        print(f"Total Products:      {db.products.count_documents({})}")
        print(f"Total Orders:        {db.orders.count_documents({})}")
        print(f"Total Revenue:       ₹{total_revenue:,}")
        print("=" * 60)

        # Display sample credentials
        print("\n" + "=" * 60)
        print("🔑 Sample Login Credentials")
        print("=" * 60)
        
        print("\n📍 MANUFACTURERS:")
        for user in sample_data['users']:
            if user['role'] == 'manufacturer':
                print(f"   {user['name']}")
                print(f"   Email: {user['email']}")
                print(f"   Password: {user['password']}")
                print(f"   City: {user['city']}\n")
        
        print("📍 BUYERS:")
        for user in sample_data['users']:
            if user['role'] == 'buyer':
                print(f"   {user['name']}")
                print(f"   Email: {user['email']}")
                print(f"   Password: {user['password']}")
                print(f"   City: {user['city']}\n")
        
        print("=" * 60)
        print("\n✅ Database seeding completed successfully!\n")
        print("🚀 You can now start the server and login with above credentials\n")

    except Exception as e:
        print(f"\n❌ Error seeding database: {e}")
    finally:
        client.close()
        print("🔌 Database connection closed\n")


if __name__ == '__main__':
    seed_database()
